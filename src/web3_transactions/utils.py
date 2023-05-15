import base64
import json

import ipfsapi
from io import BytesIO


def add_file_to_ipfs(file) -> str:
    """Отправляем файл file в ipfs"""

    # Клиент ipfs должен быть запущен на сервере
    api = ipfsapi.Client(host='http://127.0.0.1', port=5001)  # подключение к ipfs
    file = base64.b64decode(file)
    bytes_stream = BytesIO(file)
    CID = api.add(bytes_stream)['Hash']
    ipfs_link = "https://ipfs.io/ipfs/" + CID
    return ipfs_link
