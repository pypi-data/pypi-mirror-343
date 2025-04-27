# NeuralCore Python SDK

The **NeuralCore Python SDK** provides an easy-to-use interface for interacting with the NeuralCore AI APIs, including chat, vision, and text-to-speech (TTS) capabilities. This module enables seamless integration of NeuralCore’s powerful AI features into your applications.

## Features

- **Chat API**: Send messages and interact with NeuralCore's language models.
- **Vision API**: Analyze images with advanced vision models.
- **Text-to-Speech (TTS) API**: Convert text into speech using various voice options.
- **Custom Configuration**: Set default parameters like temperature and tokens to customize responses.
- **System Messages**: Utilize system messages for providing context or instructions to models.
- **Custom FineTuned Model Chat API**: FineTune our Model with your data and use its in API.

---

## Installation

Clone or download this repository and ensure you have Python 3.7+ installed. Install the required dependencies:

```bash
pip install NeuralCore
```

---

## Usage

### Initialization

To use the NeuralCore Python SDK, initialize the client with your API key:

```python
from neuralcore import NeuralCore

api_key = "your_api_key_here"
client = NeuralCore(api_key)
```

### Chat API

Send a chat request to NeuralCore. You can include system messages to provide specific instructions or context to the model:

```python
response = client.chat(
    messages=[
        {"role": "system", "content": "You are an assistant that provides concise answers."},
        {"role": "user", "content": "What is the capital of France?"}
    ],
    model="neura-3.5-aala",
    temperature=0.8,
    tokens=150
)
print(response)
```

**Note:** System messages are optional but useful for guiding the model's behavior. Messages should follow the format:
- **role**: "system", "user", or "assistant"
- **content**: Text content for the respective role

### Vision API

Send an image analysis request to NeuralCore. This feature allows models to interpret visual content based on a provided prompt:

```python
response = client.vision(
    image_url="https://example.com/image.jpg",
    prompt="Describe the objects in the image.",
    model="neura-vision-3.5",
    temperature=0.7,
    tokens=200
)
print(response)
```
### Text-to-Speech (TTS) API

Generate speech from text using NeuralCore's TTS API. Specify the desired voice to customize the output:

```python
response = client.speak(
    text="Hello, how can I assist you?",
    voice="luna"  # Options: asteria, luna, stella, athena, hera, orion, arcas, perseus, angus, orpheus, helios, zeus
)
print(response)
```
### Custom FineTuned Models API
Use your Custom FineTuned models using API

```python
response = client.finetune_chat(
    "What is the capital of France?",
    model="YOUR_FINETUNED_MODEL_ID" #you can find your ModelID in https://neuralcore.org/dashboard/finetune
)
print(response)
```
Or using a message list
```python
messages = [
    {"role": "system", "content": "You are a helpful AI assistant"},
    {"role": "user", "content": "What is the capital of France?"}
]
response = client.finetune_chat(
    messages=messages,
    model="YOUR_FINETUNED_MODEL_ID", #you can find your ModelID in https://neuralcore.org/dashboard/finetune
    temperature=0.7,
    tokens=200
)
print(response)
```
---

## Models Overview

### Chat Models

NeuralCore offers several models for language processing tasks:
- **neura-1.0**: Base model for general language tasks.
- **neura-2.0**: Enhanced version with improved context handling.
- **neura-3.5-aala**: Latest release with advanced capabilities.
- **neura-4.0-think**: Latest Realease for reasoning.
- **llama3-70b-8192**: External model powered by Meta.

### Vision Models

NeuralCore also provides specialized models for image analysis:
- **neura-vision-1.0**: Stable release for basic image analysis.
- **neura-vision-2.0**: Enhanced version with improved detail recognition.
- **neura-vision-3.5**: Latest release with advanced capabilities.

### Text-to-Speech Voices

NeuralCore's TTS API supports the following voices:
- **Female Voices**: asteria, luna, stella, athena, hera
- **Male Voices**: orion, arcas, perseus, angus, orpheus, helios, zeus
---

## Configuration

You can customize the default settings during initialization:

```python
from neuralcore import NeuralCoreConfig, NeuralCore

config = NeuralCoreConfig(
    api_key="your_api_key_here",
    base_url="https://api.neuralcore.org/api/n",
    tts_url="https://api.neuralcore.org/api/v1/tts",
    default_temperature=0.6,
    default_tokens=250,
    default_voice="luna"
)
client = NeuralCore(api_key=config.api_key)
```

---

## Error Handling

The SDK raises a `NeuralCoreError` for any issues with API requests. Example:

```python
try:
    response = client.chat("What's the weather?")
except NeuralCoreError as e:
    print(f"Error: {e}")
```

---

## Requirements

- Python 3.7+
- `requests` library

---

## License

This project is licensed under the MIT License.

---

## Support

For support, contact **NeuralCore Support** or open an issue in this repository.
