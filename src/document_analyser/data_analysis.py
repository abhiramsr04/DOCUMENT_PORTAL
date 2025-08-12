import os
from utils.model_loder import ModelLoader
from exception.custom_exception import DocumentPortalException
from logs.custom_logger import CustomLogger
from model.models import *

from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentAnalyzer:
    def __init__(self):
        pass
    
    def analyze_metadata(self, document_path):
        pass