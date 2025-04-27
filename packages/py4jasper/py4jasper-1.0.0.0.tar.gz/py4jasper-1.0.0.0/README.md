# py4jasper

[![Build Status](https://img.shields.io/travis/sanskarg25/py4jasper)](https://github.com/sanskarg25/py4jasper)
[![PyPI version](https://badge.fury.io/py/py4jasper.svg)](https://pypi.org/project/py4jasper/)

**py4jasper** is a Python library that enables easy interaction with the JasperReports system through a Py4J-based Java Gateway bridge.  
It allows generating reports (PDF, DOCX, XLSX) from `.jrxml` templates using Python.

---

## Features
- Connects to JasperReports Java backend via Py4J
- Supports multiple output formats: **PDF**, **DOCX**, **XLSX**
- Converts Python data structures into Java-compatible formats automatically
- Simple API for report generation


## Installation Locally

First, clone the repository:

```bash
git clone https://github.com/yourusername/py4jasper.git
cd py4jasper


## Usage
from py4jasper.main import generate_report

## License
This project is licensed under the MIT License.