import os
import re
from karhu import globals
from termcolor import colored

# Check for DISABLE_AUDIO flag
if os.environ.get("DISABLE_AUDIO"):
    class TextToSpeech:
        def __init__(self, *args, **kwargs):
            print("TextToSpeech (Google Cloud) disabled.")
            self.is_valid = False # Mark as invalid

        def clean_text_for_speech(self, text):
            return text # Just return the text

        def list_available_voices(self):
            print("TextToSpeech disabled: list_available_voices() called.")
            return []

        def get_current_voice(self):
            print("TextToSpeech disabled: get_current_voice() called.")
            return 0, "Disabled", "disabled"

        def set_voice(self, voice_index):
            print("TextToSpeech disabled: set_voice() called.")
            return False

        def speak(self, text):
            print("TextToSpeech disabled: speak() called.")

        def stop(self):
            print("TextToSpeech disabled: stop() called.")

else:
    
    from google.cloud import texttospeech
    import platform
    import os
    import tempfile
    import subprocess
    import re 
    from karhu import globals
    from termcolor import colored

    class TextToSpeech:
        def __init__(self, voice_name="en-US-Chirp-HD-O", language_code="en-US", speaking_rate=1.0):
            """
            Initialize Google Cloud TTS.
            
            Args:
                voice_name: Voice name (e.g., "en-US-Neural2-F" for a female voice)
                language_code: Language code (e.g., "en-US")
                speaking_rate: Speed of speech (1.0 is normal speed)
            """
            try:
                self.client = texttospeech.TextToSpeechClient()
                self.voice = texttospeech.VoiceSelectionParams(
                    language_code=language_code,
                    name=voice_name
                )
                self.audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3,
                    speaking_rate=speaking_rate
                )
                self.current_process = None
                print(colored(" ✓ Google TTS initialized with voice: " + voice_name, "green"))    
            except Exception as e:
                print(colored(" ⅹ Error initializing Google TTS: " + str(e), "red"))
                # Mark this instance as invalid
                self.client = None
                self.is_valid = False
                # Don't set other properties
                return  # Stop initialization here
            
            # Mark as valid if we get here
            self.is_valid = True



        def clean_text_for_speech(self, text):
            """
            Remove markdown formatting, emojis, and other non-speech elements
            to make the text more suitable for speech synthesis.
            """
            # Remove markdown elements
            cleaned = text.replace('*', '').replace('#', '').replace('`', '')
            
            # Remove emojis and other special unicode characters
            # This handles most emoji ranges
            cleaned = re.sub(globals.EMOJI_PATTERN, '', cleaned)
            
            # Replace common symbols with their spoken form
            cleaned = cleaned.replace('&', ' and ')
            cleaned = cleaned.replace('%', ' percent ')
            
            # Remove multiple spaces
            cleaned = re.sub(r'\s+', ' ', cleaned)
            
            return cleaned.strip()

        def list_available_voices(self):
            """List available voices from Google Cloud"""
            response = self.client.list_voices()
            voices = []
            
            for i, voice in enumerate(response.voices):
                # Filter for US English female voices only
                if "en-US" in voice.language_codes and voice.ssml_gender == texttospeech.SsmlVoiceGender.FEMALE:
                    # Add to the list (with a counter separate from the original enumeration)
                    if len(voices) < 15:  # Limit to 10 voices
                        voices.append((len(voices), voice.name, voice.name))
                    
            return voices
        
        def get_current_voice(self):
            """Get current voice"""
            return 0, self.voice.name, self.voice.name
        
        def set_voice(self, voice_index):
            """Set voice by index"""
            voices = self.list_available_voices()
            if 0 <= voice_index < len(voices):
                _, _, voice_name = voices[voice_index]
                self.voice.name = voice_name
                return True
            return False
        
        def speak(self, text):
            """Convert text to speech and play it"""
            if not text or self.client is None:
                return
            
            clean_text = self.clean_text_for_speech(text)

            # Truncate text if too long (API limit)
            if len(clean_text) > 5000:
                clean_text = clean_text[:5000] + "..."

            synthesis_input = texttospeech.SynthesisInput(text=clean_text)
            
            # Generate audio
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=self.voice,
                audio_config=self.audio_config
            )
            
            # Save audio to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                f.write(response.audio_content)
                temp_file = f.name
            
            # Stop any currently playing audio
            self.stop()
            
            # Use platform-appropriate audio player
            

            system = platform.system()
            if system == "Darwin":  # macOS
                self.current_process = subprocess.Popen(["afplay", temp_file])
            elif system == "Linux":
                self.current_process = subprocess.Popen(["mpg123", temp_file])
            else:
                print(f"Unsupported platform for audio playback: {system}")
                # Fall back to Python's built-in audio playback if available 
                ## @TODO LATER 
            self.current_process.wait()  # Wait for audio to finish
            
            # Clean up temporary file
            os.unlink(temp_file)
            
        def stop(self):
            """Stop currently playing audio"""
            if self.current_process and self.current_process.poll() is None:
                # Process is still running, terminate it
                self.current_process.terminate()
                self.current_process = None