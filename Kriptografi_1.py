import tkinter as tk
from tkinter import filedialog, Text, messagebox
import numpy as np

def encrypt_text_vigenere(plain_text, key):
    key = key.lower()
    encrypted_text = []
    key_index = 0

    for char in plain_text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 97
            if char.islower():
                encrypted_text.append(chr((ord(char) - 97 + shift) % 26 + 97))
            else:
                encrypted_text.append(chr((ord(char) - 65 + shift) % 26 + 65))
            key_index += 1
        else:
            encrypted_text.append(char)
    return ''.join(encrypted_text)

def decrypt_text_vigenere(encrypted_text, key):
    key = key.lower()
    decrypted_text = []
    key_index = 0

    for char in encrypted_text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 97
            if char.islower():
                decrypted_text.append(chr((ord(char) - 97 - shift) % 26 + 97))
            else:
                decrypted_text.append(chr((ord(char) - 65 - shift) % 26 + 65))
            key_index += 1
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)

def encrypt_text_playfair(plain_text, key):
    plain_text =  removeSpaces(toLowerCase(plain_text))
    PlainTextList = Diagraph(FillerLetter(plain_text))
    if len(PlainTextList[-1]) != 2:
        PlainTextList[-1] = PlainTextList[-1]+'z'
    key = toLowerCase(key)
    Matrix = generateKeyTable(key, list1)
    CipherList = encryptByPlayfairCipher(Matrix, PlainTextList)
    CipherText = ""
    for i in CipherList:
        CipherText += i
    return ''.join(CipherText)

def generateKeyTable(word, list1):
    key_letters = []
    for i in word:
        if i not in key_letters:
            key_letters.append(i)

    compElements = []
    for i in key_letters:
        if i not in compElements:
            compElements.append(i)
    for i in list1:
        if i not in compElements:
            compElements.append(i)

    matrix = []
    while compElements != []:
        matrix.append(compElements[:5])
        compElements = compElements[5:]

    return matrix

def search(mat, element):
    for i in range(5):
        for j in range(5):
            if(mat[i][j] == element):
                return i, j

def encrypt_RowRule(matr, e1r, e1c, e2r, e2c):
    char1 = ''
    if e1c == 4:
        char1 = matr[e1r][0]
    else:
        char1 = matr[e1r][e1c+1]

    char2 = ''
    if e2c == 4:
        char2 = matr[e2r][0]
    else:
        char2 = matr[e2r][e2c+1]

    return char1, char2

def encrypt_ColumnRule(matr, e1r, e1c, e2r, e2c):
    char1 = ''
    if e1r == 4:
        char1 = matr[0][e1c]
    else:
        char1 = matr[e1r+1][e1c]

    char2 = ''
    if e2r == 4:
        char2 = matr[0][e2c]
    else:
        char2 = matr[e2r+1][e2c]

    return char1, char2

def encrypt_RectangleRule(matr, e1r, e1c, e2r, e2c):
    char1 = ''
    char1 = matr[e1r][e2c]

    char2 = ''
    char2 = matr[e2r][e1c]

    return char1, char2

def encryptByPlayfairCipher(Matrix, plainList):
    CipherText = []
    for i in range(0, len(plainList)):
        c1 = 0
        c2 = 0
        print(plainList[i][0])
        ele1_x, ele1_y = search(Matrix, plainList[i][0])
        ele2_x, ele2_y = search(Matrix, plainList[i][1])

        if ele1_x == ele2_x:
            c1, c2 = encrypt_RowRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)

        elif ele1_y == ele2_y:
            c1, c2 = encrypt_ColumnRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        else:
            c1, c2 = encrypt_RectangleRule(
                Matrix, ele1_x, ele1_y, ele2_x, ele2_y)

        cipher = c1 + c2
        CipherText.append(cipher)
    return CipherText

list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm',
         'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def FillerLetter(text):
    k = len(text)
    if k % 2 == 0:
        for i in range(0, k, 2):
            if text[i] == text[i+1]:
                new_word = text[0:i+1] + str('x') + text[i+1:]
                new_word = FillerLetter(new_word)
                break
            else:
                new_word = text
    else:
        for i in range(0, k-1, 2):
            if text[i] == text[i+1]:
                new_word = text[0:i+1] + str('x') + text[i+1:]
                new_word = FillerLetter(new_word)
                break
            else:
                new_word = text
    return new_word

def Diagraph(text):
    Diagraph = []
    group = 0
    for i in range(2, len(text), 2):
        Diagraph.append(text[group:i])

        group = i
    Diagraph.append(text[group:])
    return Diagraph

def removeSpaces(text):
    newText = ""
    for i in text:
        if i == " ":
            continue
        else:
            newText = newText + i
    return newText

def toLowerCase(text):
    return text.lower()

def remove_spaces(text):
    return text.replace(" ", "")

def generate_key_table(key):
    key = remove_spaces(toLowerCase(key))
    key = key.replace('j', 'i')
    key = ''.join(dict.fromkeys(key))  

    alphabet = "abcdefghiklmnopqrstuvwxyz"  
    key_table = [c for c in key if c in alphabet]

    for char in alphabet:
        if char not in key_table:
            key_table.append(char)

    key_table = np.array(key_table).reshape(5, 5)
    return key_table

