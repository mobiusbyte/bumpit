from dataclasses import dataclass


@dataclass
class SemVer:
    major: int
    minor: int
    patch: int
    pre_release: str
    build_metadata: str

    def __str__(self):
        as_str = f"{self.major}.{self.minor}.{self.patch}"

        if self.pre_release:
            as_str += f"-{self.pre_release}"

        if self.build_metadata:
            as_str += f"+{self.build_metadata}"

        return as_str
