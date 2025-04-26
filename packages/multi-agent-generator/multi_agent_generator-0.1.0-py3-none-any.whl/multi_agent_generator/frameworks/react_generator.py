from typing import List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.agents import AgentFinish, AgentAction
from langchain_core.tools import BaseTool
import json

def create_react_code(config: Dict[str, Any]) -> str:
    code = """from langchain_core.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from typing import Dict, List, Any

"""
    
    # Define tools
    code += "# Define tools\n"
    for tool in config.get("tools", []):
        code += f"""class {tool["name"].capitalize()}Tool(BaseTool):
    name = "{tool["name"]}"
    description = "{tool["description"]}"
    
    def _run(self, {", ".join(tool["parameters"].keys())}) -> str:
        # Implement actual functionality here
        return f"Result from {tool["name"]} tool"
    
    async def _arun(self, {", ".join(tool["parameters"].keys())}) -> str:
        # Implement actual functionality here
        return f"Result from {tool["name"]} tool"

"""
    
    # Collect tools
    code += "# Create tool instances\n"
    code += "tools = [\n"
    for tool in config.get("tools", []):
        code += f"    {tool['name'].capitalize()}Tool(),\n"
    code += "]\n\n"
    
    # Define example-based prompt
    code += "# Define example-based ReAct prompt\n"
    examples = config.get("examples", [])
    if examples:
        code += "examples = [\n"
        for example in examples:
            code += f"""    {{
        "query": "{example["query"]}",
        "thought": "{example["thought"]}",
        "action": "{example["action"]}",
        "observation": "{example["observation"]}",
        "final_answer": "{example["final_answer"]}"
    }},
"""
        code += "]\n\n"
    
    # Default agent
    if config.get("agents"):
        agent = config["agents"][0]  # Use the first agent
        code += f"""# Create ReAct agent
llm = ChatOpenAI(model="{agent["llm"]}")

# Create the agent using the ReAct framework
react_prompt = ChatPromptTemplate.from_messages([
    ("system", \"\"\"You are {agent["role"]}. Your goal is to {agent["goal"]}.
    
Use the following tools to assist you:
{{tool_descriptions}}

Use the following format:
Question: The user question you need to answer
Thought: Consider what to do to best answer the question
Action: The action to take, should be one of {{tool_names}}
Action Input: The input to the action
Observation: The result of the action
... (Thought/Action/Action Input/Observation can repeat)
Thought: I now know the final answer
Final Answer: The final answer to the question\"\"\"),
    ("human", "{{input}}")
])

agent = create_react_agent(llm, tools, react_prompt)

# Create an agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run the agent
def run_agent(query: str) -> str:
    \"\"\"Run the agent on a query.\"\"\"
    response = agent_executor.invoke({{"input": query}})
    return response.get("output", "No response generated")

# Example usage
if __name__ == "__main__":
    result = run_agent("Your query here")
    print(result)
"""
    
    # Now wrap the generated code in JSON format
    # return json.dumps({"generated_code": code}, indent=4)
    return code
