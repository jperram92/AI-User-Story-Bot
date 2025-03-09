class DocumentProcessor:
    def __init__(self, llm_service):
        self.llm_service = llm_service

    async def process_document(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                
            processed_content = {
                "role": "",
                "goal": "",
                "benefit": "",
                "acceptance_criteria": []
            }
            
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            for line in lines:
                if "As a" in line:
                    processed_content["role"] = line.replace("As a", "").strip()
                elif "I want" in line:
                    processed_content["goal"] = line.replace("I want", "").strip()
                elif "So that" in line:
                    processed_content["benefit"] = line.replace("So that", "").strip()
                elif line.startswith("-"):
                    processed_content["acceptance_criteria"].append(line.replace("-", "").strip())

            return processed_content
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
