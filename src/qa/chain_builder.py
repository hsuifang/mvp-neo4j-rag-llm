from pathlib import Path
import sys
import os
# Add the project root directory to the Python path
project_root = Path(__file__).resolve().parents[2]
src_path = Path(__file__).resolve().parents[1]
# Add project root to sys.path
sys.path.append(str(project_root))

from langchain_xai import ChatXAI
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

from src.qa.utils import load_prompt

def build_chain() -> GraphCypherQAChain:
    # 載入 prompt
    system_prompt = load_prompt(src_path / "prompt/system_prompt.txt")
    cypher_prompt = load_prompt(src_path / "prompt/cypher_prompt.txt")

    # 連接圖資料庫
    graph = Neo4jGraph(
        url="bolt://localhost:7687",
        username="neo4j",
        password=os.getenv("NEO4J_PASSWORD")
    )
    # 初始化 Grok (xAI) 模型
    chat = ChatXAI(
        xai_api_key=os.getenv("GROK_API_KEY"),
        model="grok-3-latest",
        temperature=0,
        seed=202504201
    )
    
    cypher_generation_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=cypher_prompt),
        HumanMessagePromptTemplate.from_template("{question}")
    ])

        # 最後建立 Chain
    chain = GraphCypherQAChain.from_llm(
        llm=chat,
        graph=graph,
        verbose=True,
        allow_dangerous_requests=True,
        use_function_response=True,
        function_response_system=system_prompt, #用於控制 LLM 如何處理和格式化最終的查詢結果
        cypher_llm_kwargs={"prompt": cypher_generation_prompt} #用於控制 LLM 如何生成 Cypher 查詢語句
    )

    return chain