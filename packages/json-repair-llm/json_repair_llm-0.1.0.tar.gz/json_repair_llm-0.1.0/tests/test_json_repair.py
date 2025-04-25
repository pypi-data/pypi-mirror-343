import unittest
from unittest.mock import patch, MagicMock

from pydantic import BaseModel

from json_repair_llm import FSMProcessor, JsonRepairProcessor


class TestModel(BaseModel):
    name: str
    age: int
    email: str


class NestedModel(BaseModel):
    user: TestModel
    is_active: bool


class TestFSMProcessor(unittest.TestCase):
    """Tests for the FSM-based JSON repair processor."""

    def setUp(self):
        self.processor = FSMProcessor(TestModel)
        self.nested_processor = FSMProcessor(NestedModel)

    def test_valid_json(self):
        """Test processing valid JSON input."""
        valid_json = '{"name": "John Doe", "age": 30, "email": "john@example.com"}'
        result = self.processor(valid_json)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "John Doe")
        self.assertEqual(result.age, 30)
        self.assertEqual(result.email, "john@example.com")

    def test_minor_json_errors(self):
        """Test processing JSON with minor errors."""
        broken_json = '{name: "John Doe", "age": 30, "email": "john@example.com"}'
        result = self.processor(broken_json)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "John Doe")
        self.assertEqual(result.age, 30)
        self.assertEqual(result.email, "john@example.com")

    def test_nested_json(self):
        """Test processing nested JSON structures."""
        nested_json = """
        {
            "user": {"name": "John Doe", "age": 30, "email": "john@example.com"},
            "is_active": true
        }
        """
        result = self.nested_processor(nested_json)
        self.assertIsNotNone(result)
        self.assertEqual(result.user.name, "John Doe")
        self.assertEqual(result.user.age, 30)
        self.assertEqual(result.user.email, "john@example.com")
        self.assertTrue(result.is_active)

    def test_broken_nested_json(self):
        """Test processing broken nested JSON structures."""
        broken_nested_json = """
        {
            "user": {name: "John Doe", age: 30, email: "john@example.com"},
            is_active: true
        }
        """
        result = self.nested_processor(broken_nested_json)
        self.assertIsNotNone(result)
        self.assertEqual(result.user.name, "John Doe")
        self.assertEqual(result.user.age, 30)
        self.assertEqual(result.user.email, "john@example.com")
        self.assertTrue(result.is_active)

    def test_invalid_json(self):
        """Test processing severely broken JSON that can't be repaired."""
        invalid_json = "This is not JSON at all."
        result = self.processor(invalid_json, errors="ignore")
        self.assertIsNone(result)

        with self.assertRaises(ValueError):
            self.processor(invalid_json, errors="raise")

    def test_empty_input(self):
        """Test processing empty input."""
        result = self.processor("", errors="ignore")
        self.assertIsNone(result)

        with self.assertRaises(ValueError):
            self.processor("", errors="raise")


class TestJsonRepairProcessor(unittest.TestCase):
    """Tests for the JsonRepairProcessor with different backends."""

    # FIXME: add mock for LLM backend

    def test_fsm_backend(self):
        """Test FSM backend for JSON repair."""
        processor = JsonRepairProcessor(TestModel, backend="fsm")
        broken_json = '{name: "John Doe", "age": 30, "email": "john@example.com"}'
        result = processor(broken_json)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "John Doe")
        self.assertEqual(result.age, 30)
        self.assertEqual(result.email, "john@example.com")

    def test_llm_backend(self):
        """Test LLM backend for JSON repair."""
        processor = JsonRepairProcessor(TestModel, backend="llm")
        broken_json = '{name: "John Doe", "age": 30, "email": "john@example.com"}'
        result = processor(broken_json)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "John Doe")
        self.assertEqual(result.age, 30)
        self.assertEqual(result.email, "john@example.com")

    def test_all_backend_fsm_success(self):
        """Test 'all' backend when FSM succeeds."""
        processor = JsonRepairProcessor(TestModel, backend="all")
        broken_json = '{name: "John Doe", "age": 30, "email": "john@example.com"}'
        result = processor(broken_json)
        self.assertIsNotNone(result)

    def test_all_backend_fsm_fails(self):
        """Test 'all' backend when FSM fails and LLM succeeds."""
        # Configure mock to return a valid model
        processor = JsonRepairProcessor(TestModel, backend="all")
        # This is too broken for FSM but should be handled by LLM
        very_broken_json = "User: John Doe, Age: 30, Email: john@example.com"
        result = processor(very_broken_json)
        self.assertIsNotNone(result)

    def test_slot_filling(self):
        """Test slot filling functionality."""
        processor = JsonRepairProcessor(TestModel, backend="llm")
        unstructured_text = "My name is John Doe and I'm 30 years old. You can reach me at john@example.com."
        result = processor(unstructured_text, use_slot_filling=True)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "John Doe")
        self.assertEqual(result.age, 30)
        self.assertEqual(result.email, "john@example.com")


if __name__ == "__main__":
    unittest.main()
