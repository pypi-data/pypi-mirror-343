from parser.base_parser import BaseParser
from utils.text_cleaner import TextCleaner

class ItemsParser(BaseParser):

    def parse(self):
        text_list = self.load_text()
        first_page_text = "\n".join(text_list[:40]).lower()

        if "armor bonus" in first_page_text or "damage:" in first_page_text or "critical:" in first_page_text:
            return self.parse_equipment(text_list)
        elif "aura:" in first_page_text and "caster level:" in first_page_text and "construction requirements:" in first_page_text:
            return self.parse_magic_items(text_list)
        else:
            print("[!] Could not detect item format. Skipping.")
            return {'table': 'unknown', 'records': []}

    def parse_equipment(self, text_list):
        blocks = self.split_blocks(text_list)
        records = []

        for block in blocks:
            item = self.extract_equipment(block)
            if item:
                records.append(item)

        return {'table': 'equipment', 'records': records}

    def extract_equipment(self, block_text):
        lines = block_text.split("\n")
        lines = [TextCleaner.clean_text(line) for line in lines if line.strip()]

        if not lines:
            return None

        equipment = {
            'name': lines[0].strip(),
            'cost': None,
            'damage': None,
            'critical': None,
            'armor_bonus': None,
            'max_dex_bonus': None,
            'armor_check_penalty': None,
            'arcane_spell_failure': None,
            'speed': None,
            'weight': None,
            'type': None
        }

        for line in lines[1:]:
            lower = line.lower()

            if "cost:" in lower:
                equipment['cost'] = line.split(":", 1)[-1].strip()
            elif "damage:" in lower:
                equipment['damage'] = line.split(":", 1)[-1].strip()
            elif "critical:" in lower:
                equipment['critical'] = line.split(":", 1)[-1].strip()
            elif "armor bonus:" in lower:
                equipment['armor_bonus'] = line.split(":", 1)[-1].strip()
            elif "max dex bonus:" in lower:
                equipment['max_dex_bonus'] = line.split(":", 1)[-1].strip()
            elif "armor check penalty:" in lower:
                equipment['armor_check_penalty'] = line.split(":", 1)[-1].strip()
            elif "arcane spell failure:" in lower:
                equipment['arcane_spell_failure'] = line.split(":", 1)[-1].strip()
            elif "speed:" in lower:
                equipment['speed'] = line.split(":", 1)[-1].strip()
            elif "weight:" in lower:
                equipment['weight'] = line.split(":", 1)[-1].strip()
            elif "type:" in lower:
                equipment['type'] = line.split(":", 1)[-1].strip()

        return equipment

    def parse_magic_items(self, text_list):
        blocks = self.split_blocks(text_list)
        records = []

        for block in blocks:
            item = self.extract_magic_item(block)
            if item:
                records.append(item)

        return {'table': 'magic_items', 'records': records}

    def extract_magic_item(self, block_text):
        lines = block_text.split("\n")
        lines = [TextCleaner.clean_text(line) for line in lines if line.strip()]

        if not lines:
            return None

        magic_item = {
            'name': lines[0].strip(),
            'aura': None,
            'caster_level': None,
            'slot': None,
            'price': None,
            'weight': None,
            'description': None,
            'construction_requirements': None
        }

        found_structured_fields = False
        description_lines = []

        for line in lines[1:]:
            lower_line = line.lower()

            if lower_line.startswith("aura:"):
                magic_item['aura'] = line.split(":", 1)[-1].strip()
            elif lower_line.startswith("caster level:"):
                magic_item['caster_level'] = line.split(":", 1)[-1].strip()
            elif lower_line.startswith("slot:"):
                magic_item['slot'] = line.split(":", 1)[-1].strip()
            elif lower_line.startswith("price:"):
                magic_item['price'] = line.split(":", 1)[-1].strip()
            elif lower_line.startswith("weight:"):
                magic_item['weight'] = line.split(":", 1)[-1].strip()
            elif lower_line.startswith("description:"):
                found_structured_fields = True
                description_lines.append(line.split(":", 1)[-1].strip())
            elif lower_line.startswith("construction requirements:"):
                magic_item['construction_requirements'] = line.split(":", 1)[-1].strip()
            elif found_structured_fields:
                description_lines.append(line.strip())

        if description_lines:
            magic_item['description'] = " ".join(description_lines)

        return magic_item
