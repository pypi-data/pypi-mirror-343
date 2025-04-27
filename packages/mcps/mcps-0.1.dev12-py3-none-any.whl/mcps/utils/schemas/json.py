from typing import Dict, Any, Type, TypeVar, Generic, Optional
import json
from jsonschema import validate, ValidationError
from ..base import SchemaValidator

T = TypeVar('T')

class JSONSchemaValidator(SchemaValidator[T]):
    """JSON Schema-based implementation of schema validation"""
    
    def __init__(self):
        self._schemas: Dict[Type, Dict[str, Any]] = {}
    
    def register_schema(self, schema_type: Type[T], schema: Dict[str, Any]) -> None:
        """Register a schema for a type
        
        Args:
            schema_type: Type to register schema for
            schema: JSON Schema definition
        """
        self._schemas[schema_type] = schema
    
    def validate(self, data: Dict[str, Any], schema: Type[T]) -> T:
        """Validate data against schema
        
        Args:
            data: Data to validate
            schema: Schema type to validate against
            
        Returns:
            Validated and typed data
            
        Raises:
            ValidationError: If data is invalid
        """
        if schema not in self._schemas:
            raise ValueError(f"No schema registered for type {schema.__name__}")
            
        try:
            # Validate against JSON Schema
            validate(instance=data, schema=self._schemas[schema])
            
            # Convert to target type
            return schema(**data)
        except ValidationError as e:
            raise ValidationError(f"Validation error: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Error converting data: {str(e)}")
    
    def is_valid(self, data: Dict[str, Any], schema: Type[T]) -> bool:
        """Check if data is valid against schema
        
        Args:
            data: Data to check
            schema: Schema type to check against
            
        Returns:
            True if data is valid
        """
        if schema not in self._schemas:
            return False
            
        try:
            validate(instance=data, schema=self._schemas[schema])
            return True
        except ValidationError:
            return False
    
    def get_schema(self, schema_type: Type[T]) -> Optional[Dict[str, Any]]:
        """Get schema for a type
        
        Args:
            schema_type: Type to get schema for
            
        Returns:
            Schema definition if found
        """
        return self._schemas.get(schema_type)
    
    def export_schema(self, schema_type: Type[T], file_path: str) -> None:
        """Export schema to file
        
        Args:
            schema_type: Type to export schema for
            file_path: Path to save schema to
        """
        if schema_type not in self._schemas:
            raise ValueError(f"No schema registered for type {schema_type.__name__}")
            
        with open(file_path, 'w') as f:
            json.dump(self._schemas[schema_type], f, indent=2)
    
    def import_schema(self, schema_type: Type[T], file_path: str) -> None:
        """Import schema from file
        
        Args:
            schema_type: Type to import schema for
            file_path: Path to load schema from
        """
        with open(file_path, 'r') as f:
            schema = json.load(f)
            
        self.register_schema(schema_type, schema) 