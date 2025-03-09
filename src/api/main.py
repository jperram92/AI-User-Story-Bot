from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import shutil
from pathlib import Path
import os

from src.services.template_processor import TemplateProcessor
from src.services.document_processor import DocumentProcessor
from src.services.llm_service import LLMService
from src.services.export_service import ExportService
from src.services.story_generator import StoryGenerator

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-document")
async def process_document(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            shutil.copyfileobj(file.file, tmp)
            processor = DocumentProcessor(LLMService())
            result = await processor.process_document(tmp.name)
        return result
    finally:
        Path(tmp.name).unlink()

@app.post("/generate-story")
async def generate_story(context: dict):
    try:
        template = context.get('template', {})
        generator = StoryGenerator(
            template=template,
            llm_service=LLMService()
        )
        story = await generator.generate_story(context)
        
        if context.get('export_docx'):
            export_service = ExportService()
            file_path = export_service.export_to_docx(
                story,
                f"story_{context['id']}"
            )
            story['docx_path'] = os.path.abspath(file_path)  # Return absolute path
            
        return story
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/templates")
async def save_template(template: dict):
    try:
        processor = TemplateProcessor()
        result = await processor.process_template(template)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
