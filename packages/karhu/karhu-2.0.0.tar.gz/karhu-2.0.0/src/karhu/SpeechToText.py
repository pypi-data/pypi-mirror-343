import os

# Check for DISABLE_AUDIO flag
if os.environ.get("DISABLE_AUDIO"):
    class SpeechToText:
        def __init__(self, *args, **kwargs):
            print("SpeechToText disabled.")
            self.client_initialized = False # Ensure this flag exists

        def record_audio(self, duration=5, output_file="input.wav"):
            print("SpeechToText disabled: record_audio() called.")
            # Need to return a valid path, even if dummy, or handle None return
            # Creating an empty dummy file might be safest for callers expecting a file
            try:
                with open(output_file, "w") as f:
                    f.write("") # Create empty file
                return output_file
            except Exception as e:
                 print(f"Could not create dummy audio file: {e}")
                 return None # Or raise an error

        def transcribe_audio(self, file_path):
            print("SpeechToText disabled: transcribe_audio() called.")
            return "Transcription unavailable (audio disabled)."

        def listen_and_transcribe(self, duration=15):
            print("SpeechToText disabled: listen_and_transcribe() called.")
            # Optionally call dummy record_audio to create the file if needed
            # self.record_audio(duration=duration)
            return "Transcription unavailable (audio disabled)."

else:
    # Original imports only needed if audio is enabled
    import pyaudio
    import wave
    from google.cloud import speech
    from google.cloud.speech import RecognitionConfig, RecognitionAudio
    import google.auth # Import the auth module to catch the specific exception

    class SpeechToText:
        def __init__(self, language_code="en-US", rate=16000, chunk_size=1024):
            self.language_code = language_code
            self.rate = rate
            self.chunk_size = chunk_size
            self.client = None # Initialize client to None
            self.client_initialized = False # Flag to track initialization status
            try:
                self.client = speech.SpeechClient()
                self.client_initialized = True # Set flag to True if successful
            except google.auth.exceptions.DefaultCredentialsError:
                print("--------------------------------------------------------------------")
                print("⚠️ Google Cloud Credentials Error:")
                print("Speech-to-text functionality requires authentication.")
                print("Please set up your Google Cloud credentials.")
                print("Run 'gcloud auth application-default login' in your terminal,")
                print("or set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
                print("--------------------------------------------------------------------")
                # Don't raise the exception, allow the program to continue
            except Exception as e:
                # Catch other potential initialization errors
                print(f"Failed to initialize Google Speech client: {e}")
                # Optionally re-raise or handle other errors differently
                # raise

        def record_audio(self, duration=5, output_file="input.wav"):
            """
            Record audio from the microphone and save it as a WAV file.
            """
            p = pyaudio.PyAudio()
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )

            print(f"Recording for {duration} seconds...")
            frames = []

            for _ in range(0, int(self.rate / self.chunk_size * duration)):
                data = stream.read(self.chunk_size)
                frames.append(data)

            print("Recording complete.")

            # Stop and close the stream
            stream.stop_stream()
            stream.close()
            p.terminate()

            # Save the audio to a WAV file
            with wave.open(output_file, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                wf.setframerate(self.rate)
                wf.writeframes(b"".join(frames))

            return output_file

        def transcribe_audio(self, file_path):
            """
            Transcribe audio from a WAV file using Google Speech-to-Text API.
            """
            if not self.client_initialized:
                print("Speech-to-text client not initialized due to credential error.")
                return "Transcription unavailable (credential error)."

            try:
                with open(file_path, "rb") as audio_file:
                    content = audio_file.read()

                # Check if the audio file has content
                if len(content) <= 44:  # WAV header is 44 bytes, so this would be an empty audio file
                    print("Warning: Audio file appears to be empty or corrupted")
                    return "No audio content detected"

                audio = RecognitionAudio(content=content)
                config = RecognitionConfig(
                    encoding=RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=self.rate,
                    language_code=self.language_code,
                    # Add these options to improve transcription quality
                    enable_automatic_punctuation=True,
                    model="default"  # Use the best available model
                )

                print("Transcribing audio...")
                response = self.client.recognize(config=config, audio=audio) # Use self.client here

                # Extract and return the transcription
                if response.results:
                    return response.results[0].alternatives[0].transcript
                else:
                    print("Transcription service returned no results - check audio quality")
                    return "No transcription available."
            except Exception as e:
                print(f"Error during transcription: {e}")
                return f"Transcription error: {str(e)}"

        def listen_and_transcribe(self, duration=15):
            """
            Record audio and transcribe it in one step.
            """
            if not self.client_initialized:
                print("Speech-to-text client not initialized due to credential error. Cannot transcribe.")
                # Still record, but inform user transcription won't happen
                audio_file = self.record_audio(duration=duration)
                print(f"Audio recorded to {audio_file}, but transcription is unavailable.")
                # Decide if you want to keep the file or remove it
                # os.remove(audio_file)
                return "Transcription unavailable (credential error)."

            # If client is initialized, proceed as normal
            audio_file = self.record_audio(duration=duration)
            transcription = self.transcribe_audio(audio_file)
            os.remove(audio_file)  # Clean up the temporary audio file
            return transcription