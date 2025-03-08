from docx import Document
from docx.shared import Pt
import markdown
import os

class ExportService:
    def __init__(self):
        self.output_dir = "exports"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def export_to_docx(self, content: dict, filename: str) -> str:
        doc = Document()
        
        # Add title
        title = doc.add_heading(content['title'], 0)
        
        # Add sections
        for section in content['sections']:
            heading = doc.add_heading(section['heading'], level=1)
            doc.add_paragraph(section['content'])
        
        # Save document
        output_path = os.path.join(self.output_dir, f"{filename}.docx")
        doc.save(output_path)
        return output_path