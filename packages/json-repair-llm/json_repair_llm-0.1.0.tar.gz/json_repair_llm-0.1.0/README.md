# JSON Repair LLM

A Python package for repairing broken JSON using multiple backends: LLMs and FSM-based processing with Pydantic models.

## Disclaimer

This package is not a replacement for a full-fledged JSON parser or parsers like `json-repair`.
It is designed to assist in repairing broken JSON structures, that cloud LLMs might produce 
(some models even with proper prompting still might return broken JSON or JSON with extra-text).

The main purpose is to process output from cloud LLMs, where packages like `outlines` or `xgrammar` are not applicable.

## Features

- **Multiple backends**: Choose between LLM-based repair, FSM-based repair, or both
- **Pydantic integration**: Validate and enforce schema compliance
- **Slot filling**: Extract structured information from unstructured text
- **Flexible configuration**: Use with different LLM models
- **Low dependency mode**: Use FSM processor with minimal dependencies

## How It Works

1. LLM-based repair:
   - uses a large language model(`HuggingFaceTB/SmolLM2-360M-Instruct`) to repair broken JSON.
   - outlines helps to generate a grammatically correct JSON.
   - additionally, llm backend can be used as "slot filling" processor to extract structured data from unstructured text.
   - based on pydantic models, it can validate and enforce schema compliance.
2. FSM-based repair:
   - uses a very simplistic finite state machine (FSM) to parse and repair broken JSON (if `json-repair` was not successful).
   - based on pydantic models, it can validate and enforce schema compliance.

## Installation

```bash
# Basic installation
pip install json-repair-llm

# With FSM capabilities
pip install json-repair-llm[fsm]

# With all dependencies (including flash-attention)
pip install json-repair-llm[full]
```

## Flash Attention (Optional)

For better performance with LLM-based repair, you can install flash-attention:

```bash
pip install flash-attn --no-build-isolation
```

## Usage

### Basic Usage

```python
from json_repair_llm import JsonRepairProcessor
from pydantic import BaseModel


# Define your data schema
class UserProfile(BaseModel):
    name: str
    age: int
    email: str


# Create processor with default LLM backend
processor = JsonRepairProcessor(UserProfile)

# Process broken JSON
broken_json = '{name": "John Doe"\, "age": 30, email: "john@example.com"}'
result = processor(broken_json)

print(result.model_dump())
# {'name': 'John Doe', 'age': 30, 'email': 'john@example.com'}
```

### Using Different Backends

```python
# Use FSM backend (no LLM required)
processor_fsm = JsonRepairProcessor(UserProfile, backend="fsm")

# Use both backends (FSM first, then LLM if needed)
processor_all = JsonRepairProcessor(UserProfile, backend="all")
```

### Slot Filling for Unstructured Text

```python
# Extract structured data from plain text
processor = JsonRepairProcessor(UserProfile, backend="llm")
plain_text = """
Hello, my name is Jane Smith. I'm 28 years old.
You can contact me at jane.smith@example.com for more information.
"""
result = processor(plain_text, use_slot_filling=True)
print(result.model_dump())
# {'name': 'Jane Smith', 'age': 28, 'email': 'jane.smith@example.com'}
```

### Using a Custom LLM Model

```python
processor = JsonRepairProcessor(
    UserProfile,
    backend="llm",
    model_name="gpt2",  # Replace with your preferred model
    prompt_template="Fix this JSON: {{ broken_json }}\nSchema: {{ schema }}\nFixed JSON:"
)
```

## FSM vs LLM Backend

- **FSM Backend**:
    - Faster, no external API calls
    - Works without internet connection
    - Limited to simpler JSON repairs
    - No dependencies on ML libraries

- **LLM Backend**:
    - Better at handling complex repairs
    - Can extract structure from unstructured text
    - Higher accuracy for severely broken JSON
    - Requires ML libraries and models

## License

MIT License