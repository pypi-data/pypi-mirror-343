# Changelog

All notable changes to the DomRetryLibrary will be documented in this file.

## [2.7.2] - 2024-07-05

### Fixed
- Improved handling of element descriptions to avoid confusion between similar elements
- Added unique hashing to cache keys to prevent description mix-ups
- Enhanced AI prompts to focus specifically on the exact element description
- Fixed issues with fallback mechanism getting the wrong element
- Added navigation elements as separate chunks for better processing
- Added more detailed logging to track AI description resolution
- Added new `clear_transformation_cache` keyword to force fresh AI lookups

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