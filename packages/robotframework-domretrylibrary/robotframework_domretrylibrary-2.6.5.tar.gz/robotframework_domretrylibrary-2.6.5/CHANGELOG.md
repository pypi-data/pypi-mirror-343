# Changelog

All notable changes to the DomRetryLibrary will be documented in this file.

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