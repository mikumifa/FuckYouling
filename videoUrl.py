import base64
from Cryptodome.Util.Padding import unpad
from Cryptodome.Cipher import DES

video_url_key = "cf#yu*df"


def decrypt_des(base64_encoded_str, des_key):
    try:
        # 解码Base64字符串
        decoded_bytes = base64.b64decode(base64_encoded_str)
        cipher = DES.new(des_key.encode("utf-8"), DES.MODE_ECB)
        decrypted_bytes = cipher.decrypt(decoded_bytes)
        decrypted_text = unpad(decrypted_bytes, DES.block_size).decode("utf-8")
        return decrypted_text
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    res = decrypt_des("MWqRpp8dE0XabgHzlvXnNlkeWQeJjM6b46uFRLyPiYp4y9eT313exhxmhG3KCuXcvGS2ovoBpNUvAdrNQo0e/DkvRHQvEQHi6/NLzY2jI58=",video_url_key)
    print(res)


