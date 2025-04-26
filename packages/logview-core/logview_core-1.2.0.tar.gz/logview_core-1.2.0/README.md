### LogView is a local log manager for your application

## Installation :
Install LogView via pip:

```sh
pip install logview_core
```

## Import :
```sh
from logview_core import LogViewHandler
```

## Use Example :
```sh
from logview_core import LogViewHandler
import logger

handler = LogViewHandler(source_token="...",host="...")
logger = logging.getLogger("TEST")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.info("hello")
```