# Prompt-structure
## 🚀 What Is This About?
This is a professional way to organize, manage, and use prompt templates for LLM-based apps (like chatbots or summarizers). It supports:

-Reusability
-Personalization (e.g., tone, language, user status)
-Version control
-A/B testing
-Security
-Performance optimization

# Advanced Prompt Template Management for LLM Applications


## 1. File Organization Structure
When you're building an LLM application (e.g., chatbot, summarizer, assistant), you'll have many prompt templates for different purposes:

Some for chatting

Some for technical replies

Some for summarizing

Some common pieces reused in many prompts

To avoid confusion and improve reusability, versioning, and testing, you organize them into folders and files.

```
prompts/
├── version.txt                # 1. Version number of the prompts
├── chat/                      # 2. Chat-related prompts
│   ├── base.yaml              # Base chat prompt everyone inherits from
│   ├── customer_support.yaml  # A prompt tailored for customer support
│   └── technical.yaml         # A prompt for technical Q&A
├── summarization/             # 3. Prompts for summarization tasks
│   ├── short.yaml             # Short summaries
│   └── detailed.yaml          # Long summaries
└── shared/                    # 4. Reusable prompt parts (common components like header and footer)
    ├── personas.yaml          # Shared personas (e.g., assistant, expert)
    └── formats.yaml           # Shared formats/templates

```

## 2. YAML Template Deep Dive
This section shows how to write a single prompt template using YAML + Jinja2 templating language.

It's like a blueprint for generating prompts dynamically, using variables, conditions, and reusable parts.

This YAML template:

Uses Jinja2 to insert variables and conditions

Pulls in reusable parts (like personas)

Validates and tests the prompt

Keeps everything modular, reusable, and clean


### Complete Template Example (`prompts/chat/main.yaml`)
```yaml
metadata:
  version: 1.2.0
  last_updated: 2023-11-15
  author: AI Team
  description: "Main chat prompt for customer interactions"

system_prompt: |
  {% from "shared/personas.yaml" import assistant_persona %}
  {{ assistant_persona }}
  
  Current Context:
  - Time: {{ current_time }}
  - User status: {% if is_premium %}Premium member{% else %}Free tier{% endif %}
  
  Guidelines:
  - Respond in {{ language }} language
  - Tone: {{ tone|default('professional') }}
  - Length: {{ length|default('medium') }}

user_prompt: |
  User [{{ user_id }}]: {{ user_input }}

variables:
  required:
    - current_time
    - user_input
    - user_id
  optional:
    - language: en
    - tone: professional
    - length: medium
    - is_premium: false

examples:
  - input: 
      user_input: "How do I reset my password?"
      is_premium: true
    output: |
      Hello valued premium member! To reset your password:
      1. Visit account settings
      2. Click "Reset Password"
      3. Check your email for verification
    evaluation:
      clarity: 9/10
      politeness: 10/10
      accuracy: 10/10

  - input: 
      user_input: "What's the weather today?"
      language: es
    output: |
      Lo siento, actualmente no tengo acceso a datos meteorológicos. 
      ¿En qué otra cosa puedo ayudarte?

validation:
  max_length: 500
  banned_phrases:
    - "I'm sorry, I can't help with that"
    - "As an AI language model"
  required_components:
    - greeting
    - clear_instructions
```

## 3. Advanced Templating with Jinja2

**Macros in Jinja2**
A macro in Jinja2 is essentially a reusable block of template code, similar to a function in traditional programming languages. You can define a macro in one template (like shared/personas.yaml) and call it wherever you need it, making your templates cleaner and more modular.

### Macros (in `shared/personas.yaml`)
```yaml
assistant_persona: |
  You are {{ persona_name|default('a helpful AI assistant') }} working for {{ company_name }}.
  Your capabilities include:
  {% for capability in capabilities %}
  - {{ capability }}
  {% endfor %}

professional_persona: |
  You are a senior {{ specialty }} consultant with {{ years }} years of experience.
  Respond with authoritative but approachable guidance.
```

