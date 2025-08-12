import yaml

def load_config(config_path:str = "D:\Agentic AI\projects\DOCUMENT_PORTAL\config\config.yaml") -> dict:
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
    
