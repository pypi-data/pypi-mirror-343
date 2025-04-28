# Changelog

All notable changes to the AI Fallback Locator will be documented in this file.

## [1.0.4] - 2024-08-30

### Fixed
- Fixed issue with locator_storage_file being None causing TypeError
- Added default value for locator_storage_file parameter in AIFallbackLocator class
- Resolved error: "stat: path should be string, bytes, os.PathLike or integer, not NoneType"

## [1.0.3] - 2024-08-30

### Enhanced
- Added support for loading OpenAI API configuration from .env file
- Improved flexibility by allowing environment variables for API key, URL, and model
- Simplified configuration by removing the need to pass API key in Robot test files
- Made it easier to switch between different OpenAI models and endpoints
- Users can now create a .env file with OPENAI_API_KEY, OPENAI_API_URL, and OPENAI_MODEL settings

## [1.0.2] - 2023-12-19

### Fixed
- Fixed import issues with Robot Framework when using `Library    AIFallbackLocator`
- Added proper class inheritance for better compatibility with Robot Framework's import system
- Improved module structure for direct class loading

## [1.0.1] - 2023-12-19

### Enhanced
- Added support for importing the library as `AIFallbackLocator`
- Users can now simply use `Library     AIFallbackLocator    api_key=${OPENAI_API_KEY}` in their Robot Framework test files
- Fixed backward compatibility issues with existing test code

## [1.0.0] - 2023-12-19

### First Release
- Initial release of AI Fallback Locator, a rebranded and cleaned-up version of DomRetryLibrary
- Using the ID-First approach for maximum robustness
- Prioritizes unique element identifiers (id, data-*, aria-*)
- Avoids complex hierarchical selectors
- Enhanced AI-powered element selection
- Smart path separator handling that preserves attribute expressions
- Intuitive API for Robot Framework integration

## [4.0.1] - 2023-12-19

### Fixed
- **Critical Fix**: Added a robust post-processing mechanism to forcibly convert any direct path separators (`/`) to indirect ones (`//`) in XPath expressions
- Implemented a smart path separator converter that preserves attribute expressions while ensuring maximum robustness
- Fixed issue where generated selectors were still failing due to direct path relationships in complex DOM structures
- Added comprehensive logging to show XPath transformations for better debugging
- This fix guarantees that even if the AI model generates direct paths, they will be automatically converted to indirect ones

## [4.0.0] - 2023-12-19

### Major Changes
- **Complete redesign of XPath generation strategy** with a focus on maximum robustness
- New ID-First approach that prioritizes direct element selection via unique attributes:
  - Prioritizes element IDs as the most reliable selectors
  - Targets test-specific attributes (data-test, data-cy, etc.)
  - Uses direct attribute selectors for form elements (name, placeholder)
  - Falls back to simple class-based selectors when appropriate
- **Eliminated complex hierarchical selectors** that were proving fragile in real-world applications
- Simplified selector algorithm to focus on unique element identifiers
- Optimized for modern web applications with complex, nested DOM structures
- Fixed issues with selectors failing on deeply nested form elements

### Enhanced
- New detailed instructions for the AI model on selecting robust XPath expressions
- Added prioritized rules system for selector creation
- Improved examples for what constitutes good vs. bad selectors

## [3.3.0] - 2023-12-19

### Enhanced
- **Critical Improvement**: Enforced mandatory use of `//` between ALL elements in XPath selectors
- Completely revised XPath generation rules to handle deeply nested DOM structures
- Added detailed examples showing incorrect and correct path separator usage
- Fixed issues with locators failing due to complex nested form structures
- Addressed the specific case where locators would fail when elements are nested inside forms or other containers
- Enhanced prompts to strongly enforce the rule: "ALWAYS use '//' between ALL elements in XPath"

## [3.2.1] - 2023-12-19

### Enhanced
- Improved XPath generation by prioritizing robustness over strict hierarchical matching:
  - Now preferring `//` (indirect path) over `/` (direct path) in most cases to handle dynamic DOM structures
  - Using `//` to better handle cases where there might be intermediate elements in the DOM
  - Only using `/` when 100% certain the parent-child relationship is direct

## [3.2.0] - 2023-12-19

### Enhanced
- Added important rule for XPath generation regarding path separators:
  - Use `/` for immediate child elements (direct parent-child relationship)
  - Use `//` for elements at any depth (can be nested deeper in the hierarchy)
- This improves the accuracy and reliability of generated XPath selectors

## [3.1.0] - 2023-12-19

### Enhanced
- Added ability to properly handle locators when passed as resolved variables `${VARIABLE}` instead of just variable names `VARIABLE`
- Improved AI variable lookup system for element descriptions
- Fixed "Empty primary locator provided" warning when using already resolved variables

### How to use
Now both syntaxes work correctly in keywords:
```robot
# Both these syntaxes work correctly
Wait And Input Text    USERNAME_FIELD    ok
Wait And Input Text    ${USERNAME_FIELD}    ok
```

This change is backward compatible with all previous versions.

## [3.0.0] - 2024-08-14

### Changed
- Updated the OpenAI model from GPT-4o to GPT-4.1 for improved locator generation
- Major version bump to reflect the significant model change
- Enhanced AI processing capabilities with the newer model

## [2.9.0] - 2024-08-07