### Template Inheritance
```yaml
# prompts/chat/technical.yaml
_extends: base.yaml

system_prompt: |
  {{ super().system_prompt }}
  
  Additional Technical Guidelines:
  - Use Markdown for code samples
  - Include relevant API references
  - Explain concepts at {{ expertise_level }} level
```

## 4. Version Control Strategy

1. **Semantic Versioning**:
   - MAJOR: Breaking changes
   - MINOR: New features
   - PATCH: Fixes/optimizations

2. **Version Tags**:
```yaml
# prompts/version.yaml
current: 1.2.0
history:
  - version: 1.1.0
    date: 2023-10-01
    changes: "Added multilingual support"
  - version: 1.0.0
    date: 2023-09-15
    changes: "Initial release"
```

3. **A/B Testing Support**:
```yaml
# prompts/chat/variants/
├── v1_plain.yaml
├── v2_emojis.yaml
└── v3_technical.yaml
```

## 5. Dynamic Prompt Generation

### Python Loader Class
```python
from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader

class PromptManager:
    def __init__(self, template_dir="prompts"):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
        
    def get_prompt(self, template_path, context=None):
        template = self.env.get_template(template_path)
        return template.render(**(context or {}))
        
    def validate_prompt(self, prompt_text):
        # Add validation logic
        if len(prompt_text) > 2000:
            raise ValueError("Prompt exceeds maximum length")

# Usage
pm = PromptManager()
context = {
    "current_date": "2023-11-15",
    "user_input": "Help with my account",
    "language": "en"
}
prompt = pm.get_prompt("chat/main.yaml", context)
```

## 6. Testing and Evaluation

### Test Cases File (`prompts/tests/chat_test.yaml`)
```yaml
test_cases:
  - name: "Premium user greeting"
    template: "chat/main.yaml"
    input:
      user_id: "user123"
      user_input: "Hello"
      is_premium: true
      language: "en"
    expected:
      contains: ["valued premium member"]
      excludes: ["Free tier"]
      max_length: 300

  - name: "Technical query handling"
    template: "chat/technical.yaml"
    input:
      user_input: "Explain OAuth 2.0"
      expertise_level: "beginner"
    expected:
      contains: ["authentication flow"]
      evaluation:
        readability: ">=8"
        accuracy: ">=9"
```

## 7. Performance Optimization

1. **Template Caching**:
```python
from jinja2 import select_autoescape

env = Environment(
    loader=FileSystemLoader("prompts"),
    autoescape=select_autoescape(),
    cache_size=1000  # Cache up to 1000 templates
)
```

2. **Pre-compiled Prompts**:
To pre-load and compile all your Jinja2 prompt templates during deployment or app startup.
This makes your app faster because templates don’t have to be reloaded and recompiled every time you use them.
```python
# During build/deployment:
compiled = {}
for template_file in Path("prompts").glob("**/*.yaml"):
    template = env.get_template(str(template_file))
    compiled[template_file.stem] = template
```

```python
#saving the compiled template into a dictionary
compiled = {
    "main": <Template object>,
    "variant_emoji": <Template object>
}
```

## 8. Security Considerations

1. **Input Sanitization**:
```python
from markupsafe import escape
#escape() will neutralize special characters, like: {, }, <, >, " (used in Jinja2 or HTML)

context = {
    "user_input": escape(user_input)  # Prevent prompt injection
}
```

2. **Audit Trail**:
You want to track what templates were used, what context was passed, and what output was generated — for debugging, security auditing, or user support.
```python
def log_prompt_generation(template, context, output):
    audit_log = {
        "timestamp": datetime.utcnow(),
        "template": template,
        "context_hash": hash(frozenset(context.items())), #A hashed version of the context (for security, instead of storing it raw)
        "output_sample": output[:200]
    }
    # Store to database or file
```

# ✅ Summary: Why Use This?
This system allows you to:

-Manage prompts like code
-Easily update, test, and reuse prompts
-Add context-awareness and personalization
-Ensure security, quality, and version control
