import json
import re
from collections.abc import Callable
from typing import Literal, Type, TypeVar, Any, Optional, ClassVar, Union, Dict

import jinja2
from json_repair.json_repair import loads as json_repair_loads
from loguru import logger
from pydantic import BaseModel, ValidationError

try:
    import torch
    import outlines
    from outlines import generate, models
    from transformers import AutoModelForCausalLM, AutoTokenizer

    HAS_LLM_DEPS = True
except ImportError:
    HAS_LLM_DEPS = False
    logger.warning("LLM dependencies not found. LLM backend will not be available.")

try:
    from transitions import Machine

    HAS_TRANSITIONS = True
except ImportError:
    Machine = None
    HAS_TRANSITIONS = False
    logger.warning("transitions package not found. FSM will use simple state management.")

T = TypeVar("T", bound=BaseModel)


class FSMProcessor(Callable[[str, ...], T]):
    """Finite State Machine for processing and repairing broken JSON according to a Pydantic schema."""

    def __init__(self, model_class: Type[T], use_transitions: bool = True):
        self.model_class = model_class
        self.use_transitions = use_transitions and HAS_TRANSITIONS
        self.output = None
        self.error = None
        self.parsed_data = None

        # Define states
        self.states = ["START", "PROCESSING", "PARSING", "VALIDATING", "FORMATTING", "DONE", "ERROR"]

        # Define transitions (state -> next_state, condition, action)
        self.transitions_config = [
            {"source": "START", "dest": "PROCESSING", "condition": self._always_true, "action": self._clean_text},
            {"source": "PROCESSING", "dest": "PARSING", "condition": self._is_cleaned, "action": self._parse_output},
            {"source": "PARSING", "dest": "VALIDATING", "condition": self._is_parsed, "action": None},
            {
                "source": "VALIDATING",
                "dest": "FORMATTING",
                "condition": self._is_valid_schema,
                "action": self._validate_schema,
            },
            {"source": "FORMATTING", "dest": "DONE", "condition": self._always_true, "action": self._format_output},
            {"source": "START", "dest": "ERROR", "condition": self._is_invalid_input, "action": self._set_error},
            {
                "source": "PROCESSING",
                "dest": "ERROR",
                "condition": self._is_invalid_processing,
                "action": self._set_error,
            },
            {"source": "PARSING", "dest": "ERROR", "condition": self._is_invalid_parsing, "action": self._set_error},
            {"source": "VALIDATING", "dest": "ERROR", "condition": self._is_invalid_schema, "action": self._set_error},
        ]

        if self.use_transitions:
            self._init_transitions_machine()
        else:
            self.state = "START"

    def _init_transitions_machine(self):
        """Initialize the transitions library Machine."""
        self.machine = Machine(model=self, states=self.states, initial="START")
        for t in self.transitions_config:
            self.machine.add_transition(
                trigger="next", source=t["source"], dest=t["dest"], conditions=t["condition"], after=t["action"]
            )

    def _always_true(self, *args, **kwargs) -> bool:
        return True

    def _is_invalid_input(self, data: Any) -> bool:
        return data is None or (isinstance(data, str) and not data.strip())

    def _is_cleaned(self, *args, **kwargs) -> bool:
        return self.output is not None and isinstance(self.output, (str, dict))

    def _is_parsed(self, *args, **kwargs) -> bool:
        return self.parsed_data is not None and isinstance(self.parsed_data, dict)

    def _is_valid_schema(self, *args, **kwargs) -> bool:
        try:
            self.model_class.model_validate(self.parsed_data)
            return True
        except ValidationError:
            return False

    def _is_invalid_schema(self, *args, **kwargs) -> bool:
        return not self._is_valid_schema()

    def _is_invalid_processing(self, *args, **kwargs) -> bool:
        return self.output is None

    def _is_invalid_parsing(self, *args, **kwargs) -> bool:
        return self.parsed_data is None

    def _clean_text(self, data: Any):
        """Clean the input text (e.g., remove extra whitespace, special characters)."""
        if isinstance(data, str):
            # Try json_repair first for simple fixes
            try:
                fixed_json = json_repair_loads(data)
                if isinstance(fixed_json, dict):
                    self.output = fixed_json
                    return
            except Exception:
                pass  # Continue with normal cleaning if repair fails

            # Remove extra whitespace and normalize JSON-like syntax
            self.output = data.strip()
        elif isinstance(data, dict):
            self.output = data  # Pass through structured data
        else:
            self.output = str(data)

    def _parse_output(self, *args, **kwargs):
        """Parse the cleaned output into a dictionary."""
        if isinstance(self.output, dict):
            self.parsed_data = self.output
        elif isinstance(self.output, str):
            try:
                # Attempt to extract JSON from string
                json_match = re.search(r"\{.*\}|\[.*\]", self.output, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    try:
                        # Try standard JSON parsing first
                        self.parsed_data = json.loads(json_str)
                    except json.JSONDecodeError:
                        # Fall back to repair if needed
                        self.parsed_data = json_repair_loads(json_str)
                else:
                    # Try to repair the whole string if no clear JSON pattern
                    self.parsed_data = json_repair_loads(self.output)
            except Exception as e:
                self.error = f"Failed to parse JSON: {str(e)}"
                self.parsed_data = None
        else:
            self.error = "Invalid output format for parsing"
            self.parsed_data = None

    def _validate_schema(self, *args, **kwargs):
        """Validate the parsed output against the Pydantic schema."""
        try:
            validated = self.model_class.model_validate(self.parsed_data)
            self.output = validated.model_dump()  # Convert to dict
        except ValidationError as e:
            self.error = f"Schema validation failed: {str(e)}"
            self.output = None

    def _format_output(self, *args, **kwargs):
        """Format the validated output."""
        # No additional formatting needed, already validated against schema
        pass

    def _set_error(self, *args, **kwargs):
        """Set error state with a message."""
        logger.error(f"Error in state {self.state}: {self.error or 'Invalid data'}")
        self.error = self.error or "Processing failed"

    def process(self, input_data: Any) -> dict[str, Any]:
        """Process the input data through the FSM."""
        self.output = None
        self.error = None
        self.parsed_data = None

        if self.use_transitions:
            self.state = "START"
            try:
                while self.state not in ["DONE", "ERROR"]:
                    self.next(input_data)
            except Exception as e:
                self.state = "ERROR"
                self.error = str(e)
        else:
            self.state = "START"
            for t in self.transitions_config:
                if self.state == t["source"] and t["condition"](input_data):
                    if t["action"]:
                        t["action"](input_data)
                    self.state = t["dest"]
                    logger.debug(f"Transitioned to state: {self.state}")
                    if self.state in ["DONE", "ERROR"]:
                        break

        return {"state": self.state, "output": self.output, "error": self.error}

    def _get_default_values(self) -> dict:
        """Generate default values based on the schema."""
        schema = self.model_class.model_json_schema()

        def process_properties(properties: dict) -> dict:
            result = {}
            for field, field_info in properties.items():
                field_type = field_info.get("type")
                if field_type == "object":
                    result[field] = process_properties(field_info.get("properties", {}))
                elif field_type == "array":
                    result[field] = []
                elif field_type == "string":
                    result[field] = ""
                elif field_type in ["number", "integer"]:
                    result[field] = 0
                elif field_type == "boolean":
                    result[field] = False
                elif field_type == "null":
                    result[field] = None
                else:
                    result[field] = ""
            return result

        return process_properties(schema.get("properties", {}))

    def __call__(
        self,
        input_data: str,
        errors: Literal["ignore", "raise"] = "ignore",
        strict: bool = True,
        context: dict | None = None,
    ) -> T | None:
        """Process input data and return a validated model."""
        result = self.process(input_data)

        if self.state == "DONE" and self.output:
            try:
                return self.model_class.model_validate(self.output, strict=strict, context=context)
            except ValidationError as e:
                self.error = f"Final validation failed: {str(e)}"
                if errors == "ignore":
                    return None
                raise ValueError(f"Validation failed: {self.error}")
        elif errors == "ignore":
            return None
        else:
            raise ValueError(f"Processing failed: {self.error}")


class JsonRepairProcessor(Callable[[str, ...], T]):
    """
    JSON repair processor with multiple backend options.

    Example:
    ```python
    from pydantic import BaseModel

    class UserProfile(BaseModel):
        name: str
        age: int
        email: str

    # Use default LLM backend
    processor = JsonRepairProcessor(UserProfile)

    # Use FSM backend
    processor = JsonRepairProcessor(UserProfile, backend="fsm")

    # Try both backends (FSM first, then LLM if needed)
    processor = JsonRepairProcessor(UserProfile, backend="all")

    broken_json = '{name": "John Doe"\, "age": 30, email: "john@example.com"}'
    result = processor(broken_json)
    ```

    # For very broken JSON or plain text, use slot filling
    broken_json = '{name": "John Doe"\, "age": 30, email: "john@example.com"}'
    result = processor(broken_json, use_slot_filling=True)

    # Or plain text
    unstructured_text = "My name is John Smith, I'm 42 years old and my email is john.smith@example.com"
    result = processor(unstructured_text, use_slot_filling=True)
    """

    DEFAULT_PROMPT_TEMPLATE = (
        "Fix the following JSON to be valid and match the schema:\n "
        "Schema:\n{{ schema }}\n"
        "Change only the minimum required to correct JSON grammar "
        "(e.g., add missing quotes, commas, braces or delete extra tokens, text)\n"
        "Return only the valid JSON object\n"
        "Broken JSON: {{ broken_json }}\n"
        "Valid JSON:"
    )

    SLOT_FILLING_PROMPT_TEMPLATE = (
        "Extract information from the following text and create a valid JSON object that matches this schema:\n"
        "Schema:\n{{ schema }}\n\n"
        "Text: {{ text }}\n\n"
        "Focus on extracting the following fields: {{ fields }}\n"
        "Return only a valid JSON object with the extracted information. If a field cannot be determined from the text, "
        "use a reasonable default value or leave it as null.\n"
        "JSON:"
    )

    _models_registry = {}

    def __init__(
        self,
        model_class: Type[T],
        backend: Literal["llm", "fsm", "all"] = "llm",
        model_name: str = "HuggingFaceTB/SmolLM2-360M-Instruct",
        prompt_template: str | None = None,
        use_transitions: bool = True,
    ):
        self.model_class = model_class
        self.backend = backend
        self.schema = model_class.model_json_schema()
        self.prompt_template = prompt_template or self.DEFAULT_PROMPT_TEMPLATE
        self.use_transitions = use_transitions and HAS_TRANSITIONS

        # Initialize FSM processor if needed
        if backend in ["fsm", "all"]:
            self.fsm_processor = FSMProcessor(model_class, use_transitions=use_transitions)
        else:
            self.fsm_processor = None

        # Initialize LLM processor if needed
        if backend in ["llm", "all"]:
            if not HAS_LLM_DEPS:
                raise ImportError("LLM dependencies not found. Please install with pip install json-repair-llm[full]")

            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = (
                AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16,
                    device_map="auto",
                    trust_remote_code=True,
                    attn_implementation="flash_attention_2"
                    if "flash_attention_2" in dir(torch.nn.functional)
                    else None,
                )
                if model_name not in self._models_registry
                else self._models_registry[model_name]
            )

            self.outlines_model = models.transformers(
                model_name,
                model_kwargs={
                    "torch_dtype": torch.float16,
                    "device_map": "auto",
                    "attn_implementation": "flash_attention_2"
                    if "flash_attention_2" in dir(torch.nn.functional)
                    else None,
                },
            )
        else:
            self.tokenizer = None
            self.model = None
            self.outlines_model = None

    def _extract_information_llm(
        self, text: str, max_tokens: int | None = None, errors: Literal["ignore", "raise"] = "ignore"
    ) -> dict:
        """Extract structured information from unstructured text using LLM slot filling approach."""
        if not text.strip():
            return {}

        # Get the field names from the schema for the prompt
        schema = self.model_class.model_json_schema()
        fields = ", ".join(schema.get("properties", {}).keys())

        # Generate a template with default values to help the LLM
        default_values = self._get_default_values()

        prompt = jinja2.Template(self.SLOT_FILLING_PROMPT_TEMPLATE).render(
            text=text,
            schema=json.dumps(schema, indent=2),
            fields=fields,
        )

        if max_tokens is None:
            max_tokens = min(
                # infer from input length
                len(self.tokenizer(prompt)["input_ids"]) + 100,
                getattr(self.model.config, "max_position_embeddings", 4096),
            )

        try:
            generator = generate.json(self.outlines_model, self.model_class)
            extracted_model = generator(prompt, max_tokens=max_tokens)
            return extracted_model.model_dump()
        except Exception as e:
            logger.error(f"Failed to extract information with LLM: {e}")
            if errors == "ignore":
                return default_values
            raise ValueError(f"Failed to extract information: {e}")

    def _repair_json_llm(
        self, broken_json: str, max_tokens: int | None = None, errors: Literal["ignore", "raise"] = "ignore"
    ) -> dict:
        """Repair a broken JSON string using LLM approach."""
        if not broken_json.strip():
            return {}

        try:
            repaired_str = json_repair_loads(broken_json)
            if repaired_str:
                return repaired_str
        except Exception as e:
            logger.debug(f"json_repair failed: {e}")

        prompt = jinja2.Template(self.prompt_template).render(
            broken_json=broken_json,
            schema=json.dumps(self.schema, indent=2),
        )
        if max_tokens is None:
            max_tokens = min(
                # infer from input length
                len(self.tokenizer(prompt)["input_ids"]) + 100,
                getattr(self.model.config, "max_position_embeddings", 4096),
            )

        try:
            generator = generate.json(self.outlines_model, self.model_class)
            repaired_model = generator(prompt, max_tokens=max_tokens)
            return repaired_model.model_dump()
        except Exception as e:
            if errors == "ignore":
                return self._get_default_values()

            raise ValueError(f"Failed to generate JSON: {e}")

    def _get_default_values(self) -> dict:
        """Generate default values based on the schema."""

        def process_properties(properties: dict) -> dict:
            result = {}
            for field, field_info in properties.items():
                field_type = field_info.get("type")
                if field_type == "object":
                    result[field] = process_properties(field_info.get("properties", {}))
                elif field_type == "array":
                    result[field] = []
                elif field_type == "string":
                    result[field] = ""
                elif field_type in ["number", "integer"]:
                    result[field] = 0
                elif field_type == "boolean":
                    result[field] = False
                elif field_type == "null":
                    result[field] = None
                else:
                    result[field] = ""
            return result

        return process_properties(self.schema.get("properties", {}))

    def __call__(
        self,
        broken_json: str,
        max_tokens: int | None = None,
        errors: Literal["ignore", "raise"] = "ignore",
        strict: bool = True,
        context: dict | None = None,
        use_slot_filling: bool = False,
    ) -> T | None:
        """Repair and validate JSON, returning a Pydantic model instance using the configured backend(s)."""
        logger.debug(f"Processing with backend: {self.backend}")

        if use_slot_filling:
            if self.backend in ["llm", "all"]:
                try:
                    logger.debug("Using slot filling approach with LLM")
                    extracted_json = self._extract_information_llm(broken_json, max_tokens=max_tokens, errors=errors)
                    result = self.model_class.model_validate(extracted_json, strict=strict, context=context)
                    logger.debug("Successfully extracted information with LLM")
                    return result
                except (ValueError, json.JSONDecodeError, ValidationError) as e:
                    logger.error(f"LLM information extraction failed: {e}")
                    if errors == "ignore":
                        return None
                    raise ValueError(f"Failed to extract information: {e}")
            else:
                logger.error("Slot filling requires LLM backend")
                if errors == "ignore":
                    return None
                raise ValueError("Slot filling requires LLM backend")

        # Try FSM first if backend is "fsm" or "all"
        if self.backend in ["fsm", "all"]:
            try:
                fsm_result = self.fsm_processor(broken_json, errors="ignore", strict=strict, context=context)
                if fsm_result:
                    logger.debug("Successfully repaired with FSM backend")
                    return fsm_result
                elif self.backend == "fsm" and errors == "raise":
                    raise ValueError(f"FSM backend failed to repair JSON")
                elif self.backend == "fsm":
                    return None
            except Exception as e:
                logger.debug(f"FSM backend failed: {e}")
                if self.backend == "fsm" and errors == "raise":
                    raise ValueError(f"FSM backend failed: {e}")
                elif self.backend == "fsm":
                    return None

        if self.backend in ["llm", "all"]:
            try:
                repaired_json = self._repair_json_llm(broken_json, max_tokens=max_tokens, errors=errors)
                result = self.model_class.model_validate(repaired_json, strict=strict, context=context)
                logger.debug("Successfully repaired with LLM backend")
                return result
            except (ValueError, json.JSONDecodeError, ValidationError) as e:
                logger.error(f"LLM JSON repair failed: {e}")
                if errors == "ignore":
                    return None
                raise ValueError(f"Failed to repair JSON: {e}")

        if errors == "ignore":
            return None
        raise ValueError(f"All backends failed to repair JSON")
