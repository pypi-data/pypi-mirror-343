import os
from dotenv import load_dotenv
from .models import StackspotConfig

def load_stackspot_config() -> StackspotConfig:
    load_dotenv()
    return StackspotConfig(
        client_id=os.getenv("STACKSPOT_CLIENT_ID"),
        client_secret=os.getenv("STACKSPOT_CLIENT_SECRET"),
        realm=os.getenv("STACKSPOT_REALM"),
        quick_command=os.getenv("QUICK_COMMAND_COMMIT", 'generate-git-commit-message')
    )