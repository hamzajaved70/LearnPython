#!/usr/bin/env python3
import argparse
import os
import base64
import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def readfile_binary(file):
	with open(file, 'rb') as f:
		content = f.read()
	return content

def writefile_binary(file, content):
	with open(file, 'wb') as f:
		f.write(content)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-out', help='Output encrypted file', dest='output', required=True)
	parser.add_argument('-in', help='File to be encrypted', dest='input', required=True)
	parser.add_argument('-k', help='The key to be used for encryption, must be in hex', dest='key')
	parser.add_argument('-iv', help='The initialization vector, must be in hex', dest='iv')
	parser.add_argument('-e','--encrypt', action='store_true')
	parser.add_argument('-d','--decrypt', action='store_true')
	args = parser.parse_args()
	input_content = readfile_binary(args.input)
	backend = default_backend()
	cipher = Cipher(algorithms.AES(binascii.unhexlify(args.key)), modes.CBC(binascii.unhexlify(args.iv)), backend=backend)
	if(args.decrypt):
		print('This is decrypt mode')
		decryptor = cipher.decryptor()
		plainText = decryptor.update(input_content) + decryptor.finalize()
		unpadder = padding.ANSIX923(128).unpadder()
		unpadded_data = unpadder.update(plainText)
		finalText = unpadded_data + unpadder.finalize()
		writefile_binary(args.output, finalText) 
	elif(args.encrypt):
		print('This is encrypt mode')
		encryptor = cipher.encryptor()
		padder = padding.ANSIX923(128).padder()
		padded_data = padder.update(readfile_binary(args.input))
		padded_data += padder.finalize()
		ct = encryptor.update(padded_data) + encryptor.finalize()
		writefile_binary(args.output, ct)
	else:
		print('Select -e or -d option')

if __name__ == '__main__':
	main()
