# NFT-Text-Overlay-API

## Description
**NFT-Text-Overlay-API** is an API-interface for rendering images according to specified templates and sending them to IPFS (In progress).

___

## Installation for contributors

To install, you must first install the following software:
| Tool | Description |
|----------|---------|
| [Python](https://www.python.org/downloads/) |  Programming language |
| [venv](https://docs.python.org/3/library/venv.html) |  Environment management tool |

```Bash
# clone via HTTPS:
$ git clone https://github.com/IgorGakhov/NFT-Text-Overlay-API.git
# or clone via SSH:
$ git clone git@github.com:IgorGakhov/NFT-Text-Overlay-API.git
$ cd NFT-Text-Overlay-API
$ pip install -r requirements.txt
$ touch .env
You have to write into .env file secret database data. See .env.example.

$ uvicorn src.main:app --reload
```

___

**Thank you for attention!**

:man_technologist: Author: [@IgorGakhov](https://github.com/IgorGakhov)
