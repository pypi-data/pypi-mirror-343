"""
Validation utilities for AgentDS-Bench
"""

import pandas as pd
from typing import Tuple


def validate_csv_response(file_path: str, expected_rows: int = 0) -> Tuple[bool, str]:
    """
    Validate a CSV response file to ensure it has correct format (n×2 shape).
    
    Args:
        file_path: Path to the CSV file to validate
        expected_rows: Expected number of rows (excluding header), 0 means skip row count validation
        
    Returns:
        Tuple containing:
            - Boolean indicating if validation passed
            - Error message if validation failed, empty string otherwise
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Check if DataFrame is empty
        if df.empty:
            return False, "CSV file is empty"
        
        # Check if DataFrame has exactly 2 columns
        if df.shape[1] != 2:
            return False, f"CSV must have exactly 2 columns, found {df.shape[1]}"
        
        # Check if the number of rows matches the expected count
        # Note: df.shape[0] includes the header row, but since we're reading with
        # pandas, the header is parsed separately and not included in the row count
        if expected_rows > 0:  # Skip check if expected_rows is 0 or negative
            actual_rows = df.shape[0]
            if actual_rows != expected_rows:
                return False, f"CSV must have exactly {expected_rows} data rows, found {actual_rows}"
        
        # Check for missing values
        if df.isna().any().any():
            return False, "CSV contains missing values"
            
        return True, ""
        
    except pd.errors.EmptyDataError:
        return False, "CSV file is empty"
    except pd.errors.ParserError:
        return False, "Invalid CSV format"
    except Exception as e:
        return False, f"Error validating CSV: {str(e)}" 