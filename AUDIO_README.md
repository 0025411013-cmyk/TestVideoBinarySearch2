# Binary Search Video - Audio Generation

## Files

### Audio Files
- `binary_search_narration.wav` - TTS narration audio (currently espeak-ng placeholder)
- `binary_search_timestamps.json` - Precise timestamps for visual synchronization

### Scripts
- `generate_audio.py` - Offline audio generation using espeak-ng
- `generate_audio_kokoro.py` - High-quality audio generation using Kokoro TTS (af_bella voice)

## Generating High-Quality Audio with Kokoro TTS

The included `binary_search_narration.wav` was generated using espeak-ng as a placeholder.
For production-quality audio with the Kokoro af_bella voice, run locally:

```bash
# Install dependencies
pip install kokoro soundfile numpy

# Generate audio (requires internet for first run to download model)
python generate_audio_kokoro.py
```

This will create:
- `binary_search_narration_kokoro.wav` - High-quality TTS audio
- `binary_search_timestamps_kokoro.json` - Updated timestamps

### Kokoro af_bella Voice
The af_bella voice is an American English female voice that sounds natural and human-like,
perfect for educational content in the style of 3Blue1Brown.

## Timestamp Format

The timestamp JSON file contains:

```json
{
  "metadata": {
    "title": "How Binary Search Actually Works - Visualized",
    "voice": "af_bella",
    "language": "en-US",
    "sample_rate": 24000,
    "total_duration_seconds": 577.817,
    "audio_file": "binary_search_narration.wav"
  },
  "sections": [
    {
      "section": "INTRODUCTION",
      "start_time": 0.0,
      "end_time": 68.922,
      "duration": 68.922,
      "sentences": [
        {
          "sentence_index": 0,
          "text": "Imagine you're looking for a word in a dictionary.",
          "start_time": 0.0,
          "end_time": 3.506,
          "duration": 3.506
        }
        // ... more sentences
      ]
    }
    // ... more sections
  ]
}
```

## Using Timestamps for Visual Synchronization

The timestamps allow precise synchronization of visuals:

1. **Section-level**: Use `sections[i].start_time` and `sections[i].end_time` for major visual transitions
2. **Sentence-level**: Use `sections[i].sentences[j].start_time` for detailed animation triggers

Example (pseudocode):
```python
import json

with open('binary_search_timestamps.json') as f:
    data = json.load(f)

for section in data['sections']:
    # Trigger section visual at section['start_time']
    for sentence in section['sentences']:
        # Trigger sentence animation at sentence['start_time']
        pass
```
