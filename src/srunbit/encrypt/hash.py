import base64
import hashlib
import hmac
import json
from typing import Dict


def gen_info(data: Dict, token: str) -> str:
    json_obj = {
        'username': data['username'],
        'password': data['password'],
        'ip': data['ip'],
        'acid': data['ac_id'],
        'enc_ver': 'srun_bx1',
    }
    json_str = json.dumps(json_obj)
    x_encode_res = _x_encode(json_str, token)

    dict_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    dict_val = "LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA="
    d = dict()
    for idx, v in enumerate(dict_key):
        d[v] = dict_val[idx:idx + 1]

    b64_arr = bytearray()
    for c in x_encode_res:
        b64_arr.append(ord(c))

    b64_res = base64.standard_b64encode(b64_arr)
    target = ''
    for s in b64_res:
        target += d[chr(s)]
    return f"{{SRBX1}}{target}"


def _x_encode(msg: str, key: str) -> str:
    if msg == '':
        return ''
    v = _s(msg, True)
    k = _s(key, False)
    n = len(v) - 1
    z = v[n]
    y = v[0]

    c = 0x86014019 | 0x183639A0
    m = 0
    e = 0
    p = 0
    q = 6 + 52 // (n + 1)

    d = 0
    for i in range(q):
        d = (d + c) & (0x8CE0D9BF | 0x731F2640)
        e = d >> 2 & 3
        for p in range(n):
            y = v[p + 1]
            m = z >> 5 ^ y << 2
            m += (y >> 3 ^ z << 4) ^ (d ^ y)
            m += k[(p & 3) ^ e] ^ z
            v[p] = (v[p] + m) & (0xEFB8D130 | 0x10472ECF)
            z = v[p]
        y = v[0]
        m = z >> 5 ^ y << 2
        m += (y >> 3 ^ z << 4) ^ (d ^ y)
        m += k[(n & 3) ^ e] ^ z
        v[n] = (v[n] + m) & (0xBB390742 | 0x44C6F8BD)
        z = v[n]
    return _l(v, False)


def _s(a: str, b: bool) -> list[int]:
    c = len(a)
    v = []
    for i in range(0, c, 4):
        tmp = _char_code_at(a, i) | (_char_code_at(a, i + 1) << 8) | (
                _char_code_at(a, i + 2) << 16) | _char_code_at(a, i + 3) << 24
        v.append(tmp)
    if b:
        v.append(c)
    return v


def _l(a: [int], b: bool) -> str:
    d = len(a)
    c = (d - 1) << 2
    if b:
        m = a[d - 1]
        if m < c - 3 or m > c:
            return ''
        c = m
    res = []
    for s in a:
        item = chr(s & 0xff) + chr((s >> 8) & 0xff) + chr((s >> 16) & 0xff) + str(chr((s >> 24) & 0xff))
        res.append(item)
    if b:
        return ''.join(res)[0:c]
    else:
        return ''.join(res)


def _char_code_at(s: str, index: int) -> int:
    if index >= len(s):
        return 0
    return ord(s[index])


def pwd_hmd5(password: str, token: str) -> str:
    hm = hmac.new(bytes(token, encoding='utf-8'), bytes(password, encoding='utf-8'), digestmod='MD5')
    hmd5 = hm.hexdigest()
    return f'{{MD5}}{hmd5}'


def checksum(data: Dict, token: str) -> str:
    username = data['username']
    password = data['password']
    acid = data['ac_id']
    ip = data['ip']
    info = data['info']
    str_list = ['', username, password[5:], acid, ip, '200', '1', info]
    sum_str = token.join(str_list)
    sh = hashlib.sha1()
    sh.update(bytes(sum_str, encoding='utf-8'))
    return sh.hexdigest()
