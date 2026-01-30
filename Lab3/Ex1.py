from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

encoded_text = cipher_suite.encrypt(b"This is a really secret message")
print(f"Encoded text: {encoded_text}")

#Use the cryptography library to encode and decoode a message
decoded_text = cipher_suite.decrypt(encoded_text)
print(f"Decoded text: {decoded_text.decode('utf-8')}")

def max(num1, num2):
    #Return the maximum of two numbers
    return num1 if num1 > num2 else num2

def min(num1, num2):
    #Return the minimum of two numbers
    return num1 if num1 < num2 else num2

