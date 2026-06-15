# Changelog

<!--
## \[Version\] - YYYY-MM-DD
### Added
### Changed
### Deprecated
### Fixed
### Removed
-->

## \[1.5.4\] - 2026-06-15

### Changed
- Node name, source and target types are now saved as `VARCHAR`.

### Fixed
- Fill `None` values with empty string when writing to file.

## \[1.5.3\] - 2024-09-26

### Fixed
- Import for test module.

## \[1.5.2\] - 2024-08-28

### Fixed
- Version import for Python 3.8 and above.

## \[1.5.1\] - 2024-08-27

### Added
- Support for PEP 621.

## \[1.5\] - 2024-08-21

### Added
- New parameter `weighted` to reader function.

## \[1.4\] - 2024-08-19

### Added
- Read and write support to file objects and buffers.

## \[1.3.4\] - 2024-08-14

### Added
- Documentation for Sphinx.

## \[1.3.3\] - 2024-06-09

### Added
- Library version as import.

### Removed
- Abstract init method.

## \[1.3.2\] - 2024-02-16

### Fixed
- Predefined node attribute load.

## \[1.3.1\] - 2024-02-16

### Fixed
- Unattributed nodes and edges not being added to graph.

## \[1.3\] - 2024-02-16

### Added
- Missing "LONG" entry to dictionary mapping of types.
- Condition check for INT/LONG and FLOAT/DOUBLE types on write.

### Fixed
- Node order not being preserved on load.

### Removed
- Previous code for node ID type conversion.

## \[1.2\] - 2024-02-15

### Added
- Implemented node ID format type detection.

### Changed
- Automatically assign weights to edges in non-multigraphs.

### Fixed
- Edge direction not being stored on file write.

## \[1.1\] - 2024-08-06

### Added
- Support for double and single quotes as delimiters.
- Support for files without specific attribute types.

### Changed
- Specifies attribute as `DOUBLE` when writing `float` values to file.
- Specifies attribute as `INT` when writing `int` values with null values to file.

## \[1.0\] - 2023-08-06

- First release.
