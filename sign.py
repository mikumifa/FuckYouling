import hashlib


def s_a(input_str):
    cArr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    try:

        bys = input_str.encode()
        message_digest = hashlib.md5()
        message_digest.update(bys)
        digest = message_digest.digest()
        cArr2 = [''] * (len(digest) * 2)
        i2 = 0
        for b2 in digest:
            i3 = i2 + 1
            cArr2[i2] = cArr[(b2 >> 4) & 15]
            i2 = i3 + 1
            cArr2[i3] = cArr[b2 & 15]
        return ''.join(cArr2)
    except Exception as e:
        print(e)
        return None


def getSign(timestamp):
    salt = "183846cdf0cA3ba5"
    input_str = "buildversion=23102601&timestamp=" + timestamp + "&salt=" + salt
    return s_a(input_str)


def test_en():
    timestamp = "1699170899"
    expected_hash = "5e6f6cca72a6abb65b90e3165844663f"  # 期望的 MD5 散列值
    result = getSign(timestamp)
    print(f"expected hash: {expected_hash}")
    print(f"result: {result}")
    assert result == expected_hash, f"Expected: {expected_hash}, Got: {result}"
    print("en Test Passed!")


if __name__ == "__main__":
    test_en()
