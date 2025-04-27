from parser.base_parser import BaseParser
from utils.text_cleaner import TextCleaner

class DeitiesParser(BaseParser):

    FIELD_KEYWORDS = {
        'pantheon': 'Pantheon:',
        'alignment': 'Alignment:',
        'rank': 'Rank:',
        'portfolio': 'Portfolio:',
        'domains': 'Domains:',
        'favored_weapon': 'Favored Weapon:',
        'symbol': 'Symbol:'
    }

    def parse(self):
        text_list = self.load_text()
        blocks = self.split_blocks(text_list)

        for block in blocks:
            deity = self.extract_deity(block)
            if deity:
                self.data.append(deity)

        return {'table': 'deities', 'records': self.data}

    def extract_deity(self, block_text):
        lines = block_text.split("\n")
        lines = [TextCleaner.clean_text(line) for line in lines if line.strip()]

        if len(lines) < 2:
            return None

        deity = {
            'name': lines[0].strip(),
            'source': None,
            'pantheon': None,
            'alignment': None,
            'rank': None,
            'portfolio': None,
            'domains': None,
            'favored_weapon': None,
            'symbol': None
        }

        # Second line is often the Source (in parentheses)
        if "(" in lines[1] and ")" in lines[1]:
            deity['source'] = lines[1].strip()
            field_start_index = 2
        else:
            field_start_index = 1

        for line in lines[field_start_index:]:
            for key, keyword in self.FIELD_KEYWORDS.items():
                if line.lower().startswith(keyword.lower()):
                    value = line.split(":", 1)[-1].strip()
                    deity[key] = value
                    break

        return deity
