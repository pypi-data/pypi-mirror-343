import google.generativeai as genai
from .config import save_config, load_config

def configure_genai():
    """
    Configures Google Generative AI with the saved API key.
    """
    config = load_config()
    genai.configure(api_key=config["api_key"])
    return config["model"]

def choose_model():
    """
    Prompts the user to input their API key, lists models, and allows model selection.
    Saves the API key and selected model to the configuration.
    """
    api_key = input("Enter your Google API Key: ").strip()
    genai.configure(api_key=api_key)

    models = list(genai.list_models())
    for i, m in enumerate(models):
        print(f"{i}: {m.name} -> {m.supported_generation_methods}")

    index = int(input("Choose a model by number: "))
    model = models[index].name
    save_config(api_key, model)
    return model

def convert_pseudo_to_python(pseudo_code):
    """
    Converts pseudocode to Python using the selected model.

    Args:
        pseudo_code (str): The pseudocode to convert.

    Returns:
        str: The Python code generated from the pseudocode.
    """
    model_name = configure_genai()
    model = genai.GenerativeModel(model_name)
    prompt = f"Convert this pseudocode to Python:\n{pseudo_code}"
    response = model.generate_content(prompt)
    generated_code = response.text.strip()

    # Extract Python code block enclosed in triple backticks
    import re
    match = re.search(r"```python(.*?)```", generated_code, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return generated_code