# Robot Framework DomRetryLibrary

A Robot Framework library with AI-powered fallback for locator variables, enhancing test reliability by using OpenAI to dynamically generate element locators when primary locators fail.

## Installation

Install the library using pip:

```bash
pip install robotframework-domretrylibrary
```

## Usage

Import the library in your Robot Framework test file:

```robotframework
*** Settings ***
Library           SeleniumLibrary
Library           DomRetryLibrary
```

Define your locators and AI fallback descriptions:

```robotframework
*** Variables ***
${USERNAME_FIELD}      css=#username_id
${AI_USERNAME_FIELD}   the username input field
```

Use the AI fallback in your tests:

```robotframework
*** Test Cases ***
Login Test
    Open Browser    https://example.com    chrome
    AI Fallback Locator    Input Text    USERNAME_FIELD    myusername
    Close Browser
```

## API Key Setup

Store your OpenAI API key in a .env file or provide it when initializing the library:

```robotframework
*** Settings ***
Library    DomRetryLibrary    api_key=${OPENAI_API_KEY}
```

## License

MIT 