import os
import re
from karhu import globals
import platform

# Check for DISABLE_AUDIO flag
if os.environ.get("DISABLE_AUDIO"):
    class KokoroTTS:
        def __init__(self, *args, **kwargs):
            print("KokoroTTS disabled.")

        def clean_text_for_speech(self, text):
            return text

        def list_available_voices(self):
            print("KokoroTTS disabled: list_available_voices() called.")
            return []

        def blend_voices(self, voice_ids, weights=None):
            print("KokoroTTS disabled: blend_voices() called.")
            return "disabled_blend"

        def get_current_voice(self):
            print("KokoroTTS disabled: get_current_voice() called.")
            return 0, "Disabled", "disabled"

        def set_voice(self, voice_index):
            print("KokoroTTS disabled: set_voice() called.")
            return False

        def stop(self):
            print("KokoroTTS disabled: stop() called.")

        def stream_speech(self, text):
            print("KokoroTTS disabled: stream_speech() called.")

        def speak(self, text):
            print("KokoroTTS disabled: speak() called.")

else:
    # Original imports only needed if audio is enabled
    import pyaudio
    from openai import OpenAI
    import requests
    from termcolor import colored

    class KokoroTTS:
        """
        A class for interacting with Kokoro TTS running in a Docker container.
        Supports direct streaming to audio output for faster response times.
        """
        
        def __init__(self, base_url="http://192.168.1.69:8880/v1", voice="af_bella", connection_timeout=10):
            """
            Initialize Kokoro TTS client.
            
            Args:
                base_url: URL to the Kokoro TTS API (default: http://localhost:8880/v1)
                voice: Voice ID or combination to use (default: af_bella)
                connection_timeout: Timeout in seconds for API connection attempts (default: 3)
            """
            self.client = OpenAI(base_url=base_url, api_key="not-needed")
            self.voice = voice
            self.player = None
            self.is_playing = False
            self.connection_timeout = connection_timeout
            
            # Test connection to the API to verify if it's properly initialized
            self.is_initialized = False
            try:
                # Try to retrieve voices as a connection test with timeout
                voices = self.list_available_voices(timeout=self.connection_timeout)
                if voices and len(voices) > 0:
                    self.is_initialized = True
            except Exception as e:
                print(colored(f"Failed to initialize Kokoro TTS: {e}", "red"))
                self.is_initialized = False
            
        def clean_text_for_speech(self, text):
            """
            Remove markdown formatting and other non-speech elements.
            """
            # Remove markdown elements
            cleaned = text.replace('*', '').replace('#', '').replace('`', '')
            
            # Remove emojis and special characters
            if hasattr(globals, 'EMOJI_PATTERN'):
                cleaned = re.sub(globals.EMOJI_PATTERN, '', cleaned)
            
            # Replace common symbols with spoken form
            cleaned = cleaned.replace('&', ' and ')
            cleaned = cleaned.replace('%', ' percent ')
            
            # Remove multiple spaces
            cleaned = re.sub(r'\s+', ' ', cleaned)
            
            return cleaned.strip()

        def list_available_voices(self, timeout=None):
            """
            Retrieve available voices from the Kokoro TTS API.
            Returns a list of tuples (index, voice_name, voice_id).
            
            Args:
                timeout: Request timeout in seconds (default: None)
            """
            api_url = "http://192.168.1.69:8880/v1/audio/voices"
            try:
                # Use timeout parameter to avoid hanging indefinitely
                if timeout is None:
                    timeout = getattr(self, 'connection_timeout', 3)  # Default to 3 seconds if not specified
                
                print(colored(f"Connecting to Kokoro TTS API (timeout: {timeout}s)...", "blue"))
                response = requests.get(api_url, timeout=timeout)
                response.raise_for_status()
                voices_data = response.json()
                
                # Handle different possible response formats
                voices = []
                if isinstance(voices_data, dict) and 'voices' in voices_data:
                    # Filter for English voices (those starting with 'af_' for American female)
                    voice_list = [v for v in voices_data['voices'] if v.startswith('af_')]
                    
                    # Create display names from IDs
                    for idx, voice_id in enumerate(voice_list):
                        # Create a nicer display name from the ID
                        display_name = voice_id.replace('af_', '').title()
                        if voice_id.startswith('af_v0'):
                            display_name = f"{display_name} (V0)"
                        else:
                            display_name = f"{display_name}"
                            
                        voices.append((idx, display_name, voice_id))
                elif isinstance(voices_data, list):
                    # Direct list of voice IDs
                    voice_list = [v for v in voices_data if isinstance(v, str) and v.startswith('af_')]
                    for idx, voice_id in enumerate(voice_list):
                        display_name = voice_id.replace('af_', '').title()
                        if voice_id.startswith('af_v0'):
                            display_name = f"{display_name} (V0)"
                        else:
                            display_name = f"{display_name}"
                            
                        voices.append((idx, display_name, voice_id))
                        
                # If voices found, return them
                if voices:
                    return voices
                    
                # If no voices found, use defaults
                print("No compatible voices found in API response, using defaults")
                # Return a default list if API fails or returns no voices
                return [(0, "Default Bella", "af_bella")] 

            except requests.Timeout:
                print(colored(f"Timeout connecting to Kokoro TTS API after {timeout}s", "red"))
                raise TimeoutError(f"Connection to Kokoro TTS API timed out after {timeout}s")
            except requests.RequestException as e:
                print(colored(f"Error fetching voices from API: {e}", "red"))
                raise  # Re-raise the exception to be caught in __init__
            except Exception as e:
                print(colored(f"Error processing voices from API: {str(e)}", "red"))
                raise  # Re-raise the exception to be caught in __init__
        
        def blend_voices(self, voice_ids, weights=None):
            """
            Create a voice blend from multiple voice IDs.
            
            Args:
                voice_ids (list): List of voice IDs to blend
                weights (list, optional): List of weights for each voice. 
                                        Should sum to 1.0. Defaults to equal weights.
            
            Returns:
                str: The blended voice ID string
            """
            if not voice_ids:
                return self.voice
                
            if len(voice_ids) == 1:
                return voice_ids[0]
            
            # Create the blended voice ID string (e.g., "af_sky+af_bella")
            return "+".join(voice_ids)

        def get_current_voice(self):
            """Get current voice"""
            available_voices = self.list_available_voices()
            if not available_voices: # Handle case where list is empty
                 return 0, "Unknown", self.voice
            for i, name, voice_id in available_voices:
                if voice_id == self.voice:
                    return i, name, voice_id
            # If current voice not found in list, return the first available one
            return available_voices[0] 
        
        def set_voice(self, voice_index):
            """Set voice by index"""
            voices = self.list_available_voices()
            if voices and 0 <= voice_index < len(voices):
                _, _, voice_id = voices[voice_index]
                self.voice = voice_id
                return True
            return False
        
        def stop(self):
            """Stop currently playing audio"""
            self.is_playing = False
            if self.player:
                try:
                    self.player.stop_stream() # Stop stream before closing
                    self.player.close()
                except Exception as e:
                    print(f"Error stopping PyAudio stream: {e}") # Log potential errors
                finally:
                    self.player = None
                    # Terminate PyAudio instance if needed (consider if p is shared)
                    # p.terminate() # Be careful if p is used elsewhere
        
        def stream_speech(self, text):
            """
            Stream text to speech directly to audio output.
            This method bypasses file creation for faster response.
            """
            if not text:
                return
            
            clean_text = self.clean_text_for_speech(text)
            
            # Truncate text if too long
            if len(clean_text) > 5000:
                clean_text = clean_text[:5000] + "..."
            
            # Stop any currently playing audio
            self.stop()
            
            # Initialize PyAudio player
            p = None # Initialize p to None
            try:
                p = pyaudio.PyAudio()
                system = platform.system()
                device_index = None # Default to None
                if system == "Linux":
                    try:
                        # Retrieve the default output device index on Linux
                        default_output = p.get_default_output_device_info()
                        device_index = default_output.get('index')
                    except Exception as e:
                        print(f"Error retrieving default audio device: {e}")
                        # Don't return, try default device
                
                self.player = p.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=24000,
                    output=True,
                    output_device_index=device_index # Use None if not Linux or error
                )
                
                self.is_playing = True
                
                with self.client.audio.speech.with_streaming_response.create(
                    model="kokoro",
                    voice=self.voice,
                    response_format="pcm",
                    input=clean_text
                ) as response:
                    # Stream directly to audio output
                    for chunk in response.iter_bytes(chunk_size=1024):
                        if not self.is_playing:
                            break
                        if self.player: # Check if player exists before writing
                            self.player.write(chunk)
                        else:
                            break # Stop if player was closed
                    
            except Exception as e:
                print(f"Error streaming speech: {str(e)}")
            finally:
                self.stop() # Ensure stop is called to clean up player
                if p: # Terminate PyAudio instance if it was created
                    p.terminate()
        
        def speak(self, text):
            """
            Alias for stream_speech to maintain compatibility with TextToSpeech class.
            """
            self.stream_speech(text)