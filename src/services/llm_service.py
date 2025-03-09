from typing import Dict, Any
import openai
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        # Configuration
        openai.api_key = "your-openai-api-key"  # Replace with your API key
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 256
        self.temperature = 0.7
        
        self.system_prompt = """You are a technical writer that transforms user stories into detailed, measurable versions.
        Always respond in the exact format:
        
        Goal: [technical implementation details]
        Benefit: [measurable metrics and business value]"""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def _make_api_request(self, prompt: str) -> Dict:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            logger.error(f"OpenAI API request failed: {str(e)}")
            raise

    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        try:
            prompt = (
                f"Transform this user story into a detailed version:\n\n"
                f"As a {context.get('role', '')},\n"
                f"I want to {context.get('goal', '')},\n"
                f"So that {context.get('benefit', '')}\n"
            )

            generated_text = await self._make_api_request(prompt)
            logger.debug(f"Generated text: {generated_text}")
            
            if not generated_text or not ('Goal:' in generated_text and 'Benefit:' in generated_text):
                logger.warning("Response missing required Goal/Benefit format")
                return self._enhance_content_fallback(context)
                
            return self._enhance_content(context, generated_text)
            
        except Exception as e:
            logger.error(f"Error in LLM processing: {str(e)}")
            return self._enhance_content_fallback(context)

    def _enhance_content(self, original: Dict[str, Any], llm_response: str) -> Dict[str, Any]:
        enhanced = original.copy()
        
        try:
            # More robust parsing
            lines = [line.strip() for line in llm_response.split('\n') if line.strip()]
            goal_line = next((line for line in lines if line.lower().startswith('goal:')), None)
            benefit_line = next((line for line in lines if line.lower().startswith('benefit:')), None)
            
            if goal_line and benefit_line:
                enhanced['goal'] = goal_line.split(':', 1)[1].strip()
                enhanced['benefit'] = benefit_line.split(':', 1)[1].strip()
            else:
                return self._enhance_content_fallback(original)
                
        except Exception as e:
            logger.error(f"Error parsing LLM response: {str(e)}")
            return self._enhance_content_fallback(original)
            
        return enhanced

    def _enhance_content_fallback(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Using fallback enhancement")
        enhanced = context.copy()
        
        if 'customer' in enhanced.get('role', '').lower():
            enhanced['goal'] = (
                f"{enhanced['goal']} through a unified dashboard showing "
                "purchase history, support tickets, and contact details"
            )
            
        if 'support' in enhanced.get('benefit', '').lower():
            enhanced['benefit'] = (
                f"{enhanced['benefit']} by reducing response time "
                "by 20% and improving first-contact resolution rate"
            )
        
        logger.info(f"Fallback enhanced content: {enhanced}")
        return enhanced
