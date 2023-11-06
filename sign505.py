import hashlib
import json
from json.decoder import JSONDecodeError
from json.encoder import JSONEncoder
import execjs


def getSign505(data, timestamp, userId):
    salt = '$KJSD&)2TSz8M$oF'
    keys = list(data.keys())
    keys.sort()
    keys = [key for key in keys if data[key] is not None and data[key] != '']
    sign = ''
    for key in keys:
        value = data[key]
        if isinstance(value, bool):
            value = 'true' if value else 'false'
        sign += f'{key}={value}&'
    sign += f'timestamp={timestamp}'
    sign += f'&userid={userId}'
    sign += f'&salt={salt}'
    md5 = hashlib.md5()
    md5.update(sign.encode('utf-8'))
    sign = md5.hexdigest()
    return sign


if __name__ == "__main__":
    data = {
        "albumGoodsId": "108745",
        "choice": False,
        "currentPage": 0,
        "pageSize": 30,
        "sortType": "asc"
    }
    timestamp = '1699170899'  # Replace with your timestamp
    useID = "6007476"
    result = getSign505(data, timestamp, useID)
    expected_hash = "0d2e276c1d1df77266811a9eafd2ab09"
    print(f"expected hash: {expected_hash}")
    print(f"result: {result}")
    assert result == expected_hash, f"Expected: {expected_hash}, Got: {result}"
    print(result)