def search2(key_table, a, b):
    if a == 'j':
        a = 'i'
    if b == 'j':
        b = 'i'

    p1 = p2 = None
    for i in range(5):
        for j in range(5):
            if key_table[i, j] == a:
                p1 = (i, j)
            elif key_table[i, j] == b:
                p2 = (i, j)
    return p1, p2

def decrypt_text_playfair(cipher, key):

    if len(cipher) % 2 != 0:
        cipher += 'x'  

    key_table = generate_key_table(key)
    deciphered = []

    for i in range(0, len(cipher), 2):
        p1, p2 = search2(key_table, cipher[i], cipher[i+1])

        if p1[0] == p2[0]:

            deciphered.append(key_table[p1[0], (p1[1]-1) % 5])
            deciphered.append(key_table[p2[0], (p2[1]-1) % 5])
        elif p1[1] == p2[1]:

            deciphered.append(key_table[(p1[0]-1) % 5, p1[1]])
            deciphered.append(key_table[(p2[0]-1) % 5, p2[1]])
        else:

            deciphered.append(key_table[p1[0], p2[1]])
            deciphered.append(key_table[p2[0], p1[1]])

    decrypted_text = ''.join(deciphered)

    if decrypted_text.endswith('x'):
        decrypted_text = decrypted_text[:-1]

    return decrypted_text

keyMatrix = [[0] * 3 for i in range(3)]

messageVector = [[0] for i in range(3)]

cipherMatrix = [[0] for i in range(3)]

def getKeyMatrix(key):
    k = 0
    for i in range(3):
        for j in range(3):
            keyMatrix[i][j] = ord(key[k]) % 65
            k += 1

def encrypt(messageVector):
    for i in range(3):
        for j in range(1):
            cipherMatrix[i][j] = 0
            for x in range(3):
                cipherMatrix[i][j] += (keyMatrix[i][x] *
                                       messageVector[x][j])
            cipherMatrix[i][j] = cipherMatrix[i][j] % 26

def encrypt_text_hill(message, key):

    getKeyMatrix(key)

    for i in range(3):
        messageVector[i][0] = ord(message[i]) % 65

    encrypt(messageVector)

    CipherText = []
    for i in range(3):
        CipherText.append(chr(cipherMatrix[i][0] + 65))

    return "".join(CipherText)

def decrypt_text_hill(cipher_text, key):
    cipher_text = cipher_text.upper()

    n = int(len(cipher_text) ** 0.5)  

    if n * n != len(cipher_text):
        raise ValueError("Ciphertext length must be a perfect square (e.g., 4, 9, 16 characters)")

    key_matrix = create_key_matrix(key, n)

    cipher_vector = [ord(char) - 65 for char in cipher_text]

    key_matrix_mod_inv = Matrix(key_matrix).inv_mod(26)
    key_matrix_mod_inv = np.array(key_matrix_mod_inv).astype(int)

    decrypted_vector = np.dot(key_matrix_mod_inv, cipher_vector) % 26

    decrypted_text = ''.join([chr(num + 65) for num in decrypted_vector])

    return ''.join(decrypted_text)

def create_key_matrix(key, n):
    key = key.lower()  
    key_matrix = []

    for char in key:
        key_matrix.append(ord(char) - ord('a'))  

    while len(key_matrix) < n**2:
        key_matrix.extend(key_matrix[:n**2 - len(key_matrix)])

    return np.array(key_matrix).reshape(n, n)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            file_content = file.read()
            input_text.delete(1.0, tk.END)
            input_text.insert(tk.END, file_content)

def process_text():
    input_content = input_text.get("1.0", tk.END).strip()
    key = key_entry.get()

    if len(key) < 12:
        messagebox.showwarning("Error", "Kunci harus minimal 12 karakter.")
        return

    method = method_var.get()

    if method == "Vigenère":
        if encrypt_var.get():
            processed_content = encrypt_text_vigenere(input_content, key)
        else:
            processed_content = decrypt_text_vigenere(input_content, key)
    elif method == "Playfair":
        if encrypt_var.get():
            processed_content = encrypt_text_playfair(input_content, key)
        else:
            processed_content = decrypt_text_playfair(input_content, key)
    elif method == "Hill":
        if encrypt_var.get():
            processed_content = encrypt_text_hill(input_content, key)
        else:
            processed_content = decrypt_text_hill(input_content, key)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, processed_content)

root = tk.Tk()
root.title("Cipher - Enkripsi & Dekripsi")

input_text = Text(root, height=5, width=50)
input_text.pack(pady=10)

open_file_button = tk.Button(root, text="Buka File .txt", command=open_file)
open_file_button.pack(pady=5)

key_label = tk.Label(root, text="Masukkan kunci (minimal 12 karakter):")
key_label.pack(pady=5)
key_entry = tk.Entry(root, width=50)
key_entry.pack(pady=5)

method_var = tk.StringVar(value="Vigenère")
method_label = tk.Label(root, text="Pilih metode:")
method_label.pack(pady=5)
method_menu = tk.OptionMenu(root, method_var, "Vigenère", "Playfair", "Hill")
method_menu.pack(pady=5)

encrypt_var = tk.BooleanVar(value=True)
encrypt_checkbox = tk.Checkbutton(root, text="Enkripsi", variable=encrypt_var)
encrypt_checkbox.pack(pady=5)

process_button = tk.Button(root, text="Proses Teks", command=process_text)
process_button.pack(pady=5)

output_text = Text(root, height=10, width=50)
output_text.pack(pady=10)

root.mainloop()