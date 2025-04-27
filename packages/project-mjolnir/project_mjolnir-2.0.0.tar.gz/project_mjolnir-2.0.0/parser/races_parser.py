from parser.base_parser import BaseParser
from utils.text_cleaner import TextCleaner

class RacesParser(BaseParser):

    FIELD_KEYWORDS = {
        'type': 'Type:',
        'size': 'Size:',
        'speed': 'Speed:',
        'abilities': 'Abilities:',
        'languages': 'Languages:',
        'favored_class': 'Favored Class:',
        'level_adjustment': 'Level Adjustment:'
    }

    def parse(self):
        text_list = self.load_text()
        blocks = self.split_blocks(text_list)

        for block in blocks:
            race = self.extract_race(block)
            if race:
                self.data.append(race)

        return {'table': 'races', 'records': self.data}

    def extract_race(self, block_text):
        lines = block_text.split("\n")
        lines = [TextCleaner.clean_text(line) for line in lines if line.strip()]

        if not lines:
            return None

        race = {
            'name': lines[0].strip(),
            'type': None,
            'size': None,
            'speed': None,
            'abilities': None,
            'languages': None,
            'favored_class': None,
            'level_adjustment': None,
            'source': None
        }

        for line in lines[1:]:
            for key, keyword in self.FIELD_KEYWORDS.items():
                if line.lower().startswith(keyword.lower()):
                    value = line.split(":", 1)[-1].strip()
                    race[key] = value
                    break

        return race
