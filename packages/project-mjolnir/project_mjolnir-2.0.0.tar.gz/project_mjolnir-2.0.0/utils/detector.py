def detect_entity(text_list):
    first_page_text = "\n".join(text_list[:40]).lower()

    if "pantheon:" in first_page_text and "domains:" in first_page_text:
        return "deities"
    elif "prerequisite:" in first_page_text and "benefit:" in first_page_text:
        return "feats"
    elif "school:" in first_page_text and "casting time:" in first_page_text:
        if "components:" in first_page_text:
            return "spells"
        else:
            return "spells"
    elif "damage:" in first_page_text and ("armor bonus:" in first_page_text or "critical:" in first_page_text):
        return "equipment"
    elif "aura:" in first_page_text and "caster level:" in first_page_text and "slot:" in first_page_text:
        return "magic_items"
    elif "type:" in first_page_text and "size:" in first_page_text and "abilities:" in first_page_text:
        return "races"
    elif "hit die:" in first_page_text and "class skills" in first_page_text:
        return "classes"
    elif "hit dice:" in first_page_text and "initiative:" in first_page_text and "armor class:" in first_page_text:
        return "monsters"
    elif "level adjustment:" in first_page_text and "challenge rating:" in first_page_text:
        return "templates"
    else:
        return "unknown"
