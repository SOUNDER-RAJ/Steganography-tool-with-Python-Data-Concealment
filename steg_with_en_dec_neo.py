from PIL import Image
import os


def xor_encrypt_decrypt(text, passphrase):
    encrypted_decrypted_chars = []
    for i in range(len(text)):
        encrypted_decrypted_chars.append(chr(ord(text[i]) ^ ord(passphrase[i % len(passphrase)])))
    return ''.join(encrypted_decrypted_chars)

# using LSB
def embed_text_in_image(image_path, text, passphrase, output_path):
  
    encrypted_text = xor_encrypt_decrypt(text, passphrase)

  
    img = Image.open(image_path)
    encoded_img = img.copy()
    width, height = img.size
    index = 0

  
    binary_text = ''.join(format(ord(i), '08b') for i in encrypted_text)
    binary_text += '1111111111111110'  # Delimiter to indicate end of text

  
    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for n in range(3):  # Iterate over RGB values
                if index < len(binary_text):
                    pixel[n] = pixel[n] & ~1 | int(binary_text[index])
                    index += 1
            encoded_img.putpixel((x, y), tuple(pixel))

  
    encoded_img.save(output_path)
    print(f"Text has been embedded into {output_path}.")


def extract_decrypt_text_from_image(image_path, passphrase):

    img = Image.open(image_path)
    binary_text = ''
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            pixel = list(img.getpixel((x, y)))
            for n in range(3):  # Iterate over RGB values
                binary_text += str(pixel[n] & 1)


    all_bytes = [binary_text[i: i+8] for i in range(0, len(binary_text), 8)]
    encrypted_text = ''
    for byte in all_bytes:
        if byte == '11111111':  # Check for delimiter
            break
        encrypted_text += chr(int(byte, 2))


    decrypted_text = xor_encrypt_decrypt(encrypted_text, passphrase)
    print("Text has been extracted and decrypted.")
    print(f"Decrypted Text: {decrypted_text}")
    return decrypted_text


input_image_path = input("Enter the path to the input image: ")
passphrase = input("Enter the passphrase for encryption/decryption: ")


operation = input("Do you want to encrypt or decrypt the image? (Enter 'encrypt' or 'decrypt'): ")

if operation.lower() == 'encrypt':
    text_file_path = input("Enter the path to the text file containing the message: ")
    output_image_path = "output_image_with_text.png"


    with open(text_file_path, 'r') as file:
        embedded_text = file.read()


    embed_text_in_image(input_image_path, embedded_text, passphrase, output_image_path)

elif operation.lower() == 'decrypt':
    extracted_text_path = "extracted_text.txt"


    try:
        extracted_text = extract_decrypt_text_from_image(input_image_path, passphrase)
        with open(extracted_text_path, "w") as file:
            file.write(extracted_text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

else:
    print("Invalid operation. Please enter 'encrypt' or 'decrypt'.")
