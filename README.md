# Core Library
## docs
[https://civic-api-core.gaytomycode.com](https://civic-api-core.gaytomycode.com)

## Install
### Commandline
```bash
$ pip install git+ssh://git@github.com/gaytomycode/civic-api-core
```
### requirements.txt
```txt
civic-core @ git+ssh://git@github.com/gaytomycode/civic-api-core
```

## Usage

```python3
import civic_core
```

## Scructure
CIVIC Backend is a micro-service architecture containing:
* identity: Managing JWT tokens and sessions.
* mayor:
* scrap:

## Modules
* config: Has the settings.
* crud_base: The base crud class.
* deps: Router dependances.
* exceptions: Exceptions that result in http response.
* helpers: Utility functions.
* models_base: The base sqlachemy model class.
* schemas_base: Pydantic base that supports property.
