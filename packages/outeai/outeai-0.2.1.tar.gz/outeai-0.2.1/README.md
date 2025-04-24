# OuteAI Early Access API - TTS Client

A Python client for interacting with the [OuteAI](https://outeai.com/) Text-to-Speech (TTS) API.

```python
from outeai.api.v1 import TTSClient

client = TTSClient(token="your_access_token_here")
output = client.generate(
    text="Hello, how are you doing today?",
    temperature=0.4,
    speaker={"default": "EN-FEMALE-1-NEUTRAL"}
)
# Save the audio
output.save("output.flac")
```
