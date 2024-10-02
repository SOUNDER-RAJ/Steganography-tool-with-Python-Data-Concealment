from PIL import Image
import numpy as np

# XOR encryption/decryption function
def xor_encrypt_decrypt(text, passphrase):
    return ''.join(chr(ord(char) ^ ord(passphrase[i % len(passphrase)])) for i, char in enumerate(text))

# Embedding text into image using LSB steganography
def embed_text_in_image(image_path, text, passphrase, output_path):
    encrypted_text = xor_encrypt_decrypt(text, passphrase)

    # Open and convert the image to RGB
    img = Image.open(image_path)
    img = img.convert('RGB')
    encoded_img = np.array(img)

    height, width, _ = encoded_img.shape
    binary_text = ''.join(format(ord(char), '08b') for char in encrypted_text)
    binary_text += '1111111111111110'  # Delimiter to indicate end of text

    if len(binary_text) > width * height * 3:
        raise ValueError("Text too long to embed in the image.")

    index = 0
    for y in range(height):
        for x in range(width):
            for channel in range(3):  # Iterate through RGB channels
                if index < len(binary_text):
                    encoded_img[y, x, channel] = (encoded_img[y, x, channel] & ~1) | int(binary_text[index])
                    index += 1
                else:
                    break

    encoded_img = Image.fromarray(encoded_img)
    encoded_img.save(output_path)
    print(f"Text successfully embedded into {output_path}.")

# Extract and decrypt text from the image
def extract_decrypt_text_from_image(image_path, passphrase):
    img = Image.open(image_path)
    img = img.convert('RGB')
    encoded_img = np.array(img)

    height, width, _ = encoded_img.shape
    binary_text = ''

    for y in range(height):
        for x in range(width):
            for channel in range(3):  # Iterate through RGB channels
                binary_text += str(encoded_img[y, x, channel] & 1)

    # Split into 8-bit chunks
    all_bytes = [binary_text[i:i + 8] for i in range(0, len(binary_text), 8)]
    encrypted_text = ''
    for byte in all_bytes:
        if byte == '11111111':  # Stop at delimiter
            break
        encrypted_text += chr(int(byte, 2))

    decrypted_text = xor_encrypt_decrypt(encrypted_text, passphrase)
    print(f"Decrypted Text: {decrypted_text}")
    extracted_text_path = "extracted_text.txt"
    with open(extracted_text_path, "w") as file:
        file.write(decrypted_text)
    print(f"Decrypted text saved to {extracted_text_path}.")

# Main function to handle encryption and decryption
def run():
    passphrase = input("Enter the passphrase for encryption/decryption: ")
    operation = input("Do you want to encrypt or decrypt the image? (Enter 'encrypt' or 'decrypt'): ")

    if operation.lower() == 'encrypt':
        input_image_path = input("Enter the path to the input image: ")
        text_file_path = input("Enter the path to the text file containing the message: ")

        with open(text_file_path, 'r') as file:
            embedded_text = file.read()

        output_image_path = "output_image_with_text.png"
        embed_text_in_image(input_image_path, embedded_text, passphrase, output_image_path)

    elif operation.lower() == 'decrypt':
        input_image_path = input("Enter the path to the input image: ")
        extract_decrypt_text_from_image(input_image_path, passphrase)

    else:
        print("Invalid operation. Please enter 'encrypt' or 'decrypt'.")

# Run the script
run()
