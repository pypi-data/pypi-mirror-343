from parser.base_parser import BaseParser
from utils.text_cleaner import TextCleaner

class FeatsParser(BaseParser):

    FIELD_KEYWORDS = {
        'prerequisites': 'Prerequisite:',
        'benefit': 'Benefit:',
        'normal': 'Normal:',
        'special': 'Special:'
    }

    def parse(self):
        text_list = self.load_text()
        blocks = self.split_blocks(text_list)

        for block in blocks:
            feat = self.extract_feat(block)
            if feat:
                self.data.append(feat)

        return {'table': 'feats', 'records': self.data}

    def extract_feat(self, block_text):
        lines = block_text.split("\n")
        lines = [TextCleaner.clean_text(line) for line in lines if line.strip()]

        if not lines:
            return None

        # Extract Name + Type from first line
        first_line = lines[0]
        if "[" in first_line and "]" in first_line:
            name_part, type_part = first_line.split("[", 1)
            name = name_part.strip()
            feat_type = type_part.replace("]", "").strip()
        else:
            name = first_line.strip()
            feat_type = None

        feat = {
            'name': name,
            'type': feat_type,
            'prerequisites': None,
            'benefit': None,
            'normal': None,
            'special': None,
            'source': None
        }

        for line in lines[1:]:
            for key, keyword in self.FIELD_KEYWORDS.items():
                if line.lower().startswith(keyword.lower()):
                    value = line.split(":", 1)[-1].strip()
                    feat[key] = value
                    break

        return feat
