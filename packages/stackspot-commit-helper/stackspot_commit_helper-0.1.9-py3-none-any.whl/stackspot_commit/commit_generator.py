import sys
import re

class CommitGenerator:
    def extract_code_block(self, text: str) -> str:
        """Extracts a code block from the given text.

        This method searches for a code block enclosed in triple backticks (```) or a
        single backtick (`) and returns the content inside the code block.

        Args:
            text (str): The input text from which the code block is to be extracted.

        Returns:
            str: The content of the first found code block or inline code.
        
        Raises:
            TypeError: If the input 'text' is not a string.
            ValueError: If no code block or inline code is found.
        """
        try:
            # Ensure the argument is a string
            if not isinstance(text, str):
                raise TypeError("The argument 'text' must be a string.")

            # Search for code block enclosed in triple backticks
            match = re.search(r"```(.*?)```", text, re.DOTALL)
            if match:
                return match.group(1).strip()

            # Search for inline code enclosed in single backticks
            match = re.search(r"`(.*?)`", text)
            if match:
                return match.group(1).strip()

            # If no code block or inline code is found, raise an error
            raise ValueError("No code block or inline code found in the text.")

        except TypeError as e:
            sys.stderr.write(f"[ERROR] Invalid type: {e}\n")
        except AttributeError as e:
            sys.stderr.write(f"[ERROR] Error accessing the code block: {e}\n")
        except ValueError as e:
            sys.stderr.write(f"[WARNING] {e}\n")
        except Exception as e:
            sys.stderr.write(f"[ERROR] Unexpected error in extract_code_block: {e}\n")

        return text
