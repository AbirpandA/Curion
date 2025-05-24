import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from rich.progress import Progress
from brain import Brain

class KnowledgeIngester:
    def __init__(self):
        self.brain = Brain()
        self.processed_files = set()
        self.load_processed_list()
    
    def load_processed_list(self):
        try:
            with open("data/processed_files.log", "r") as f:
                self.processed_files = set(f.read().splitlines())
        except FileNotFoundError:
            pass
    
    def log_processed_file(self, path):
        with open("data/processed_files.log", "a") as f:
            f.write(f"{path}\n")
    
    def process_file(self, file_path):
        """Smart file processor with format detection"""
        try:
            text = ""
            ext = os.path.splitext(file_path)[1].lower()
            
            # Text-based files
            if ext in ['.txt', '.md']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            
            # PDFs
            elif ext == '.pdf':
                from pypdf import PdfReader
                reader = PdfReader(file_path)
                text = "\n".join([page.extract_text() for page in reader.pages])
            
            # Word Docs
            elif ext == '.docx':
                from docx import Document
                doc = Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs])
            
            # Process and ingest
            if text:
                self.brain.ingest_knowledge(text)
                return True
            return False
        
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return False

    def ingest_directory(self, path="data/knowledge_base"):
        files = [str(p) for p in Path(path).rglob('*') if p.is_file()]
        new_files = [f for f in files if f not in self.processed_files]
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Processing...", total=len(new_files))
            
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                for file_path in new_files:
                    futures.append(executor.submit(self.process_file, file_path))
                
                for i, future in enumerate(futures):
                    success = future.result()
                    if success:
                        self.log_processed_file(new_files[i])
                    progress.update(task, advance=1, description=f"Processed {new_files[i]}")

if __name__ == "__main__":
    ingester = KnowledgeIngester()
    ingester.ingest_directory()