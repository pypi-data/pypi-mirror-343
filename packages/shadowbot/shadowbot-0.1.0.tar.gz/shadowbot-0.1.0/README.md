# RPA Assistant

RPA Assistant Client Configuration Tool, integrated with Streamlinet Server, provides a complete set of RPA management service applications.

## Installation

You can install this package using pip:
```cmd
pip install shadow_bot
```

## Usage

```python
import xbot
from .import package
from shadow_bot import SBA, service_init

try:
    sba = SBA(xbot, package)
    service_init(sba, init=True)
except Exception as e:
    pytest.fail(f"shadow_bot raised an exception: {e}")
```