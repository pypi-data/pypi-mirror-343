from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.markdown import Markdown
from termcolor import colored
import threading
import textwrap
import os
from karhu.animation import Animation
from karhu.process_command import CommandProcessor
from karhu.Recordaudio import RecordAudio
from karhu.Errors import Errors
from karhu.SpeechToText import SpeechToText
from karhu.Display_help import Displayhelp
from karhu import globals

# Ensure the history file exists
profile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
#os.makedirs(profile_dir, exist_ok=True)  #reate the directory if it doesn't exist
history_path = os.path.join(profile_dir, ".karhu_history")

class CommandCompleter(Completer):
    """Custom completer to show suggestions only when input starts with '!'."""
    def __init__(self, commands):
        self.commands = commands

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if text.startswith("!"):  # Show suggestions only if input starts with "!"
            for command in self.commands:
                if command.startswith(text):
                    yield Completion(command, start_position=-len(text))

def simple_convert(text):
    """Apply simple markdown formatting that works with streaming"""
    # Replace bold markers
    text = text.replace("**", "\033[1m", 1)  # Bold start
    if "**" in text:
        text = text.replace("**", "\033[0m", 1)  # Bold end
    # Replace italic markers
    text = text.replace("*", "\033[3m", 1)  # Italic start
    if "*" in text:
        text = text.replace("*", "\033[0m", 1)  # Italic end "</think>"
    if "<think>" in text:
        text = text.replace("<think>", "💭 \033[90m", 1)  # Dark gray color + thinking emoji
    if "</think>" in text:
        text = text.replace("</think>", "\033[0m 💡 ", 1)
    return text

def interactive_mode(assistant):
    # Define available commands for autocompletion
    commands = [
        # Model and profile management
        "!model", "!list_models", "!profile", "!list_profiles", "!create_profile",
        
        # Content and browsing
        "!file", "!files", "!browse", "!search",
        
        # Context management
        "!context_size", "!optimize_context", "!search_context", "!chunk", "!context_info",
        
        # System prompt management
        "!system_prompt", "!setsprompt",
        
        # Conversation management
        "!save", "!clear", "!clearall",
        
        # Speech functionality
        "!lazy", "!speak", "!voices", "!voice",
        
        # Kokoro TTS commands
        "!kokoro", "!kokoro_voices", "!kokoro_voice", "!kokoro_blend",
        
        # Utility commands
        "!help", "!quit"
    ]
    command_completer = CommandCompleter(commands)

    # Create a prompt session with history and autocomplete
    session = PromptSession(
        history=FileHistory(history_path),  # Persistent history
        auto_suggest=AutoSuggestFromHistory(),  # Suggest based on history
        completer=command_completer,
        style=Style.from_dict({"prompt": "ansigreen bold"}),  # Style for the prompt
        message="You: "
    )

    # Use the speech-to-text and recorder from the AIAssistant instance instead of creating new ones
    # This ensures consistent initialization like the other components
    CommandProcessor.init_speech(None, None)

    console = Console()
    Displayhelp.banner(assistant)
    print(colored("Type ", "yellow") + "!help " + colored("for a list of commands.", "yellow"))
    
    # Create an instance of the Animation class
    animation = Animation()
    animation_thread = None

    while True:
        try:
            # Check if the user wants to use speech-to-text
            if globals.stt_mode:
                # Check if recorder is properly initialized
                if assistant.recorder is None:
                    globals.stt_mode = False
                    print(colored("\n ⅹ Speech-to-text mode disabled due to initialization failure", "red"))
                    # Fall back to text input
                    user_input = session.prompt("\nYou : ").strip()
                else:
                    user_input, exit_speech_mode = assistant.recorder.listen_for_speech()
                    # If user wants to exit speech mode or got no input, continue loop
                    if exit_speech_mode or not user_input:
                        continue
            else:
                # Prompt user input
                user_input = session.prompt("\nYou : ").strip()

            if not user_input:
                continue
            
            print("\033[1A\033[2K", end="")  # Move up one line and clear it
            print(colored(f"You: {user_input}", "cyan"))  # Redraw with new color
            

            try:
               
                # Create and start animation only if not already running
                if animation_thread is None or not animation_thread.is_alive():
                    animation_thread = threading.Thread(target=animation.start, args=("🧠 processing...",))
                    animation_thread.daemon = True  # Make thread daemon so it exits when main thread exits
                    animation_thread.start()       
               
                # Process the user input
                if user_input.startswith('!'):    
                    # Always explicitly stop the animation before displaying the response
                    if animation_thread and animation_thread.is_alive():
                        animation.stop()
                        animation_thread.join(timeout=0.5)
                        animation_thread = None  # Reset the thread
                    response = CommandProcessor.process_command(command=user_input, assistant=assistant)
                        # Save context after commands that likely modify it
                    if any(cmd in user_input for cmd in ['!file', '!files', '!browse', '!search']):
                        assistant.save_context()
                        print(colored(" 📓 Context saved to disk.", "green"))


                    if not response:
                        print(colored("No response from command processor.", "red"))
                else:
                    wrapped_input = textwrap.fill(user_input, width=80)
                    assistant.add_to_history("User", wrapped_input)
                    
                    # Use streaming response instead of regular response
                    stream = assistant.get_response_streaming(user_input)
                    
                    if not stream:
                        continue

                    # Always explicitly stop the animation before displaying the response
                    if animation_thread and animation_thread.is_alive():
                        animation.stop()
                        animation_thread.join(timeout=0.5)
                        animation_thread = None  # Reset the thread

                    # Display the response header
                    console.print("\n[italic green]Karhu: [/italic green]", end="")
                    
                    # Process and display the streaming response chunks
                    full_response = ""
                    for chunk in stream:
                        # First check if choices list exists and is not empty
                        if hasattr(chunk, 'choices') and chunk.choices and len(chunk.choices) > 0:
                            # Then check if first choice has a delta with content
                            if hasattr(chunk.choices[0], 'delta') and chunk.choices[0].delta and hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                                content = simple_convert(chunk.choices[0].delta.content)
                                full_response += content
                                console.print(content, end="", highlight=False)
                            # # Add support for Ollama format which might use 'message' instead of 'delta'
                            # elif hasattr(chunk.choices[0], 'message') and hasattr(chunk.choices[0].message, 'content') and chunk.choices[0].message.content:
                            #     content = simple_convert(chunk.choices[0].message.content)
                            #     full_response += content
                            #     console.print(content, end="", highlight=False)
                            
                    # Add a newline after the streaming response
                    console.print("")
 
                    ### TODO implement a mechanism to chose between streaming or formatted response

                    # console.print("\n[italic green]Formatted response:[/italic green]")
                    # md = Markdown(full_response)
                    # console.print(md)
                    
                    # Add the complete response to context
                    assistant.context_manager.add_to_context(
                        f"User: {user_input}\nKarhu: {full_response}",
                        source_type="conversation"
                    )
                    
                    # Add the response to the history
                    assistant.add_to_history("Assistant", full_response)

                    if globals.tts_mode:
                        if globals.kokoro_mode and CommandProcessor.kokoro_tts:
                            CommandProcessor.kokoro_tts.speak(full_response)
                        elif CommandProcessor.tts:
                            CommandProcessor.tts.speak(full_response)

            except Exception as e:
                Errors.handle_error("Failed to process command.", e)
                            
            finally:
                # Always ensure animation is stopped in the finally block
                if animation_thread and animation_thread.is_alive():
                    animation.stop()
                    animation_thread.join(timeout=0.5)
                    animation_thread = None # Reset the thread

        except KeyboardInterrupt:
            continue
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")