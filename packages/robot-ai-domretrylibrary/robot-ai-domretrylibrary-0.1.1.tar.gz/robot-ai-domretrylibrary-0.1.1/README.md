# Robot Framework AI DomRetryLibrary

A Robot Framework library that provides an AI-powered fallback mechanism for locator variables. This library enhances test reliability by using OpenAI to dynamically generate element locators when the primary locators fail.

## Features

- Automatic fallback to AI-generated locators when primary locators fail
- Seamless integration with existing Robot Framework tests
- Support for both variable names and values
- Detailed logging and comparison of primary vs. AI locators
- Uses OpenAI's GPT models to generate precise locators based on natural language descriptions

## Installation

Install the library using pip:

```bash
pip install robot-ai-domretrylibrary
```

## Usage

### Import the Library

Import the library in your Robot Framework test file:

```robotframework
*** Settings ***
Library    SeleniumLibrary
Library    DomRetryLibrary    api_key=${OPENAI_API_KEY}
```

### Define Your Locators

Define your primary locators and AI fallback descriptions:

```robotframework
*** Variables ***
${USERNAME_FIELD}      css=#username
${AI_USERNAME_FIELD}   the username input field with placeholder 'Username'

${PASSWORD_FIELD}      css=#password
${AI_PASSWORD_FIELD}   the password input field with type 'password'

${LOGIN_BUTTON}        css=#login_button
${AI_LOGIN_BUTTON}     the login button with text 'Sign In' or 'Login'
```

### Use AI Fallback in Your Tests

Use the `AI Fallback Locator` keyword to add AI fallback to any locator-based keyword:

```robotframework
*** Test Cases ***
Login Test
    Open Browser    https://example.com    chrome
    AI Fallback Locator    Input Text    USERNAME_FIELD    myusername
    AI Fallback Locator    Input Text    PASSWORD_FIELD    mypassword
    AI Fallback Locator    Click Element    LOGIN_BUTTON
    Close Browser
```

## API Key Setup

You can provide the OpenAI API key in several ways:

1. When initializing the library:
   ```robotframework
   Library    DomRetryLibrary    api_key=${OPENAI_API_KEY}
   ```

2. Using an environment variable:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

3. Using a .env file in your project:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Advanced Configuration

You can configure additional options when initializing the library:

```robotframework
Library    DomRetryLibrary    
...    api_key=${OPENAI_API_KEY}    
...    model=gpt-4o    
...    openai_api_url=https://api.openai.com/v1/chat/completions    
...    locator_storage_file=my_locators.json
```

## How It Works

The library works as follows:

1. First attempts to use the primary locator (e.g., `${USERNAME_FIELD}`)
2. If the primary locator fails, it looks for an AI description variable with the same name but prefixed with `AI_` (e.g., `${AI_USERNAME_FIELD}`)
3. It uses the description to ask OpenAI to generate a new locator based on the current page HTML
4. Retries the action with the AI-generated locator
5. Stores successful AI fallbacks in a JSON file for reference

## Examples

### Basic Usage

```robotframework
*** Settings ***
Library           SeleniumLibrary
Library           DomRetryLibrary

*** Variables ***
${USERNAME_FIELD}     css=#non_existent_username_id
${AI_USERNAME_FIELD}  the username input field with placeholder 'Username'

*** Test Cases ***
Login Test
    Open Browser    https://example.com    chrome
    AI Fallback Locator    Input Text    USERNAME_FIELD    myusername
    Close Browser
```

## License

MIT License

## Author

Kristijan Plaushku (info@plaushkusolutions.com) 