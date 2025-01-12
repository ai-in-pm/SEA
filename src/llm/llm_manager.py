from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from groq import Groq
from ..utils.config import Config
import logging
import json

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class BaseLLM(ABC):
    """Base class for LLM implementations."""
    
    @abstractmethod
    def process(self, prompt: str) -> Dict[str, Any]:
        """Process a prompt and return response."""
        pass

class OpenAILLM(BaseLLM):
    """OpenAI implementation."""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def process(self, prompt: str) -> Dict[str, Any]:
        """Process prompt using OpenAI."""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"response": response.choices[0].message.content}

class AnthropicLLM(BaseLLM):
    """Anthropic implementation."""
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    def process(self, prompt: str) -> Dict[str, Any]:
        """Process prompt using Anthropic."""
        response = self.client.messages.create(
            model="claude-2",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"response": response.content}

class GroqLLM(BaseLLM):
    """Groq implementation."""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def process(self, prompt: str) -> Dict[str, Any]:
        """Process prompt using Groq."""
        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"response": response.choices[0].message.content}

class LLMManager:
    """Manages interactions with multiple LLM providers."""
    
    def __init__(self, config: Config):
        self.config = config
        self.default_provider = config.get("llm.default_provider", "openai")
        self.providers = self._initialize_providers()
    
    def _initialize_providers(self) -> Dict[str, BaseLLM]:
        """Initialize LLM providers based on configuration."""
        providers = {}
        
        if os.getenv("OPENAI_API_KEY"):
            providers["openai"] = OpenAILLM()
        if os.getenv("ANTHROPIC_API_KEY"):
            providers["anthropic"] = AnthropicLLM()
        if os.getenv("GROQ_API_KEY"):
            providers["groq"] = GroqLLM()
        
        if not providers:
            raise ValueError("No LLM providers configured. Please set API keys in .env file.")
        
        return providers
    
    def analyze_requirements(self, task: str, req_type: str) -> Dict[str, Any]:
        """Analyze project requirements using LLM."""
        prompt = f"""Analyze the following task and extract {req_type} requirements:
        
        Task: {task}
        
        Please provide a detailed analysis focusing on {req_type} aspects."""
        
        response = self._get_completion(prompt)
        return self._process_llm_response(response, "dict")
    
    def identify_patterns(self, task: str) -> List[str]:
        """Identify applicable design patterns for the task."""
        prompt = f"""Identify design patterns that would be suitable for this task:
        
        Task: {task}
        
        Please list and briefly explain why each pattern would be beneficial."""
        
        response = self._get_completion(prompt)
        return self._process_llm_response(response, "list")
    
    def design_architecture(self, task: str, aspect: str) -> Dict[str, Any]:
        """Design system architecture aspects using LLM."""
        prompt = f"""Design the {aspect} for this task:
        
        Task: {task}
        
        Please provide a detailed design focusing on {aspect}."""
        
        response = self._get_completion(prompt)
        return self._process_llm_response(response, "dict")
    
    def generate(self, task: str, component: str) -> Optional[str]:
        """Generate code or content based on a task description and component."""
        try:
            prompt = self._build_prompt(task, component)
            response = self._get_completion(prompt)
            return self._process_llm_response(response, "str")
        except Exception as e:
            logger.error(f"Error generating content for {component}: {str(e)}")
            return None
    
    def _build_prompt(self, task: str, component: str) -> str:
        """Build a structured prompt for code generation."""
        return f"""Generate code for the following component:

Task Description: {task}
Component: {component}

Requirements:
1. Code should be clean, well-documented, and follow best practices
2. Include proper error handling and logging
3. Use type hints where appropriate
4. Include docstrings for classes and functions
5. Follow PEP 8 style guidelines

Please provide only the code, without any additional explanations or markdown formatting."""
    
    def _get_completion(self, prompt: str) -> str:
        """Get completion from the default LLM provider."""
        provider = self.providers.get(self.default_provider)
        if not provider:
            provider = next(iter(self.providers.values()))
        
        try:
            response = provider.process(prompt)
            return response["response"]
        except Exception as e:
            logger.error(f"Error getting completion: {str(e)}")
            return ""
    
    def _process_llm_response(self, response: str, output_type: str = "str") -> Any:
        """Process and format LLM response based on desired output type."""
        if not response:
            if output_type == "dict":
                return {}
            elif output_type == "list":
                return []
            return ""
        
        try:
            if output_type == "dict":
                return json.loads(response)
            elif output_type == "list":
                return [line.strip() for line in response.split("\n") if line.strip()]
            return response
        except Exception as e:
            logger.error(f"Error processing LLM response: {str(e)}")
            if output_type == "dict":
                return {}
            elif output_type == "list":
                return []
            return ""
    
    def select_llm(self, task_analysis: Dict[str, Any]) -> BaseLLM:
        """
        Select the most appropriate LLM based on task analysis.
        
        Selection criteria:
        - OpenAI: Complex reasoning, creative solutions
        - Anthropic: Safety-critical, ethical considerations
        - Groq: High-performance technical analysis
        """
        provider_name = self._apply_selection_criteria(task_analysis)
        return self.providers.get(provider_name, self.providers[self.default_provider])
    
    def _apply_selection_criteria(self, task_analysis: Dict[str, Any]) -> str:
        """Apply selection criteria to choose appropriate LLM."""
        complexity = task_analysis.get("complexity", "medium")
        domain = task_analysis.get("domain", "general")
        
        if complexity == "high" or domain == "creative":
            return "openai"
        elif domain in ["safety", "ethics"]:
            return "anthropic"
        elif domain in ["technical", "performance"]:
            return "groq"
        
        return self.default_provider
