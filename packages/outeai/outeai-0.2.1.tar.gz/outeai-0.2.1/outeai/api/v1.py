import base64
import requests
from dataclasses import dataclass
from loguru import logger
import json

API_URL = "https://outeai.com/api/v1/tts" 

@dataclass
class AudioOutput:
    """Class for handling the audio output from the TTS API."""
    audio_bytes: bytes
    sample_rate: int = 44100
    
    def save(self, path: str) -> None:
        with open(path, "wb") as wav_file:
            if not path.endswith(".flac"):
                path += ".flac"
            wav_file.write(self.audio_bytes)
            logger.info(f"File saved in: {path}")

class TTSClient:
    """Client for interacting with the OuteTTS API."""
    
    def __init__(self, token: str):
        """Initialize the TTS client.
        
        Args:
            token: API token for authentication
        """
        self.token = token
        self.session = requests.Session()
    
    def generate(
        self,
        text: str,
        temperature: float = 0.4,
        speaker: dict = {"default": "EN-FEMALE-1-NEUTRAL"},
        verbose: bool = True,
    ):
        """Generate speech from text with streaming.
        
        Args:
            text: Text to convert to speech
            temperature: Generation temperature (default: 0.4)
            speaker: Speaker ID (default: {"default": "EN-FEMALE-1-NEUTRAL"})
        
        Yields:
            A dictionary containing partial generation data from the API
            (e.g., generated tokens and final audio when request is finished)
        
        Raises:
            ValueError: If the API request fails
            requests.RequestException: If there's a network error
        """

        if not text:
            raise ValueError("The 'text' parameter is required and cannot be empty.")
        if not speaker:
            raise ValueError("The 'speaker' parameter is required and cannot be empty.")
        if not (0.1 <= temperature <= 1.0):
            raise ValueError("The 'temperature' parameter must be between 0.1 and 1.0.")
        
        payload = {
            "token": self.token,
            "text": text,
            "temperature": temperature,
            "speaker": speaker
        }

        audio_bytes = None
        
        try:
            with self.session.post(API_URL, json=payload, stream=True) as response:
                try:
                    response.raise_for_status()
                except requests.HTTPError as e:
                    error_message = response.json().get("message", "Unknown error")
                    logger.error(f"API request failed: {error_message}")
                    raise ValueError(f"API request failed: {e}")
                
                logger.info("Generating audio...")

                for line in response.iter_lines(decode_unicode=True):
                    if line.strip():
                        try:
                            chunk = line.strip()
                            data = json.loads(chunk)
                            if data.get("data", {}):
                                audio_bytes = data.get("data", {}).get("audio_bytes", None)
                            else:
                                status = {
                                    "status": data.get("generation_status", "unknown"), 
                                }
                                if 'generated_seconds' in data:
                                    status['generated_seconds'] = f"{data['generated_seconds']:.2f}s"

                                if verbose:
                                    logger.info(status)

                        except Exception as e:
                            logger.error(f"Failed to parse chunk: {e}")
                            continue
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise

        if audio_bytes is not None:
            audio_bytes = base64.b64decode(audio_bytes)

        return AudioOutput(audio_bytes)
        
