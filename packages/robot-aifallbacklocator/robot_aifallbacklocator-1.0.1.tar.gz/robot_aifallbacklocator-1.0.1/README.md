# Robot Framework AI Fallback Locator

An AI-powered library for Robot Framework that dynamically generates robust element locators when primary locators fail, making your tests more reliable on complex web applications.

## Installation

Install the library using pip:

```bash
pip install robot-aifallbacklocator
```

## Key Features

- **ID-First Approach**: Prioritizes unique element identifiers for maximum robustness
- **AI-Powered Fallback**: Uses OpenAI to intelligently locate elements when standard selectors fail
- **Modern Web App Ready**: Handles complex DOM structures with nested elements effectively
- **Smart Path Handling**: Automatically uses the most reliable XPath patterns for your application
- **Simple Integration**: Works seamlessly with existing Robot Framework tests

## Usage

Import the library in your Robot Framework test file:

```robotframework
*** Settings ***
Library           SeleniumLibrary
Library           AIFallbackLocator    api_key=${OPENAI_API_KEY}
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

## How The Selectors Work

The AI Fallback Locator uses a prioritized approach to find elements:

1. **ID-First**: If an element has an ID, use it directly: `//*[@id='login-button']`
2. **Test Attributes**: Look for testing-specific attributes: `//*[@data-test='username']`
3. **Form Attributes**: For inputs, use name/placeholder: `//*[@placeholder='Enter username']`
4. **Meaningful Classes**: Only if needed: `//*[contains(@class, 'login-button')]`

This approach is much more reliable than complex hierarchical selectors and works even in deeply nested DOM structures with forms and dynamic elements.

## API Key Setup

Store your OpenAI API key in a .env file or provide it when initializing the library:

```robotframework
*** Settings ***
Library    AIFallbackLocator    api_key=${OPENAI_API_KEY}
```

## License

MIT 