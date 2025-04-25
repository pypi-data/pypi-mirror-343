import sys
from .converter import choose_model, convert_pseudo_to_python
from .config import load_config, save_config
from .runner import execute_python_code

def prompt_change_config():
    """
    Allows the user to change their API key and selected model.
    """
    print("🔄 Changing API Key and Model...")
    api_key = input("Enter your new Google API Key: ").strip()

    # Configure the API with the new key
    import google.generativeai as genai
    genai.configure(api_key=api_key)

    # Fetch the available models and convert the generator to a list
    models = list(genai.list_models())
    print("\nAvailable Models:")
    for i, model in enumerate(models):
        print(f"{i}: {model.name} -> {model.supported_generation_methods}")

    # Prompt the user to select a model
    index = int(input("Choose a model by number: "))
    selected_model = models[index].name

    # Save the new configuration
    save_config(api_key, selected_model)
    print(f"\n✅ Configuration updated successfully! Model '{selected_model}' saved.")
    
def main():
    """
    Main entry point for the CLI tool.
    """
    if len(sys.argv) < 2:
        print("Usage: pseudorun <command> [file]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "change-config":
        # Change API key and model
        prompt_change_config()
        sys.exit(0)

    # Default behavior: process a pseudocode file
    config = load_config()
    if not config:
        # Prompt user for API key and model if configuration is missing
        choose_model()

    if command == "run":
        if len(sys.argv) != 3:
            print("Usage: pseudorun run <filename.pseudo>")
            sys.exit(1)

        file_path = sys.argv[2]
        with open(file_path, 'r') as f:
            pseudo_code = f.read()

        print("🔄 Converting Pseudocode to Python...")
        python_code = convert_pseudo_to_python(pseudo_code)

        print("\n--- 🐍 Python Code Generated ---\n")
        print(python_code)
        print("\n--- 🔽 Output ---\n")
        execute_python_code(python_code)
    else:
        print(f"Unknown command: {command}")
        print("Available commands: run, change-config")
        sys.exit(1)