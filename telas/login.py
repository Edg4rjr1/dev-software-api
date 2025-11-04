import customtkinter as ctk
from tkinter import messagebox
from api.api import enviar
from api.criptografia import encrypt

class TelaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("500x420")
        self.url_normal = "https://datse.com.br/dev/syncjava.php"
        self.url_seguro = "https://datse.com.br/dev/syncjava2.php"

        self.entry_login = ctk.CTkEntry(self, placeholder_text="Usuário")
        self.entry_login.pack(pady=10)

        self.entry_senha = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.entry_senha.pack(pady=10)

        ctk.CTkButton(self, text="Login sem segurança", command=self.login_simples).pack(pady=5)
        ctk.CTkButton(self, text="Login Seguro", command=self.login_seguro).pack(pady=5)

    def login_simples(self):
        dados = {"usuario": self.entry_login.get(), "senha": self.entry_senha.get()}
        status, resposta = enviar(self.url_normal, dados)
        messagebox.showinfo("Resultado", f"Status: {status}\n{resposta}")

    def login_seguro(self):
        dados = {"usuario": self.entry_login.get(), "senha": encrypt(self.entry_senha.get())}
        status, resposta = enviar(self.url_seguro, dados)
        messagebox.showinfo("Resultado", f"Status: {status}\n{resposta}")
