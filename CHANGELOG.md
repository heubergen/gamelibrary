# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0] - 2022-08-14
### Added
- Add different style for long tables on mobile/tablet

### Changed
- Fix Remove wishlist button wrong width  
- Move error messages to above table for wish- and playlist
- Move css to correct path

### Removed
- Icon due to license issues 

## [1.4.0] - 2022-08-13
### Added
- Add purchase price to form and table
- Add calculated columns Cost Per Hour and X Rating to Table
- Add genre to wishlist table
- Raise exceptions if run in debug mode instead of showing error message

### Changed
- Use best practice and switch to explicit db connections
- Move creating tables to models.py

### Removed
- Unused file query.py

## [1.3.0] - 2022-08-10
### Changed
- Use function to get data from database and use connection_context

## [1.2.1] - 2022-08-10
### Changed
- Use connection_context fo creating/checking tables

## [1.2.0] - 2022-08-10
### Added
- Add CHANGELOG.md file
- Add upload feature to import
- Add CSRF protection to all forms

### Changed
- Use Flask-WTF for all forms
- Add CSRF protection to all forms
- Use correct validation
- Fix forms not cleared after submission

### Removed
- Remove SQLAlchemy usage
- Removed support to import file from disk
 
## [1.1.0] - 2022-08-07
### Added
- Add venv support

## [1.0.0] - 2022-08-05
- Initial version
