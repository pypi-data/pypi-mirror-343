# -*- coding: utf-8 -*-
# file path : src/karhu/ai_assistant.py
from karhu.document_processor import DocumentProcessor
from karhu.web_browser import WebBrowser
import os
from openai import OpenAI
from datetime import datetime
from termcolor import colored
import json
from karhu.Errors import Errors
from karhu.context_manager import ContextManager

# GLobals for Aht local API 
API_CONFIG = {
    'api_type': os.getenv('KARHU_API_TYPE', 'azure'),  # Default to azure, can be overridden by model config 
    'openai_api_key': os.getenv('OPENAI_API_KEY', ''),  
    'api_key': os.getenv('GITHUB_TOKEN', ''),
    'ollama_base_url': os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434/v1'),
}


class AIAssistant:
    def __init__(self, profile=None):
        self.client = self.setup_client()
        self.doc_processor = DocumentProcessor()
        self.web_browser = WebBrowser()
        self.conversation_history = []
        self.model = profile.get('model', 'gpt-4o')
        self.temp = profile.get('temp', 1)
        self.max_tokens = profile.get('max_tokens', 4096)
        self.top_p = profile.get('top_p', 1)
        self.context_manager = ContextManager()
        
        # Speech components are now initialized on demand via properties
        self._stt = None
        self._recorder = None
        
        self.load_current_model_and_update_api_type()
        
    @property
    def stt(self):
        """Lazy initialization of SpeechToText component"""
        if self._stt is None:
            try:
                from karhu.SpeechToText import SpeechToText
                from karhu import globals as karhu_globals
                from google.auth.exceptions import DefaultCredentialsError
                
                # Try to verify Google credentials before initializing
                try:
                    import google.auth
                    _, _ = google.auth.default()
                    credentials_available = True
                except (DefaultCredentialsError, ImportError):
                    credentials_available = False
                
                # Only proceed with initialization if credentials are available or DISABLE_AUDIO is set
                if credentials_available or os.environ.get("DISABLE_AUDIO"):
                    self._stt = SpeechToText()
                    if hasattr(self._stt, 'client_initialized') and self._stt.client_initialized:
                        print(colored("	🎙️ Speech-to-Text initialized successfully", "green"))
                    else:
                        print(colored("	⚠️ Speech-to-Text initialized with limited functionality", "yellow"))
                else:
                    print(colored("\n ⅹ	Cannot initialize Speech-to-Text: Google Cloud credentials not available", "red"))
                    print(colored(" ℹ️	Run 'gcloud auth application-default login' or set GOOGLE_APPLICATION_CREDENTIALS", "yellow"))
                    karhu_globals.stt_mode = False  # Disable STT mode since we can't initialize
                    return None
            except Exception as e:
                print(colored(f" ⅹ	Error initializing Speech-to-Text: {str(e)}", "red"))
                from karhu import globals as karhu_globals
                karhu_globals.stt_mode = False  # Disable STT mode on error
                return None
                
        return self._stt
    
    @property
    def recorder(self):
        """Lazy initialization of RecordAudio component"""
        if self._recorder is None:
            # First ensure STT is initialized
            stt = self.stt
            
            # Only initialize recorder if STT was successfully initialized
            if stt is not None:
                try:
                    from karhu.Recordaudio import RecordAudio
                    self._recorder = RecordAudio(stt)
                    print(colored(" 🎙️ Audio recorder initialized", "green"))
                except Exception as e:
                    print(colored(f" ⅹ Error initializing Audio recorder: {str(e)}", "red"))
                    from karhu import globals as karhu_globals
                    karhu_globals.stt_mode = False  # Disable STT mode on error
                    return None
            else:
                # STT failed to initialize, so we can't initialize recorder
                from karhu import globals as karhu_globals
                karhu_globals.stt_mode = False  # Ensure STT mode is disabled
                return None
                
        return self._recorder

    def setup_client(self):
        """Setup OpenAI client with configurable endpoint (Azure, OpenAI, or Ollama)"""
        try:
            api_type = API_CONFIG['api_type'].lower()
            
            if api_type == 'ollama':
                # Ollama setup 
                print(f"Setting up Ollama client with base URL: {API_CONFIG['ollama_base_url']}")
                return OpenAI(
                    base_url=API_CONFIG['ollama_base_url'],
                    api_key="ollama",  # Ollama API requires a non-empty string but doesn't verify it
                )
            elif api_type == 'azure':
                # Azure setup
                if not API_CONFIG['api_key']:
                    raise ValueError("API key for Azure not configured")
                
                return OpenAI(
                    base_url="https://models.inference.ai.azure.com",
                    api_key=API_CONFIG['api_key'],
                )
            elif api_type == 'openai':
                # Standard OpenAI API
                if not API_CONFIG['openai_api_key']:
                    raise ValueError("API key for OpenAI not configured")
                
                return OpenAI(api_key=API_CONFIG['openai_api_key'])
            else:
                raise ValueError(f"Unknown API type: {api_type}")
                
        except Exception as e:
            print(f"Error setting up client: {str(e)}")
            return None

    def save_context(self, filename=None):
        self.context_manager.save_context(filename)
        
    def load_context(self, filename=None):
        self.context_manager.load_context(filename)
        
    def clear_context(self, filename=None):
        return self.context_manager.clear_context(filename)

    @property
    def current_context(self):
        return self.context_manager.current_context

    @current_context.setter
    def current_context(self, value):
        self.context_manager.current_context = value

    def add_to_history(self, role, content):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        })

    def save_conversation(self):
        """Save conversation history to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            for entry in self.conversation_history:
                f.write(f"**[{entry['timestamp']}] {entry['role']}:** {entry['content']} \n\n")
        return filename
            

    system_prompt_path = os.path.join(os.path.dirname(__file__), "config/system_prompt.json")    

    def get_system_prompt(self, filename=None):
        """
        Get the current system prompt.
        
        Args:
            filename (str, optional): Path to the system prompt file. 
                                    Defaults to the class system_prompt_path.
        
        Returns:
            str: The current system prompt
        """
        try:
            if filename is None:
                filename = self.system_prompt_path
                
            # Check if file exists
            if not os.path.exists(filename):
                # Return a default prompt if file doesn't exist
                return "You are a helpful assistant."
                
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get("system_prompt", "You are a helpful assistant.")
                
        except Exception as e:
            print(colored(f"Error reading system prompt: {str(e)}", "red"))
            return "You are a helpful assistant."  # Default fallback

    def set_system_prompt(self, new_prompt, filename=None):
        """
        Set a new system prompt for the assistant.
        
        Args:
            new_prompt (str): The new system prompt to use
            filename (str, optional): Path to save the prompt. 
                                    Defaults to the class system_prompt_path.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if filename is None:
                filename = self.system_prompt_path
                
            # Ensure the directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Save the new system prompt
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump({"system_prompt": new_prompt}, file, indent=4)
                
            print(colored("System prompt updated successfully", "green"))
            return True
            
        except Exception as e:
            print(colored(f"Error updating system prompt: {str(e)}", "red"))
            return False


    def update_api_type_from_model(self, model_name):
        """Update API type based on model configuration"""
        try:
            # Load models.json
            models_path = os.path.join(os.path.dirname(__file__), "config/models.json")
            if os.path.exists(models_path):
                with open(models_path, 'r') as f:
                    models_config = json.load(f)
                
                # Check if model exists and has api_type
                if (model_name in models_config.get('models', {}) and 
                    'api_type' in models_config['models'][model_name]):
                    # Update global API_CONFIG
                    API_CONFIG['api_type'] = models_config['models'][model_name]['api_type']
                    # Reinitialize client with new API type
                    self.client = self.setup_client()
                    return True
        except Exception as e:
            print(colored(f"Error updating API type: {str(e)}", "red"))
        
        return False

    
    def get_response(self, prompt, system_prompt=None):
        """Get response from AI model"""
        try:
            if not self.client:
                return "AI client not properly initialized"
            
            # Get optimized context with token limit
            token_limit = self.max_tokens // 2
            formatted_context = self.context_manager.get_formatted_context(token_limit)
            
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Create a structured prompt with context if available
            if formatted_context:
                full_prompt = (
                    "I'm providing you with context information that includes previous conversations "
                    "and/or content the user has shared. The context has metadata with source types and timestamps.\n\n"
                    f"CONTEXT:\n{formatted_context}\n\n"
                    f"USER QUESTION: {prompt}\n\n"
                    "Based on the context above, please answer the user's question. "
                    "If the context doesn't contain relevant information, you can answer based on your knowledge.\n"
                    f"Current date and time: {current_time}. Please use this information if relevant to the query."
                )
            else:
                full_prompt = (
                    f"Current date and time: {current_time}. Please use this information if relevant to the query."
                    f"USER QUESTION: {prompt}\n\n"
                )
                
            system_prompt = self.get_system_prompt() if system_prompt is None else system_prompt

            # Use appropriate model based on API type
            model_to_use = self.model
            if API_CONFIG['api_type'] == 'ollama':
                model_to_use = API_CONFIG['ollama_model']
                print(f"Using Ollama model: {model_to_use}")
            
            # # Debug information
            # print(f"Sending request to API with model: {model_to_use}")
            
            # Create the API request
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": full_prompt,
                    }
                ],
                model=model_to_use,
                temperature=self.temp,
                max_tokens=self.max_tokens,
                top_p=self.top_p
            )

            ai_response = response.choices[0].message.content

            # Add the interaction to context
            self.context_manager.add_to_context(
                f"User: {prompt}\nKarhu: {ai_response}",
                source_type="conversation"
            )

            return ai_response
        except Exception as api_error:
            print(colored(f"API Error: {str(api_error)}", "red"))
            # More detailed error information
            import traceback
            traceback.print_exc()
            return "Sorry, I couldn't process your request at this time."

    def get_response_streaming(self, prompt, system_prompt=None):
        """Get streaming response from AI model"""
        try:
            if not self.client:
                return "AI client not properly initialized"
                
            # Setup similar to your existing get_response method
            token_limit = self.max_tokens // 2
            formatted_context = self.context_manager.get_formatted_context(token_limit)
            
            # Create prompt with context
            if formatted_context:
                full_prompt = (
                    "I'm providing you with context information...\n\n"
                    f"CONTEXT:\n{formatted_context}\n\n"
                    f"USER QUESTION: {prompt}\n\n"
                    "Based on the context above, please answer the user's question..."
                )
            else:
                full_prompt = prompt
                
            system_prompt = self.get_system_prompt() if system_prompt is None else system_prompt

            # Determine model to use
            model_to_use = self.model
            if API_CONFIG['api_type'] == 'ollama':
                model_to_use = self.model
            
            # Create the streaming API request
            stream = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_prompt}
                ],
                model=model_to_use,
                temperature=self.temp,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                stream=True  # Enable streaming
            )
            
            # Return the stream object to be processed in the interactive loop
            return stream
                
        except Exception as api_error:
            Errors.format_rate_limit_error("Error during streaming response", api_error)
            print(colored(f"API Error: {str(api_error)}", "red"))
            return None

    def load_current_model_and_update_api_type(self):
        # """Load the current model from models.json and update API type accordingly"""
        try:
            # Load models.json
            models_path = os.path.join(os.path.dirname(__file__), "config/models.json")
            if os.path.exists(models_path):
                with open(models_path, 'r') as f:
                    models_config = json.load(f)
                
                # Get current model name
                current_model = models_config.get('current_model')
                if current_model:
                    #print(colored(f"Loading last used model: {current_model}", "green"))
                    
                    # Update model parameters from config
                    if current_model in models_config.get('models', {}):
                        model_config = models_config['models'][current_model]
                        self.model = model_config.get('model', current_model)
                        self.temp = model_config.get('temp', self.temp)
                        self.max_tokens = model_config.get('max_tokens', self.max_tokens)
                        self.top_p = model_config.get('top_p', self.top_p)
                    
                    # Update API type based on model
                    self.update_api_type_from_model(current_model)
        except Exception as e:
            print(colored(f"Error loading current model: {str(e)}", "red"))