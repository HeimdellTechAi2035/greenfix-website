import re
from pathlib import Path

root = Path('.')
header_block_pattern = re.compile(r'(\.header-content\s*\{[^}]*\})', re.DOTALL)

for path in sorted(root.glob('*.html')):
    text = path.read_text(encoding='utf-8')
    if '.header-content' not in text:
        continue

    new_text = text
    # Replace justify-content if used
    def replace_block(match):
        block = match.group(1)
        block = re.sub(r'justify-content\s*:\s*space-between\s*;?', 'justify-content: flex-start;', block)
        if 'flex-wrap' not in block:
            block = block.replace('align-items: center;', 'align-items: center;\n            flex-wrap: wrap;\n            gap: 0.75rem')
        if 'gap' not in block:
            if 'flex-wrap' in block and 'gap' not in block:
                block = block.replace('flex-wrap: wrap;', 'flex-wrap: wrap;\n            gap: 0.75rem')
        return block

    new_text = header_block_pattern.sub(replace_block, new_text, count=1)

    if '.header-content .phone-link:first-of-type' not in new_text:
        new_text = header_block_pattern.sub(
            r"\1\n\n        .header-content .phone-link:first-of-type {\n            margin-left: auto;\n        }\n\n        .header-content .phone-link {\n            padding: 0.35rem 0.6rem;\n            font-size: 0.9rem;\n            border-width: 1px;\n            border-radius: 0.5rem;\n        }",
            new_text,
            count=1,
        )

    # If the first-of-type rule exists but the compact phone-link rule is missing, insert it after the first-of-type block
    if '.header-content .phone-link:first-of-type' in new_text and '.header-content .phone-link {' not in new_text:
        new_text = re.sub(r'(\.header-content\s*\.phone-link:first-of-type\s*\{[^}]*\})',
                          r"\1\n\n        .header-content .phone-link {\n            padding: 0.35rem 0.6rem;\n            font-size: 0.9rem;\n            border-width: 1px;\n            border-radius: 0.5rem;\n        }",
                          new_text,
                          count=1,
                          flags=re.DOTALL)

    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print(f'Updated {path.name}')
