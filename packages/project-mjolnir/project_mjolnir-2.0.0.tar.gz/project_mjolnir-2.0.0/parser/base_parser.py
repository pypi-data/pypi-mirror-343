from abc import ABC, abstractmethod

class BaseParser(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    @abstractmethod
    def parse(self):
        pass

    def load_text(self):
        from docx import Document
        document = Document(self.file_path)
        full_text = []
        for para in document.paragraphs:
            if para.text.strip():
                full_text.append(para.text.strip())
        return full_text

    def split_blocks(self, text_list):
        """
        Default block splitter based on empty lines between entries.
        Can be overridden by child parsers if needed.
        """
        blocks = []
        current_block = []

        for line in text_list:
            if line.strip() == "":
                if current_block:
                    blocks.append("\n".join(current_block))
                    current_block = []
            else:
                current_block.append(line)

        if current_block:
            blocks.append("\n".join(current_block))

        return blocks
