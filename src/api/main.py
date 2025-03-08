from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import tempfile

# Import required services and processors
from ..services.template_processor import TemplateProcessor
from ..services.document_processor import DocumentProcessor
from ..services.llm_service import LLMService
from ..services.story_generator import StoryGenerator
from ..services.export_service import ExportService

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/templates")
async def create_template(template_data: dict):
    try:
        template_processor = TemplateProcessor()
        template_processor.save_template(
            template_data['name'],
            template_data
        )
        return {"message": "Template created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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
        generator = StoryGenerator(
            template=context['template'],
            llm_service=LLMService()
        )
        story = await generator.generate_story(context)
        
        # Export to Word if requested
        if context.get('export_docx'):
            export_service = ExportService()
            file_path = export_service.export_to_docx(
                story,
                f"story_{context['id']}"
            )
            story['docx_path'] = file_path
            
        return story
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
