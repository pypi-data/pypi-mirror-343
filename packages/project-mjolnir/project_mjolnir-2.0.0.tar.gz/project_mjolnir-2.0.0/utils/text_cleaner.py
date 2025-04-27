import docx

class TextCleaner:

    @staticmethod
    def load_text(file_path):
        doc = docx.Document(file_path)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return text

    @staticmethod
    def clean_text(text):
        text = text.replace("‘", "'").replace("’", "'")
        text = text.replace("“", '"').replace("”", '"')
        text = text.replace("\u2013", "-").replace("\u2014", "-")
        text = text.replace("\xa0", " ").replace("–", "-")
        text = ' '.join(text.split())
        return text.strip()
