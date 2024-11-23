# Crypter 🔒

Crypter is a Python program that allows users to securely encrypt and decrypt text using a combination of XOR, shift, and reverse encryption techniques. It provides a menu-driven interface to choose between encrypting text, decrypting text, and saving/loading encrypted data to/from a file.

## Features ✨
- **🔐 Encrypt Text**: Encrypts user-provided text using a randomized combination of operations (XOR, shift, reverse).
- **🔓 Decrypt Text**: Decrypts previously encrypted data using the metadata that stores the encryption process details.
- **💾 Save and Load**: Saves the encrypted data along with the encryption metadata to a file. It can later load the encrypted data for decryption.
- **📁 File Handling**: Supports saving encrypted data to files with automatic metadata storage for easy decryption later.
- **⚠️ Error Handling**: Includes built-in error handling for file issues and invalid inputs.

## How It Works 🛠️
1. **Encryption**: 
   - The program uses three operations: `XOR`, `Shift`, and `Reverse`. The order of operations is randomized during encryption for added security.
   - The result is a base64-encoded string of encrypted data along with metadata, including a random key, shift value, seed, and the order of operations used.
   
2. **Decryption**:
   - The program loads the encrypted data and metadata from a file and reverses the operations (in the reverse order) to retrieve the original text.

## Usage 🚀

### Run the Program 🖥️

To run the program, simply execute the Python file `main.py`:

```bash
python main.py
```

The program will display a menu with the following options:
1. **🔒 Encrypt Text**: Enter the text you want to encrypt. You will also be prompted to save the encrypted data to a file. By default, this file is named `keys.txt`.
2. **🔓 Decrypt Text**: Enter the filename containing the encrypted data. The program will load and decrypt the data, then display the result or save it as a binary file if the decryption results in non-text data.
3. **❌ Exit**: Exit the program.

### Example of Encryption 💬:
```
Enter the text to encrypt: Hello, World!
Encrypted Data: <base64_encoded_encrypted_data>
Metadata: {'key': 'base64_encoded_key', 'shift': 12, 'seed': 'base64_encoded_seed', 'operations': ['reverse_encrypt', 'xor_encrypt', 'shift_encrypt']}
```

### Example of Decryption 🔑:
```
Enter the filename to load (default: keys.txt): keys.txt
Decrypted Data: Hello, World!
```

If the decrypted data is binary, it will be saved as `keys.bin`.

### Save and Load Files 💾:
Encrypted data, along with the metadata, is saved into a `.txt` file with the following structure:
```
Encrypted Data: <encrypted_data>
Metadata: {'key': '<key>', 'shift': <shift>, 'seed': '<seed>', 'operations': ['operation1', 'operation2']}
```

## Dependencies 📦
- Python 3.x
- No external libraries required (uses built-in libraries: `random`, `base64`, `os`).

## Collaborating 🤝
We welcome contributions! If you'd like to improve or add new features to this project, feel free to fork this repository and submit a pull request. Here are some ways you can help:

- Add more encryption algorithms: Contribute new encryption techniques to make the program even more secure.
- Improve error handling: Help make the program more robust by improving its error handling for various edge cases.
- Documentation: Improve the documentation to make it easier for others to contribute.

Thanks for checking out!
