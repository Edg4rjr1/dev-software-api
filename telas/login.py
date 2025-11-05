import customtkinter as ctk
from tkinter import messagebox
from api.api import enviar
from api.criptografia import encrypt
from telas.telaInicial import TelaInicial

class TelaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("400x380") 
        self.resizable(False, False)

        self.url_normal = "https://datse.com.br/dev/syncjava.php"
        self.url_seguro = "https://datse.com.br/dev/syncjava2.php"

        # Container principal
        self.frame = ctk.CTkFrame(self, corner_radius=20)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="Acesso ao Sistema", font=("Arial", 18, "bold")).pack(pady=10)

        # Usuário
        ctk.CTkLabel(self.frame, text="Usuário:").pack(anchor="w", padx=40)
        self.entry_login = ctk.CTkEntry(self.frame, width=250)
        self.entry_login.pack(pady=5)

        # Senha
        ctk.CTkLabel(self.frame, text="Senha:").pack(anchor="w", padx=40)
        self.entry_senha = ctk.CTkEntry(self.frame, width=250, show="*")
        self.entry_senha.pack(pady=5)

        # Botões
        ctk.CTkButton(self.frame, text="Logar", width=200, command=self.login_simples).pack(pady=10)
        ctk.CTkButton(self.frame, text="Logar Criptografado", width=200, command=self.login_seguro).pack(pady=5)
        ctk.CTkButton(self.frame, text="Fechar", width=200, fg_color="#c0392b", hover_color="#922b21", command=self.destroy).pack(pady=15)

    def abrir_tela_principal(self):
        self.withdraw()
        TelaInicial(self)

    def login_simples(self):
        usuario = self.entry_login.get()
        senha = self.entry_senha.get()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Por favor, preencha usuário e senha.")
            return

        dados = {"usuario": usuario, "senha": senha}
        status, resposta = enviar(self.url_normal, dados)

        # --- MUDANÇA ---
        # A mensagem agora é formatada ANTES da verificação
        mensagem_api = f"Status Code: {status}\n\nResposta: {resposta}"

        if "sucesso" in resposta.lower():
            # Mostra o alert de SUCESSO
            messagebox.showinfo("Sucesso - API Simples", mensagem_api)
            # Abre a tela principal
            self.abrir_tela_principal()
        else:
            # Mostra o alert de ERRO
            messagebox.showerror("Erro - API Simples", mensagem_api)

    def login_seguro(self):
        usuario = self.entry_login.get()
        senha = self.entry_senha.get()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Por favor, preencha usuário e senha.")
            return

        senha_cript = encrypt(senha)

        dados = {"usuario": usuario, "senha": senha_cript}
        status, resposta = enviar(self.url_seguro, dados)

        # --- MUDANÇA ---
        # A mensagem agora é formatada ANTES da verificação
        mensagem_api = f"Status Code: {status}\n\nResposta: {resposta}"

        if "sucesso" in resposta.lower():
            # Mostra o alert de SUCESSO
            messagebox.showinfo("Sucesso - API Segura (AES)", mensagem_api)
            # Abre a tela principal
            self.abrir_tela_principal()
        else:
            # Mostra o alert de ERRO
            messagebox.showerror("Erro - API Segura (AES)", mensagem_api)