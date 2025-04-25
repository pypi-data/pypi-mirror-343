import sys
import logging
from stackspot import Stackspot
from .models import StackspotConfig
from .commit_generator import CommitGenerator  

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class StackspotService:
    def __init__(self, config: StackspotConfig):
        self.config = config
        self._setup_stackspot()
        self.commit_gen = CommitGenerator() 

    def _setup_stackspot(self) -> None:
        Stackspot.instance().config({
            'client_id': self.config.client_id,
            'client_secret': self.config.client_secret,
            'realm': self.config.realm,
        })
        logger.info("Stackspot instance successfully configured.")

    def generate_commit_message(self, diff: str) -> str:
        try:

            execution_id = Stackspot.instance().ai.quick_command.create_execution(
                self.config.quick_command,
                diff
            )
      
            previous_status = None

            def on_callback_response(e):
                nonlocal previous_status
                current_status = e['progress']['status']
                if current_status != previous_status:

                    previous_status = current_status

                    logger.info(f"🔄 Execution quick command status: {current_status}")

            execution = Stackspot.instance().ai.quick_command.poll_execution(
                execution_id,
                { 
                    'delay': 0.5, 
                    'on_callback_response': on_callback_response
                }
            )
            
            if execution['progress']['status'] == 'FAILED':
                error_message = execution['progress'].get('error', 'Unknown error')
                logger.error(f"Execution failed: {error_message}")
                raise Exception(f"Execution failed: {error_message}")
            
            logger.info(f"✅ Execution successful")
            if len(execution.get("steps", [])) == 1:
                answer = execution["steps"][0]["step_result"]["answer"]
            else:
                answer = self.commit_gen.extract_code_block(execution["result"]) 
                
            return answer 
        except Exception as e:
            logger.error(f"StackSpot API error: {e}")
            sys.exit(1)
