from dataclasses import dataclass

@dataclass
class StackspotConfig:
    client_id: str
    client_secret: str
    realm: str
    quick_command: str = 'generate-git-commit-message'