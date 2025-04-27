"""
Module for interacting with the Jasper Java system to generate reports.
"""

import os
from py4j.java_gateway import JavaGateway

DUMMY = [
    {"name": "John Doe", "age": 30, "city": "New York"},
    {"name": "Jane Smith", "age": 25, "city": "San Francisco"},
    {"name": "Alice Brown", "age": 28, "city": "Los Angeles"}
]


def generate_report(file_type: str = 'pdf', input_file_path: str = 'example.jrxml', output_file_path: str = None, data: list = DUMMY) -> str:
    """
    Generates a report using the py4j Java Gateway.

    Args:
        file_type (str): The output file format (pdf, docx, xlsx).
        input_file_path (str): The path to the input file.

    Returns:
        str: The output file name.
    """
    # ? Start the Py4J gateway to communicate with Java
    gateway = JavaGateway()
    output_file_path = os.path.join(
            os.getcwd(), f"{os.path.splitext(os.path.basename(input_file_path))[0]}.{file_type}"
        )

    # ? Storing generated file in current directory
    if not output_file_path:
        output_file_path = os.path.join(
            os.getcwd(), f"{os.path.splitext(os.path.basename(input_file_path))[0]}.{file_type}"
        )

    # ? Convert Python list to Java HashMap
    java_map = gateway.jvm.java.util.ArrayList()
    for row in data:
        java_row = gateway.jvm.java.util.HashMap()
        for key, value in row.items():
            java_row.put(key, value)
        java_map.add(java_row)

    try:
        gateway.entry_point.generate_report(input_file_path, output_file_path, java_map, file_type)
    except Exception as e:
        raise RuntimeError(f"Failed to generate report: {e}")

    return output_file_path
