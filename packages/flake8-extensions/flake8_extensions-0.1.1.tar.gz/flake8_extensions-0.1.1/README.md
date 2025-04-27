# Flake8 Absolute Imports Plugin

A Flake8 plugin that enforces absolute imports in Python projects.

## Installation

```bash
pip install flake8-absolute-imports
```

## Usage

Add to your flake8 configuration (e.g. `.flake8`):

```ini
[flake8]
plugins = flake8-absolute-imports
select = IA
```

## Error Codes

| Code | Description |
|------|-------------|
| IA001 | Relative imports are not allowed |

## Example

Bad:
```python
from ..utils import helper  # IA001
from .models import User   # IA001
```

Good:
```python
from my_project.utils import helper
from my_project.models import User
```

## Development

Install development dependencies:
```bash
pip install -e .[dev]
```

Run tests:
```bash
pytest
```

Run flake8 with the plugin:
```bash
flake8 your_file.py
```

## License

MIT