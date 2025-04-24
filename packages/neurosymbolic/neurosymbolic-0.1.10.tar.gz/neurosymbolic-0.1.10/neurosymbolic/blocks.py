## Sample building blocks for building neurosym tools.
## Example taken from:
## https://github.com/langchain-ai/langgraph-example/blob/main/my_agent/agent.py

import os

from functools import partial
from typing import TypedDict, Annotated, Sequence, Literal, List, Optional, Tuple, Any

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langgraph.graph import add_messages, StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.errors import GraphRecursionError

from langchain_core.output_parsers import PydanticToolsParser
from langchain_core.runnables import Runnable
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from pydantic import BaseModel, Field


class NotFoundError(Exception):
    pass


NEUROSYM_DEFAULT_MODEL = os.environ.get("NEUROSYM_DEFAULT_MODEL", "gpt-3.5-turbo")


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    result: Optional[BaseModel]


# Define the config
class GraphConfig(TypedDict):
    model_name: Literal["openai"]  # other models can be added here


# Define the function that determines whether to continue using tools
# or not
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    # If there are no tool calls, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


SYSTEM_PROMPT = os.environ.get(
    "NEUROSYM_SYSTEM_PROMPT",
    "Solve the task you were provided. You can run as many actions as necessary to solve the problem. You can use all tools at your disposal. Do not use a tool if you do not need it. Note that all commands you invoke have to be **'one-shot'**, in other words you **can't launch interactive sessions** because you are running within an llm chain.",
)


class Result(BaseModel):
    """Result class for the neurosymbolic solver."""

    result: str = Field(
        default="",
        description="The result of the neurosymbolic solver's goal.",
        example="42",
    )


def cast_chain(
    data: Any, target_type: Optional[BaseModel] = None, agent=None
) -> Runnable:
    """Cast an object to a given type."""

    if target_type is None:
        target_type = Result
    if agent is None:
        agent = ChatOpenAI(temperature=0, model_name=NEUROSYM_DEFAULT_MODEL)

    tools_parser = PydanticToolsParser(tools=[target_type])

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "You are a tool that converts data to the given type. The type is: {type}"
            ),
            HumanMessagePromptTemplate.from_template(
                "Convert the following data to the given type: {data}"
            ),
        ]
    )
    chain: Runnable = prompt | agent.bind_tools([target_type]) | tools_parser  # TODO: consider adding strict=True

    return chain


def cast_n(data: Any, target_type: Optional[BaseModel], agent=None, config=None) -> BaseModel:
    """Cast an object to a given type using agents based on neural models."""
    if target_type is None:
        target_type = Result
    if agent is None:
        agent = ChatOpenAI(temperature=0, model_name=NEUROSYM_DEFAULT_MODEL)
    if config is None:
        config = {
            "configurable": {"thread_id": 42},
        }
    chain = cast_chain(data, target_type, agent=agent)
    return chain.invoke(
        {
            "data": data,
            "type": target_type,
        },
        config=config,
    )


# Define the function that calls the model
def call_model(state, config, model):
    messages = state["messages"]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    response = model.invoke(messages, config)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# Define the function that calls the model
def call_postprocess(state, config, model, target_type):
    messages = state["messages"]
    result = cast_n(
        messages,
        target_type,
        agent=model,
        config=config,
    )
    return {"result": result[0]}


