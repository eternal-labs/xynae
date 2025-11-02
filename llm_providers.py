"""
LLM Provider Abstraction Layer
Supports multiple AI model providers: Anthropic, OpenAI, Google Gemini
"""

import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import random


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 150, temperature: float = 0.9) -> str:
        """Generate text from a prompt"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is properly configured"""
        pass


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider"""
    
    def __init__(self, api_key: str = None, model: str = "claude-sonnet-4-20250514"):
        from anthropic import Anthropic
        
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        if self.api_key:
            self.client = Anthropic(api_key=self.api_key)
        else:
            self.client = None
    
    def is_available(self) -> bool:
        return self.client is not None and self.api_key is not None
    
    def generate(self, prompt: str, max_tokens: int = 150, temperature: float = 0.9) -> str:
        if not self.is_available():
            raise ValueError("Anthropic API key not configured")
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.content[0].text.strip()


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def is_available(self) -> bool:
        return self.client is not None and self.api_key is not None
    
    def generate(self, prompt: str, max_tokens: int = 150, temperature: float = 0.9) -> str:
        if not self.is_available():
            raise ValueError("OpenAI API key not configured")
        
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.choices[0].message.content.strip()


class GeminiProvider(LLMProvider):
    """Google Gemini provider"""
    
    def __init__(self, api_key: str = None, model: str = "gemini-1.5-flash"):
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("Google Generative AI package not installed. Run: pip install google-generativeai")
        
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.model_name = model
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None
    
    def is_available(self) -> bool:
        return self.model is not None and self.api_key is not None
    
    def generate(self, prompt: str, max_tokens: int = 150, temperature: float = 0.9) -> str:
        if not self.is_available():
            raise ValueError("Google API key not configured")
        
        # Gemini uses different parameter names
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
        
        response = self.model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        return response.text.strip()


class LLMProviderManager:
    """Manages multiple LLM providers with fallback support"""
    
    def __init__(self, preferred_provider: str = "auto"):
        """
        Initialize LLM provider manager
        
        Args:
            preferred_provider: "auto", "anthropic", "openai", or "gemini"
        """
        self.providers = {}
        self.preferred_provider = preferred_provider
        
        # Initialize all available providers
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize all available providers"""
        # Anthropic
        try:
            anthropic = AnthropicProvider()
            if anthropic.is_available():
                self.providers["anthropic"] = anthropic
        except Exception as e:
            print(f"[LLM] Anthropic provider unavailable: {e}")
        
        # OpenAI
        try:
            openai = OpenAIProvider()
            if openai.is_available():
                self.providers["openai"] = openai
        except Exception as e:
            print(f"[LLM] OpenAI provider unavailable: {e}")
        
        # Gemini
        try:
            gemini = GeminiProvider()
            if gemini.is_available():
                self.providers["gemini"] = gemini
        except Exception as e:
            print(f"[LLM] Gemini provider unavailable: {e}")
    
    def get_provider(self, provider_name: str = None) -> LLMProvider:
        """
        Get a specific provider or the preferred one
        
        Args:
            provider_name: Specific provider name, or None for preferred/auto
        
        Returns:
            LLMProvider instance
        """
        if provider_name:
            if provider_name not in self.providers:
                raise ValueError(f"Provider '{provider_name}' not available. Available: {list(self.providers.keys())}")
            return self.providers[provider_name]
        
        # Auto selection
        if self.preferred_provider == "auto":
            # Use first available provider
            if not self.providers:
                raise ValueError("No LLM providers configured. Please set API keys.")
            return list(self.providers.values())[0]
        else:
            if self.preferred_provider not in self.providers:
                raise ValueError(f"Preferred provider '{self.preferred_provider}' not available")
            return self.providers[self.preferred_provider]
    
    def generate(self, prompt: str, max_tokens: int = 150, temperature: float = 0.9, 
                 provider: str = None) -> str:
        """
        Generate text using the specified or preferred provider
        
        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
            provider: Specific provider to use, or None for auto/preferred
        
        Returns:
            Generated text
        """
        provider_instance = self.get_provider(provider)
        
        try:
            return provider_instance.generate(prompt, max_tokens, temperature)
        except Exception as e:
            print(f"[LLM] Error with {provider or 'current'} provider: {e}")
            # Try fallback to other providers
            for name, prov in self.providers.items():
                if name != (provider or self.preferred_provider):
                    try:
                        print(f"[LLM] Trying fallback provider: {name}")
                        return prov.generate(prompt, max_tokens, temperature)
                    except:
                        continue
            
            # If all fail, raise
            raise Exception(f"All LLM providers failed. Last error: {e}")
    
    def list_available_providers(self) -> List[str]:
        """List all available providers"""
        return list(self.providers.keys())

