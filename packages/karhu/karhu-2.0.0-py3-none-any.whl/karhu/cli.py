import sys
import os
from karhu import globals
import argparse
from termcolor import colored
from karhu.kokorotts import KokoroTTS
from rich.console import Console
from rich.markdown import Markdown
from karhu.ai_assistant import AIAssistant
from karhu.TextToSpeech import TextToSpeech
from karhu.model_manager import ModelManager
from karhu.interactive import interactive_mode
from karhu.process_command import CommandProcessor

# try:
#     import pkg_resources
# except ImportError:
#     pkg_resources = None

def create_parser():
    parser = argparse.ArgumentParser(description="Karhu AI Assistant CLI")
    
    # Input methods
    parser.add_argument('--query', '-q', type=str, help="Direct question to ask")
    parser.add_argument('--interactive', '-i', action='store_true', help="Start in interactive chat mode")
    
    # Context and content sources
    parser.add_argument('--file', '-f', type=str, help="Path to the file to be processed")
    parser.add_argument('--files', '-ff', type=str, help="Read all files in a directory")
    parser.add_argument('--web', '-w', type=str, help="URL to browse")
    parser.add_argument('--search', '-s', type=str, help="Search query using DuckDuckGo")
    parser.add_argument('--clear', '-c', action='store_true', help="Clear the current context")
    
    # Model management
    parser.add_argument('--model', '-m', type=str, help="Model to use (e.g., gpt-4o, claude-3.5-sonnet)")
    parser.add_argument('--list_models', '-lm', action='store_true', help="List all available models")
    
    # Profile management
    parser.add_argument('--profile', '-p', type=str, help="Profile to use for system prompts")
    parser.add_argument('--list_profiles', '-lp', action='store_true', help="List all available profiles")
    
    # System prompt management
    parser.add_argument('--system_prompt', '-sprompt', action='store_true', help="Show the current system prompt")
    parser.add_argument('--setsprompt', '-sp', type=str, help="Set the system prompt")
    
    # Text-to-speech options
    parser.add_argument('--speak', '-tts', action='store_true', help="Enable text-to-speech output")
    parser.add_argument('--voice', '-v', type=int, help="Set the voice for text-to-speech (index number)")
    parser.add_argument('--list_voices', '-lv', action='store_true', help="List available TTS voices")
    
    # Kokoro TTS options
    parser.add_argument('--kokoro', '-k', action='store_true', help="Enable Kokoro TTS instead of default TTS")
    parser.add_argument('--kokoro_voice', '-kv', type=int, help="Set the Kokoro voice (index number)")
    parser.add_argument('--kokoro_voices', '-kvs', action='store_true', help="List available Kokoro voices")
    parser.add_argument('--kokoro_blend', '-kb', type=str, help="Blend multiple Kokoro voices (space-separated indices)")
    
    # Conversation management
    parser.add_argument('--save', action='store_true', help="Save the conversation as an md file")

    parser.add_argument('--summarize_context', '-sumc', action='store_true', help="Summarize the current context to reduce token usage")
    parser.add_argument('--context_info', '-ci', action='store_true', help="Show information about the current context")
 
    # Context management options
    parser.add_argument('--optimize', '-o', action='store_true', help="Optimize the current context to reduce token usage")
    parser.add_argument('--context_size', '-cs', action='store_true', help="Show the current context size in characters and estimated tokens")
    parser.add_argument('--max_context', '-mc', type=int, help="Set maximum context size in characters (default: 8000)")
    parser.add_argument('--search_context', '-sc', type=str, help="Search the current context for specific information")
    
    # Help and version
    parser.add_argument('--help_commands', '-hc', action='store_true', help="Show all available interactive commands")
    parser.add_argument('--version', action='version', version='Karhu AI 2.0')
    
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    # config_parser = ConfigParser(config_path)
    
    # List models
    if args.list_models:
        CommandProcessor.process_command("!list_models", assistant=None)
        return
    
    # List profiles 
    if args.list_profiles:
        CommandProcessor.process_command("!list_profiles", assistant=None)
        return
    
    # Set model if specified
    if args.model:
        ModelManager.set_current_model(args.model)
        print(colored(f"Switched to model: {args.model}", "green"))
    
    # Load current model config
    current_model_name = ModelManager.get_current_model()
    model_config = ModelManager.get_model_config(current_model_name)
    
    if not model_config:
        print(colored(f"Model '{current_model_name}' not found. Using default.", "yellow"))
        model_config = ModelManager.get_model_config("gpt-4o")  # Default fallback
    
    # Initialize assistant
    assistant = AIAssistant(model_config)
    assistant.model = model_config.get('model', 'gpt-4o')
    assistant.temp = model_config.get('temp', 0.7)
    assistant.max_tokens = model_config.get('max_tokens', 4096)
    assistant.top_p = model_config.get('top_p', 1)
    assistant.load_context()
    # context = assistant.current_context
    
    tts = None
    kokoro_tts = None
    # CommandProcessor.init_speech(tts, kokoro_tts)
    
    # Process simple flag commands
    if args.clear:
        assistant.clear_context()
        print(colored("General context cleared.", "green"))
        return
    
    if args.system_prompt:
        CommandProcessor.process_command("!system_prompt", assistant)
        return
    