def agent_tool_loop(agent, toolbox, target_type):
    """
    Basic neurosym while loop iterating over a toolbox
    by calling an agent to decide whether to continue or end.
    """
    # set_debug(True)

    # Define a new graph
    workflow = StateGraph(AgentState, config_schema=GraphConfig)
    toolnode = ToolNode(toolbox)

    # Define the model / only OpenAI for now, can be configured
    model = agent.bind_tools(toolbox)  # TODO: consider adding strict=True
    agentnode = partial(call_model, model=model)

    # Define the two nodes we will cycle between
    workflow.add_node("agent", agentnode)
    workflow.add_node("action", toolnode)

    # Define a post-processing node
    postprocessmodel = agent
    postprocessnode = partial(
        call_postprocess, model=postprocessmodel, target_type=target_type
    )
    workflow.add_node("postprocess", postprocessnode)

    # Set the entrypoint as `agent`
    # This means that this node is the first one called
    workflow.set_entry_point("agent")

    # We now add a conditional edge
    workflow.add_conditional_edges(
        # First, we define the start node. We use `agent`.
        # This means these are the edges taken after the `agent` node is called.
        "agent",
        # Next, we pass in the function that will determine which node is called next.
        should_continue,
        # Finally we pass in a mapping.
        # The keys are strings, and the values are other nodes.
        # END is a special node marking that the graph should finish.
        # What will happen is we will call `should_continue`, and then the output of that
        # will be matched against the keys in this mapping.
        # Based on which one it matches, that node will then be called.
        {
            # If `tools`, then we call the tool node.
            "continue": "action",
            # Otherwise we finish.
            "end": "postprocess",
        },
    )

    # We now add a normal edge from `tools` to `agent`.
    # This means that after `tools` is called, `agent` node is called next.
    workflow.add_edge("action", "agent")

    # Finish it off by adding an edge from `postprocess` to `END`.
    workflow.add_edge("postprocess", END)

    # Finally, we compile it!
    # This compiles it into a LangChain Runnable,
    # meaning you can use it as you would any other runnable
    checkpointer = MemorySaver()
    graph = workflow.compile(checkpointer=checkpointer)
    return graph


def compute(
    prompt: str,
    toolbox: List[Any],
    max_iterations: int = 100,
    target_type=Optional[BaseModel],
) -> Optional[Tuple[BaseModel, List[BaseMessage]]]:
    """Run the following tools in a loop up to max_iterations and return the result as a string."""

    agent = ChatOpenAI(temperature=0, model_name=NEUROSYM_DEFAULT_MODEL)
    program = agent_tool_loop(agent, toolbox, target_type)
    try:
        final_state = program.invoke(
            {"messages": [HumanMessage(content=prompt)]},
            config={
                "configurable": {"thread_id": 42},
                "recursion_limit": max_iterations,
            },
        )
        messages = final_state["messages"]
        result = final_state["result"]
        return result, messages
    except GraphRecursionError:
        return None


def eval_s(data: Any, target_type: Optional[BaseModel] = None, prompt=None, agent=None, model_name=None, toolbox=None, max_iterations: int = 100) -> Optional[Tuple[BaseModel, List[BaseMessage]]]:
    """
    Perform an evaluation on the given data and return an object of the target type.
    For evaluation, we use the provided neurosymbolic agent. We allow the agent to run
    up to max_iterations.
    """
    if target_type is None:
        target_type = Result
    if agent is None:

        agent = ChatOpenAI(temperature=0, model_name=NEUROSYM_DEFAULT_MODEL)
    if toolbox is None:
        toolbox = []
    if prompt is None:
        prompt = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"{data}"),
        ]
    program = agent_tool_loop(agent, toolbox, target_type)
    try:
        final_state = program.invoke(
            {"messages": prompt},
            config={
                "configurable": {"thread_id": 42},
                "recursion_limit": max_iterations,
                # additionalProperties: {

            },
        )
        messages = final_state["messages"]
        result = final_state["result"]
        return result, messages
    except GraphRecursionError:
        return None


def eval_python(*args, **kwargs):
    """
    Evaluate the given data using the Python interpreter.
    """
    from neurosymbolic.python_interpreter import PythonInterpreter

    # Create a new instance of the Python interpreter
    python_interpreter = PythonInterpreter()

    # Call the eval_s function with the Python interpreter as the agent
    return eval_s(*args, toolbox=[python_interpreter], **kwargs)
