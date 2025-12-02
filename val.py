"""
val.py

Validates a JSON file produced by the ESP32 against a predefined schema.
Uses the 'jsonschema' library.
"""

import json
import sys
from typing import Dict, Any, Optional
from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

class JSONValidator:
    """
    Class responsible for validating JSON data against a specific schema.
    """

    # Schema definition
    SCHEMA: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "status": {
                "type": "object",
                "properties": {
                    "temperature": {"type": "number"},
                    "light": {"type": "number"},
                    "regul": {"type": "string"},
                    "fire": {"type": "boolean"},
                    "heat": {"type": "string"},
                    "cold": {"type": "string"},
                    "fanspeed": {"type": "number"}
                },
                "required": ["temperature", "light", "regul", "fire"]
            },
            "location": {
                "type": "object",
                "properties": {
                    "room": {"type": "string"},
                    "gps": {
                        "type": "object",
                        "properties": {
                            "lat": {"type": "number"},
                            "lon": {"type": "number"}
                        },
                        "required": ["lat", "lon"]
                    },
                    "address": {"type": "string"}
                },
                "required": ["room", "gps"]
            },
            "regul": {
                "type": "object",
                "properties": {
                    "lt": {"type": "number"},
                    "ht": {"type": "number"}
                },
                "required": ["lt", "ht"]
            },
            "info": {
                "type": "object",
                "properties": {
                    "ident": {"type": "string"},
                    "user": {"type": "string"},
                    "loc": {"type": "string"}
                },
                "required": ["ident", "user", "loc"]
            },
            "net": {
                "type": "object",
                "properties": {
                    "uptime": {"type": "string"},
                    "ssid": {"type": "string"},
                    "mac": {"type": "string"},
                    "ip": {"type": "string"}
                },
                "required": ["ssid", "ip"]
            },
            "reporthost": {
                "type": "object",
                "properties": {
                    "target_ip": {"type": "string"},
                    "target_port": {"type": "number"},
                    "sp": {"type": "number"}
                },
                "required": ["target_ip", "target_port", "sp"]
            },
            "piscine": {
                "type": "object",
                "properties": {
                    "occuped": {"type": "boolean"},
                    "hotspot": {"type": "boolean"}
                },
                "required": ["occuped", "hotspot"]
            }
        },
        "required": ["status", "location", "regul", "info", "net", "reporthost"]
    }

    @staticmethod
    def validate_file(filename: str) -> bool:
        """
        Validates a JSON file against the schema.

        Args:
            filename (str): The path to the JSON file.

        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            validate(instance=data, schema=JSONValidator.SCHEMA)
            print(f"✅ The JSON file '{filename}' is valid according to the schema.")
            return True

        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
        except json.JSONDecodeError as e:
            print(f"❌ JSON Syntax Error: {e}")
        except ValidationError as e:
            print(f"❌ Invalid JSON: {e.message}")
        except SchemaError as e:
            print(f"❌ Schema Error: {e.message}")
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
        
        return False

if __name__ == "__main__":
    # Default to "test.json" if no argument is provided
    file_to_check = "test.json"
    if len(sys.argv) > 1:
        file_to_check = sys.argv[1]
    
    JSONValidator.validate_file(file_to_check)
