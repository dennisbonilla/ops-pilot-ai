import asyncio
import json
from pathlib import Path
from .agent import Agent
from .retrieval import KnowledgeBase


async def main():
    agent = Agent(KnowledgeBase())
    cases = [json.loads(line) for line in Path("evals/dataset.jsonl").read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    passed = 0
    for case in cases:
        result = await agent.run(case["question"])
        content_ok = all(term.lower() in result.answer.lower() for term in case["must_contain"])
        actual_tool = result.tool_proposal.name if result.tool_proposal else None
        ok = content_ok and actual_tool == case["expected_tool"] and (bool(result.citations) or actual_tool is not None)
        passed += ok
        print(json.dumps({"question": case["question"], "passed": ok, "tool": actual_tool}, ensure_ascii=False))
    score = passed / len(cases)
    print(f"quality_score={score:.2f}")
    if score < .8:
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
