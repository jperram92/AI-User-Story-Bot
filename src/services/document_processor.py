from typing import List
import pypdf
import docx
import chardet
from pathlib import Path
from .llm_service import LLMService

class DocumentProcessor:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
        self.supported_formats = ['.docx', '.pdf', '.txt']
        
    async def process_document(self, file_path: str) -> dict:
        """Processes business documents and extracts relevant information"""
        content = self._extract_content(file_path)
        structured_data = self._analyze_content(content)
        return structured_data
        
    def _extract_content(self, file_path: str) -> str:
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return self._read_pdf(file_path)
        elif file_ext == '.docx':
            return self._read_docx(file_path)
        elif file_ext == '.txt':
            return self._read_txt(file_path)
        
        raise ValueError(f"Unsupported file format: {file_ext}")
    
    def _read_pdf(self, file_path: str) -> str:
        with open(file_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            return ' '.join(page.extract_text() for page in reader.pages)
    
    def _read_docx(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        return ' '.join(paragraph.text for paragraph in doc.paragraphs)
    
    def _read_txt(self, file_path: str) -> str:
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            encoding = chardet.detect(raw_data)['encoding']
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()
        
    def _analyze_content(self, content: str) -> dict:
        # Use LLM to analyze and structure content
        pass
