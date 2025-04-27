import secrets
import string
import tkinter as tk
from tkinter import messagebox

# Funktion zur Passwortgenerierung
def generate_secure_password(length=12, use_special_chars=True, use_digits=True, use_uppercase=True, use_lowercase=True):
    alphabet = ""

    if use_lowercase:
        alphabet += string.ascii_lowercase  # Kleinbuchstaben
    if use_uppercase:
        alphabet += string.ascii_uppercase  # Großbuchstaben
    if use_digits:
        alphabet += string.digits  # Zahlen
    if use_special_chars:
        alphabet += string.punctuation  # Sonderzeichen

    if not alphabet:
        raise ValueError("Kein Zeichenpool ausgewählt! Wähle mindestens eine Zeichenart.")
    
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

# Funktion, die die Eingaben von der GUI liest und das Passwort generiert
def generate_password():
    try:
        length = int(length_entry.get())
        use_special_chars = special_chars_var.get()
        use_digits = digits_var.get()
        use_uppercase = uppercase_var.get()
        use_lowercase = lowercase_var.get()

        # Passwort generieren
        password = generate_secure_password(length, use_special_chars, use_digits, use_uppercase, use_lowercase)
        
        # Das generierte Passwort in das Textfeld ausgeben
        password_output.delete(0, tk.END)  # Lösche vorheriges Passwort
        password_output.insert(tk.END, password)
    
    except ValueError as e:
        messagebox.showerror("Fehler", f"Ungültige Eingabe: {e}")

# GUI-Anwendung
root = tk.Tk()
root.title("Passwort Generator")

# Länge des Passworts
length_label = tk.Label(root, text="Länge des Passworts:")
length_label.grid(row=0, column=0, padx=10, pady=10)

length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1, padx=10, pady=10)

# Checkboxen für Auswahl von Zeichenarten
lowercase_var = tk.BooleanVar(value=True)
lowercase_checkbox = tk.Checkbutton(root, text="Kleinbuchstaben", variable=lowercase_var)
lowercase_checkbox.grid(row=1, column=0, padx=10, pady=5)

uppercase_var = tk.BooleanVar(value=True)
uppercase_checkbox = tk.Checkbutton(root, text="Großbuchstaben", variable=uppercase_var)
uppercase_checkbox.grid(row=1, column=1, padx=10, pady=5)

digits_var = tk.BooleanVar(value=True)
digits_checkbox = tk.Checkbutton(root, text="Zahlen", variable=digits_var)
digits_checkbox.grid(row=2, column=0, padx=10, pady=5)

special_chars_var = tk.BooleanVar(value=True)
special_chars_checkbox = tk.Checkbutton(root, text="Sonderzeichen", variable=special_chars_var)
special_chars_checkbox.grid(row=2, column=1, padx=10, pady=5)

# Button zum Generieren des Passworts
generate_button = tk.Button(root, text="Passwort generieren", command=generate_password)
generate_button.grid(row=3, column=0, columnspan=2, pady=10)

# Textfeld, um das generierte Passwort anzuzeigen
password_output_label = tk.Label(root, text="Generiertes Passwort:")
password_output_label.grid(row=4, column=0, padx=10, pady=10)

password_output = tk.Entry(root, width=30)
password_output.grid(row=4, column=1, padx=10, pady=10)

# Starten der GUI
root.mainloop()
