import random
import base64
import os

# Encryption operations
def xor_encrypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def shift_encrypt(data, shift):
    return bytes([(b + shift) % 256 for b in data])

def reverse_encrypt(data):
    return data[::-1]

# Decryption operations
def xor_decrypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def shift_decrypt(data, shift):
    return bytes([(b - shift) % 256 for b in data])

def reverse_decrypt(data):
    return data[::-1]

# Dynamic encryption and decryption function
def dynamic_encrypt(plaintext):
    # Generate a random key and shift
    key = os.urandom(16)  # Random key (16 bytes)
    shift = random.randint(1, 255)  # Random shift value
    random_seed = os.urandom(16)  # Random seed for the randomizer

    # Define operations sequence
    operations = ['reverse_encrypt', 'xor_encrypt', 'shift_encrypt']
    random.shuffle(operations)  # Shuffle operations for randomness

    # Define encryption operations
    operation_map = {
        "xor_encrypt": xor_encrypt,
        "shift_encrypt": shift_encrypt,
        "reverse_encrypt": reverse_encrypt
    }

    # Perform the operations in random order
    encrypted_data = plaintext.encode("utf-8")  # Convert to bytes
    for op_name in operations:
        op_func = operation_map[op_name]
        if op_name == "reverse_encrypt":
            encrypted_data = op_func(encrypted_data)
        else:
            encrypted_data = op_func(encrypted_data, key if "xor" in op_name else shift)

    # Encode the encrypted data and metadata to base64
    encrypted_data_base64 = base64.b64encode(encrypted_data).decode("utf-8")
    metadata = {
        "key": base64.b64encode(key).decode("utf-8"),
        "shift": shift,
        "seed": base64.b64encode(random_seed).decode("utf-8"),
        "operations": operations
    }
    return encrypted_data_base64, metadata

def dynamic_decrypt(encrypted_data, metadata):
    # Decode encrypted data and metadata
    encrypted_data = base64.b64decode(encrypted_data)
    key = base64.b64decode(metadata["key"])
    shift = metadata["shift"]
    random_seed = base64.b64decode(metadata["seed"])

    # Restore the randomizer sequence
    random.seed(random_seed)
    operation_sequence = metadata["operations"]

    # Define decryption operations
    operation_map = {
        "xor_encrypt": xor_decrypt,
        "shift_encrypt": shift_decrypt,
        "reverse_encrypt": reverse_decrypt
    }

    # Reverse the operations for decryption
    decrypted_data = encrypted_data
    for op_name in reversed(operation_sequence):
        op_func = operation_map[op_name]
        if op_name == "reverse_encrypt":
            decrypted_data = op_func(decrypted_data)
        else:
            decrypted_data = op_func(decrypted_data, key if "xor" in op_name else shift)

    return decrypted_data

# Load data and metadata from a file
def load_from_file(filename):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        # Ensure file has the expected structure
        if len(lines) < 2:
            raise ValueError("File format is incorrect or incomplete. Ensure it contains encrypted data and metadata.")

        # Parse encrypted data and metadata
        encrypted_data_line = [line for line in lines if "Encrypted Data:" in line]
        metadata_line = [line for line in lines if "Metadata:" in line]

        if not encrypted_data_line or not metadata_line:
            raise ValueError("Missing required 'Encrypted Data' or 'Metadata' in the file.")

        encrypted_data = encrypted_data_line[0].split("Encrypted Data:")[1].strip()
        metadata = eval(metadata_line[0].split("Metadata:")[1].strip())  # Convert metadata string to dict
        return encrypted_data, metadata

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        exit(1)
    except ValueError as ve:
        print(f"Error: {ve}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

# Save data and metadata to a file
def save_to_file(filename, encrypted_data, metadata):
    try:
        with open(filename, "w") as file:
            file.write(f"Encrypted Data: {encrypted_data}\n")
            file.write(f"Metadata: {metadata}\n")
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

# Main menu-driven script
def main():
    while True:
        print("\nMenu:")
        print("1. Encrypt Text")
        print("2. Decrypt Text")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # Encrypt text
            plaintext = input("Enter the text to encrypt: ").strip()
            encrypted_data, metadata = dynamic_encrypt(plaintext)
            print("\nEncrypted Data:")
            print(encrypted_data)

            # Save to file
            filename = input("Enter the filename to save (def: keys.txt): ").strip()
            if not filename:
                filename = "keys.txt"
            save_to_file(filename, encrypted_data, metadata)

        elif choice == "2":
            # Decrypt text
            filename = input("Enter the filename to load (def: keys.txt): ").strip()
            if not filename:
                filename = "keys.txt"

            # Load encrypted data and metadata
            encrypted_data, metadata = load_from_file(filename)

            # Decrypt the data
            decrypted_data = dynamic_decrypt(encrypted_data, metadata)
            try:
                # Attempt to print the decrypted data as a string
                print("\nDecrypted Data:", decrypted_data.decode("utf-8"))
            except UnicodeDecodeError:
                # If decoding fails, save it as a binary file
                with open("keys.bin", "wb") as output_file:
                    output_file.write(decrypted_data)
                print("\nDecrypted data saved as 'decrypted_output.bin'.")

        elif choice == "3":
            print("Exiting the program...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
