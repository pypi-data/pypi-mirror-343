import logging
from typing import TypedDict

from langgraph.graph import START, END, StateGraph
from langgraph.graph.graph import CompiledGraph

from airas.research_preparation_subgraph.nodes.fork_repository import (
    fork_repository,
    DEVICETYPE,
)
from airas.research_preparation_subgraph.nodes.check_github_repository import (
    check_github_repository,
)
from airas.research_preparation_subgraph.nodes.check_branch_existence import (
    check_branch_existence,
)
from airas.research_preparation_subgraph.nodes.create_branch import (
    create_branch,
)
from airas.research_preparation_subgraph.nodes.retrieve_main_branch_sha import (
    retrieve_main_branch_sha,
)

from airas.utils.logging_utils import setup_logging

from airas.utils.execution_timers import time_node, ExecutionTimeState


setup_logging()
logger = logging.getLogger(__name__)


class ResearchPreparationStartState(TypedDict):
    github_repository: str
    branch_name: str


class ResearchPreparationHiddenState(TypedDict):
    github_owner: str
    repository_name: str
    repository_exists: bool
    fork_result: bool
    target_branch_sha: str
    create_result: bool
    main_sha: str


class ResearchPreparationState(
    ExecutionTimeState,
    ResearchPreparationStartState,
    ResearchPreparationHiddenState,
):
    pass


class ResearchPreparationSubgraph:
    def __init__(
        self,
        device_type: DEVICETYPE = "cpu",
        organization: str = "",
    ):
        self.device_type = device_type
        self.organization = organization

    def _init(self, state: dict) -> dict:
        github_repository = state["github_repository"]
        if "/" in github_repository:
            github_owner, repository_name = github_repository.split("/", 1)
            return {
                "github_owner": github_owner,
                "repository_name": repository_name,
            }
        else:
            raise ValueError("Invalid repository name format.")

    @time_node("research_preparation", "_get_github_repository")
    def _check_github_repository(self, state: ResearchPreparationState) -> dict:
        repository_exists = check_github_repository(
            github_owner=state["github_owner"],
            repository_name=state["repository_name"],
        )
        return {"repository_exists": repository_exists}

    @time_node("research_preparation", "_fork_repository")
    def _fork_repository(self, state: ResearchPreparationState) -> dict:
        fork_result = fork_repository(
            repository_name=state["repository_name"],
            device_type=self.device_type,
            organization=self.organization,
        )
        return {"fork_result": fork_result}

    @time_node("research_preparation", "_retrieve_branch_name")
    def _check_branch_existence(self, state: ResearchPreparationState) -> dict:
        target_branch_sha = check_branch_existence(
            github_owner=state["github_owner"],
            repository_name=state["repository_name"],
            branch_name=state["branch_name"],
        )
        return {"target_branch_sha": target_branch_sha}

    @time_node("research_preparation", "_retrieve_main_branch_sha")
    def _retrieve_main_branch_sha(self, state: ResearchPreparationState) -> dict:
        main_sha = retrieve_main_branch_sha(
            github_owner=state["github_owner"],
            repository_name=state["repository_name"],
        )
        return {"main_sha": main_sha}

    @time_node("research_preparation", "_create_branch")
    def _create_branch(self, state: ResearchPreparationState) -> dict:
        create_result = create_branch(
            github_owner=state["github_owner"],
            repository_name=state["repository_name"],
            branch_name=state["branch_name"],
            main_sha=state["main_sha"],
        )
        return {"create_result": create_result}

    def _should_fork_repo(self, state: ResearchPreparationState) -> str:
        if not state["repository_exists"]:
            return "fork_repository"
        else:
            return "check_branch_existence"

    def _should_create_branch(self, state: ResearchPreparationState) -> str:
        if not state["target_branch_sha"]:
            return "retrieve_main_branch_sha"
        else:
            return "end"

    def build_graph(self) -> CompiledGraph:
        graph_builder = StateGraph(ResearchPreparationState)
        # make nodes
        graph_builder.add_node("init", self._init)
        graph_builder.add_node("check_github_repository", self._check_github_repository)
        graph_builder.add_node("fork_repository", self._fork_repository)
        graph_builder.add_node("check_branch_existence", self._check_branch_existence)
        graph_builder.add_node(
            "retrieve_main_branch_sha", self._retrieve_main_branch_sha
        )
        graph_builder.add_node("create_branch", self._create_branch)

        # make edges
        graph_builder.add_edge(START, "init")
        graph_builder.add_edge("init", "check_github_repository")
        graph_builder.add_conditional_edges(
            "check_github_repository",
            self._should_fork_repo,
            {
                "fork_repository": "fork_repository",
                "check_branch_existence": "check_branch_existence",
            },
        )
        graph_builder.add_edge("fork_repository", "check_branch_existence")
        graph_builder.add_conditional_edges(
            "check_branch_existence",
            self._should_create_branch,
            {
                "retrieve_main_branch_sha": "retrieve_main_branch_sha",
                "end": END,
            },
        )
        graph_builder.add_edge("retrieve_main_branch_sha", "create_branch")
        graph_builder.add_edge("create_branch", END)

        return graph_builder.compile()

    def run(self, input: dict) -> dict:
        graph = self.build_graph()
        result = graph.invoke(input)
        return result


if __name__ == "__main__":
    github_repository = "auto-res2/test-tanaka-2"
    # github_repository = "fuyu-quant/test-1"
    branch_name = "test"

    subgraph = ResearchPreparationSubgraph(
        device_type="gpu",
        organization="auto-res2",
    )

    input = {
        "github_repository": github_repository,
        "branch_name": branch_name,
    }
    result = subgraph.run(input)
    print(result)
