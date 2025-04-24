# ScaledgeWhisper - Live Transcription & Translation for Edge Devices

**ScaledgeWhisper** is a Python package designed to provide live transcription and translation capabilities using Whisper models, optimized for edge devices like Raspberry Pi. Built on top of Faster Whisper, this package allows users to transcribe or translate audio in real-time, with support for multiple languages and customizable settings.

For more details on the Faster Whisper implementation and setup, please refer to the [Faster Whisper README.md](https://github.com/SYSTRAN/faster-whisper/blob/master/README.md).

## Features

- **Live Transcription & Translation**: Supports both live audio transcription and translation (from any language to English) in real-time.
- **Optimized for Edge Devices**: Designed to run efficiently on devices like Raspberry Pi, using small-sized Whisper models.
- **Language Detection & Support**: Automatic language detection for transcription and support for English and Auto language modes for live tasks.
- **Customizability**: Offers multiple configuration options such as saving recordings, transcription, and customizing file names.
- **Cross-Platform**: Works across multiple platforms with automatic device selection (CPU, CUDA).

## Installation

### Prerequisites

- Python 3.9+
- `torch` installed (with proper support for your device)
- `ctranlate2` and other dependencies installed

You can install the package via pip:

```bash
pip install ScaledgeWhisper
```

Alternatively, you can install it from source:

```bash
git clone https://github.com/ScaledgeTechnology/ScaledgeWhisper.git
cd ScaledgeWhisper
pip install -e .
```

## Usage

You can use ScaledgeWhisper via the command line interface (CLI). Here’s a breakdown of how to use it.

### Command-line Options

```bash
usage: scaledgewhisper   [-h] [--list_models] [--available_languages] [--model]
                  [--live] [--live_language] [--language] [--info]
                  [--save_recording] [--save_transcription]
                  [--save_location] [--recording_name]
                  [--transcription_name] [--full_prediction]
                  [--chunk_size] [--num_threads]
                  [--info] task [paths ...]

```

- `task` (required): Choose between `transcribe` or `translate` to specify the task.
- `path` (optional): Path to the audio file for non-live tasks (required only for non-live tasks).
- `--available_languages`: Returns a list of all the available language codes along with their names.
- `--list_models`: Returns a list of all the available Whisper models to choose from if needed.
- `--info`: Provides several information on given audio files (requires input audio file paths).
- `--live`: Enable live transcription or translation (requires a microphone input).
- `--live_language`: Set the language (`English`, `Auto`) for live  transcription or translation (default is `English`).
- `--language`: Set the language for non-live tasks (default is autodetect).
- `--model`: Specify which Whisper model to use (`default`, `edge`, `model name` or `custom model path`).
- `--save_recording`: Whether to save the audio recording after the live task.
- `--save_transcription`: Whether to save the transcription after the live task.
- `--save_location`: Directory to save the files if `--save_recording` or `--save_transcription` is enabled (default is cwd)
- `--recording_name`: Custom name for the saved audio recording file (default is saved as `full_recording.wav`)
- `--transcription_name`: Custom name for the transcription file (default is saved as `transcriptions.json`)
- `--full_prediction`: Perform transcription or translation on the entire audio at the end
- `--chunk_size`: Size of audio chunks (in samples per second) to process. Higher values improve accuracy but increase latency. Default is `32000`.
- `--num_threads`: Number of threads for parallel processing. Minimum is `2`. Default is `4`.


### Example Usage

1. **Live Transcription:**

   To transcribe audio from the microphone in real-time:

   ```bash
   scaledgewhisper transcribe --live --model edge --live_language english
   ```

2. **Live Translation:**

   To translate audio from any language to English in real-time:

   ```bash
   scaledgewhisper translate --live --model edge --live_language english
   ```

3. **Non-Live Transcription:**

   For transcribing a pre-recorded audio file:

   ```bash
   scaledgewhisper transcribe /path/to/audio/file_1.wav /path/to/audio/file_2.wav --model default --language en
   ```

4. **Non-Live Translation:**

   To translate a pre-recorded audio file into English:

   ```bash
   scaledgewhisper transcribe /path/to/audio/file_1.wav /path/to/audio/file_2.wav --model edge --language multi
   ```

5. **Listing Available Models:**

   To list all available Whisper models:

   ```bash
   scaledgewhisper --list_models
   ```

6. **Listing Available Languages:**

   To list all available languages for live and non-live tasks:

   ```bash
   scaledgewhisper --available_languages
   ```

7. **Saving Recording:**

   To save the final recording for live tasks:

   ```bash
   scaledgewhisper transcribe --live --save_recording --recording_name /path/for/your/recording.wav
   ```

8. **Saving Transcription:**

   To save the final recording for live tasks, path will be cwd and transcripton.json by default:

   ```bash
   scaledgewhisper transcribe --live --save_transcription /cwd/your/transcription.json
   ```

9. **Getting Full Prediction:**

   To get full prediction on your recorded audio:

   ```bash
   scaledgewhisper transcribe --live --full_prediction
   ```

10. **Getting info on audio files:**

     To get information on audio files such as language, language probability etc:
     
     ```bash
     scaledgewhisper /path/to/audio/file_1.wav /path/to/audio/file_2.wav --info
     ```

## RealTime Class

The core class for live transcription and translation is `RealTime`. It handles both real-time transcription and translation, making use of the `keyboard` library to start and stop recording using hotkeys.

### Example Code:

```python
from ScaledgeWhisper import RealTime

# Initialize RealTime with edge model and auto device selection
rstt = RealTime(model_size_or_path="edge", device="auto")

# Start live transcription
rstt.transcribe(
    task="transcribe",  # or "translate"
    language="English",  # Set language for transcription
    save_recording=True,
    save_transcription=True,
    save_location=None,   # saved_data by default
    recording_name="live_recording.wav",
    transcription_name="live_transcription.json"
    return_output=False
)
```

## Development

### Running Tests

ScaledgeWhisper comes with a suite of unit tests to verify its functionality. You can run the tests using `pytest`:

```bash
pytest tests/
```

### Contributing

Feel free to open issues or submit pull requests for bug fixes or new features. To contribute, please fork the repository and submit a pull request.

1. Make sure the existing tests are still passing (and consider adding new tests as well!):

```bash
pytest tests/
```

2. Reformat and validate the code with the following tools:

```bash
black .
isort .
flake8 .
```

---

## License

This package is open-source and available under the MIT License.

---

### Notes

- Ensure that the audio input and desired task settings align with the expected functionality for the best results.
- For live tasks, make sure you have a microphone set up and accessible.
