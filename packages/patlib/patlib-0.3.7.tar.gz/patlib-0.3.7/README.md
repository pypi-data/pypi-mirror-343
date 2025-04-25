# patlib

Should not be used in production code. Purposes:

- Expanded snippet (or "tips and tricks") library.
- Share tools across my projects, such as DAPPER.
- Provide common, version-controlled (and versioned) source
  of dependency specifications for various projects.
  NB: Not sure if good idea.
  Maybe you forget numpy when publishing a "dependant" project.

  Example:
  ```toml
  [tool.poetry.dev-dependencies]
  # Either:
  patlib = {version = "==0.2.8", extras = ["mydev", "misc"]}
  # Or:
  patlib = {path = "../../py/patlib", extras = ["mydev", "misc"], develop=true}
  ```

  Also note that `pip>=21.3` supports editable installs,
  but this also requires that you have a recent `poetry` installed on your system.