# Process commands with context updates
    command_executed = False
    
    if args.file:
        result = CommandProcessor.process_command(f"!file {args.file}", assistant)
        # File command already updates the assistant.current_context
        assistant.save_context()  # Save to file for persistence
        command_executed = True
        print(result)
    
    if args.files:
        result = CommandProcessor.process_command(f"!files {args.files}", assistant)
        assistant.save_context()  # Save to file for persistence
        command_executed = True
        print(result)
    
    if args.web:
        result = CommandProcessor.process_command(f"!browse {args.web}", assistant)
        assistant.save_context()  # Save to file for persistence
        command_executed = True
        print(result)
        
    if args.search:
        result = CommandProcessor.process_command(f"!search {args.search}", assistant)
        assistant.save_context()  # Save to file for persistence
        command_executed = True
        print(result)
    
    if command_executed:
        assistant.save_context()
        print(colored("Context saved.", "green"))
    
    # Handle profile selection
    if args.profile:
        CommandProcessor.process_command(f"!profile {args.profile}", assistant)
    
    if args.setsprompt:
        CommandProcessor.process_command(f"!setsprompt {args.setsprompt}", assistant)
    
    # TTS options
    if args.speak or args.voice is not None or args.list_voices:
        from karhu.TextToSpeech import TextToSpeech
        tts = TextToSpeech()
        globals.tts_mode = True if args.speak else globals.tts_mode
    
    if args.kokoro or args.kokoro_voice is not None or args.kokoro_voices or args.kokoro_blend:
        from karhu.kokorotts import KokoroTTS
        kokoro_tts = KokoroTTS()
        globals.tts_mode = True if args.kokoro else globals.tts_mode
        globals.kokoro_mode = True if args.kokoro else globals.kokoro_mode
    
    # Initialize speech system with whatever we've loaded (may be None)
    CommandProcessor.init_speech(tts, kokoro_tts)
    
    if args.voice is not None:
        CommandProcessor.process_command(f"!voice {args.voice}", assistant)
    
    if args.kokoro_voice is not None:
        CommandProcessor.process_command(f"!kokoro_voice {args.kokoro_voice}", assistant)
    
    if args.list_voices:
        CommandProcessor.process_command("!voices", assistant)
        return
    
    if args.kokoro_voices:
        CommandProcessor.process_command("!kokoro_voices", assistant)
        return
    
    if args.kokoro_blend:
        CommandProcessor.process_command(f"!kokoro_blend {args.kokoro_blend}", assistant)
    
    if args.help_commands:
        CommandProcessor.process_command("!help", assistant)
        return
    
    # Handle direct query
    if args.query:
        console = Console()
        response = assistant.get_response(args.query)
        console.print("\n[italic green]Karhu: [/italic green]", end="")
        markdown_response = Markdown(response) if isinstance(response, str) else response
        console.print(markdown_response)
        
        if globals.tts_mode:
            if globals.kokoro_mode and CommandProcessor.kokoro_tts:
                CommandProcessor.kokoro_tts.speak(response)
            elif CommandProcessor.tts:
                CommandProcessor.tts.speak(response)
        
        if args.save:
            assistant.save_conversation()
            print(colored("Conversation saved.", "green"))
    
    # Interactive mode
    if args.interactive:
        interactive_mode(assistant)
    
    # Default help
    if len(sys.argv) == 1:
        parser.print_help()

    if args.summarize_context:
        CommandProcessor.process_command("!optimize_context", assistant)
        return
        
    if args.context_info:
        CommandProcessor.process_command("!context_info", assistant)
        return

if __name__ == "__main__":
    main()
