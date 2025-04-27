import os
from py4jasper.main import generate_report

def test_generate_report(monkeypatch):


    file_type = "pdf"
    input_file_path = "example.jrxml"
    data = [
        {"name": "John Doe", "age": 30, "city": "New York"},
        {"name": "Jane Smith", "age": 25, "city": "San Francisco"},
        {"name": "Alice Brown", "age": 28, "city": "Los Angeles"}
    ]

    output = generate_report(file_type=file_type, input_file_path=input_file_path, data=data)

    expected_output = os.path.join(
        os.getcwd(), f"{os.path.splitext(os.path.basename(input_file_path))[0]}.{file_type}"
    )
    assert output == expected_output
