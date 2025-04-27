"""Mock data for tool testing."""

from datetime import datetime

MOCK_TOOL_METADATA = {
    "tool1": {
        "id": "tool1",
        "name": "Test Tool 1",
        "description": "A test tool for testing purposes",
        "version": "1.0.0",
        "type": "local",
        "parameters": {
            "input": {
                "type": "string",
                "description": "Input text to process",
                "required": True
            },
            "options": {
                "type": "object",
                "description": "Processing options",
                "required": False,
                "properties": {
                    "case_sensitive": {
                        "type": "boolean",
                        "default": True
                    },
                    "max_length": {
                        "type": "integer",
                        "default": 1000
                    }
                }
            }
        },
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    "tool2": {
        "id": "tool2",
        "name": "Test Tool 2",
        "description": "Another test tool for testing purposes",
        "version": "1.0.0",
        "type": "remote",
        "parameters": {
            "image": {
                "type": "string",
                "description": "Base64 encoded image data",
                "required": True
            },
            "options": {
                "type": "object",
                "description": "Processing options",
                "required": False,
                "properties": {
                    "format": {
                        "type": "string",
                        "enum": ["jpg", "png"],
                        "default": "jpg"
                    },
                    "quality": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 100,
                        "default": 90
                    }
                }
            }
        },
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
}

MOCK_TOOL_EXECUTIONS = {
    "tool1": {
        "tool_id": "tool1",
        "execution_id": "exec1",
        "status": "completed",
        "start_time": datetime.now().isoformat(),
        "end_time": datetime.now().isoformat(),
        "duration_ms": 150,
        "input": {
            "input": "test input",
            "options": {
                "case_sensitive": True,
                "max_length": 1000
            }
        },
        "output": {
            "result": "processed test input",
            "metadata": {
                "processed_length": 17,
                "processing_time_ms": 150
            }
        }
    },
    "tool2": {
        "tool_id": "tool2",
        "execution_id": "exec2",
        "status": "completed",
        "start_time": datetime.now().isoformat(),
        "end_time": datetime.now().isoformat(),
        "duration_ms": 250,
        "input": {
            "image": "base64_encoded_image_data",
            "options": {
                "format": "jpg",
                "quality": 90
            }
        },
        "output": {
            "result": "processed_image_data",
            "metadata": {
                "width": 800,
                "height": 600,
                "format": "jpg",
                "size_bytes": 102400
            }
        }
    }
} 