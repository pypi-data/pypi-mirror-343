import logging

from langgraph.graph import START, END, StateGraph
from langgraph.graph.graph import CompiledGraph
from typing import TypedDict

from airas.analytic_subgraph.nodes.analytic_node import analytic_node

from airas.utils.logging_utils import setup_logging

from airas.utils.execution_timers import time_node, ExecutionTimeState
from airas.utils.github_utils.graph_wrapper import create_wrapped_subgraph

setup_logging()
logger = logging.getLogger(__name__)


class AnalyticSubgraphInputState(TypedDict):
    new_method: str
    verification_policy: str
    experiment_code: str
    output_text_data: str


class AnalyticSubgraphHiddenState(TypedDict):
    pass


class AnalyticSubgraphOutputState(TypedDict):
    analysis_report: str


class AnalyticSubgraphState(
    AnalyticSubgraphInputState,
    AnalyticSubgraphHiddenState,
    AnalyticSubgraphOutputState,
    ExecutionTimeState,
):
    pass


class AnalyticSubgraph:
    def __init__(
        self,
        llm_name: str,
    ):
        self.llm_name = llm_name

    @time_node("analytic_subgraph", "_analytic_node")
    def _analytic_node(self, state: AnalyticSubgraphState) -> dict:
        analysis_report = analytic_node(
            llm_name=self.llm_name,
            new_method=state["new_method"],
            verification_policy=state["verification_policy"],
            experiment_code=state["experiment_code"],
            output_text_data=state["output_text_data"],
        )
        return {"analysis_report": analysis_report}

    def build_graph(self) -> CompiledGraph:
        graph_builder = StateGraph(AnalyticSubgraphState)
        # make nodes
        graph_builder.add_node("analytic_node", self._analytic_node)
        # make edges
        graph_builder.add_edge(START, "analytic_node")
        graph_builder.add_edge("analytic_node", END)

        return graph_builder.compile()


Analyst = create_wrapped_subgraph(
    AnalyticSubgraph,
    AnalyticSubgraphInputState,
    AnalyticSubgraphOutputState,
)

if __name__ == "__main__":
    llm_name = "o1-2024-12-17"
    github_repository = "auto-res2/test20"
    branch_name = "test2"
    retriever = Analyst(
        github_repository=github_repository, branch_name=branch_name, llm_name=llm_name
    )

    result = retriever.run()
    print(f"result: {result}")
