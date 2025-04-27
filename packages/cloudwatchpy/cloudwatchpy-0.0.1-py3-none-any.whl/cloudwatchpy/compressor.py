import gzip
import json
from io import BytesIO
from typing import Union

def compress_data_if_enabled(data: Union[str, dict], compress: bool = True) -> bytes:
    """
    Compress log data using GZIP if `compress` is True.
    Accepts JSON string or dictionary.
    Returns raw or compressed bytes.
    """
    if isinstance(data, dict):
        data = json.dumps(data)

    raw_bytes = data.encode("utf-8")

    if not compress:
        return raw_bytes

    buffer = BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb") as gzip_file:
        gzip_file.write(raw_bytes)
    return buffer.getvalue()
