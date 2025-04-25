"""
Task representation for the AgentDS-Bench platform
"""

from typing import Any, Dict, Optional


class Task:
    """
    Represents a benchmarking task in the AgentDS-Bench platform.
    
    A task contains the data, instructions, and metadata needed for an agent to complete
    a specific data science challenge.
    """
    
    def __init__(
        self, 
        task_number: int, 
        domain: str, 
        category: str, 
        data: Any, 
        instructions: str, 
        side_info: Optional[Any] = None, 
        response_format: Optional[Dict] = None,
        test_size: Optional[int] = None
    ):
        """
        Initialize a new Task instance.
        
        Args:
            task_number: Task number (1-10) within the domain
            domain: The domain or field this task belongs to
            category: The scaling category (Fidelity, Volume, Noise, Complexity)
            data: The primary data for the task
            instructions: Task instructions and requirements
            side_info: Additional information or context (optional)
            response_format: Expected format for the response (optional)
            test_size: Expected number of rows in the response CSV (optional)
        """
        self.task_number = task_number
        self.domain = domain
        self.category = category
        self.data = data
        self.instructions = instructions
        self.side_info = side_info or {}
        self.response_format = response_format or {}
        self.test_size = test_size
        
        # Initialize dataset_path for later use
        self.dataset_path = None
    
    def get_data(self) -> Any:
        """
        Get the primary data for this task.
        
        Returns:
            The task data
        """
        return self.data
    
    def get_instructions(self) -> str:
        """
        Get the instructions for this task.
        
        Returns:
            Task instructions as a string
        """
        return self.instructions
    
    def get_side_info(self) -> Any:
        """
        Get additional information or context for this task.
        
        Returns:
            Additional information
        """
        return self.side_info
    
    def get_response_format(self) -> Dict:
        """
        Get the expected format for the response.
        
        Returns:
            A dictionary describing the expected response format
        """
        return self.response_format
    
    def get_test_size(self) -> Optional[int]:
        """
        Get the expected number of rows in the response CSV.
        
        Returns:
            Expected number of rows or None if not specified
        """
        return self.test_size
    
    def validate_response(self, response: Any) -> bool:
        """
        Validate that a response matches the expected format.
        
        Args:
            response: The response to validate
            
        Returns:
            True if the response is valid, False otherwise
        """
        # Basic validation - can be extended with more specific checks
        if not self.response_format:
            # If no format is specified, accept any response
            return True
            
        # If there is a response format, check that it matches the expected format
        # This is a simple implementation and should be extended based on the actual
        # response format specification
        try:
            if isinstance(self.response_format, dict) and isinstance(response, dict):
                # Check that all required keys are present
                for key in self.response_format:
                    if key not in response:
                        print(f"Missing required key in response: {key}")
                        return False
                return True
            else:
                # For non-dict formats, just check the type
                return isinstance(response, type(self.response_format))
        except Exception as e:
            print(f"Error validating response: {e}")
            return False 