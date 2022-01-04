import os
import argparse
import json
import glob
from functools import lru_cache
from hashlib import sha256
from typing import Mapping, Union


B58_ALPHABET = \
    b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def b58encode_int(
    i: int, default_one: bool = True, alphabet: bytes = B58_ALPHABET
) -> bytes:
    """
    Encode an integer using Base58
    """
    if not i and default_one:
        return alphabet[0:1]
    string = b""
    base = len(alphabet)
    while i:
        i, idx = divmod(i, base)
        string = alphabet[idx:idx+1] + string
    return string


def scrub_input(v: Union[str, bytes]) -> bytes:
    if isinstance(v, str):
        v = v.encode('ascii')

    return v
  
def b58encode(
    v: Union[str, bytes], alphabet: bytes = B58_ALPHABET
) -> bytes:
    """
    Encode a string using Base58
    """
    v = scrub_input(v)

    origlen = len(v)
    v = v.lstrip(b'\0')
    newlen = len(v)

    acc = int.from_bytes(v, byteorder='big')  # first byte is most significant

    result = b58encode_int(acc, default_one=False, alphabet=alphabet)
    return alphabet[0:1] * (origlen - newlen) + result


def find_keypair_files():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for filename in glob.glob(os.path.join(dir_path, '*.json')): #only process .JSON files in folder.      
        yield filename


def get_contents(filename):
    file = open(filename, 'r')
    return file.read()

def main(search=""):
    """
    If we've provided a search term, use that in solana-keygen to generate a keypair and then b58 encode the bytearray. Show the private keys.
    No search term provided? Simply show the private keys for previously downloaded keypairs.
    """
    if len(search) > 0:
        os.system(f'solana-keygen grind --num-threads 24 --starts-with {search}:1 | grep Wrote')

    for filename in find_keypair_files(): 
        contents = get_contents(filename)
        decoded = json.loads(contents)
        b58_encoded = b58encode(bytearray(decoded))

        print(f'File: {os.path.basename(filename)}\tPrivate Key: {b58_encoded.decode("utf-8")}')

program_description = 'Vanity SOL Address Helper. Pass a desired prefix to attempt '\
    'to find the Solana address of your dreams. Make sure to install Solana Tool Suite first.'

prefix_help = 'Prefix to search on. Anything more than 4 characters will take a really long time. '\
    'Avoid to see not search and simply see private keys of existing keypairs.'

parser = argparse.ArgumentParser(description=program_description)
parser.add_argument('prefix', metavar='Prefix', type=str, nargs='?', help=prefix_help)
args = parser.parse_args()

if __name__ == '__main__':
    if args.prefix: 
        main(args.prefix[0])
    else:
        main()
