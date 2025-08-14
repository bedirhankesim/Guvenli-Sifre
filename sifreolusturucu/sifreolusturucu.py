import random
import string
import tkinter as tk
from PIL import Image, ImageTk
import pyperclip
import os
import sys

# Şifre oluşturma fonksiyonu
def password_generator(length=15):
    if length < 10:
        length = 15  # En az 10 karakter, ama biz 15 sabitledik
    
    # Karakter setleri
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    punctuation = string.punctuation
    all_chars = lowercase + uppercase + digits + punctuation
    
    # Harflerin çoğunlukta olması için ağırlıklar
    weights = (
        [1.0] * len(lowercase) +  # Küçük harfler
        [1.0] * len(uppercase) +  # Büyük harfler
        [0.2] * len(digits) +     # Rakamlar (düşük ağırlık)
        [0.2] * len(punctuation)  # Özel karakterler (düşük ağırlık)
    )
    
    while True:
        # En az birer tane zorunlu karakter
        password = [
            random.choice(lowercase),  # En az 1 küçük harf
            random.choice(uppercase),  # En az 1 büyük harf
            random.choice(digits),     # En az 1 rakam
            random.choice(punctuation)  # En az 1 özel karakter
        ]
        
        # Kalan karakterleri ağırlıklı olarak seç
        remaining_length = length - 4
        password += random.choices(all_chars, weights=weights, k=remaining_length)
        
        # Şifreyi karıştır
        password = ''.join(random.sample(password, len(password)))
        
        # Şifrenin kurallara uyduğunu kontrol et
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password)):
            return password

# Şifre kontrol fonksiyonu
def password_checker(password):
    feedback = []  # Hata mesajları
    if len(password) < 10:
        feedback.append("Şifre en az 10 karakter olmalı.")
    if not any(c.islower() for c in password):
        feedback.append("Şifre en az bir küçük harf içermeli.")
    if not any(c.isupper() for c in password):
        feedback.append("Şifre en az bir büyük harf içermeli.")
    if not any(c.isdigit() for c in password):
        feedback.append("Şifre en az bir rakam içermeli.")
    if not any(c in string.punctuation for c in password):
        feedback.append("Şifre en az bir özel karakter içermeli.")
    if feedback:
        return "Şifre zayıf: " + " ".join(feedback)
    else:
        return "Şifre güçlü!"

# GUI fonksiyonları
def generate_password():
    password = password_generator()  # Yeni şifre üret
    password_entry.delete(0, tk.END)  # Giriş kutusunu temizle
    password_entry.insert(0, password)  # Şifreyi giriş kutusuna yaz
    copy_button.config(state=tk.NORMAL)  # Kopyala butonunu aktif et
    result_label.config(text="")  # Sonuç etiketini sıfırla

def copy_password():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        result_label.config(text="Şifre kopyalandı!", fg="green")
    else:
        result_label.config(text="Kopyalanacak şifre yok!", fg="red")

def check_password():
    password = password_entry.get()
    if password:
        result = password_checker(password)
        result_label.config(text=result, fg="green" if "güçlü" in result else "red")
    else:
        result_label.config(text="Lütfen bir şifre girin!", fg="red")

# Resim dosyasının yolunu dinamik olarak belirleme
def resource_path(relative_path):
    """EXE için dosya yolunu doğru şekilde al"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller ile çalışırken geçici klasörden al
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# GUI oluşturma
root = tk.Tk()
root.title("Şifre Oluşturucu")
root.geometry("450x500")
root.resizable(False, False)  # Pencere büyütme/küçültme engellendi
root.configure(bg="#f0f0f0")  # Arka plan rengi: açık gri

# Şifre oluştur butonu
generate_button = tk.Button(root, text="Şifre Oluştur", command=generate_password, bg="#FFC107", fg="black")
generate_button.pack(pady=10)

# Şifre giriş kutusu ve kopyala butonu (aynı satırda)
entry_frame = tk.Frame(root, bg="#f0f0f0")
entry_frame.pack(pady=10)
password_entry = tk.Entry(entry_frame, width=30)
password_entry.pack(side=tk.LEFT, padx=5)
copy_button = tk.Button(entry_frame, text="Kopyala", command=copy_password, state=tk.DISABLED, bg="#FFC107", fg="black")
copy_button.pack(side=tk.LEFT, padx=5)

# Şifre denetleme butonu
check_button = tk.Button(root, text="Şifreyi Denetle", command=check_password, bg="#FFC107", fg="black")
check_button.pack(pady=10)

# Sonuç etiketi
result_label = tk.Label(root, text="", wraplength=350, bg="#f0f0f0", fg="black")
result_label.pack(pady=5)

# Resim ekleme
try:
    image_path = resource_path("hana.png")
    image = Image.open(image_path)
    # Resmi pencereye sığdırmak için boyutlandır (örneğin, 300x300 piksel)
    image = image.resize((300, 300), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(root, image=photo, bg="#f0f0f0")
    image_label.image = photo  # Referansı tut
    image_label.pack(pady=5)
except Exception as e:
    result_label.config(text=f"Resim yüklenemedi: {str(e)}", fg="red")

# GUI başlat ve kapatma
root.mainloop()