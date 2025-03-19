from plugin_framework import DocumentProcessorPlugin
from typing import Dict, List, Any
import pandas as pd
import os

class ExcelProcessorPlugin(DocumentProcessorPlugin):
    """Plugin for processing Excel files."""
    
    @property
    def name(self) -> str:
        return "Excel Processor"
    
    @property
    def supported_extensions(self) -> List[str]:
        return [".xlsx", ".xls"]
    
    def can_process(self, file_path: str) -> bool:
        """Check if this plugin can process the given file."""
        return file_path.lower().endswith((".xlsx", ".xls"))
    
    def process(self, file_path: str) -> List[Dict[str, Any]]:
        """Process an Excel file and return structured content."""
        content = []
        
        try:
            # Read Excel file
            excel_data = pd.read_excel(file_path, sheet_name=None)
            
            # Process each sheet
            for sheet_name, df in excel_data.items():
                # Convert column names to strings
                df.columns = df.columns.astype(str)
                
                # Process each row
                for row_idx, row in df.iterrows():
                    row_data = {
                        "sheet": sheet_name,
                        "row": int(row_idx),
                        "type": "excel_row",
                        "cells": {}
                    }
                    
                    # Process each cell
                    for col_name in df.columns:
                        cell_value = row[col_name]
                        # Handle NaN values
                        if pd.isna(cell_value):
                            cell_value = None
                        
                        row_data["cells"][col_name] = cell_value
                    
                    content.append(row_data)
            
            return content
        except Exception as e:
            print(f"Error processing Excel file: {e}")
            return [{
                "error": str(e),
                "type": "error"
            }]

# This will be automatically loaded by the plugin manage