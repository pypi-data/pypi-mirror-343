## Release v0.1.8 - TBD

### Added

- Added test to check number of datapoints correctness in output file
- Added test to check that `JobsAPI._get_job_data` does not generate more data than the job allows
- Added `JobsAPI.status`

### Changed

- Updated data fetching logic in `JobsAPI.generate_data`
- Updated `tests` folder layout
- Renamed `CreditModel` to `CreditResponseModel`
- Updated `test_generate_data_check_number_of_samples` to allow for `JobsAPI.generate_data` to generate more datapoints than
  are requested
- Modified return type of `JobsAPI.generate_data` from `SuccessResponse` to `ActionResult`
- Merged `handle_validation_errors` and `auto_validate_methods` into a single decorator
- Updated `README.md`

### Fixed

- Fixed bug causing some tests to delete the `.env` file

## Release v0.1.7 - April 13, 2025

### Fixed

- Fixed bug causing Pydantic to `raise ImportError('email-validator is not installed)`
- Fixed bug causing `JobsAPI.generate_data()` to crash when parameter `output_path` contains a file name but not a path
- Fixed bug causing `JobsAPI.generate_data()` to generate an incorrect number of datapoints

### Changed

- Updated `JobOutputType` and `JobOutputSchemaDefinition`

### Added

- Added `JobOutputFieldDatatype`