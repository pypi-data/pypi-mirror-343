from typing import List

class NewLines:
    NL_PLACEHOLDER = "%nl%"

    def __init__(self):
        self.lines: List[str] = []

    def add_line(self, line: str) -> None:
        self.lines.append(line)

    def get_content(self) -> str:
        return self.NL_PLACEHOLDER.join(self.lines)

    def print_code_newline(self) -> None:
        content_with_newlines = self.get_content().replace(self.NL_PLACEHOLDER, "\n")
        print(content_with_newlines)

    def print_newline(self, text: str) -> None:
        print(text.replace(self.NL_PLACEHOLDER, "\n"))

    def clear(self) -> None:
        self.lines.clear()
