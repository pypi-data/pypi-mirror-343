# Changelog

All notable changes to the DomRetryLibrary will be documented in this file.

## [2.6.1] - 2024-07-01

### Fixed
- Added support for direct CSS/XPath locators in AI Fallback Locator by finding matching variables in the global scope
- Improved handling of locators provided directly rather than as variable names
- Fixed issue where tests would fail when using `AI Fallback Locator` in custom keywords with direct CSS selectors

## [2.6.0] - 2024-07-01

### Added
- Improved fallback description mechanism with smarter AI variable selection
- Enhanced fallback chain with better cascading logic for finding descriptions
- Optimized performance for variable lookup and description selection
- Reduced overhead for tests with multiple fallback operations

### Changed
- Refactored the `_find_any_matching_ai_variable` method for better efficiency
- Improved error handling with more descriptive messages

## [2.5.5] - 2024-05-25

### Added
- Added browser-specific optimizations for Microsoft Edge and other browsers
- Implemented adaptive interaction strategies based on detected browser type
- New dedicated input and click handlers for different browser engines
- Cross-browser compatible element interaction approaches

### Fixed
- Fixed persistent "InvalidElementStateException" issues with Microsoft Edge
- Enhanced fallback mechanisms for element interactions across different browsers
- Made element interaction more robust in problematic browser contexts

## [2.5.4] - 2024-05-25

### Changed
- Removed specific element type references (username, password, button) from keyword handler
- Implemented generic, element-agnostic matching logic for all interaction types
- Improved variable naming for better code clarity and maintainability
- Made the library more adaptable to different application domains

## [2.5.3] - 2024-05-25

### Fixed
- Completely removed complex interaction handling to solve Microsoft Edge compatibility issues
- Simplified element interaction to a basic direct approach without retries or JavaScript
- Fixed "InvalidElementStateException" issues in Microsoft Edge browser
- Reverted to a simpler interaction model similar to the original working implementation

## [2.5.2] - 2024-05-25

### Changed
- Removed JavaScript fallback mechanisms to avoid compatibility issues with Microsoft Edge
- Simplified element interaction by relying on native Robot Framework/Selenium methods
- Enhanced element interaction now uses standard scrolling and visibility checks

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