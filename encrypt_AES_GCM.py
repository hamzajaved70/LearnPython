#!/usr/bin/env python3
import argparse
import os
import binascii
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)

def readfile_binary(file):
	with open(file, 'rb') as f:
		content = f.read()
	return content

def writefile_binary(file, content):
	with open(file, 'wb') as f:
		f.write(content)

def encrypt(key, iv, plaintext, associated_data):
    encryptor = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend()).encryptor()
    encryptor.authenticate_additional_data(associated_data)
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return (ciphertext, encryptor.tag)

def decrypt(key, iv, associated_data, ciphertext, tag):
    decryptor = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend() ).decryptor()
    decryptor.authenticate_additional_data(associated_data)
    return decryptor.update(ciphertext) + decryptor.finalize()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-out', help='Output encrypted file', dest='output', required=True)
	parser.add_argument('-in', help='File to be encrypted', dest='input', required=True)
	parser.add_argument('-ad', help='Authenticated data', dest='ad', required=True)
	parser.add_argument('-k', help='The key to be used for encryption, must be in hex', dest='key')
	parser.add_argument('-iv', help='The initialization vector, must be in hex', dest='iv')
	parser.add_argument('-tag', help='Tag from encryption', dest='tag')
	parser.add_argument('-e', '--encrypt', action='store_true', help='Option to encrypt')
	parser.add_argument('-d', '--decrypt', action='store_true', help='Option to decrypt')
	args = parser.parse_args()
	if(args.encrypt):
		input_content_plaintext = readfile_binary(args.input)
		input_content_ad = readfile_binary(args.ad)
		cipherText, tag = encrypt(binascii.unhexlify(args.key), binascii.unhexlify(args.iv), input_content_plaintext, input_content_ad)
		writefile_binary(args.output, cipherText)
		writefile_binary('tag', tag)
	elif(args.decrypt):
		input_content_ciphertext = readfile_binary(args.input)
		input_content_ad = readfile_binary(args.ad)
		input_content_tag = readfile_binary(args.tag)
		pt = decrypt(binascii.unhexlify(args.key), binascii.unhexlify(args.iv), input_content_ad, input_content_ciphertext, input_content_tag)
		writefile_binary(args.output, pt)
	else:
		print('Specify -e or -d')

if __name__ == '__main__':
    main()
