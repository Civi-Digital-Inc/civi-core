# Core Library
## docs
[https://civi-core.gaytomycode.com](https://civi-core.gaytomycode.com)

## Install
### Commandline
```bash
$ pip install git+ssh://git@github.com/gaytomycode/civi-core
```
### requirements.txt
```txt
civi-core @ git+ssh://git@github.com/gaytomycode/civi-core
```

## Usage

```python3
import civi_core
```

## Scructure
CIVI Backend is a micro-service architecture containing:
* identity: Managing JWT tokens and sessions.
* table:
* scrap:

## Modules
* config: Has the settings.
* crud_base: The base crud class.
* deps: Router dependances.
* exceptions: Exceptions that result in http response.
* helpers: Utility functions.
* models_base: The base sqlachemy model class.
* schemas_base: Pydantic base that supports property.
* choices:
