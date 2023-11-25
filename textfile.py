import re
from pathlib import Path
from typing import Dict, Union


class TextFile:
    def __init__(self, path:Union[Path,str]):
        self.path = Path(path) if isinstance(path, str) else path

    def add_missing(self, lines_to_add) -> 'TextFile':
        """Add provided lines if they don't already exist in the file."""
        self.touch()
        existing_lines = set()
        if self.path.exists():
            with self.path.open('r') as file:
                existing_lines = {line.strip() for line in file}
        with self.path.open('a') as file:
            for line in lines_to_add:
                if line and line not in existing_lines:
                    file.write(f'{line}\n')
        return self

    def touch(self) -> 'TextFile':
        """Ensure the file and all it's parent directories exists."""
        self.path.parent.mkdir(exist_ok=True)
        self.path.touch()
        return self

    def update_lines(self, updates: Dict[str, str]):
        """Update lines based on a dictionary where keys are regex patterns and values are new lines."""
        self.touch()
        lines = self.path.read_text().splitlines(keepends=True)
        used_patterns = {pattern: False for pattern in updates}
        with self.path.open('w') as file:
            for line in lines:
                for pattern, new_line in updates.items():
                    if re.search(pattern, line.strip()):
                        file.write(f'{new_line}\n')
                        used_patterns[pattern] = True
                        break
                else:
                    file.write(line)
            for pattern, new_line in updates.items():
                if not used_patterns[pattern]:
                    file.write(f'{new_line}\n')