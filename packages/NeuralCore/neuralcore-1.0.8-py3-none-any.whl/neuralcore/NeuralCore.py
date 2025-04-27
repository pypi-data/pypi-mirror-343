import requests
from typing import Dict, List, Optional, Union
from dataclasses import dataclass

@dataclass
class NeuralCoreConfig:
    api_key: str
    base_url: str = "https://api.neuralcore.org/api/n"
    tts_url: str = "https://api.neuralcore.org/api/v1/tts"
    finetune_url: str = "https://api.neuralcore.org/api/v3/finetune/chat"
    default_temperature: float = 0.7
    default_tokens: int = 200
    default_voice: str = "luna"

class NeuralCoreError(Exception):
    """Custom exception for NeuralCore-related errors"""
    pass

class NeuralCore:
    def __init__(self, api_key: str):
        """
        Initialize NeuralCore client
        
        Args:
            api_key (str): Your NeuralCore API key
        """
        self.config = NeuralCoreConfig(api_key=api_key)
    
    def chat(
        self,
        messages: Union[str, List[Dict[str, str]]],
        model: str = "neura-3.5-aala",
        temperature: Optional[float] = None,
        tokens: Optional[int] = None
    ) -> Dict:
        """
        Send a chat request to NeuralCore
        
        Args:
            messages: Either a single string message or a list of message dictionaries
            model: Model identifier to use
            temperature: Temperature for response generation
            tokens: Maximum tokens for response
            
        Returns:
            Dict containing the response
        """
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
            
        data = {
            "messages": messages,
            "model": model,
            "api": self.config.api_key,
            "temperature": temperature or self.config.default_temperature,
            "tokens": tokens or self.config.default_tokens
        }
        
        try:
            response = requests.post(f"{self.config.base_url}/", json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise NeuralCoreError(f"Error communicating with NeuralCore: {str(e)}")
    
    def vision(
        self,
        image_url: str,
        prompt: str,
        model: str = "neura-vision-3.5",
        temperature: Optional[float] = None,
        tokens: Optional[int] = None
    ) -> Dict:
        """
        Analyze an image using NeuralCore Vision
        
        Args:
            image_url: URL of the image to analyze
            prompt: Text prompt describing what to analyze in the image
            model: Vision model identifier to use
            temperature: Temperature for response generation
            tokens: Maximum tokens for response
            
        Returns:
            Dict containing the vision analysis response
        """
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "model": model,
            "api": self.config.api_key,
            "temperature": temperature or self.config.default_temperature,
            "tokens": tokens or self.config.default_tokens,
            "url": image_url,
            "code": prompt
        }
        
        try:
            response = requests.post(f"{self.config.base_url}/vision", json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise NeuralCoreError(f"Error communicating with NeuralCore Vision: {str(e)}")
    
    def speak(
        self,
        text: str,
        voice: Optional[str] = None
    ) -> Dict:
        """
        Generate speech from text using NeuralCore TTS
        
        Args:
            text: The text to convert to speech
            voice: Voice to use (options: asteria, luna, stella, athena, hera, orion,
                  arcas, perseus, angus, orpheus, helios, zeus)
            
        Returns:
            Dict containing the TTS response
        """
        headers = {
            'X-API-Key': self.config.api_key,
            'Content-Type': 'application/json'
        }
        
        data = {
            "text": text,
            "voice": voice or self.config.default_voice,
        }
        
        try:
            response = requests.post(
                self.config.tts_url,
                json=data,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise NeuralCoreError(f"Error communicating with NeuralCore TTS: {str(e)}")
    
    def finetune_chat(
        self,
        messages: Union[str, List[Dict[str, str]]],
        model: str,
        temperature: Optional[float] = None,
        tokens: Optional[int] = None
    ) -> Dict:
        """
        Send a chat request to NeuralCore's finetuned model endpoint
        
        Args:
            messages: Either a single string message or a list of message dictionaries
            model: Finetuned model identifier to use
            temperature: Temperature for response generation
            tokens: Maximum tokens for response
            
        Returns:
            Dict containing the response
        """
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
            
        data = {
            "messages": messages,
            "model": model,
            "api": self.config.api_key,
            "temperature": temperature or self.config.default_temperature,
            "tokens": tokens or self.config.default_tokens
        }
        
        try:
            response = requests.post(f"{self.config.finetune_url}", json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise NeuralCoreError(f"Error communicating with NeuralCore Finetune: {str(e)}")