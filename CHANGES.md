## Releases

#### 1.0.0

- First release.

#### 1.0.1

- Typo fixes and other minor changes.

#### 1.1.0

- README improvements.

#### 1.2.0

- Added support for relevant read-only dict behaviors.

- Added docstrings.

#### 1.2.6

- README improvements.

#### 1.3.0

- Changed signature to `cons(_clsname, **kwargs)` to avoid conflict when a
  user's kwargs needs `name` as a key.

#### 2.0.0

- Switched from attrs to dataclass.

- Dropped support for Pythons earlier than 3.7.

- Reworked the API to prioritize convenience: `cons()` and `enumcons()` offer
  default behavior as easily as possible; and `constants()` allows the user to
  control the name of the underlying dataclass (a required parameter in v1) or
  to supply a callable to compute each value from its name (similar behavior
  was in v1).

#### 2.1.0

- Enhanced `constants()` to support the creation of non-frozen
  dataclass instances.

- Added `dc()` to support the creation of quick-and-dirty dataclasses.

