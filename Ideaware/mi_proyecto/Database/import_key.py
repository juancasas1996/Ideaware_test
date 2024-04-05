import json  # Import the json module for working with JSON data

def load_api_key_from_config(config_file_path):
    try:
        with open(config_file_path, 'r') as config_file:  # Open the specified file in read mode
            config = json.load(config_file)  # Load the JSON data from the file into a dictionary
            return config.get("openai_api_key")  # Return the value associated with the key "openai_api_key"
    except FileNotFoundError:  # Handle the case where the specified file does not exist
        # Return None to indicate that the API key could not be loaded due to the file not being present
        return None
    except json.JSONDecodeError:  # Handle the case where the file does not contain valid JSON data
        # Return None to indicate that the API key could not be loaded due to invalid JSON data
        return None
