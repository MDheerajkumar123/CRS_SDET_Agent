import re


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:
        if not text:
            return ""

        # Normalize Windows and old-style line endings.
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Replace tabs with spaces.
        text = text.replace("\t", " ")

        # Remove trailing spaces from each line.
        text = "\n".join(
            line.rstrip()
            for line in text.split("\n")
        )

        # Collapse multiple spaces, but preserve line breaks.
        text = re.sub(r"[ ]{2,}", " ", text)

        # Collapse excessive blank lines to a maximum of one blank line.
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()
