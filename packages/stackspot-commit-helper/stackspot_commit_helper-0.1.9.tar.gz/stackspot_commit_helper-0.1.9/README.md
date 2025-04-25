# Stackspot Commit Helper

## Overview

The **Stackspot Commit Helper** is a Python tool that automates Git commit message generation using Stackspot AI. It analyzes your code changes and creates meaningful commit messages while handling the commit and push operations seamlessly.

## Features

- 🤖 **AI-Powered Commit Messages**: Generates contextual commit messages based on your code changes
- 🔄 **Automated Git Workflow**: Handles staging, commit and push operations
- 🔢 **Branch Number Integration**: Optional inclusion of branch numbers in commit messages
- ⚡ **Simple CLI Interface**: Easy to use command-line tool
- 🔐 **Secure Configuration**: Environment variable based configuration

## Stackspot Credentials
To use Stackspot's AI for commit message generation, you must set up credentials with the Stackspot Platform.

1. Create an account at Stackspot Platform.
2. Go to Stackspot AI.
3. Access Profile → Access Token.
4. Create new credentials and copy the following:

    **Client ID**

    **Client Secret**
    
    **Realm**

## Installation

Install using pip:

```bash
pip install stackspot-commit-helper
```

After installation, set the following environment variables to configure the tool based on your system::

```bash
STACKSPOT_CLIENT_ID="your_client_id"
STACKSPOT_CLIENT_SECRET="your_client_secret"
STACKSPOT_REALM="your_realm"
QUICK_COMMAND_COMMIT="your_quick_command_name"  # Optional: if your account has the 'generate-git-commit-message' command
```

## Usage
Once the tool is installed and configured, you can use it from the terminal:

**Commit and Push**
To run the tool and generate a commit message based on the code changes:

```bash
scommit
```

**Include Branch Number**
If you want to include the current branch number in your commit message, you can use the -b or --branch option:

```bash
scommit -b
```
This will prepend the branch number (if available) to the generated commit message, like [#123] - <commit_message>.


## Dependencies

**This tool requires the following Python packages:**

python-dotenv
– For loading environment variables from a .env file.

stackspot
– For interacting with Stackspot's AI services.


## Troubleshooting

**No Changes to Commit**

If the tool reports "No changes to commit", it means that there are no unstaged changes in your Git repository. Ensure that you have made changes before running the command.

**Stackspot API Error**

If there is an issue with the Stackspot API (e.g., invalid credentials or a failed execution), you will receive an error message. Make sure your Stackspot credentials are correct and try again.

## Contributing
Contributions are welcome! If you find a bug or have a feature request, feel free to open an issue or submit a pull request.
