import os

# Check for DISABLE_RECORD_AUDIO flag
if os.environ.get("DISABLE_AUDIO"):
    class RecordAudio:
        def __init__(self, stt, device_index=None):
            self.stt = stt
            print("RecordAudio disabled.")

        def start_recording(self):
            print("RecordAudio disabled: start_recording() called.")

        def stop_recording(self):
            print("RecordAudio disabled: stop_recording() called.")
            return ""
        
        def listen_for_speech(self):
            print("RecordAudio disabled: listen_for_speech() called.")
            return "", False
        
        def _flush_input(self):
            pass
else:
    # Import the globals module with a more specific name to avoid conflicts
    from karhu import globals as karhu_globals
    import threading
    import pyaudio
    import wave
    import tempfile
    import os
    from pynput import keyboard
    from termcolor import colored
    import time
    import queue
    import platform

    class RecordAudio:
        def __init__(self, stt, device_index=None):
            """Initialize with a reference to the SpeechToText object"""
            self.stt = stt
            self.recording = False
            self.frames = []
            self.p = None
            self.audio_stream = None
            self.user_input = ""
            self.exit_speech_mode = False
            self.lock = threading.Lock()  # Add a lock for thread safety
            self.device_index = device_index  # Add device index
            self.transcription_queue = queue.Queue()  # Queue for passing transcribed text
        
        def start_recording(self):
            """Start recording audio"""
            with self.lock:
                if self.recording:
                    return
                self.recording = True
                self.frames = []
                try:
                    self.p = pyaudio.PyAudio()

                    # If no device_index is provided, detect the default input device
                    if self.device_index is None:
                        system = platform.system()
                        try:
                            default_input = self.p.get_default_input_device_info()
                            self.device_index = default_input.get('index')
                        except Exception as e:
                            print(colored(f"Error retrieving default input device: {e}", "red"))
                            return

                    self.audio_stream = self.p.open(
                        format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=1024,
                        input_device_index=self.device_index  # Use detected device index
                    )
                    print(colored("\r🎤 Recording... (Hold spacebar)", "green"), end="", flush=True)
                    
                    # Start a background thread to capture audio frames
                    self.recording_thread = threading.Thread(target=self._capture_frames)
                    self.recording_thread.daemon = True
                    self.recording_thread.start()
                    
                except Exception as e:
                    print(colored(f"Error starting recording: {e}", "red"))
                    self.recording = False
                    self.audio_stream = None
                    self.p = None
                    
        def _capture_frames(self):
            """Capture audio frames while recording is active"""
            while self.recording and self.audio_stream:
                try:
                    data = self.audio_stream.read(1024, exception_on_overflow=False)
                    self.frames.append(data)
                except Exception as e:
                    print(colored(f"Error capturing audio: {e}", "red"))
                    break
        
        def stop_recording(self):
            """Stop recording and transcribe audio"""
            with self.lock:
                if not self.recording:
                    return ""
                
                print(colored("\r🔍 Processing...", "green") + " " * 30)
                self.recording = False
                
                # Wait for recording thread to finish if it exists
                if hasattr(self, 'recording_thread') and self.recording_thread.is_alive():
                    self.recording_thread.join(timeout=1.0)
                
                # Stop recording
                if self.audio_stream:
                    try:
                        self.audio_stream.stop_stream()
                        self.audio_stream.close()
                    except Exception as e:
                        print(colored(f"Error stopping stream: {e}", "red"))
                if self.p:
                    try:
                        self.p.terminate()
                    except Exception as e:
                        print(colored(f"Error terminating PyAudio: {e}", "red"))
                
                # Check if we got any audio data
                if not self.frames:
                    print(colored("No audio data recorded", "yellow"))
                    return ""
                    
                # Create a temporary file for audio
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    temp_audio_file = temp_file.name
                    
                    # Save recorded audio
                    try:
                        with wave.open(temp_audio_file, 'wb') as wf:
                            wf.setnchannels(1)
                            if self.p:
                                wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
                            else:
                                wf.setsampwidth(2)  # Default to 2 bytes if p is None
                            wf.setframerate(16000)
                            wf.writeframes(b''.join(self.frames))
                    except Exception as e:
                        print(colored(f"Error saving audio: {e}", "red"))
                        return ""
                
                # Transcribe the audio
                try:
                    self.user_input = self.stt.transcribe_audio(temp_audio_file)
                except Exception as e:
                    print(colored(f"Error transcribing audio: {e}", "red"))
                    self.user_input = ""
                
                # Clean up temporary file
                try:
                    os.unlink(temp_audio_file)
                except Exception as e:
                    print(colored(f"Error deleting temp file: {e}", "red"))
                
                print(colored(f"\rYou said: {self.user_input}", "green"))
                
                # Check for exit commands
                if self.user_input.lower() in ["stop listening", "exit speech mode", 
                                            "disable speech", "turn off speech",
                                            "stop speech", "stop stt", "stop"]:
                    self.exit_speech_mode = True
                    self.user_input = ""  # Clear input
                    print(colored("Speech input mode disabled.", "yellow"))
                    karhu_globals.stt_mode = False  # Update global state here
                
                return self.user_input
        
        def listen_for_speech(self):
            """Main method to handle push-to-talk functionality"""
            self.exit_speech_mode = False
            self.user_input = ""
            
            print(colored("\nHold SPACEBAR to talk, release when finished...", "green"))
            print(colored("(Press ESC to exit speech mode)", "yellow"))
            
            # Define handlers for keyboard events
            def on_press(key):
                if key == keyboard.Key.space:
                    self.start_recording()
                elif key == keyboard.Key.esc:
                    print(colored("\nExiting speech mode.", "yellow"))
                    self.exit_speech_mode = True
                    karhu_globals.stt_mode = False  # Update global state here
                    return False  # Stop listener
            
            def on_release(key):
                if key == keyboard.Key.space:
                    transcription = self.stop_recording()
                    self.transcription_queue.put(transcription)  # Put transcription in queue
                    return False  # Stop listener
            
            # Use keyboard listener to detect key presses
            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                try:
                    listener.join()  # Wait for key release or Esc
                except AttributeError:
                    # Handle the AttributeError that can occur when the listener stops
                    pass
                
            # Get transcription from queue
            try:
                self.user_input = self.transcription_queue.get_nowait()
            except queue.Empty:
                self.user_input = ""
            
            self._flush_input()  # Flush any pending input from stdin

            return self.user_input, self.exit_speech_mode
        
        def _flush_input(self):
            """Flush any pending input from stdin to prevent it from affecting the interactive mode"""
            try:
                import sys
                import termios
                import tty
                
                # For Unix-like systems
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            except (ImportError, AttributeError):
                try:
                    # For Windows
                    import msvcrt
                    while msvcrt.kbhit():
                        msvcrt.getch()
                except ImportError:
                    # Simple fallback - just yield processor time to allow any pending input to clear
                    time.sleep(0.1)