# This app will encode or decode text messages in an image file.
# The app will use RGB channels so only PNG files will be accepted.
# This technique will focus on Least Significant Bit (LSB) encoding.

from PIL import Image
import os

# ---------- Helper Functions ----------

def numberToBinary(num):
    """Takes a base10 number and converts to a binary string with 8 bits"""
    binary = bin(num)[2:]           # convert to binary and remove '0b'
    binary = binary.zfill(8)        # pad to ensure it's 8 bits
    return binary

def binaryToNumber(binaryString):
    """Takes a binary string and converts it to a base10 integer."""
    return int(binaryString, 2)     # interpret string as base 2


# ---------- Encoding Function ----------

def encode(img, msg):
    """Encodes a secret message into an image using LSB technique."""
    pixels = img.load()
    width, height = img.size
    letterSpot = 0
    pixel = 0
    letterBinary = ""
    msgLength = len(msg)

    # Store message length in first pixel’s red value
    red, green, blue = pixels[0, 0]
    pixels[0, 0] = (msgLength, green, blue)

    for i in range(msgLength * 3):
        x = i % width
        y = i // width
        red, green, blue = pixels[x, y]

        redBinary = numberToBinary(red)
        greenBinary = numberToBinary(green)
        blueBinary = numberToBinary(blue)

        if pixel % 3 == 0:
            letterBinary = numberToBinary(ord(msg[letterSpot]))
            greenBinary = greenBinary[:7] + letterBinary[0]
            blueBinary = blueBinary[:7] + letterBinary[1]

        elif pixel % 3 == 1:
            redBinary = redBinary[:7] + letterBinary[2]
            greenBinary = greenBinary[:7] + letterBinary[3]
            blueBinary = blueBinary[:7] + letterBinary[4]

        else:
            redBinary = redBinary[:7] + letterBinary[5]
            greenBinary = greenBinary[:7] + letterBinary[6]
            blueBinary = blueBinary[:7] + letterBinary[7]
            letterSpot += 1  # move to next letter after 3 pixels

        red = binaryToNumber(redBinary)
        green = binaryToNumber(greenBinary)
        blue = binaryToNumber(blueBinary)

        pixels[x, y] = (red, green, blue)
        pixel += 1

    # Save encoded image
    img.save("secretImg.png", "PNG")
    print("Message encoded and saved as secretImg.png")


# ---------- Decoding Function ----------

def decode(img):
    """Reads the least significant bits to extract the hidden message."""
    msg = ""
    pixels = img.load()
    red, green, blue = pixels[0, 0]
    msgLength = red
    width, height = img.size
    pixel = 0
    letterBinary = ""

    for i in range(msgLength * 3):
        x = i % width
        y = i // width
        red, green, blue = pixels[x, y]
        redBinary = numberToBinary(red)
        greenBinary = numberToBinary(green)
        blueBinary = numberToBinary(blue)

        if pixel % 3 == 0:
            letterBinary = greenBinary[7] + blueBinary[7]
        elif pixel % 3 == 1:
            letterBinary += redBinary[7] + greenBinary[7] + blueBinary[7]
        else:
            letterBinary += redBinary[7] + greenBinary[7] + blueBinary[7]
            msg += chr(binaryToNumber(letterBinary))
        pixel += 1

    return msg


# ---------- Main Function ----------

def main():
    choice = input("Do you want to encode (e) or decode (d)? ").lower()

    if choice == 'e':
        file = input("Enter image file name (PNG only): ")
        if not file.lower().endswith(".png"):
            print("Only PNG files are supported.")
            return
        img = Image.open(file)
        msg = input("Enter the secret message: ")
        encode(img, msg)
        img.close()

    elif choice == 'd':
        file = input("Enter encoded image file name: ")
        img = Image.open(file)
        hidden_msg = decode(img)
        print("Decoded message:", hidden_msg)
        img.close()

    else:
        print("Invalid choice.")


if __name__ == '__main__':
    main()
