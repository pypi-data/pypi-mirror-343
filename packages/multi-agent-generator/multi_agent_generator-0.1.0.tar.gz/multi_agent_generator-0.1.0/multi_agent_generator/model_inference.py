from openai import OpenAI
from typing import Dict, Any, Optional, List
import os
import json


class ModelInference:
    """
    Wrapper for OpenAI model inference.
    
    This class provides a simplified interface for text generation
    using OpenAI's models.
    """
    
    def __init__(
        self,
        model_id: str,
        params: Dict[str, Any],
        credentials: Optional[Dict[str, str]] = None,
        project_id: Optional[str] = None
    ):
        """
        Initialize the OpenAI client.
        
        Args:
            model_id: The ID of the model to use (e.g., "gpt-4o")
            params: Generation parameters (like max_tokens, temperature, etc.)
            credentials: Optional API credentials
            project_id: Not used for OpenAI, kept for API compatibility
        """
        self.model_id = model_id
        self.params = params
        
        # Get API key from credentials or environment
        api_key = None
        if credentials and "api_key" in credentials:
            api_key = credentials["api_key"]
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            
        self.client = OpenAI(api_key=api_key)
    
    def generate_text(
        self, 
        prompt: str, 
        guardrails: bool = False  # Kept for API compatibility
    ) -> str:
        """
        Generate text based on the prompt.
        
        Args:
            prompt: The text prompt to generate from
            guardrails: Not used for OpenAI, kept for API compatibility
            
        Returns:
            The generated text response
        """
        try:
            # For system/user formatted prompts (e.g., Llama format)
            messages = self._extract_messages_from_prompt(prompt)
            
            # Generate text using the model
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                max_tokens=self.params.get("max_new_tokens", 1000),
                temperature=self.params.get("temperature", 0.7),
                top_p=self.params.get("top_p", 1.0),
                frequency_penalty=self.params.get("frequency_penalty", 0.0),
                presence_penalty=self.params.get("presence_penalty", 0.0)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error in text generation: {e}")
            return f"Error generating text: {str(e)}"
    
    def generate_text_stream(
        self, 
        prompt: str, 
        guardrails: bool = False  # Kept for API compatibility
    ) -> List[str]:
        """
        Generate text in a streaming fashion.
        
        Args:
            prompt: The text prompt to generate from
            guardrails: Not used for OpenAI, kept for API compatibility
            
        Returns:
            List of text chunks from the stream
        """
        try:
            # For system/user formatted prompts
            messages = self._extract_messages_from_prompt(prompt)
            
            # Generate text using the model with streaming
            responses = []
            stream = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                max_tokens=self.params.get("max_new_tokens", 1000),
                temperature=self.params.get("temperature", 0.7),
                top_p=self.params.get("top_p", 1.0),
                frequency_penalty=self.params.get("frequency_penalty", 0.0),
                presence_penalty=self.params.get("presence_penalty", 0.0),
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    responses.append(chunk.choices[0].delta.content)
            
            return responses
            
        except Exception as e:
            print(f"Error in streaming text generation: {e}")
            return [f"Error generating text: {str(e)}"]
    
    def _extract_messages_from_prompt(self, prompt: str) -> List[Dict[str, str]]:
        """
        Convert a formatted prompt string to OpenAI messages format.
        
        This handles Llama-style prompt formats like:
        <|begin_of_text|>
        <|system|>
        System prompt
        <|user|>
        User message
        <|assistant|>
        
        Args:
            prompt: The formatted prompt string
            
        Returns:
            List of message dictionaries for OpenAI API
        """
        messages = []
        
        # Check if this is a formatted prompt
        if "<|system|>" in prompt:
            # Split by the markers
            parts = prompt.split("<|")
            
            for part in parts:
                if not part.strip():
                    continue
                    
                # Extract role and content
                if "system|>" in part:
                    content = part.replace("system|>", "", 1).strip()
                    if content:
                        messages.append({"role": "system", "content": content})
                elif "user|>" in part:
                    content = part.replace("user|>", "", 1).strip()
                    if content:
                        messages.append({"role": "user", "content": content})
                elif "assistant|>" in part:
                    # We don't include the assistant part in the prompt
                    pass
        else:
            # Simple prompt - just use as user message
            messages.append({"role": "user", "content": prompt})
            
        return messages