import re
import tempfile
import unittest
from pathlib import Path
from textwrap import dedent

from mkdocs_fun_plugin.plugin import _Executor


class TestExecutor(unittest.TestCase):
    def setUp(self) -> None:
        # Create a temporary module file for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.module_path = Path(self.temp_dir.name) / "test_module.py"

        with self.module_path.open("w") as f:
            f.write(
                dedent("""
                from functools import cache
                def add(a, b):
                    return a + b

                def greet(name="World"):
                    return f"Hello, {name}!"

                def list_items(*items):
                    return ", ".join(str(item) for item in items)

                def _private_func():
                    return "This is private"
                @cache
                def cached_func(param):
                    return f"Cached: {param}"
            """),
            )

        # Create the executor with a simple pattern
        self.pattern = re.compile(r"{{(?P<func>\w+)(\((?P<params>.*?)\))?}}")
        self.executor = _Executor(pattern=self.pattern, module=self.module_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_init_loads_public_functions(self) -> None:
        """Test that initialization loads public functions from the module."""
        self.assertIn("add", self.executor._map)
        self.assertIn("greet", self.executor._map)
        self.assertIn("list_items", self.executor._map)
        self.assertIn("cached_func", self.executor._map)  # Should load decorated functions
        self.assertNotIn("_private_func", self.executor._map)

    def test_parse_params(self) -> None:
        """Test parsing parameters with different complexity levels."""
        # Empty params
        args, kwargs = self.executor._parse_params("")
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {})

        # Simple args and kwargs
        args, kwargs = self.executor._parse_params('1, "test", key="value", num=42')
        self.assertEqual(args, (1, "test"))
        self.assertEqual(kwargs, {"key": "value", "num": 42})

        # Complex params with nested structures
        args, kwargs = self.executor._parse_params(
            '[1, 2], {"a": 1}, key=[1, 2, 3], data={"x": "y"}',
        )
        self.assertEqual(args, ([1, 2], {"a": 1}))
        self.assertEqual(kwargs, {"key": [1, 2, 3], "data": {"x": "y"}})

    def test_parse_value(self) -> None:
        """Test parsing different value types."""
        self.assertEqual(self.executor._parse_value("42"), 42)
        self.assertEqual(self.executor._parse_value('"hello"'), "hello")
        self.assertEqual(self.executor._parse_value("[1, 2, 3]"), [1, 2, 3])
        self.assertEqual(self.executor._parse_value('{"a": 1}'), {"a": 1})
        # Non-evaluable strings should be returned as is
        self.assertEqual(self.executor._parse_value("hello"), "hello")

    def test_call_with_replacements(self) -> None:
        """Test that __call__ replaces function calls in markdown."""
        markdown = dedent("""
            # Test Document

            Calculate: {{add(5, 10)}}

            Greeting: {{greet()}}

            Custom: {{greet(name="User")}}

            List: {{list_items(1, 2, 3, "four", five)}}
        """).strip()

        expected = dedent("""
            # Test Document

            Calculate: 15

            Greeting: Hello, World!

            Custom: Hello, User!

            List: 1, 2, 3, four, five
        """).strip()

        result = self.executor(markdown)
        self.assertEqual(result, expected)

    def test_call_with_none(self) -> None:
        """Test that __call__ handles None input."""
        self.assertIsNone(self.executor(None))

    def test_call_with_overlapping_matches(self) -> None:
        """Test multiple replacements in the same string."""
        markdown = "{{add(1, 2)}} and {{add(3, 4)}}"
        expected = "3 and 7"
        result = self.executor(markdown)
        self.assertEqual(result, expected)

    def test_call_with_decorated_function(self) -> None:
        """Test that decorated functions work properly."""
        markdown = "{{cached_func('test')}}"
        expected = "Cached: test"
        result = self.executor(markdown)
        self.assertEqual(result, expected)

    def test_function_not_found(self) -> None:
        """Test that an assertion error is raised when a function is not found."""
        markdown = "{{nonexistent_func()}}"
        with self.assertRaises(AssertionError):
            self.executor(markdown)

    def test_params_with_quotes_and_brackets(self) -> None:
        """Test parsing parameters with quotes and nested brackets."""
        markdown = '{{list_items("item with, comma", [1, 2, {"nested": "value"}])}}'
        expected = "item with, comma, [1, 2, {'nested': 'value'}]"
        result = self.executor(markdown)
        self.assertEqual(result, expected)
