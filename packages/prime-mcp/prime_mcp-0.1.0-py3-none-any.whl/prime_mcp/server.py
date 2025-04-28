from functools import lru_cache
import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from pydantic import ValidationError

from prime_mcp.operations import CaseModel, IssueID, IssueSummaryAttributesModel

RESOURCES = Path(__file__).parent / "data"
RECOMMENDATIONS = RESOURCES / "recommendation.json"
SUMMARY = RESOURCES / "summary.json"


@lru_cache(maxsize=1)
def load_recommendations() -> CaseModel:
    with open(RECOMMENDATIONS) as f:
        try:
            data = json.load(f)
            return CaseModel.model_validate(data)
        except ValidationError as e:
            raise ValueError(f"Invalid JSON: {e}") from e


@lru_cache(maxsize=1)
def load_summary() -> IssueSummaryAttributesModel:
    with open(SUMMARY) as f:
        data = json.load(f)
        return IssueSummaryAttributesModel.model_validate(data)


async def main():
    mcp = FastMCP("Prime-MCP")

    @mcp.tool(name="issue-summary", description="Summarize an issue")
    def issue_summary(issue_id: IssueID) -> IssueSummaryAttributesModel:
        print(f"Loading issue summary for {issue_id}")
        return load_summary()

    @mcp.tool(name="recommendations", description="Concerns and Recommendations for an issue")
    def recommendations(issue_id: IssueID) -> CaseModel:
        print(f"Loading recommendations for {issue_id}")
        return load_recommendations()

    await mcp.run_stdio_async()


a = load_recommendations()
print(a)
