import os
import uuid
import fitz
from datetime import datetime
from logs.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentHandler:
    def __init__(self, data_dir=None, session_id=None):
        try:
            self.log=CustomLogger().get_logger(__name__)
            self.data_dir = data_dir or os.getenv(
                "DATA_STORAGE_PATH",
                os.path.join(os.getcwd(), "data", "document_analysis")
            )
            self.session_id = session_id or f"session_{datetime.utcnow().strftime('%Y_%m_%d_%H-%M-%S')}_{uuid.uuid4().hex[:8]}"
            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)
            
            self.log.info("PDFHandler Initiated", session_id=self.session_id, session_path=self.session_path)
            
        except DocumentPortalException as e:
            self.log.error(f"Error in initializing DocumentHandler", exception=e, session_id=self.session_id, session_path=self.session_path)
            raise DocumentPortalException("Error in initializing DocumentHandler",e) from e
        
        
    def save_pdf(self, uploaded_file):
        try:
            filename = os.path.basename(uploaded_file.name)
            if not filename.lower().endswith(".pdf"):
                raise DocumentPortalException("Invalid filetype Only PDF files are allowed.")
            save_path = os.path.join(self.session_path, filename)
            with open(save_path, "wb") as file:
                file.write(uploaded_file.getbuffer())
                
            self.log.info("PDF Saved to Session Path", file=filename, save_path=save_path, session_id=self.session_id)
            return save_path

        except DocumentPortalException as e:
            self.log.error(f"Error in saving PDF", exception=e, session_id=self.session_id)
            raise DocumentPortalException("Error in saving PDF",e) from e

                
    def read_pdf(self, pdf_filepath:str)->str:
        try:
            text_chunks = []
            with fitz.open(pdf_filepath) as doc:
                for page_num, page in enumerate(doc,start=1):
                    text_chunks.append(f"\n---- Page {page_num} ----\n{page.get_text()}")
                    
            text = "\n".join(text_chunks)
            self.log.info("PDF Read Successfully", pdf_filepath=pdf_filepath, session_id=self.session_id, pages = len(text_chunks))
            return text
        except Exception as e:
            self.log.error(f"Error in reading PDF", exception=e, session_id=self.session_id)
            raise DocumentPortalException("Error in reading PDF",e) from e

if __name__ == "__main__":
    from pathlib import Path
    from io import BytesIO
    
    pdf_filepath = r"D:\\Agentic AI\\projects\\DOCUMENT_PORTAL\\data\\document_analysis\\NIPS-2017-attention-is-all-you-need-Paper.pdf"
    
    class DummyFile:
        def __init__(self,file_path):
            self.name = Path(file_path).name
            self._file_path = file_path
        def getbuffer(self):
            return open(self._file_path, "rb").read()
        
        
    dummy_pdf = DummyFile(pdf_filepath)
    handler = DocumentHandler(session_id="test_session")
    try:
        saved_path = handler.save_pdf(dummy_pdf)
        print(saved_path)
        
        content = handler.read_pdf(saved_path)
        print(content[:500])
        
    except Exception as e:
        print(f"Error: {e}")