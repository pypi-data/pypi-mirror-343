import sys
import logging
from .git_handler import GitHandler
from .stackspot_service import StackspotService

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class CommitTool:
    def __init__(self, git_handler: GitHandler, stackspot_service: StackspotService):
        """Initializes the CommitTool with GitHandler and StackspotService.

        Args:
            git_handler (GitHandler): The handler responsible for interacting with Git.
            stackspot_service (StackspotService): The service responsible for generating commit messages using Stackspot AI.
        """
        self.git_handler = git_handler
        self.stackspot_service = stackspot_service

    def auto_commit(self) -> None:
        """Performs the automatic commit process.

        This method:
        1. Fetches the unstaged changes (diff) in the repository.
        2. Uses Stackspot AI to generate a commit message based on the changes.
        3. Commits and pushes the changes with the generated commit message.
        
        If there are no changes or the commit message cannot be generated, the process will stop with an error message.
        """
        
        # Get the unstaged changes (diff)
        diff = self.git_handler.get_diff()
        
        if not diff:
            logger.error("No changes to commit.")
            sys.exit(1)

        # Generate the commit message using Stackspot AI
        message = self.stackspot_service.generate_commit_message(diff)
        
        if not message:
            logger.error("Could not generate commit message.")
            sys.exit(1)

        # Commit and push the changes
        self.git_handler.commit(message)
        logger.info("Commit and push successful.")
