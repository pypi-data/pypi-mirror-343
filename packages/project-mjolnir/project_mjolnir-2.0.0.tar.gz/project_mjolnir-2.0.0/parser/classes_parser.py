from parser.base_parser import BaseParser
from utils.text_cleaner import TextCleaner

class ClassesParser(BaseParser):

    def parse(self):
        text_list = self.load_text()
        blocks = self.split_blocks(text_list)

        for block in blocks:
            cls = self.extract_class(block)
            if cls:
                self.data.append(cls)

        return {'table': 'classes', 'records': self.data}

    def extract_class(self, block_text):
        lines = block_text.split("\n")
        lines = [TextCleaner.clean_text(line) for line in lines if line.strip()]

        if not lines:
            return None

        cls = {
            'name': lines[0].strip(),
            'hit_die': None,
            'class_skills': None,
            'skill_points_1st_level': None,
            'skill_points_each_additional_level': None,
            'weapon_armor_proficiency': None,
            'requirements': None,
            'class_features': None,
            'progression_table': None
        }

        inside_table = False
        table_data = []
        features = []
        current_feature = None
        feature_text = []

        for line in lines[1:]:
            lower = line.lower()

            if "hit die:" in lower:
                cls['hit_die'] = line.split(":", 1)[-1].strip()
            elif "class skills" in lower:
                cls['class_skills'] = line.split(":", 1)[-1].strip()
            elif "skill points at 1st level" in lower:
                cls['skill_points_1st_level'] = line.split(":", 1)[-1].strip()
            elif "skill points at each additional level" in lower:
                cls['skill_points_each_additional_level'] = line.split(":", 1)[-1].strip()
            elif "weapon and armor proficiency" in lower:
                cls['weapon_armor_proficiency'] = line.split(":", 1)[-1].strip()
            elif "requirements:" in lower:
                cls['requirements'] = line.split(":", 1)[-1].strip()
            elif "level" in lower and "base attack bonus" in lower:
                inside_table = True
                continue
            elif inside_table and (line.strip() == "---" or line.lower().startswith("class features")):
                inside_table = False
                continue
            elif inside_table:
                table_data.append(line.strip())
            elif any(line.startswith(word) for word in ("Special Ability:", "Special Abilities:", "Class Features:", "Abilities:")):
                continue
            else:
                if line.endswith(":") and not current_feature:
                    current_feature = line[:-1].strip()
                    feature_text = []
                elif current_feature:
                    feature_text.append(line.strip())

                if current_feature and (not line or line == lines[-1]):
                    features.append({
                        'name': current_feature,
                        'description': " ".join(feature_text)
                    })
                    current_feature = None
                    feature_text = []

        if table_data:
            cls['progression_table'] = table_data
        if features:
            cls['class_features'] = features

        return cls
