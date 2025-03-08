from jinja2 import Environment, BaseLoader
import yaml
from pathlib import Path

class TemplateProcessor:
    def __init__(self):
        self.env = Environment(loader=BaseLoader())
        self.templates_dir = Path("templates")
        self.templates_dir.mkdir(exist_ok=True)
    
    def save_template(self, template_name: str, template_data: dict):
        template_path = self.templates_dir / f"{template_name}.yaml"
        with open(template_path, 'w') as f:
            yaml.dump(template_data, f)
    
    def load_template(self, template_name: str) -> dict:
        template_path = self.templates_dir / f"{template_name}.yaml"
        with open(template_path) as f:
            return yaml.safe_load(f)
    
    def render_template(self, template_str: str, context: dict) -> str:
        template = self.env.from_string(template_str)
        return template.render(**context)