# -*- coding: utf-8 -*-
# Wiley Yu

try:
    from pkcs7 import PKCS7Encoder
except ImportError:
    from .pkcs7 import PKCS7Encoder

import base64
import binascii

from Crypto.Cipher import AES
from Crypto.Hash import SHA256


# lets cache those values!

pkc = PKCS7Encoder()
post_headers = {
    'X-Requested-With': 'XMLHttpRequest'
}

'''
#before version 3

cartoon_hex = "a5e8d2e9c1721ae0e84ad660c472c1f3".encode('utf8')
cartoon_k = binascii.unhexlify(cartoon_hex)
cartoon_g = "WrxLl3rnA48iafgCy".encode('utf8')
cartoon_h = "CartKS$2141#".encode('utf8')
cartoon_l = KDF.PBKDF2(cartoon_g, cartoon_h)
'''

asian_c = "32b812e9a1321ae0e84af660c4722b3a".encode('utf8')
cartoon_hex = "a5e8d2e9c1721ae0e84ad660c472c1f3".encode('utf8')

comb = dict()
# BEGIN ASIAN
comb['Asian'] = {}
comb['Asian']['sha'] = ""
comb['Asian']['topost'] = 'http://kissasian.com/External/RSK'
comb['Asian']['payload'] = {"krsk": "krsk"}
comb['Asian']['f'] = binascii.unhexlify(asian_c)
# END ASIAN

# BEGIN CARTOON
comb['Cartoon'] = {}
comb['Cartoon']['sha'] = ""
comb['Cartoon']['topost'] = 'http://kisscartoon.me/External/RSK'
comb['Cartoon']['payload'] = {}
comb['Cartoon']['f'] = binascii.unhexlify(cartoon_hex)
# END CARTOON

'''
# before version 3

def kissencCartoon(raw_str):
    cartoon_i = AES.new(cartoon_l, AES.MODE_CBC, cartoon_k)
    jj = base64.b64decode(raw_str)
    filled = cartoon_i.decrypt(jj)

    return pkc.decode(filled).decode('utf8')
'''


def ver5(raw_str, sess, type_t):
    # for version 5
    # requires a session because the js makes an ajax request
    # in 256
    sha = comb[type_t]['sha']
    topost = comb[type_t]['topost']
    payload = comb[type_t]['payload']
    f = comb[type_t]['f']

    if sha == '':
        post_data = sess.post(topost, headers=post_headers, data=payload)
        comb[type_t]['sha'] = post_data.text.encode('utf8')
        sha = comb[type_t]['sha']

    obj_sha = SHA256.new(sha)
    a = binascii.unhexlify(obj_sha.hexdigest())
    g = AES.new(a, AES.MODE_CBC, f)
    jj = base64.b64decode(raw_str)
    #
    filled = g.decrypt(jj)
    return pkc.decode(filled).decode('utf8')


def ver3(raw_str, sess, type_t):
    # lazy fix
    # since cartoon_payload is empty, the functionality should still be the same
    return ver5(raw_str, sess, type_t)


def kissencCartoon(raw_str, sess):
    # Using Version 3
    return ver3(raw_str, sess, "Cartoon")


def kissencAsian(raw_str, sess):
    # Using Version 5
    return ver5(raw_str, sess, "Asian")


def kissencAnime(raw_str):
    return base64.b64decode(raw_str).decode('utf8')
