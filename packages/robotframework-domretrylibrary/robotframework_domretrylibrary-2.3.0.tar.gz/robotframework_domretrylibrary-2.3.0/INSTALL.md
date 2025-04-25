# Installing DomRetryLibrary

## Installation from PyPI

The simplest way to install the latest version of DomRetryLibrary is from PyPI:

```bash
pip install robotframework-domretrylibrary
```

## Installation from Source

If you want to install from the source:

1. Clone the repository
2. Run the setup script:

```bash
python setup.py install
```

## Usage in Robot Framework Tests

Import the library in your Robot Framework test file:

```robotframework
# Simple direct import
Library    DomRetryLibrary
```

## Example Setup with OpenAI API Key

```robotframework
*** Settings ***
Library    SeleniumLibrary
Library    DomRetryLibrary    api_key=${OPENAI_API_KEY}

*** Variables ***
${OPENAI_API_KEY}      your_api_key_here
${USERNAME_FIELD}      id:non-existent-username-field
${AI_USERNAME_FIELD}   the username input field with placeholder 'Username'

*** Test Cases ***
Login Test
    Open Browser    https://example.com    chrome
    AI Fallback Locator    Input Text    USERNAME_FIELD    myusername
    Close Browser
```

## Troubleshooting

If you encounter any issues with the library, make sure you have installed the latest version:

```bash
pip install --upgrade robotframework-domretrylibrary
```

For more detailed documentation, see the README.md file. 