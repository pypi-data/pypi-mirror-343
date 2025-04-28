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

Use the AI fallback in your tests (either with variable name or resolved variable):

```robotframework
*** Test Cases ***
Login Test
    Open Browser    https://example.com    chrome
    # Both syntaxes work in version 3.1.0+
    AI Fallback Locator    Input Text    USERNAME_FIELD    myusername
    # OR directly use the resolved variable
    AI Fallback Locator    Input Text    ${USERNAME_FIELD}    myusername
    Close Browser
```

You can also use custom keywords with fallback:

```robotframework
*** Keywords ***
Wait And Input Text
    [Arguments]    ${locator}    ${text}    ${timeout}=10
    [Documentation]    Input text with AI fallback if the primary locator fails
    ${status}    ${error}=    Run Keyword And Ignore Error    Input Text    ${locator}    ${text}
    Run Keyword If    '${status}' == 'FAIL'    AI Fallback Locator    Input Text    ${locator}    ${text}
```

## API Key Setup

Store your OpenAI API key in a .env file or provide it when initializing the library:

```robotframework
*** Settings ***
Library    DomRetryLibrary    api_key=${OPENAI_API_KEY}
```

## License

MIT 