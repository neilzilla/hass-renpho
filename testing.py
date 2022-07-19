from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64encode
import sys

key = RSA.importKey('-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+25I2upukpfQ7rIaaTZtVE744\nu2zV+HaagrUhDOTq8fMVf9yFQvEZh2/HKxFudUxP0dXUa8F6X4XmWumHdQnum3zm\nJr04fz2b2WCcN0ta/rbF2nYAnMVAk2OJVZAMudOiMWhcxV1nNJiKgTNNr13de0EQ\nIiOL2CUBzu+HmIfUbQIDAQAB\n-----END PUBLIC KEY-----')
cipher = PKCS1_v1_5.new(key)
newPassword = b64encode(cipher.encrypt(bytes(sys.argv[1])))

print(newPassword)