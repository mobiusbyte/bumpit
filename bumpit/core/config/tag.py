from dataclasses import dataclass


@dataclass
class Tag:
    apply: bool
    format: str

    @staticmethod
    def load(section):
        apply = section.get("apply", "")
        if not (apply is True or apply is False):
            raise ValueError(
                f"Invalid tag.apply value '{section.get('apply')}'. It should be a bool."
            )

        try:
            tag = Tag(**section)
        except TypeError as e:
            raise ValueError(f"Missing tag field(s). {e}")

        if "{version}" not in tag.format:
            raise ValueError("Tag format must include '{version}' token.")

        return tag

    def __eq__(self, other):
        return self.apply == other.apply and self.format == other.format
