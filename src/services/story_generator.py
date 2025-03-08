from typing import List
from ..models.story_template import StoryTemplate

class StoryGenerator:
    def __init__(self, template: StoryTemplate, llm_service):
        self.template = template
        self.llm = llm_service
        self.industry_keywords = self._load_industry_keywords()
    
    async def generate_story(self, context: dict) -> dict:
        """Generates user story based on template and context"""
        story = await self._apply_template(context)
        enhanced_story = self._enhance_with_keywords(story)
        return enhanced_story
    
    def _apply_template(self, context: dict) -> dict:
        # Apply template format to context
        pass
    
    def _enhance_with_keywords(self, story: dict) -> dict:
        # Enhance story with industry-specific keywords
        pass