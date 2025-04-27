from parser.base_parser import BaseParser
from utils.text_cleaner import TextCleaner

class SpellsParser(BaseParser):

    def parse(self):
        text_list = self.load_text()
        first_page_text = "\n".join(text_list[:40]).lower()

        if "school:" in first_page_text and "casting time:" in first_page_text:
            if "components:" in first_page_text:
                return self.parse_full_descriptions(text_list)
            else:
                return self.parse_basic_spells(text_list)
        elif "0 level" in first_page_text or "1st level" in first_page_text:
            return self.parse_spells_by_class(text_list)
        else:
            print("[!] Could not detect spell format. Skipping.")
            return {'table': 'unknown', 'records': []}

    def parse_basic_spells(self, text_list):
        blocks = self.split_blocks(text_list)
        records = []
        for block in blocks:
            spell = self.extract_basic_spell(block)
            if spell:
                records.append(spell)
        return {'table': 'spells', 'records': records}

    def extract_basic_spell(self, block_text):
        lines = block_text.split("\n")
        lines = [TextCleaner.clean_text(line) for line in lines if line.strip()]

        if not lines or len(lines) < 4:
            return None

        spell = {
            'name': lines[0].strip(),
            'school': None,
            'level_by_class': None,
            'casting_time': None,
            'range': None,
            'effect': None,
            'duration': None,
            'saving_throw': None,
            'spell_resistance': None
        }

        for line in lines[1:]:
            if "school:" in line.lower():
                spell['school'] = line.split(":", 1)[-1].strip()
            elif "level:" in line.lower():
                spell['level_by_class'] = line.split(":", 1)[-1].strip()
            elif "casting time:" in line.lower():
                spell['casting_time'] = line.split(":", 1)[-1].strip()
            elif "range:" in line.lower():
                spell['range'] = line.split(":", 1)[-1].strip()
            elif "effect:" in line.lower() or "area:" in line.lower() or "target:" in line.lower():
                spell['effect'] = line.split(":", 1)[-1].strip()
            elif "duration:" in line.lower():
                spell['duration'] = line.split(":", 1)[-1].strip()
            elif "saving throw:" in line.lower():
                spell['saving_throw'] = line.split(":", 1)[-1].strip()
            elif "spell resistance:" in line.lower():
                spell['spell_resistance'] = line.split(":", 1)[-1].strip()

        return spell

    def parse_spells_by_class(self, text_list):
        records = []
        current_class = None
        current_level = None

        for line in text_list:
            line = TextCleaner.clean_text(line)
            if not line:
                continue

            if "spells" in line.lower() and "level" not in line.lower():
                current_class = line.replace("Spells", "").strip()
                continue

            if "level" in line.lower():
                current_level = line.strip()
                continue

            if current_class and current_level and line:
                records.append({
                    'class_name': current_class,
                    'spell_level': current_level,
                    'spell_name': line.strip()
                })

        return {'table': 'spells_by_class', 'records': records}

    def parse_full_descriptions(self, text_list):
        blocks = self.split_blocks(text_list)
        records = []
        for block in blocks:
            spell = self.extract_full_description(block)
            if spell:
                records.append(spell)
        return {'table': 'spell_descriptions', 'records': records}

    def extract_full_description(self, block_text):
        lines = block_text.split("\n")
        lines = [TextCleaner.clean_text(line) for line in lines if line.strip()]

        if not lines or len(lines) < 5:
            return None

        spell = {
            'name': lines[0].strip(),
            'school': None,
            'components': None,
            'level_by_class': None,
            'casting_time': None,
            'range': None,
            'effect': None,
            'duration': None,
            'saving_throw': None,
            'spell_resistance': None,
            'description': None
        }

        field_mapping = {
            'school': 'school',
            'components': 'components',
            'level': 'level_by_class',
            'casting time': 'casting_time',
            'range': 'range',
            'effect': 'effect',
            'area': 'effect',
            'target': 'effect',
            'duration': 'duration',
            'saving throw': 'saving_throw',
            'spell resistance': 'spell_resistance'
        }

        found_structured_fields = False
        description_lines = []

        for line in lines[1:]:
            lower_line = line.lower()
            matched = False
            for key, field in field_mapping.items():
                if lower_line.startswith(f"{key}:"):
                    spell[field] = line.split(":", 1)[-1].strip()
                    matched = True
                    found_structured_fields = True
                    break

            if not matched and found_structured_fields:
                description_lines.append(line)

        if description_lines:
            spell['description'] = " ".join(description_lines)

        return spell
