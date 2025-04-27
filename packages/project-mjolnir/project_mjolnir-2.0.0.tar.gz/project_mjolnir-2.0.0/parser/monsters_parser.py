from parser.base_parser import BaseParser
from utils.text_cleaner import TextCleaner

class MonstersParser(BaseParser):

    def parse(self):
        text_list = self.load_text()
        blocks = self.split_blocks(text_list)

        for block in blocks:
            monster = self.extract_monster(block)
            if monster:
                self.data.append(monster)

        return {'table': 'monsters', 'records': self.data}

    def extract_monster(self, block_text):
        lines = block_text.split("\n")
        lines = [TextCleaner.clean_text(line) for line in lines if line.strip()]

        if not lines:
            return None

        monster = {
            'name': lines[0].strip(),
            'type': None,
            'hit_dice': None,
            'initiative': None,
            'speed': None,
            'armor_class': None,
            'base_attack_grapple': None,
            'attack': None,
            'full_attack': None,
            'space_reach': None,
            'special_attacks': None,
            'special_qualities': None,
            'saves': None,
            'abilities': None,
            'skills': None,
            'feats': None,
            'environment': None,
            'organization': None,
            'challenge_rating': None,
            'treasure': None,
            'alignment': None,
            'advancement': None,
            'level_adjustment': None
        }

        for line in lines[1:]:
            lower = line.lower()

            if "hit dice:" in lower:
                monster['hit_dice'] = line.split(":", 1)[-1].strip()
            elif "initiative:" in lower:
                monster['initiative'] = line.split(":", 1)[-1].strip()
            elif "speed:" in lower:
                monster['speed'] = line.split(":", 1)[-1].strip()
            elif "armor class:" in lower:
                monster['armor_class'] = line.split(":", 1)[-1].strip()
            elif "base attack/grapple:" in lower:
                monster['base_attack_grapple'] = line.split(":", 1)[-1].strip()
            elif "attack:" in lower and "full attack" not in lower:
                monster['attack'] = line.split(":", 1)[-1].strip()
            elif "full attack:" in lower:
                monster['full_attack'] = line.split(":", 1)[-1].strip()
            elif "space/reach:" in lower:
                monster['space_reach'] = line.split(":", 1)[-1].strip()
            elif "special attacks:" in lower:
                monster['special_attacks'] = line.split(":", 1)[-1].strip()
            elif "special qualities:" in lower:
                monster['special_qualities'] = line.split(":", 1)[-1].strip()
            elif "saves:" in lower:
                monster['saves'] = line.split(":", 1)[-1].strip()
            elif "abilities:" in lower:
                monster['abilities'] = line.split(":", 1)[-1].strip()
            elif "skills:" in lower:
                monster['skills'] = line.split(":", 1)[-1].strip()
            elif "feats:" in lower:
                monster['feats'] = line.split(":", 1)[-1].strip()
            elif "environment:" in lower:
                monster['environment'] = line.split(":", 1)[-1].strip()
            elif "organization:" in lower:
                monster['organization'] = line.split(":", 1)[-1].strip()
            elif "challenge rating:" in lower:
                monster['challenge_rating'] = line.split(":", 1)[-1].strip()
            elif "treasure:" in lower:
                monster['treasure'] = line.split(":", 1)[-1].strip()
            elif "alignment:" in lower:
                monster['alignment'] = line.split(":", 1)[-1].strip()
            elif "advancement:" in lower:
                monster['advancement'] = line.split(":", 1)[-1].strip()
            elif "level adjustment:" in lower:
                monster['level_adjustment'] = line.split(":", 1)[-1].strip()
            elif not monster['type']:
                monster['type'] = line.strip()

        return monster
