import wave
# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it

from PIL import Image

def case(b):
    if (b==1):
        image()
    elif(b == 2):
        audio()
    else:
        print("invalid choice")
        
        
# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):

		# list of binary codes
		# of given data
		newd = []

		for i in data:
			newd.append(format(ord(i), '08b'))
		return newd

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):

	datalist = genData(data)
	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):

		# Extracting 3 pixels at a time
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		# Pixel value should be made
		# odd for 1 and even for 0
		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1

			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1
				# pix[j] -= 1

		# Eighth pixel of every set tells
		# whether to stop ot read further.
		# 0 means keep reading; 1 means thec
		# message is over.
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]

def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)

	for pixel in modPix(newimg.getdata(), data):

		# Putting modified pixels in the new image
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1

# Encode data into image
def encode():
	img = input("Enter image name(with extension) : ")
	image = Image.open(img, 'r')

	data = input("Enter data to be encoded : ")
	if (len(data) == 0):
		raise ValueError('Data is empty')

	newimg = image.copy()
	encode_enc(newimg, data)

	new_img_name = input("Enter the name of new image(with extension) : ")
	newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Decode the data in the image
def decode():
 password="JJ@IFET"
 for i in range(3):
     pwd=input(" enter password for decoding:")
     j=3
     if(pwd==password):
         print("password is correct \n Decoding starts...")
         img = input("Enter image name(with extension) : ")
         image = Image.open(img, 'r')
     
         data = ''
         imgdata = iter(image.getdata())
         while (True):
    	        pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]

		# string of binary data
		    binstr = ''
                    for i in pixels[:8]:
                        if (i % 2 == 0):
                            binstr += '0'
                        else:
                            binstr += '1'
		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0):
			return data
      else:
             print("incorrect password try again and chance left",j-i)
             continue
             print("\n try next time")
# Main Function
def image():
	a = int(input("Image Steganography\n"
						"1. Encode\n2. Decode\n"))
	if (a == 1):
		encode()

	elif (a == 2):
		print("Decoded Word : " + decode())
	else:
		print("Enter correct input")


def audio():
    c = int(input("Audio stegnography\n 1.Encode \n2.Decode"))
    if c == 1:
        encodee()
    elif c == 2:
        decodee()
    elif c == 3:
        quit()
    else:
        print("\nEnter valid Choice!")

def encodee():
	print("\nEncoding Starts..")
	audio = wave.open("sample.wav",mode="rb")
	frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
	string = input("Enter text to be encoded: ")
	print(string)
	string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
	bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
	for i, bit in enumerate(bits):
	    frame_bytes[i] = (frame_bytes[i] & 254) | bit
	frame_modified = bytes(frame_bytes)
	newAudio =  wave.open('sampleStego.wav', 'wb')
	newAudio.setparams(audio.getparams())
	newAudio.writeframes(frame_modified)

	newAudio.close()
	audio.close()
	print(" |---->succesfully encoded inside sampleStego.wav")

def decodee():
        password="ARJ.IFET"
        for i in range(3):
             pwd=input(" enter password for decoding:")
             j=3
             if(pwd==password):
               print("password is correct \n Decoding starts...")
               audio = wave.open("sampleStego.wav", mode='rb')
               frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
               extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
               string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2))
               for i in range(0,len(extracted),8))
               decoded = string.split("###")[0]
               print("Sucessfully decoded: "+decoded)
               audio.close()
               break

             else:
                print("incorrect password try again and chance left",j-i)
                continue
                print("\n try next time")

while(1):
	print("\nSelect an option: \n1)Encode\n2)Decode\n3)exit")
	val = int(input("\nChoice:"))
	case(val)
	



