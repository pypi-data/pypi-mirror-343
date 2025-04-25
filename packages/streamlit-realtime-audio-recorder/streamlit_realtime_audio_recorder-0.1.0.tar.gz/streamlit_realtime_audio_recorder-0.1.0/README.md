# Streamlit Realtime Audio Recorder

A Streamlit component that records audio in real-time and automatically stops recording after a configurable silence period.

## Installation

```bash
pip install streamlit-realtime-audio-recorder
```

## Usage

```python
import streamlit as st
from streamlit_realtime_audio_recorder import audio_recorder

# Basic usage
result = audio_recorder()

# With custom parameters
result = audio_recorder(
    interval=50,      # How often to check audio level in ms
    threshold=-60,    # Audio level threshold for speech detection
    silenceTimeout=20000  # Time in ms to wait after silence before stopping recording
)

# Process the recorded audio
if result:
    if "audioData" in result:
        # Process audio data
        audio_data = result["audioData"]
        # You can save this as a file, process it, etc.
        
    if "status" in result:
        st.write(f"Recording status: {result['status']}")
        
    if "error" in result:
        st.error(f"Error: {result['error']}")
```

## Parameters

- `interval` (optional, default: 50): How often to check audio level in milliseconds
- `threshold` (optional, default: -60): Audio level threshold for speech detection in dB
- `silenceTimeout` (optional, default: 1500): Time in milliseconds to wait after silence before stopping recording
- `play` (optional, default: False): Whether to play the audio during recording

## Example App

```python
import streamlit as st
import base64
from streamlit_realtime_audio_recorder import audio_recorder

st.title("Audio Recorder Example")

result = audio_recorder(
    interval=50,
    threshold=-60,
    silenceTimeout=2000
)

if result:
    if "audioData" in result:
        st.audio(data=base64.b64decode(result["audioData"]), format="audio/webm")
    
    if "error" in result:
        st.error(f"Error: {result['error']}")
```

## License

MIT