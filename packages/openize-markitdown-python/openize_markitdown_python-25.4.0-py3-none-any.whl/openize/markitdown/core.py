import os

from processor import DocumentProcessor


class MarkItDown:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def convert_document(self, input_file, insert_into_llm=False):
        """Run the document conversion process."""
        processor = DocumentProcessor(self.output_dir)
        processor.process_document(input_file, insert_into_llm)

    def convert_directory(self, input_dir: str, insert_into_llm: bool = False):
        supported_exts = [".docx", ".pdf", ".xlsx", ".pptx"]
        for filename in os.listdir(input_dir):
            filepath = os.path.join(input_dir, filename)
            if os.path.isfile(filepath) and os.path.splitext(filename)[1].lower() in supported_exts:
                self.convert_document(filepath, insert_into_llm)
