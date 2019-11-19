from dataclasses import dataclass


@dataclass
class Commit:
    author: str

    @staticmethod
    def load(section):
        author = section.get("author") or ""
        if not author.strip():
            raise ValueError(
                f"Invalid commit.author value '{section.get('author')}'. "
                f"It should be a non-empty string."
            )

        return Commit(**section)

    def __eq__(self, other):
        return self.author == other.author and self.author == other.author
