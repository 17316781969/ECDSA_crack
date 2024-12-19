# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import requests
from Crypto.Hash import keccak
from web3 import Web3
from rlp import encode,codec
from web3.types import HexBytes
from web3.datastructures import AttributeDict

from eth_utils import to_bytes

def calculate_z(tx_list):
    tx_nonce=tx_list[0]
    tx_gas_price=tx_list[1]
    tx_gas_limit=tx_list[2]
    tx_to=tx_list[3]
    tx_value=tx_list[4]
    tx_data=tx_list[5]
    tx_chainId = 3
    tx_homesteadBlock = 0
    tx_eip155Block = 0
    k = keccak.new(digest_bits=256)
    k.update(codec.encode_raw(encode([tx_nonce, tx_gas_price, tx_gas_limit, tx_to, tx_value, tx_data, tx_chainId, tx_homesteadBlock, tx_eip155Block]))[1:])

    return k.hexdigest()



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def inverse_mod( a, m ):
    """Inverse of a mod m."""
    if a < 0 or m <= a: a = a % m
    c, d = a, m
    uc, vc, ud, vd = 1, 0, 0, 1
    while c != 0:
        q, c, d = divmod( d, c ) + ( c, )
        uc, vc, ud, vd = ud - q*uc, vd - q*vc, uc, vc

    assert d == 1
    if ud > 0: return ud
    else: return ud + m


def derivate_privkey(p, r, s1, s2, z1, z2):
    z = z1 - z2
    s = s1 - s2
    r_inv = inverse_mod(r, p)
    s_inv = inverse_mod(s, p)
    k = (z * s_inv) % p
    d = (r_inv * (s1 * k - z1)) % p
    return d, k

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    r = 0x69a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166

    tx1 = [0,0x3b9aca00,0x5208,0x92b28647ae1f3264661f72fb2eb9625a89d88a31,0x1111d67bb1bb0000,0]
    z1 = int(calculate_z(tx1),16)
    s1 = 0x7724cedeb923f374bef4e05c97426a918123cc4fec7b07903839f12517e1b3c8

    tx2 = [1,0x3b9aca00,0x5208,0x92b28647ae1f3264661f72fb2eb9625a89d88a31,0x1922e95bca330e00,0]
    z2 = int(calculate_z(tx2),16)
    s2 = 0x2bbd9c2a6285c2b43e728b17bda36a81653d5f4612a2e0aefdb48043c5108de


    p  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    print("privatekey:%x\n k:%x" % derivate_privkey(p, r, s1, s2, z1, z2))
