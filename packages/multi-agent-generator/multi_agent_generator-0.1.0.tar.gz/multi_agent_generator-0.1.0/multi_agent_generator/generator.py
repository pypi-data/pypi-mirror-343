import os
import json
import streamlit as st
from .model_inference import ModelInference

from typing import Dict, Any

class AgentGenerator:
    def __init__(self):
        # Initialize OpenAI model
        self.model_id = "gpt-4o-mini"  
        self.parameters = {
            "max_new_tokens": 1000,  # Max tokens to generate
            "temperature": 0.7,      # Creativity level
            "top_p": 0.95,           # Nucleus sampling
            "frequency_penalty": 0,  # Discourage repetition
            "presence_penalty": 0    # Discourage topic repetition
        }
        
        # Initialize model on first use instead of constructor
        self.model = None
    
    def _initialize_model(self):
        if self.model is None:
            # Get API key from environment
            api_key = os.getenv("OPENAI_API_KEY")
            
            if not api_key:
                st.warning("OpenAI API Key not found in environment. Please enter it below.")
                api_key = st.text_input("Enter OpenAI API Key:", type="password")
                if not api_key:
                    st.stop()
                os.environ["OPENAI_API_KEY"] = api_key
            
            credentials = {"api_key": api_key}
            
            self.model = ModelInference(
                model_id=self.model_id,
                params=self.parameters,
                credentials=credentials
            )
        
    def analyze_prompt(self, user_prompt: str, framework: str) -> Dict[str, Any]:
        self._initialize_model()
        
        system_prompt = self._get_system_prompt_for_framework(framework)
        
        try:
            # Format prompt for OpenAI
            formatted_prompt = f"""<|begin_of_text|>
<|system|>
{system_prompt}
<|user|>
{user_prompt}
<|assistant|>
"""
            
            # Generate response using OpenAI
            response = self.model.generate_text(prompt=formatted_prompt)
            
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                st.warning("Could not extract valid JSON from model response. Using default configuration.")
                return self._get_default_config(framework)
                
        except Exception as e:
            st.error(f"Error in analyzing prompt: {e}")
            return self._get_default_config(framework)

    def _get_system_prompt_for_framework(self, framework: str) -> str:
        if framework == "crewai":
            return """
            You are an expert at creating AI research assistants using CrewAI. Based on the user's request,
            suggest appropriate agents, their roles, tools, and tasks. Format your response as JSON with this structure:
            {
                "agents": [
                    {
                        "name": "agent name",
                        "role": "specific role description",
                        "goal": "clear goal",
                        "backstory": "relevant backstory",
                        "tools": ["tool1", "tool2"],
                        "verbose": true,
                        "allow_delegation": true/false
                    }
                ],
                "tasks": [
                    {
                        "name": "task name",
                        "description": "detailed description",
                        "tools": ["required tools"],
                        "agent": "agent name",
                        "expected_output": "specific expected output"
                    }
                ]
            }
            """
        elif framework == "langgraph":
            return """
            You are an expert at creating AI agents using LangChain's LangGraph framework. Based on the user's request,
            suggest appropriate agents, their roles, tools, and nodes for the graph. Format your response as JSON with this structure:
            {
                "agents": [
                    {
                        "name": "agent name",
                        "role": "specific role description",
                        "goal": "clear goal",
                        "tools": ["tool1", "tool2"],
                        "llm": "model name (e.g., gpt-4)"
                    }
                ],
                "nodes": [
                    {
                        "name": "node name",
                        "description": "detailed description",
                        "agent": "agent name"
                    }
                ],
                "edges": [
                    {
                        "source": "source node name",
                        "target": "target node name",
                        "condition": "condition description (optional)"
                    }
                ]
            }
            """
        elif framework == "react":
            return """
            You are an expert at creating AI agents using the ReAct (Reasoning + Acting) framework. Based on the user's request,
            suggest appropriate agents, their roles, tools, and specific reasoning steps. Format your response as JSON with this structure:
            {
                "agents": [
                    {
                        "name": "agent name",
                        "role": "specific role description",
                        "goal": "clear goal",
                        "tools": ["tool1", "tool2"],
                        "llm": "model name (e.g., gpt-4)"
                    }
                ],
                "tools": [
                    {
                        "name": "tool name",
                        "description": "detailed description of what the tool does",
                        "parameters": {
                            "param1": "parameter description",
                            "param2": "parameter description"
                        }
                    }
                ],
                "examples": [
                    {
                        "query": "example user query",
                        "thought": "example thought process",
                        "action": "example action to take",
                        "observation": "example observation",
                        "final_answer": "example final answer"
                    }
                ]
            }
            """
        else:
            return """
            You are an expert at creating AI research assistants. Based on the user's request,
            suggest appropriate agents, their roles, tools, and tasks.
            """

    def _get_default_config(self, framework: str) -> Dict[str, Any]:
        if framework == "crewai":
            return {
                "agents": [{
                    "name": "default_assistant",
                    "role": "General Assistant",
                    "goal": "Help with basic tasks",
                    "backstory": "Versatile assistant with general knowledge",
                    "tools": ["basic_tool"],
                    "verbose": True,
                    "allow_delegation": False
                }],
                "tasks": [{
                    "name": "basic_task",
                    "description": "Handle basic requests",
                    "tools": ["basic_tool"],
                    "agent": "default_assistant",
                    "expected_output": "Task completion"
                }]
            }
        elif framework == "langgraph":
            return {
                "agents": [{
                    "name": "default_assistant",
                    "role": "General Assistant",
                    "goal": "Help with basic tasks",
                    "tools": ["basic_tool"],
                    "llm": "gpt-4"
                }],
                "nodes": [{
                    "name": "process_input",
                    "description": "Process user input",
                    "agent": "default_assistant"
                }],
                "edges": [{
                    "source": "process_input",
                    "target": "END",
                    "condition": "task completed"
                }]
            }
        elif framework == "react":
            return {
                "agents": [{
                    "name": "default_assistant",
                    "role": "General Assistant",
                    "goal": "Help with basic tasks",
                    "tools": ["basic_tool"],
                    "llm": "gpt-4"
                }],
                "tools": [{
                    "name": "basic_tool",
                    "description": "A basic utility tool",
                    "parameters": {
                        "input": "User input to process"
                    }
                }],
                "examples": [{
                    "query": "Help me find information",
                    "thought": "I need to search for relevant information",
                    "action": "Use search tool",
                    "observation": "Found relevant results",
                    "final_answer": "Here is the information you requested"
                }]
            }
        else:
            return {}