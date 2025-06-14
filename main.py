import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import time

# === Struktur Node & BST ===
class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        if self.root is None:
            self.root = Node(key, data)
        else:
            self._insert(self.root, key, data)

    def _insert(self, current, key, data):
        if key < current.key:
            if current.left is None:
                current.left = Node(key, data)
            else:
                self._insert(current.left, key, data)
        else:
            if current.right is None:
                current.right = Node(key, data)
            else:
                self._insert(current.right, key, data)

    def trace_search_path(self, key):
        path = []
        self._trace_path(self.root, key, path)
        return path

    def _trace_path(self, current, key, path):
        if current is None:
            return
        path.append(current.data)
        if key == current.key:
            return
        elif key < current.key:
            self._trace_path(current.left, key, path)
        else:
            self._trace_path(current.right, key, path)

# === Struktur AVL ===
class AVLNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if not node:
            return AVLNode(key, data)
        if key < node.key:
            node.left = self._insert(node.left, key, data)
        else:
            node.right = self._insert(node.right, key, data)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        # Rotasi
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def search(self, key):
        path = []
        return self._search(self.root, key, path), path

    def _search(self, node, key, path):
        if not node:
            return None
        path.append(node.data)
        if key == node.key:
            return node.data
        elif key < node.key:
            return self._search(node.left, key, path)
        else:
            return self._search(node.right, key, path)

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        return x

    def _get_height(self, node):
        return node.height if node else 0

    def _get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

# === Aplikasi GUI ===
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Pencarian Data Mahasiswa - BST vs AVL")

        self.data = pd.read_excel("urut.xlsx")
        self.data.columns = self.data.columns.str.strip()

        self.bst = BST()
        self.avl = AVLTree()
        self.build_trees()

        self.build_gui()

    def build_trees(self):
        for _, row in self.data.iterrows():
            nama = str(row['Nama Lengkap']).strip().lower()
            record = row.to_dict()
            self.bst.insert(nama, record)
            self.avl.insert(nama, record)

    def build_gui(self):
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack()

        tk.Label(self.frame, text="Masukkan Nama:").grid(row=0, column=0)
        self.entry_nama = tk.Entry(self.frame, width=30)
        self.entry_nama.grid(row=0, column=1)

        tk.Button(self.frame, text="🌳 Cari BST", command=self.search_bst).grid(row=1, column=0)
        tk.Button(self.frame, text="🌲 Cari AVL", command=self.search_avl).grid(row=1, column=1)
        tk.Button(self.frame, text="📋 Tampilkan Semua", command=self.show_all).grid(row=2, column=0, columnspan=2)

        self.label_waktu = tk.Label(self.root, text="Waktu: -", fg="blue", pady=5)
        self.label_waktu.pack()

        self.tree = ttk.Treeview(self.root, columns=self.data.columns.tolist(), show='headings')
        for col in self.data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def show_all(self):
        self.tree.delete(*self.tree.get_children())
        for _, row in self.data.iterrows():
            self.tree.insert('', 'end', values=list(row))
        self.label_waktu.config(text="Waktu: -")

    def search_bst(self):
        nama = self.entry_nama.get().strip().lower()
        hasil = self.bst.trace_search_path(nama)

        self.tree.delete(*self.tree.get_children())
        if hasil:
            for data in hasil:
                self.tree.insert('', 'end', values=list(data.values()))
        else:
            messagebox.showinfo("Hasil", "Data tidak ditemukan di BST.")

    def search_avl(self):
        nama = self.entry_nama.get().strip().lower()
        hasil, path = self.avl.search(nama)

        self.tree.delete(*self.tree.get_children())
        if hasil:
            for data in path:
                self.tree.insert('', 'end', values=list(data.values()))
        else:
            messagebox.showinfo("Hasil", "Data tidak ditemukan di AVL.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
