# Karhu AI Assistant CLI

Karhu is a powerful command-line AI assistant designed for productivity, research, and creative tasks. It supports file and document processing, web browsing, contextual conversations, speech synthesis, and advanced profile/model management—all from your terminal.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [CLI Options](#cli-options)
  - [Interactive Mode](#interactive-mode)
  - [Example Commands](#example-commands)
- [Profiles and Models](#profiles-and-models)
- [Speech and Voice Features](#speech-and-voice-features)
- [Context Management](#context-management)
- [Module Reference](#module-reference)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **File & Document Processing**: Read and process PDF, text, and other files.
- **Web Browsing & Search**: Browse web pages and perform web searches directly from the CLI.
- **Contextual Conversations**: Maintain, save, and manage conversation context for seamless multi-turn interactions.
- **Profile & Model Management**: Switch between AI models and conversational profiles (e.g., coding, creative, academic, therapist).
- **Speech Synthesis & Recognition**: Text-to-speech (TTS) and speech-to-text (STT) support, including multiple voice engines.
- **Interactive Mode**: Chat with Karhu in a conversational loop with command autocompletion and history.
- **Robust Error Handling**: Graceful error messages and recovery for all operations.
- **Extensible**: Modular design for easy addition of new features and integrations.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/karhu-cli.git
   cd karhu-cli
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(If using a virtual environment, activate it first.)*

3. **(Optional) Install extra system dependencies** for TTS/STT features (see [Speech and Voice Features](#speech-and-voice-features)).

---

## Configuration

Karhu uses JSON configuration files in `src/karhu/config/`:

- **models.json**: Define available AI models and their parameters.
- **profiles.json**: Define conversational profiles (e.g., coding, creative, therapist).
- **system_prompt.json**: Set the default system prompt for the assistant.

You can customize or add new profiles and models by editing these files.

---

## Usage

### CLI Options

Run Karhu from the project root:

```bash
python src/karhu/cli.py [OPTIONS]
```

**Main options:**

- `--query`, `-q <question>`: Ask a direct question.
- `--interactive`, `-i`: Start interactive chat mode.
- `--file`, `-f <path>`: Process a specific file.
- `--files`, `-ff <directory>`: Process all files in a directory.
- `--web`, `-w <url>`: Browse a web page.
- `--search`, `-s <query>`: Perform a web search.
- `--model`, `-m <name>`: Select AI model.
- `--profile`, `-P <name>`: Select conversational profile.
- `--setsprompt <prompt>`: Set a custom system prompt.
- `--save`: Save conversation context.
- `--clear`, `-c`: Clear current context.
- `--list-models`: List available models.
- `--list-profiles`: List available profiles.
- `--voices`: List TTS voices.
- `--kokoro-voices`: List Kokoro TTS voices.
- `--kokoro-blend <indices>`: Blend Kokoro voices.
- `--help-commands`: Show all available commands.

### Interactive Mode

Start with:

```bash
python src/karhu/cli.py --interactive
```

Features:
- Command autocompletion and history.
- All CLI and special commands available as `!command` (see below).

#### Interactive Commands

- `!model [name]` — Switch AI model.
- `!list_models` — List models.
- `!profile [name]` — Switch profile.
- `!list_profiles` — List profiles.
- `!create_profile [name:prompt]` — Create a new profile.
- `!system_prompt` — Show current system prompt.
- `!setsprompt [prompt]` — Set system prompt.
- `!file [path]` — Read a file.
- `!files [directory]` — Read all files in a directory.
- `!browse [url]` — Browse a web page.
- `!search [query]` — Web search.
- `!context_size` — Show context size.
- `!context_info` — Show context details.
- `!optimize_context` — Summarize/optimize context.
- `!search_context [query]` — Search within context.
- `!chunk [id]` — List/retrieve document chunks.
- `!save` — Save conversation.
- `!clear` — Clear context.
- `!clearall` — Clear all context/history.
- `!lazy` — Toggle speech-to-text mode.
- `!speak` — Toggle text-to-speech mode.
- `!voices` — List TTS voices.
- `!voice [index]` — Change TTS voice.
- `!kokoro` — Toggle Kokoro TTS.
- `!kokoro_voices` — List Kokoro voices.
- `!kokoro_voice [index]` — Change Kokoro voice.
- `!kokoro_blend [indices]` — Blend Kokoro voices.
- `!help` — Show help.
- `!quit` — Exit.

### Example Commands

- Process a PDF:
  ```bash
  python src/karhu/cli.py --file path/to/file.pdf
  ```
- Web search:
  ```bash
  python src/karhu/cli.py --search "What is quantum computing?"
  ```
- Switch to therapist profile in interactive mode:
  ```bash
  python src/karhu/cli.py --interactive --profile therapist
  ```

---

## Profiles and Models

Karhu supports multiple AI models (e.g., GPT-4o, Claude, Gemma) and conversational profiles (e.g., coding, creative, academic, therapist, funny, sarcastic, chill). You can switch or create new ones at runtime.

- **List models:** `!list_models`
- **Switch model:** `!model <name>`
- **List profiles:** `!list_profiles`
- **Switch profile:** `!profile <name>`
- **Create profile:** `!create_profile name:prompt`

Profiles are defined in `src/karhu/config/profiles.json`.

---

## Speech and Voice Features

- **Text-to-Speech (TTS):** Use `!speak`, `!voices`, `!voice [index]` to enable and select voices.
- **Kokoro TTS:** Advanced TTS engine with voice blending (`!kokoro`, `!kokoro_voices`, `!kokoro_voice`, `!kokoro_blend`).
- **Speech-to-Text (STT):** Use `!lazy` to toggle speech input mode.

*Note: Some features may require additional system dependencies (e.g., `espeak`, `ffmpeg`, or platform-specific TTS engines).*

---

## Context Management

- **Save context:** `!save`
- **Clear context:** `!clear`
- **Clear all:** `!clearall`
- **Show context size/info:** `!context_size`, `!context_info`
- **Optimize context:** `!optimize_context`
- **Search context:** `!search_context [query]`
- **Chunking:** `!chunk [id]` for large documents

---

## Module Reference

- **ai_assistant.py**: Core assistant logic and LLM interaction.
- **cli.py**: Command-line interface and argument parsing.
- **interactive.py**: Interactive chat mode.
- **model_manager.py**: Model selection and management.
- **profile_manager.py**: Profile selection and management.
- **context_manager.py**: Context storage, retrieval, and optimization.
- **document_processor.py**: File and document parsing.
- **web_browser.py**: Web browsing and search.
- **TextToSpeech.py / SpeechToText.py / kokorotts.py**: Speech synthesis and recognition.
- **Display_help.py**: Command help and documentation.
- **Errors.py**: Error handling and reporting.
- **config_parser.py**: Configuration file parsing.
- **globals.py**: Global state and settings.

---

## Testing

Run all tests with:

```bash
pytest
```

Tests are located in the `tests/` directory and cover core modules and features.

---

## Contributing

1. Fork the repository and create a new branch.
2. Add your feature or fix.
3. Write or update tests as needed.
4. Submit a pull request with a clear description.

---

## License

This project is licensed under the MIT License.

---

For questions or support, please open an issue on GitHub.
