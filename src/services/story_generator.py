from typing import List, Dict
from ..models.story_template import StoryTemplate

class StoryGenerator:
    def __init__(self, template: dict, llm_service):
        self.template = StoryTemplate(**template)
        self.llm = llm_service
        self.industry_keywords = self._load_industry_keywords()
    
    def _load_industry_keywords(self) -> List[str]:
        """Loads industry-specific keywords"""
        return [
            "customer satisfaction",
            "support ticket",
            "response time",
            "customer history",
            "contact information",
            "service quality",
            "customer experience"
        ]
    
    async def generate_story(self, context: dict) -> dict:
        """Generates user story based on template and context"""
        base_story = await self._apply_template(context)
        
        # Process through LLM
        enhanced_story = await self.llm.process(base_story)
        
        # Further enhance with industry keywords
        final_story = self._enhance_with_keywords(enhanced_story)
        return final_story
    
    async def _apply_template(self, context: dict) -> dict:
        """Apply template format to context"""
        return {
            "role": context.get("role", ""),
            "goal": context.get("goal", ""),
            "benefit": context.get("benefit", ""),
            "acceptance_criteria": context.get("acceptance_criteria", [])
        }
    
    def _enhance_with_keywords(self, story: dict) -> dict:
        """Enhance story with industry-specific keywords"""
        enhanced_story = story.copy()
        
        # Enhance the goal with relevant keywords if not present
        for keyword in self.industry_keywords:
            if keyword not in story["goal"].lower():
                if "customer" in keyword and "customer" in story["goal"].lower():
                    enhanced_story["goal"] = f"{story['goal']} with improved {keyword}"
                    break
        
        return enhanced_story
