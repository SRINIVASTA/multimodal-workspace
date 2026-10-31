import pytest
from unittest.mock import MagicMock, patch
from src.api.text_service import TextService
from src.api.media_service import MediaService
from src.api.client import OpenRouterClient

@pytest.fixture
def mock_client():
    """Fixture to provide a mocked OpenRouterClient layer."""
    client = MagicMock(spec=OpenRouterClient)
    return client

# ==========================================
# 1. TEXT SERVICE VALIDATION SUITE
# ==========================================

def test_generate_document_success(mock_client):
    """Verifies document generation constructs the proper payload and parses returns."""
    text_service = TextService(client=mock_client)
    
    # Mocking structural return payloads from OpenRouter chat completions
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "# Research Report\n\nThis is a mocked response with web citations [1]."
                }
            }
        ]
    }
    mock_client.post.return_value = mock_response

    # Execute service method target
    result = text_service.generate_document(topic="Quantum Computing", model="perplexity/sonar-reasoning")

    # Assert tracking matrix parameters
    assert "# Research Report" in result
    assert "[1]" in result
    mock_client.post.assert_called_once_with(
        "chat/completions",
        {
            "model": "perplexity/sonar-reasoning",
            "messages": [{"role": "user", "content": "Write a comprehensive technical report on: Quantum Computing. Include markdown citations."}]
        }
    )

def test_selective_edit_success(mock_client):
    """Verifies that block-targeted text transformations process strings correctly."""
    text_service = TextService(client=mock_client)
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Shortened text segment content."}}]
    }
    mock_client.post.return_value = mock_response

    result = text_service.selective_edit(block="Long paragraph content here...", action="Shorten")

    assert result == "Shortened text segment content."
    mock_client.post.assert_called_once()


# ==========================================
# 2. MEDIA SERVICE VALIDATION SUITE
# ==========================================

def test_generate_image_success(mock_client):
    """Ensures image pipeline returns structural delivery asset URLs."""
    media_service = MediaService(client=mock_client)
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {"url": "https://openrouter.ai"}
    }
    mock_client.post.return_value = mock_response

    result = media_service.generate_image(prompt="Cinematic layout asset", model="openai/dall-e-3")

    assert result == "https://openrouter.ai"
    mock_client.post.assert_called_once_with(
        "images/generations",
        {
            "model": "openai/dall-e-3",
            "prompt": "Cinematic layout asset",
            "response_format": "url"
        }
    )

def test_text_to_speech_success(mock_client):
    """Verifies binary speech synthesis serialization."""
    media_service = MediaService(client=mock_client)
    
    mock_response = MagicMock()
    mock_response.content = b"BinaryAudioStreamSequenceDataMock"
    mock_client.post.return_value = mock_response

    result = media_service.text_to_speech(text="Synthesize target sequence.", model="openai/tts-1-hd")

    assert result == b"BinaryAudioStreamSequenceDataMock"
    assert isinstance(result, bytes)
    mock_client.post.assert_called_once_with(
        "audio/speech",
        {
            "model": "openai/tts-1-hd",
            "input": "Synthesize target sequence."
        }
    )
