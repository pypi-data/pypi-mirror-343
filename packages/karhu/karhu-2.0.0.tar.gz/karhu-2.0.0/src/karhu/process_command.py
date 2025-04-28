import re
import os
import time
import json
from karhu import globals 
from karhu.Errors import Errors
from rich.panel import Panel
from termcolor import colored
from rich.console import Console
from karhu.Display_help import Displayhelp
from karhu.model_manager import ModelManager
from karhu.profile_manager import ProfileManager
from karhu.TextToSpeech import TextToSpeech

profile_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(profile_dir, "config/config.json")

class CommandProcessor:
    tts = None
    kokoro_tts = None

    @classmethod
    def init_speech(cls, tts_instance, kokoro_tts_instance=None):
        """Initialize speech-to-text and text-to-speech"""
        cls.tts = tts_instance
        cls.kokoro_tts = kokoro_tts_instance

    @classmethod
    def ensure_tts_loaded(cls):
        """Ensure TTS is loaded when needed"""
        if cls.tts is None:
            try:
                from karhu.TextToSpeech import TextToSpeech
                print(colored("\n 🔊 Initializing text-to-speech...", "blue"))
                cls.tts = TextToSpeech()
                # print(f"\n {cls.tts}")
                if cls.tts == None or not getattr(cls.tts, 'is_valid', False):
                    print(colored(" ⅹ Failed to initialize TTS: TTS instance is invalid", "red"))
                    cls.tts = None  # Reset to None
                    return False
                else:
                    print(colored(" ✓ Google TTS initialized successfully ", "green"))
            except Exception as e:
                print(colored(f" ⅹ Error initializing TTS : {str(e)}", "red"))
                cls.tts = None
                return False
        return True
    
    @classmethod
    def ensure_kokoro_loaded(cls, timeout=3):
        """Ensure Kokoro TTS is loaded when needed
        
        Args:
            timeout (int): Timeout in seconds for API connection (default: 3)
        """
        if cls.kokoro_tts is None:
            try:
                from karhu.kokorotts import KokoroTTS
                from karhu import globals as karhu_globals
                print(colored("\n 🔊 Initializing Kokoro TTS...", "blue"))
                
                # Try to initialize Kokoro TTS with the specified timeout
                cls.kokoro_tts = KokoroTTS(connection_timeout=timeout)
                
                # Check if the initialization was successful by verifying that voices can be retrieved
                if cls.kokoro_tts is None or not hasattr(cls.kokoro_tts, 'is_initialized') or not cls.kokoro_tts.is_initialized:
                    print(colored(" ⅹ Failed to initialize Kokoro TTS: TTS instance is not properly initialized", "red"))
                    cls.kokoro_tts = None  # Reset to None
                    karhu_globals.kokoro_mode = False
                    karhu_globals.tts_mode = False
                    return False
                
                # Try to get the current voice as a final validation
                try:
                    _, voice_name, voice_id = cls.kokoro_tts.get_current_voice()
                    print(colored(f" ✓ Kokoro TTS initialized successfully with voice: {voice_name}", "green"))
                    return True
                except Exception as voice_error:
                    print(colored(f" ⅹ Error retrieving Kokoro voices: {str(voice_error)}", "red"))
                    cls.kokoro_tts = None  # Reset to None
                    karhu_globals.kokoro_mode = False
                    karhu_globals.tts_mode = False
                    return False
                    
            except Exception as e:
                print(colored(f" ⅹ Error initializing Kokoro TTS: {str(e)}", "red"))
                cls.kokoro_tts = None  # Reset to None
                from karhu import globals as karhu_globals
                karhu_globals.kokoro_mode = False
                karhu_globals.tts_mode = False
                return False
        
        # Verify that the existing instance is still valid
        try:
            _, _, _ = cls.kokoro_tts.get_current_voice()
            return True
        except Exception:
            print(colored(" ⅹ Kokoro TTS connection lost or invalid", "red"))
            cls.kokoro_tts = None
            from karhu import globals as karhu_globals
            karhu_globals.kokoro_mode = False
            karhu_globals.tts_mode = False
            return False
    



    @staticmethod
    def process_command(command, assistant):
        """Process special commands"""
        parts = command.split(' ', 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == '!files':
            if os.path.isdir(arg):
                print("Reading FILESs from directory...")
                files_library = assistant.doc_processor.process_files_directory(arg)
                assistant.current_context = "\n".join(files_library.values())
                assistant.add_to_history("user", command)
                file_list = "\n".join(files_library.keys())
                print(f"Loaded {len(files_library)} files:\n{file_list}")
            print("Directory not found!")

        elif cmd == '!file':
            try:
                if os.path.exists(arg):
                    if os.path.isdir(arg):
                        print(colored("\nCannot open a directory! please provide a path to a file", "red"))
                        return
                    print(colored("\n 🔎 Reading file...", "green"))
                    file_content = assistant.doc_processor.read_file(arg)
                    # Use the enhanced add_to_context method
                    assistant.context_manager.add_to_context(
                        file_content, 
                        source_type="file", 
                        source_name=os.path.basename(arg)
                    )
                    return colored(f"\n ✓ File {arg} loaded successfully!\n ⌀ Context length: {len(assistant.context_manager.current_context)} characters\n", "green")
                else:
                    return colored("\n ⅹ File not found!", "red")
            except Exception as e:
                Errors.handle_error("Failed to process file command.", e)

        elif cmd == '!browse':
            try:
                print(colored(f"\n 🌐 Browsing {arg}...", "green"))
                web_content = assistant.web_browser.browse_url(arg)
                
                # Use the enhanced add_to_context method
                assistant.context_manager.add_to_context(
                    web_content, 
                    source_type="web", 
                    source_name=arg
                )
                
                # Create a preview of the content (first ~500 characters)
                preview_length = 500
                content_preview = web_content[:preview_length] + "..." if len(web_content) > preview_length else web_content
                
                # Display the content preview in a panel
                console = Console()
                console.print("\n[bold cyan]Web Page Content Preview:[/bold cyan]")
                console.print(Panel(content_preview, title=f"📄 {arg}", expand=False))
                
                # Show content stats
                content_length = len(web_content)
                tokens_estimate = content_length // 4
                console.print(f"\n[green]✓ Page loaded successfully![/green]")
                console.print(f"[dim]Content: {content_length} characters (~{tokens_estimate} tokens)[/dim]")
                console.print(f"[dim]Full content added to context[/dim]")
                
                return f"Webpage loaded and added to context: {arg} ({content_length} characters)"
            except Exception as e:
                Errors.handle_error("Failed to process browse command.", e)
                return f"Error browsing webpage: {str(e)}"

        elif cmd == '!search':
            print(f"Searching for: {arg}")
            results = assistant.web_browser.search_duckduckgo(arg)
            try:
                if isinstance(results, list):
                    search_context = []
                    for i, result in enumerate(results, 1):
                        print(f"\n{i}. {result['title']}")
                        print(f"   URL: {result['url']}")
                        search_context.append(f"Result {i}:\nTitle: {result['title']}\nURL: {result['url']}\nSnippet: {result['snippet']}\n")
                    
                    # Use the enhanced add_to_context method
                    combined_results = "\n".join(search_context)
                    assistant.context_manager.add_to_context(
                        combined_results, 
                        source_type="search", 
                        source_name=f"Search: {arg}"
                    )
                    return "Search results loaded and summarized in context!"
                return f"Search failed: {results}"
            except Exception as e:
                Errors.handle_error("Failed to process search command.", e)

        elif cmd == '!save':
            filename = assistant.save_conversation()
            print(colored(f"\n ✓ Conversation saved to {filename}", "green"))
            return f"Conversation saved to {filename}"
        
        elif cmd == '!clear':
            assistant.current_context = ""
            print(colored("\n 🗑️ Context cleared!", "green"))
            return "Context cleared!"
        
        elif cmd == '!clearall':
            assistant.current_context = ""
            assistant.conversation_history = []
            assistant.context_manager.clear_context()
            print(colored("\n 🗑️ Context and conversation history cleared!", "green"))
            return "Context and conversation history cleared!"

        
        elif cmd == '!setsprompt':
            new_prompt = arg
            try:
                with open(assistant.system_prompt_path, 'w', encoding='utf-8') as file:
                    json.dump({"system_prompt": new_prompt}, file, indent=4)
                print(colored("\n ✓ System prompt updated successfully!", "green"))
                return 1
            except Exception as e:
                print(colored(f"Error updating system prompt: {str(e)}", "red"))


        elif cmd == '!system_prompt':
            print(colored(f"Current system prompt: {assistant.get_system_prompt()}", "green"))
            return 1 


        elif cmd == '!create_profile':
            try:
                # Parse arguments: profile_name:system_prompt
                if ':' not in arg:
                    print(colored("Usage: !create_profile profile_name:system_prompt", "red"))
                    return "Invalid format. Use !create_profile profile_name:system_prompt"
                    
                profile_name, system_prompt = arg.split(':', 1)
                profile_name = profile_name.strip()
                system_prompt = system_prompt.strip()
                
                if not profile_name or not system_prompt:
                    print(colored("Both profile name and system prompt are required", "red"))
                    return "Both profile name and system prompt are required"
                
                # Check if profile already exists
                profiles = ProfileManager.get_profiles()
                if profile_name in profiles:
                    print(colored(f"Profile '{profile_name}' already exists. Use a different name.", "yellow"))
                    return f"Profile '{profile_name}' already exists. Use a different name."
                    
                # Create the new profile
                success = ProfileManager.create_profile(profile_name, system_prompt)
                if success:
                    print(colored(f"Profile '{profile_name}' created successfully.", "green"))
                    return f"Profile '{profile_name}' created successfully."
                else:
                    print(colored("Failed to create profile.", "red"))
                    return "Failed to create profile."
                    
            except Exception as e:
                Errors.handle_error("Failed to create profile.", e)
                return f"Error creating profile: {str(e)}"

        # Replace the !model command implementation with this:
        elif cmd == '!model':
            try:
                # Clean and validate the model name
                model_name = arg.strip()
                if not model_name:
                    print(colored("Usage: !model <model_name>", "red"))
                    return "Model name cannot be empty."

                # Check if the model exists
                model_config = ModelManager.get_model_config(model_name)
                if not model_config:
                    return f"Model '{model_name}' not found. Use !list_models to see available models."

                # Set as current model
                ModelManager.set_current_model(model_name)

                # Dynamically update the assistant's model and related attributes
                assistant.model = model_config.get('model', 'gpt-4o')
                assistant.temp = model_config.get('temp', 0.7)
                assistant.max_tokens = model_config.get('max_tokens', 4096)
                assistant.top_p = model_config.get('top_p', 1)
                assistant.update_api_type_from_model(model_name)

                print(colored(f"Switched to model: {model_name}", "green"))
                return f"Model switched to: {model_name}"

            except ValueError:
                print(colored("Usage: !model <model_name>", "red"))
                return "Invalid model name."
            except Exception as e:
                Errors.handle_error("Failed to switch model.", e)
                return f"Error switching model: {str(e)}"
        
        elif cmd == '!list_models':
            try:
                models = ModelManager.get_models()
                if not models:
                    return "No models found."
                
                current = ModelManager.get_current_model()
                response = colored("\nAvailable models:\n", "cyan")
                for name, config in models.items():
                    model_id = config.get('model', name)
                    if name == current:
                        response += f"* {name} ({model_id}) (current)\n"
                    else:
                        response += f"- {name} ({model_id})\n"
                print(response)
                return response
            except Exception as e:
                Errors.handle_error("Failed to list models.", e)
                return f"Error listing models: {str(e)}"

        # switch to a new profile commands for system prompt management
        elif cmd == '!profile':
            try:
                # Clean and validate the profile name
                profile_name = arg.strip()
                if not profile_name:
                    print(colored("Usage: !profile <profile_name>", "red"))
                    return "Profile name cannot be empty."

                # Check if the profile exists
                profiles = ProfileManager.get_profiles()
                if profile_name not in profiles:
                    print(colored(f"Profile '{profile_name}' does not exist.", "red"))
                    return f"Profile '{profile_name}' not found. Use !list_profiles to see available profiles."

                # Apply the selected profile's system prompt
                system_prompt = profiles[profile_name]["system_prompt"]
                assistant.set_system_prompt(system_prompt)
                ProfileManager.set_current_profile(profile_name)
                
                print(colored(f"Switched to profile: {profile_name}", "green"))
                return f"Profile switched to: {profile_name}"

            except Exception as e:
                Errors.handle_error("Failed to switch profile.", e)
                return f"Error switching profile: {str(e)}"

        elif cmd == '!list_profiles':
            try:
                profiles = ProfileManager.get_profiles()
                if not profiles:
                    return "No profiles found."
                
                current = ProfileManager.get_current_profile()
                response = colored("\nAvailable profiles:\n", "cyan")
                for name in profiles:
                    if name == current:
                        response += f"* {name} (current)\n"
                    else:
                        response += f"- {name}\n"
                print(response)
                return response
            except Exception as e:
                Errors.handle_error("Failed to list profiles.", e)
                return f"Error listing profiles: {str(e)}"

        # Speech-to-text toggle
        if cmd == "!lazy":
            globals.stt_mode = not globals.stt_mode
            return f"Speech input mode {'enabled' if globals.stt_mode else 'disabled'}."
        
        # Text-to-speech toggle
        elif cmd == "!speak":
            if globals.tts_mode:
                # If already enabled, disable it
                globals.tts_mode = False
                print(colored(f"\n 🎤 Speech output mode disabled ⅹ", "green"))
            else:
                # Enable TTS and make sure it's loaded
                if CommandProcessor.tts is False:
                    globals.tts_mode = False
                    print(colored(f"\n ⅹ Failed to initialize TTS. Check credentials and try again.", "red"))
                elif CommandProcessor.ensure_tts_loaded():
                    globals.tts_mode = True
                    print(colored(f"\n 🎤 Speech output mode enabled ✓", "green"))
            return "command processed"
                        
        elif cmd == "!voices":
            # Initialize TTS if needed
            if CommandProcessor.ensure_tts_loaded():
                voices = CommandProcessor.tts.list_available_voices()
                response = colored("\nAvailable voices:\n", "cyan")
                for idx, name, voice_id in voices:
                    response += f"{idx}: {name}\n"
                print(response)
                return response
            else:
                return "Failed to initialize text-to-speech."
                  
        # Change voice google cloud TTS
        elif cmd == "!voice":
            # Initialize TTS if needed
            if not CommandProcessor.ensure_tts_loaded():
                return "Failed to initialize text-to-speech."
            
            if not arg:
                return print(colored("Please provide a voice index. Example: !voice 0", "red"))
            
            try:
                voice_idx = int(arg)
                if CommandProcessor.tts.set_voice(voice_idx):
                    current_idx, name, _ = CommandProcessor.tts.get_current_voice()
                    print(colored(f"\n ⌮ Voice changed to: {name}", "green"))
                    return f"Voice changed to: {name}"
                else:
                    return print(colored("Invalid voice index. Use !voices to see available options.", "red"))
            except ValueError:
                return print(colored("Please provide a numeric voice index.", "red"))

        
        elif cmd == "!kokoro":
            if globals.kokoro_mode:
                # If already enabled, disable it
                globals.kokoro_mode = False
                print(colored(f"\n 🎤 Kokoro speech mode disabled ⅹ", "green"))
            else:
                # Enable Kokoro TTS and make sure it's loaded, with a timeout parameter
                if CommandProcessor.ensure_kokoro_loaded(timeout=3):  # Use a 3 second timeout
                    globals.tts_mode = True
                    globals.kokoro_mode = True
                    
                    # Get the current voice information when enabling Kokoro
                    current_idx, voice_name, voice_id = CommandProcessor.kokoro_tts.get_current_voice()
                    print(colored(f"\n 🎤 Kokoro speech mode enabled ✓ using voice: {voice_name} ({voice_id})", "green"))
                else:
                    print(colored(f"\n ⅹ Failed to initialize Kokoro TTS. Speech mode not enabled.", "red"))
                    globals.kokoro_mode = False
                    globals.tts_mode = False
            return 1

        elif cmd == "!kokoro_voices":
            if CommandProcessor.kokoro_tts:
                voices = CommandProcessor.kokoro_tts.list_available_voices()
                response = colored("\nAvailable Kokoro voices:\n", "cyan")
                for idx, name, voice_id in voices:
                    response += f"{idx}: {name} ({voice_id})\n"
                print(response)
                return response
            else:
                return "Kokoro TTS not initialized."

        elif cmd == "!kokoro_voice":
            if not CommandProcessor.kokoro_tts:
                return "Kokoro TTS not initialized."
            
            if not arg:
                return print(colored("Please provide a voice index. Example: !kokoro_voice 0", "red"))
            
            try:
                voice_idx = int(arg)
                if CommandProcessor.kokoro_tts.set_voice(voice_idx):
                    current_idx, name, voice_id = CommandProcessor.kokoro_tts.get_current_voice()
                    print(colored(f"\n ⌮ Kokoro voice changed to: {name}", "green"))
                    return f"Voice changed to: {name} ({voice_id})"
                else:
                    return print(colored("Invalid voice index. Use !kokoro_voices to see available options.", "red"))
            except ValueError:
                return print(colored("Please provide a numeric voice index.", "red"))

        elif cmd == "!kokoro_blend":
            if not CommandProcessor.kokoro_tts:
                return "Kokoro TTS not initialized."
            
            try:
                voice_indices = [int(idx) for idx in arg.split()]
                if not voice_indices or len(voice_indices) > 3:
                    return print(colored("Please provide 1-3 voice indices. Example: !kokoro_blend 0 1", "red"))
                
                voice_ids = []
                for idx in voice_indices:
                    voices = CommandProcessor.kokoro_tts.list_available_voices()
                    if 0 <= idx < len(voices):
                        _, _, voice_id = voices[idx]
                        voice_ids.append(voice_id)
                
                if not voice_ids:
                    return print(colored("No valid voice indices provided.", "red"))
                
                blended_voice = CommandProcessor.kokoro_tts.blend_voices(voice_ids)
                CommandProcessor.kokoro_tts.voice = blended_voice
                
                print(colored(f"\n ⌮ Kokoro voices blended: {blended_voice}", "green"))
                return f"Voices blended: {blended_voice}"
            except ValueError:
                return print(colored("Please provide numeric voice indices.", "red"))


        elif cmd == '!context_size':
            context_length = len(assistant.context_manager.current_context)
            tokens_estimate = context_length // 4  # Rough estimate of tokens
            print(colored(f"Context size: {context_length} characters (approx. {tokens_estimate} tokens)", "green"))
            return f"Context size: {context_length} characters (approx. {tokens_estimate} tokens)"

        elif cmd == '!optimize_context':
            old_size = len(assistant.context_manager.current_context)
            optimized = assistant.context_manager.optimize_content(assistant.context_manager.current_context)
            assistant.context_manager.current_context = optimized
            new_size = len(assistant.context_manager.current_context)
            reduction = ((old_size - new_size) / old_size) * 100 if old_size > 0 else 0
            print(colored(f"Context optimized: {old_size} → {new_size} chars ({reduction:.1f}% reduction)", "green"))
            return f"Context optimized: {old_size} → {new_size} chars ({reduction:.1f}% reduction)"

        elif cmd == '!search_context':
            query = arg.strip()
            if not query:
                print(colored("Please provide a search term", "red"))
                return "Please provide a search term"
            
            results = assistant.context_manager.search_context(query)
            if results:
                # Format results to make them more readable
                formatted_results = f" ✓ Found relevant content for '{query}':\n\n{results}"
                print(colored(f"Found relevant content for '{query}'", "green"))
                return formatted_results
            else:
                print(colored(f" ⅹ No matches found for '{query}'", "red"))
                return f"No matches found for '{query}' in context."
        
        elif cmd == '!chunk':
            try:
                chunk_id = arg.strip()
                if not chunk_id:
                    # List available chunks
                    chunks = list(assistant.context_manager.chunks.keys())
                    if not chunks:
                        print(colored(" ⅹ No document chunks available", "red"))
                        return "No document chunks available"
                    
                    chunk_list = "\n".join(chunks)
                    print(colored(" → Available chunks:", "green"))
                    print(chunk_list)
                    return "Available chunks:\n" + chunk_list
                
                # Retrieve specific chunk
                chunk = assistant.context_manager.get_chunk(chunk_id)
                if chunk != "Chunk not found":
                    print(colored(f" → Retrieved chunk: {chunk_id}", "green"))
                    return chunk
                else:
                    print(colored(f" ⅹ Chunk not found: {chunk_id}", "red"))
                    return f"Chunk not found: {chunk_id}"
            except Exception as e:
                print(colored(f"Error retrieving chunk: {str(e)}", "red"))
                return f"Error retrieving chunk: {str(e)}"

        elif cmd == '!context_info':
            try:
                context = assistant.context_manager.current_context
                chunk_count = len(assistant.context_manager.chunks)
                context_size = len(context)
                token_estimate = context_size // 4  # Rough estimate
                
                info = f"Context Information:\n"
                info += f"- Size: {context_size} characters (approx. {token_estimate} tokens)\n"
                info += f"- Stored chunks: {chunk_count}\n"
                
                # Extract source types from context
                sources = re.findall(r'Source: (\w+)', context)
                source_counts = {}
                for source in sources:
                    if source in source_counts:
                        source_counts[source] += 1
                    else:
                        source_counts[source] = 1
                        
                if source_counts:
                    info += "- Content sources:\n"
                    for source, count in source_counts.items():
                        info += f"  • {source}: {count} entries\n"
                
                print(colored(info, "cyan"))
                return info
            except Exception as e:
                print(colored(f"Error getting context info: {str(e)}", "red"))
                return f"Error getting context info: {str(e)}"
          
        elif cmd == '!quit':
            print("Exiting program...")
            time.sleep(1)
            exit()

        elif cmd == '!help':
            Displayhelp.display_commands()
            return 1
        else:
            return None
