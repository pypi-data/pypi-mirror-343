from parser.base_parser import BaseParser
from utils.text_cleaner import TextCleaner

class TemplatesParser(BaseParser):

    def parse(self):
        text_list = self.load_text()
        blocks = self.split_blocks(text_list)

        for block in blocks:
            template = self.extract_template(block)
            if template:
                self.data.append(template)

        return {'table': 'templates', 'records': self.data}

    def extract_template(self, block_text):
        lines = block_text.split("\n")
        lines = [TextCleaner.clean_text(line) for line in lines if line.strip()]

        if not lines:
            return None

        template = {
            'name': lines[0].strip(),
            'type_change': None,
            'hit_dice': None,
            'armor_class': None,
            'attack': None,
            'damage': None,
            'special_attacks': None,
            'special_qualities': None,
            'saves': None,
            'abilities': None,
            'skills': None,
            'feats': None,
            'environment': None,
            'challenge_rating': None,
            'alignment': None,
            'level_adjustment': None
        }

        for line in lines[1:]:
            lower = line.lower()

            if "type:" in lower:
                template['type_change'] = line.split(":", 1)[-1].strip()
            elif "hit dice:" in lower:
                template['hit_dice'] = line.split(":", 1)[-1].strip()
            elif "armor class:" in lower:
                template['armor_class'] = line.split(":", 1)[-1].strip()
            elif "attack:" in lower and "full attack" not in lower:
                template['attack'] = line.split(":", 1)[-1].strip()
            elif "damage:" in lower:
                template['damage'] = line.split(":", 1)[-1].strip()
            elif "special attacks:" in lower:
                template['special_attacks'] = line.split(":", 1)[-1].strip()
            elif "special qualities:" in lower:
                template['special_qualities'] = line.split(":", 1)[-1].strip()
            elif "saves:" in lower:
                template['saves'] = line.split(":", 1)[-1].strip()
            elif "abilities:" in lower:
                template['abilities'] = line.split(":", 1)[-1].strip()
            elif "skills:" in lower:
                template['skills'] = line.split(":", 1)[-1].strip()
            elif "feats:" in lower:
                template['feats'] = line.split(":", 1)[-1].strip()
            elif "environment:" in lower:
                template['environment'] = line.split(":", 1)[-1].strip()
            elif "challenge rating:" in lower:
                template['challenge_rating'] = line.split(":", 1)[-1].strip()
            elif "alignment:" in lower:
                template['alignment'] = line.split(":", 1)[-1].strip()
            elif "level adjustment:" in lower:
                template['level_adjustment'] = line.split(":", 1)[-1].strip()

        return template
