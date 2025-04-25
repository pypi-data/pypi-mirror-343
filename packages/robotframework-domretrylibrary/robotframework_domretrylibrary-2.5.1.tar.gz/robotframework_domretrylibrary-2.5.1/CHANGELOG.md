# Changelog

All notable changes to the DomRetryLibrary will be documented in this file.

## [2.5.1] - 2024-05-25

### Fixed
- Fixed JavaScript compatibility issues that caused errors with private fields syntax
- Improved error messages for missing AI descriptions with clear guidance on how to fix
- Enhanced JavaScript fallback mechanisms with more robust retry strategies

## [2.5.0] - 2024-05-25

### Added
- Enhanced AI processor with multi-strategy locator generation
- Smart transformation caching system to remember successful locator transformations
- New parameter `transformation_cache_file` to configure the cache location
- Intelligent use of original locator as context for better alternatives
- Element type classification for more targeted locators
- Improved HTML preprocessing focusing on relevant page sections
- Page URL capture for additional context in locator generation

### Fixed
- More robust handling of elements in shadow DOM and iframes
- Improved handling of elements that are not immediately interactable
- Better fallback mechanisms when API calls fail

## [2.4.0] - 2024-04-10

### Added
- Backward compatibility for existing test patterns
- Support for handling empty locators by inferring from context
- Ability to find any matching AI_ variable if none is explicitly specified
- Graceful continuation of execution when no description is found

## [2.3.0] - 2024-03-15

### Added
- Direct AI descriptions with the `ai_description` parameter
- Support for inline descriptions without needing AI_ variables
- Improved error handling with better diagnostics

## [2.1.0] - 2024-02-01

### Added
- Initial public release
- Basic AI fallback mechanism with OpenAI integration
- Support for variable-based locator descriptions
- Locator comparison storage 