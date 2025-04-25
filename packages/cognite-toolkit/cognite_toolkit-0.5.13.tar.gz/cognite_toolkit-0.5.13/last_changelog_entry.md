## cdf 

### Changed

- Currently the `--host=` option value is ignored if it does not
case-sensitively match a value in the `REPOSITORY_HOSTING` array. This
change makes the matching case-insensitive and falls back to the "Other"
repository hosting option if no match is found.

## templates

No changes.