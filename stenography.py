import cv2
import numpy as np
import types

def messageToBinary(message):
	"""
	Converts string, bytes, np.ndarray or integer
	into binary
	"""
	if type(message) == str:
		return ''.join([format(ord(i), '08b') for i in message])

	elif type(message) == bytes or type(message) == np.ndarray:
		return [format(i, '08b') for i in message]

	elif type(message) == int or type(message) == np.uint8:
		return format(message, '08b')

	else: raise TypeError('Input not supported')

def hideData(image, secret_message):
	"""
	Insert message in binary format
	inside an image by altering the
	LSB
	"""

	# calculating the maximum bytes to encode
	# and checking if the number of bytes
	# to encode is greather than the meximum allowed
	n_bytes = image.shape[0] * image.shape[1] * 3 // 8
	print('Maximum bytes to encode:', n_bytes)

	if len(secret_message) > n_bytes:
		raise ValueError('Insufficient amount of bytes, need a bigger image or a lower data to encode!!')

	secret_message += '#####' # delimiter

	# converting input data to binary format
	# using the messageToBinary function
	data_index = 0
	binary_secret_msg = messageToBinary(secret_message)
	data_len = len(binary_secret_msg)

	# hidden the binary message into the image
	for values in image:
		for pixel in values:
			# converting the RGB into binary
			r, g, b = messageToBinary(pixel)

			# hiddening the message
			if data_index < data_len:
				pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
				data_index += 1

			if data_index < data_len:
				pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
				data_index += 1

			if data_index < data_len:
				pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
				data_index += 1

			# when all the message is hidden
			# we break the for-loop
			if data_index >= data_len: break

	return image

def showData(image):
	"""
	Getting and Decoding the secret message from an image
	"""

	binary_data = ''

	for values in image:
		for pixel in values:
			r, g, b = messageToBinary(pixel)
			binary_data += r[-1] # getting LSB from red pixel
			binary_data += g[-1] # getting LSB from green pixel
			binary_data += b[-1] # getting LSB from blue pixel

	# getting just the LSB corresponding to the secret message
	all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]

	# converting the secret message from bytes to characters
	decoded_data = ''

	for byte in all_bytes:
		decoded_data += chr(int(byte, 2))

		# if the delimiter is found
		# the for-loop is broken
		if decoded_data[-5:] == '#####': break

	# returning the secret message in characters
	# excluding the delimiter
	return decoded_data[:-5]


def encodeText():
	"""
	Getting image name and secret message
	from the user and encoding the message.
	
	The image should be into the same dir of
	this script.
	"""
	image_name = input('Enter the image name (with extension): ')
	image = cv2.imread(image_name)

	# image's details
	print('Shape: ', image.shape)
	resized_image = cv2.resize(image, (500, 500))

	# getting the secret message
	data = input('Enter the data to be encoded: ')

	if len(data) == 0: raise ValueError('Data is empty!')

	# encoding the secret message
	filename = input('Enter the name of the new encoded image (with extension): ')
	encoded_image = hideData(image, data)
	cv2.imwrite(filename, encoded_image)

def decodeText():
	"""
	Entering the image's name that needs to be decoded
	and returning the decoded message
	"""
	image_name = input('Enter the name of the steganographed image that you wanna decode (with extension): ')
	image = cv2.imread(image_name)
	resized_image = cv2.resize(image, (500, 500))


	text = showData(image)
	return text

def Steganography():
	"""
	The Main Function

	The use must select one of the three available options:

	/ 1. Encode the data
	/ 2. Decode the data
	/ 3. Exit
	"""

	while True:
		menu = input('Image Stenography\n 1. Encode the data\n 2. Decode the data\n 3. Exit\n Your input is: ')
		userInput = menu

		if userInput == '1':
			print('\nEncoding...')
			encodeText()
			break

		elif userInput == '2':
			print('\nDecoding...')
			print('\nWait a little bit...')
			print('Decoded message is: "' + decodeText() + '"')
			break

		elif userInput == '3': break

		else: print('\nEnter a valid option!\n')

Steganography()