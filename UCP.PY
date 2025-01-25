import tkinter as tk
from tkinter import messagebox
import sqlite3

# Kelas untuk mengelola database SQLite
class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect_db()

    def connect_db(self):
        """koneksi ke database SQLite"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        """Membuat tabel"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            umur INTEGER NOT NULL,
            alamat TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def insert_data(self, nama, umur, alamat):
        """nyimpan data ke dalam database"""
        self.cursor.execute("INSERT INTO users (nama, umur, alamat) VALUES (?, ?, ?)",
                            (nama, umur, alamat))
        self.conn.commit()

    def fetch_all_data(self):
        """ambil semua data dari database"""
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def close(self):
        """Menutup koneksi database"""
        self.conn.close()


# Kelas untuk aplikasi utama
class Aplikasi:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.db.create_table()  # Membuat tabel jika belum ada
        self.setup_gui()

    def setup_gui(self):
        """Menyiapkan tampilan GUI"""
        self.root.title("Aplikasi Penginputan Data")

        # Membuat label dan entry untuk Nama
        self.label_nama = tk.Label(self.root, text="Nama:")
        self.label_nama.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_nama = tk.Entry(self.root, width=30)
        self.entry_nama.grid(row=0, column=1, padx=10, pady=5)

        # Membuat label dan entry untuk Umur
        self.label_umur = tk.Label(self.root, text="Umur:")
        self.label_umur.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_umur = tk.Entry(self.root, width=30)
        self.entry_umur.grid(row=1, column=1, padx=10, pady=5)

        # Membuat label dan entry untuk Alamat
        self.label_alamat = tk.Label(self.root, text="Alamat:")
        self.label_alamat.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_alamat = tk.Entry(self.root, width=30)
        self.entry_alamat.grid(row=2, column=1, padx=10, pady=5)

        # Tombol untuk mengirim data
        self.submit_button = tk.Button(self.root, text="Kirim Data", command=self.submit_data)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Tombol untuk menampilkan data yang tersimpan
        self.show_button = tk.Button(self.root, text="Tampilkan Data", command=self.show_data)
        self.show_button.grid(row=4, column=0, columnspan=2, pady=10)

    def submit_data(self):
        """simpan data ke database SQLite"""
        nama = self.entry_nama.get()
        umur = self.entry_umur.get()
        alamat = self.entry_alamat.get()

        # Validasi input
        if not nama or not umur or not alamat:
            messagebox.showwarning("Input Error", "Semua data harus diisi!")
            return

        try:
            umur = int(umur)  # Pastikan umur adalah angka
        except ValueError:
            messagebox.showwarning("Input Error", "Umur harus berupa angka!")
            return

        # Simpan data ke database
        self.db.insert_data(nama, umur, alamat)
        messagebox.showinfo("Data Tersimpan", "Data berhasil disimpan!")

        # Clear entry fields setelah data disimpan
        self.entry_nama.delete(0, tk.END)
        self.entry_umur.delete(0, tk.END)
        self.entry_alamat.delete(0, tk.END)

    def show_data(self):
        """show data yang sudah disimpan dalam database"""
        data = self.db.fetch_all_data()
        if data:
            data_str = "\n".join([f"ID: {row[0]}, Nama: {row[1]}, Umur: {row[2]}, Alamat: {row[3]}" for row in data])
            messagebox.showinfo("Data yang Tersimpan", data_str)
        else:
            messagebox.showinfo("Data ga ada", "Tidak ada data dalam database.")


# Main program
def main():
    db = Database('data.db')
    root = tk.Tk()
    app = Aplikasi(root, db)
    root.mainloop()
    db.close()


if __name__ == "__main__":
    main()
