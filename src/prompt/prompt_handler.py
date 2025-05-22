from jinja2 import Environment, FileSystemLoader
import yaml
from pathlib import Path


class PromptHandler:
    def __init__(self, base_dir="prompt_files"):
        self.env = Environment(loader=FileSystemLoader(base_dir))
        self.base_dir = Path(base_dir)

    def render_prompt(self, template_file, context):
        template = self.env.get_template(template_file)
        return template.render(**context)

    def load_yaml(self, file):
        return yaml.safe_load(open(self.base_dir / file))


if __name__ == "__main__":
    pm = PromptHandler()
    persona_data = pm.load_yaml("shared/persona.yaml")
    context = {
        "user_input": "Tell me a joke",
        "tone": "funny",
        "language": "en",
        "assistant": persona_data["assistant"],
    }
    try:

        prompt = pm.render_prompt("chat/chatting.yaml", context)
        print(prompt)

    except Exception as e:
        print(f"Error: {str(e)}")
