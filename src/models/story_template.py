from dataclasses import dataclass
from typing import List, Optional

@dataclass
class StoryTemplate:
    format_type: str
    sections: List[str]
    required_fields: List[str]
    custom_fields: Optional[dict]
    business_context: str
    
    def validate_template(self) -> bool:
        """Validates if template meets minimum requirements"""
        return all([
            self.format_type,
            len(self.sections) > 0,
            len(self.required_fields) > 0
        ])