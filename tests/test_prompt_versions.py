import json
from pathlib import Path
import sys
project_root = Path(__file__).resolve().parents[1]
# Add project root to sys.path
sys.path.append(str(project_root))

print(Path.cwd())

from src.qa.utils import load_prompt
from langchain_xai import ChatXAI
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
import os

def build_chain(system_path, cypher_path):
    system_prompt = load_prompt(system_path)
    cypher_prompt = load_prompt(cypher_path)
    
    cypher_generation_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=cypher_prompt),
        HumanMessagePromptTemplate.from_template("{question}")
    ])

    llm = ChatXAI(
        xai_api_key=os.getenv("GROK_API_KEY"),
        model="grok-3-latest",
        temperature=0,
    )

    graph = Neo4jGraph(
        url="bolt://localhost:7687",
        username="neo4j",
        password=os.getenv("NEO4J_PASSWORD")
    )

    return GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=False,
        allow_dangerous_requests=True,
        use_function_response=True,
        function_response_system=system_prompt, #用於控制 LLM 如何處理和格式化最終的查詢結果
        cypher_llm_kwargs={"prompt": cypher_generation_prompt},
    )

def run_test(cypher_ver="v1", system_ver="v1"):
    print(Path.cwd() / "tests/questions.json")
    questions = json.load(open(Path.cwd() / "tests/questions.json"))
    expected = json.load(open(Path.cwd() / "tests/expected_answers.json"))

    chain = build_chain(
        f"{Path.cwd()}/src/prompt/{system_ver}_system.txt",
        f"{Path.cwd()}/src/prompt/{cypher_ver}_cypher.txt"
    )
    for q in questions:
        print("-" * 60)
        result = chain.invoke({"query": q})
        print(f"Q: {q}")
        print(f"A: {result['result']}")
        if q in expected:
            print(f"Expected: {expected[q]}")
        print("-" * 60)

if __name__ == "__main__":
    run_test(cypher_ver="v2", system_ver="v1")  # or v2, v3
