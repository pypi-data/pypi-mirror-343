from termcolor import colored


class Displayhelp:
    def display_commands():
        """Print the list of available commands."""
        print("\nCommands:\n")
        
        print(colored("Model & Profile Management:", "cyan"))
        print("!model [name] " + colored("          Switch to a different AI model", "yellow"))
        print("!list_models" + colored("            List available AI models", "yellow"))
        print("!profile [name] " + colored("        Switch to a different profile", "yellow"))
        print("!list_profiles" + colored("          List available profiles", "yellow"))
        print("!create_profile [name:prompt] " + colored("Create a new profile", "yellow"))
        print("!system_prompt  " + colored("        Show current system prompt", "yellow"))
        print("!setsprompt [prompt] " + colored("   Set the system prompt", "yellow"))
        
        print(colored("\nContent & Context Management:", "cyan"))
        print("!file [path] " + colored("           Read a specific file", "yellow"))
        print("!files [path] " + colored("          Read all files in a directory", "yellow"))
        print("!browse [url] " + colored("          Browse a specific webpage", "yellow"))
        print("!search [query] " + colored("        Search the web", "yellow"))
        print("!context_size " + colored("          Show current context size", "yellow"))
        print("!context_info " + colored("          Show detailed context information", "yellow"))
        print("!optimize_context " + colored("      Optimize context to reduce token usage", "yellow"))
        print("!search_context [query] " + colored(" Search within current context", "yellow"))
        print("!chunk [id] " + colored("            List or retrieve document chunks", "yellow"))
        print("!clear " + colored("                 Clear current context", "yellow"))
        print("!clearall " + colored("              Clear context and conversation history", "yellow"))
        
        print(colored("\nSpeech & Voice:", "cyan"))
        print("!lazy " + colored("                  Toggle speech-to-text mode", "yellow"))
        print("!speak " + colored("                 Toggle text-to-speech mode", "yellow"))
        print("!voices " + colored("                List available voices", "yellow"))
        print("!voice [index] " + colored("         Change text-to-speech voice", "yellow"))
        
        print(colored("\nKokoro TTS:", "cyan"))
        print("!kokoro " + colored("                Toggle Kokoro TTS", "yellow"))
        print("!kokoro_voices " + colored("         List available Kokoro voices", "yellow"))
        print("!kokoro_voice [index] " + colored("  Change Kokoro voice", "yellow"))
        print("!kokoro_blend [indices] " + colored("Blend multiple Kokoro voices", "yellow"))
        
        print(colored("\nConversation Management:", "cyan"))
        print("!save " + colored("                  Save conversation history", "yellow"))
        print("!quit " + colored("                  Exit program", "yellow"))
        
        print("\n" + colored("-", "green") * 60)


    def banner(assistant):
        """Display the banner."""
        print(colored("-" * 60, "green"))
        print(colored("Karhu AI Assistant", "cyan"))
        print(colored("Current model: ", "green"), f"{assistant.model}")
        print(colored("Version: ", "green"), "      2.0")
        print(colored("Author: ", "green"), "       Agaga")
        print(colored("Date: ", "green"), "         2025-04-01")
        print(colored("-" * 60, "green"))