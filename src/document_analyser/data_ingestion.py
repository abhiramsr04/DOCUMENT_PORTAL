import os
import fitz
import uuid
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
        
        
    def save_pdf(self, pdf_data):
        try:
            pdf_path = os.path.join(self.data_dir, f"{self.session_id}.pdf")
            with open(pdf_path,'wb') as f:
                f.write(pdf_data)
            self.log.info(f"PDF saved successfully: {pdf_path}")
        except DocumentPortalException as e:
            self.log.error(f"Error in saving PDF", exception=e, session_id=self.session_id)
            raise DocumentPortalException("Error in saving PDF",e) from e

                
    def read_pdf(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Error in reading PDF", exception=e, session_id=self.session_id)
            raise DocumentPortalException("Error in reading PDF",e) from e

if __name__ == "__main__":
    document_handler = DocumentHandler()
    print(f"session_id: {document_handler.session_id}")
    print(f"Session_path: {document_handler.session_path}")