# Robot Framework AIRetrySmartLocator

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
Library           AIRetrySmartLocator
```

Define your locators and AI fallback descriptions:

```robotframework
*** Variables ***
${USERNAME_FIELD}      css=#non_existent_username_id
${AI_USERNAME_FIELD}   the username input field with placeholder 'Username'
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

Store your OpenAI API key in a .env file in your project directory:

```
OPENAI_API_KEY=your_api_key_here
```

Or provide it when initializing the library:

```robotframework
*** Settings ***
Library    AIRetrySmartLocator    api_key=${OPENAI_API_KEY}
```

## How It Works

1. The library first attempts to use your primary locator
2. If the primary locator fails, it uses OpenAI to generate a new locator based on your description
3. The AI-generated locator is used as a fallback
4. Successful fallbacks are logged for future reference

## Library Parameters

When importing the library, you can set several parameters:

```robotframework
Library    AIRetrySmartLocator    
...    api_key=${OPENAI_API_KEY}    
...    model=gpt-4o    
...    locator_storage_file=my_locators.json
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| api_key | None | OpenAI API key (falls back to environment variable) |
| model | gpt-4o | OpenAI model to use |
| locator_storage_file | locator_comparison.json | File to store successful AI locators |

## Keywords

The library provides the following keywords:

- `AI Fallback Locator` - Add AI fallback to any locator-based keyword

## License

MIT 