### Enhanced
- Added automatic whitespace normalization to text conditions in generated XPath locators
- Applied normalize-space() function to all text() comparisons for better text matching
- Added normalize-space() to contains() text functions for more reliable whitespace handling
- Improved resistance to extra spaces, newlines, and tabs in text matching
- Added detailed logging when normalize-space() is applied to XPath expressions
- Enhanced robustness of text-based locators with standardized space handling

## [2.8.0] - 2024-08-07

### Enhanced
- Enhanced XPath generation to include 2-3 levels of parent elements for more robust locators
- Improved element context by creating deeper hierarchical XPath expressions
- Added parent element levels count to logging for better visibility
- Added automatic detection of parent levels in generated XPaths
- Enhanced AI prompts to explicitly request inclusion of parent elements in locators
- Improved stability of locators by providing more DOM context

## [2.7.4] - 2024-07-22

### Fixed
- Fixed AI description matching for identical format direct locators (e.g., multiple 'xpath=non_existent_analyze' with different purposes)
- Improved variable reference mapping to ensure each locator gets its correct AI description

## [2.7.3] - 2024-07-22

### Fixed
- Fixed issue with AI Fallback Locator not working with direct locators (e.g. 'xpath=non_existent')
- Added variable reference matching for fallback locator handling

## [2.7.2] - 2024-07-05

### Fixed
- Improved handling of element descriptions to avoid confusion between similar elements
- Added unique hashing to cache keys to prevent description mix-ups
- Enhanced AI prompts to focus specifically on the exact element description
- Fixed issues with fallback mechanism getting the wrong element
- Added navigation elements as separate chunks for better processing
- Added more detailed logging to track AI description resolution
- Added new `clear_transformation_cache` keyword to force fresh AI lookups
- Enhanced compatibility with Microsoft Edge browser
- Fixed JavaScript compatibility issues with Edge's security model
- Improved robustness of element interaction

## [2.7.1] - 2024-07-04

### Changed
- Modified to generate raw XPath locators without the 'xpath=' prefix
- Updated AI prompts to explicitly request XPath expressions without prefixes
- Improved XPath format checking to ensure consistent XPath syntax
- Enhanced selector handling to strip prefixes from original locators for context
- Added extra validation to ensure XPath expressions start with / or //

## [2.7.0] - 2024-07-04

### Enhanced
- Added detailed rules for CSS and XPath selector validation in AI prompts
- Improved selector generation by providing explicit validation steps to AI
- Added specific guidelines for proper quotes, brackets, and attribute syntax
- Enhanced user messaging with step-by-step validation instructions
- Refined instructions for handling special characters and escaping

## [2.6.9] - 2024-07-03

### Added
- Enhanced HTML processing with intelligent chunking for large pages
- Added multi-chunk processing to handle very large HTML documents
- Implemented smart section extraction to focus on important content
- Added chunking information to AI prompts for better context
- Improved condensed HTML fallback approach for complex pages

## [2.6.8] - 2024-07-03

### Changed
- Removed selector validation to simplify code
- Focused on direct raw locator generation from AI
- Improved prompt for clearer guidance to AI
- Enhanced handling of markdown formatting in responses
- Simplified fallback mechanism

## [2.6.6] - 2024-07-03

### Fixed
- Added robust selector validation to prevent "InvalidSelectorException" errors
- Improved selector cleaning and normalization
- Enhanced fallback handling for invalid selectors
- Updated prompt to explicitly request valid CSS/XPath selectors
- Fixed handling of code block formatting in AI responses

## [2.6.5] - 2024-07-02

### Changed
- Significantly simplified AI processor implementation
- Removed complex multi-strategy locator generation
- Streamlined HTML preprocessing to bare minimum
- Simplified element classification and fallback logic
- Improved performance by reducing complexity

## [2.6.4] - 2024-07-02

### Fixed
- Fixed a caching issue where incorrect locators were reused across different elements
- Improved AI locator generation with element description-specific caching
- Enhanced cache key generation to prevent locator mix-ups
- Added logging improvements for better visibility into the caching process

## [2.6.3] - 2024-07-01

### Changed
- Simplified core functionality by removing browser-specific handling
- Improved code efficiency by removing unnecessary methods and features
- Optimized keyword handling for better performance

## [2.6.2] - 2024-07-01

### Fixed
- Resolved JavaScript compatibility issues with Microsoft Edge browser
- Enhanced browser input text with more robust fallback mechanisms
- Improved click operations with progressive fallback approaches
- Added direct CSS selector approach for problematic Edge scenarios
- Fixed "Private field must be declared in an enclosing class" error in Edge

## 2.7.5 / 2.5.6 (2023-12-19)

### Miglioramenti
- Aggiunta la capacità di gestire correttamente i locator quando vengono passati come variabili risolte `${VARIABLE}` invece che solo come nomi di variabili `VARIABLE`
- Migliorato il sistema di ricerca delle variabili AI per la descrizione degli elementi
- Risolto il problema di avviso "Empty primary locator provided" quando si utilizzano variabili già risolte

### Come utilizzare
Ora è possibile utilizzare entrambe le sintassi nelle keyword:
```robot
# Entrambe queste sintassi funzionano correttamente
Wait And Input Text    USERNAME_FIELD    ok
Wait And Input Text    ${USERNAME_FIELD}    ok
```

Questa modifica è retrocompatibile con tutte le versioni precedenti. 