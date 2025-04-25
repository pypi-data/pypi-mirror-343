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
Library           DomRetryLibrary    # Just use the direct class name
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

## New in Version 2.3.0: Direct AI Descriptions

You can now provide the AI description directly without needing to define an AI_ variable:

```robotframework
AI Fallback Locator    Input Text    css=#username    myusername    ai_description=the username input field
```

This approach is especially useful when you:
- Want to use a dynamic description
- Need to use locators without defining variable pairs
- Prefer inline descriptions for better readability
- Need to quickly test different descriptions

## New in Version 2.4.0: Backward Compatibility for Existing Test Patterns

Version 2.4.0 adds intelligent backward compatibility for existing test patterns. It's now more forgiving and will:

1. **Handle empty locators** by inferring from context
2. **Find any matching AI_ variable** if none is explicitly specified
3. **Continue execution** rather than failing when no description is found

This means your existing test structure will still work:

```robotframework
*** Keywords ***
Wait And Input Text
    [Arguments]    ${locator}    ${text}
    ${status}    ${error}=    Run Keyword And Ignore Error    Input Text    ${locator}    ${text}
    Run Keyword If    '${status}' == 'FAIL'    AI Fallback Locator    Input Text    ${locator}    ${text}
```

And empty locator variables will be handled gracefully:

```robotframework
*** Variables ***
${SUBMIT_BUTTON}    # Empty locator
${AI_SUBMIT_BUTTON}    the login button

*** Test Cases ***
Login Test
    AI Fallback Locator    Click Element    ${SUBMIT_BUTTON}    # Works with empty locator
```

## New in Version 2.5.0: Enhanced AI Processor with Smart Locator Generation

Version 2.5.0 introduces significant improvements to the AI processor component, delivering more precise and reliable locator generation:

1. **Multi-Strategy Locator Generation**
   - Uses three distinct AI strategies to find the best locator
   - Falls back gracefully if one approach fails
   - Provides more reliable element identification

2. **Smart Caching System**
   - Remembers successful locator transformations between runs
   - Recognizes similar locator patterns for faster resolution
   - Continually improves over time as more tests run

3. **Original Locator Context**
   - Intelligently leverages the original locator as context
   - Avoids being misled by misleading element names
   - Creates more precise alternative locators

4. **Enhanced Element Classification**
   - Automatically classifies elements by type (button, input, checkbox, etc.)
   - Tailors locator strategies to specific element types
   - Improves accuracy for different UI components

5. **Intelligent HTML Processing**
   - Focuses on relevant page sections (forms, main content)
   - Removes noise elements for better analysis
   - Prioritizes interactive elements

6. **Element Interaction Improvements**
   - Automatically scrolls elements into view
   - Falls back to JavaScript execution when needed
   - Handles elements in shadow DOM and iframes better

To enable the transformation cache feature, provide a path for the cache file:

```robotframework
*** Settings ***
Library    DomRetryLibrary    
...    transformation_cache_file=my_transforms.json
```

## API Key Setup

Store your OpenAI API key in a .env file in your project directory:

```
OPENAI_API_KEY=your_api_key_here
```

Or provide it when initializing the library:

```robotframework
*** Settings ***
Library    DomRetryLibrary    api_key=${OPENAI_API_KEY}
```

## How It Works

1. The library first attempts to use your primary locator
2. If the primary locator fails, it uses OpenAI to generate a new locator based on your description
3. The AI-generated locator is used as a fallback
4. Successful fallbacks are logged for future reference

## Library Parameters

When importing the library, you can set several parameters:

```robotframework
Library    DomRetryLibrary    
...    api_key=${OPENAI_API_KEY}    
...    model=gpt-4o    
...    locator_storage_file=my_locators.json
...    transformation_cache_file=my_transforms.json
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| api_key | None | OpenAI API key (falls back to environment variable) |
| model | gpt-4o | OpenAI model to use |
| locator_storage_file | locator_comparison.json | File to store successful AI locators |
| transformation_cache_file | ~/.dom_retry_transformation_cache.json | File to store transformation cache data |

## Keywords

The library provides the following keywords:

- `AI Fallback Locator` - Add AI fallback to any locator-based keyword

## License

MIT 