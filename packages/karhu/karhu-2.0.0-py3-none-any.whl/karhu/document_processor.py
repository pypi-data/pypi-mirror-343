# src/document_processor.py
import pdfplumber
from pathlib import Path
from bs4 import BeautifulSoup
import json
import csv
import os

class DocumentProcessor:
    def process_files_directory(self, directory):
        files_content = {}
        base_directory = os.path.abspath(directory)
        
        if not os.path.isdir(base_directory):
            raise ValueError("Provided path is not a directory")
        for filename in os.listdir(base_directory):
            # Sanitize filename to prevent path traversal
            if '..' in filename or filename.startswith('/'):
                continue
            file_path = os.path.join(base_directory, filename)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        files_content[filename] = file.read()
                except Exception as e:
                    print(f"Error reading file {file_path}: {str(e)}")
        return files_content  
    
    def read_file(self, file):
        """Read content from a file based on its extension"""
        file_extension = Path(file).suffix.lower()
        
        if file_extension == '.pdf':
            return self.read_pdf(file)
        elif file_extension == '.xml':
            return self.read_xml(file)
        elif file_extension == '.json':
            return self.read_json(file)
        elif file_extension == '.csv':
            return self.read_csv(file)
        elif file_extension in ['.html', '.htm', '.php']:
            return self.read_html(file)
        elif file_extension in ['.txt', '.py', '.c', '.cpp', '.md',]:
            return self.read_text(file)
        else:
            return f"Unsupported file type: {file_extension}"

    def read_html(self, file_path):
        """Extract text from an HTML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                return soup.get_text()
        except Exception as e:
            return f"Error reading HTML/PHP: {str(e)}"

    def read_text(self, file_path):
        """Extract text from a plain text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error reading text file: {str(e)}"
    
    def read_pdf(self, pdf_path):
        try:
            text_content = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text_content.append(page.extract_text())
            return '\n'.join(text_content)
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    def read_xml(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'xml')
                return soup.get_text()
        except Exception as e:
            return f"Error reading XML: {str(e)}"
    
    def read_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return json.dumps(data, indent=4)
        except Exception as e:
            return f"Error reading JSON: {str(e)}"
        
    def read_csv(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                return '\n' .join([', '.join(row) for row in reader])
        except Exception as e:
            return f"Error reading CSV: {str(e)}"
                         
