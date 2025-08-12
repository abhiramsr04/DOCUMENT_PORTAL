import os
import sys
from dotenv import load_dotenv
from utils.config_loder import load_config
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from logs.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

log = CustomLogger().get_logger(__name__)


class Modelloader:
    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config = load_config()
        log.info("Configuration loaded successfully", config_keys=list(self.config.keys()))
    
    
    def _validate_env(self):
        required_vars = ["GOOGLE_API_KEY", "GROQ_API_KEY"]
        self.api_keys = {key:os.getenv(key) for key in required_vars}
        missing = [k for k,v in self.api_keys.items() if not v]
        if missing:
            log.error("Missing environment variables", missing_vars=missing)
            raise DocumentPortalException("Missing required env vars",sys)
        log.info("Environment Variables validated", available_keys = [k for k in self.api_keys if self.api_keys[k]])
    
    
    def load_embedding(self):
        try:
            log.info("Loading embedding model")
            model_name = self.config["embedding_model"]["model_name"]
            return GoogleGenerativeAIEmbeddings(model=model_name)
        except Exception as e:
            log.error("Failed to load embedding", error=str(e))
            raise DocumentPortalException("Failed to load embedding model",sys)
    
    
    def load_llm(self):
        llm_bolck = self.config["llm"]
        log.info("Loading LLM")
        
        provider_key = os.getenv("LLM_PROVIDER", "groq" )
        
        if provider_key not in llm_bolck:
            log.error("LLM PROVIDER not found in config file", provider_key=provider_key)
            raise ValueError(f"Provider '{provider_key}' not found in config file")
        
        llm_config = llm_bolck[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature", 0.2)
        max_tokens = llm_config.get("max_output_tokens", 2048)
        
        if provider == "groq":
            llm = ChatGroq(
                model=model_name,
                api_key=self.api_keys["GROQ_API_KEY"],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return llm
        
        elif provider == "google":
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                api_key=self.api_keys["GOOGLE_API_KEY"],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return llm
            
        else:
            log.error("Unsupported llm provider", provider = provider)
            raise ValueError(f"Unsupproted llm provider: {provider}")
        
        
if __name__ =="__main__":
    loader = Modelloader()
    
    embeddings = loader.load_embedding()
    print(f"Embedding_model_loded: {embeddings}")
    
    llm = loader.load_llm()
    print( f"LLM_loded: {llm}") 
    
    result = llm.invoke("Hello, how are you?")
    print(f"LLM Result: {result.content}")