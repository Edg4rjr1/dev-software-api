import customtkinter as ctk
import sqlite3
from tkinter import ttk, messagebox

# --- MUDANÇA 1: Mudar de ctk.CTk para ctk.CTkToplevel
class TelaInicial(ctk.CTkToplevel): 
    
    # --- MUDANÇA 2: Receber 'master' (a TelaLogin) no __init__
    def __init__(self, master): 
        
        # --- MUDANÇA 3: Passar 'master' para o super()
        super().__init__(master) 

        self.title("Sistema - CRUD de Pessoas")
        # Aumentei um pouco a altura para caber o botão de logout
        self.geometry("700x500") 
        self.resizable(False, False)
        
        # --- MUDANÇA 4: Linhas essenciais de gerenciamento de janela
        self.transient(master) # Mantém esta janela na frente da master
        self.grab_set()        # Foca o input do usuário nesta janela (modal)
        
        # --- MUDANÇA 5: Lidar com o clique no 'X' da janela
        # Se fechar esta janela (CRUD), fecha o app inteiro.
        self.protocol("WM_DELETE_WINDOW", self.fechar_aplicativo)

        # O 'master' é a TelaLogin, vamos guardá-lo
        self.master = master 

        # --- O RESTO DO SEU CÓDIGO DO CRUD (sem alterações) ---
        
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nome = ctk.CTkEntry(frame, width=200)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame, text="Idade:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_idade = ctk.CTkEntry(frame, width=200)
        self.entry_idade.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_email = ctk.CTkEntry(frame, width=200)
        self.entry_email.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame, text="Telefone:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_telefone = ctk.CTkEntry(frame, width=200)
        self.entry_telefone.grid(row=3, column=1, padx=5, pady=5)

        ctk.CTkButton(frame, text="Cadastrar", command=self.cadastrar).grid(row=4, column=0, padx=5, pady=10)
        ctk.CTkButton(frame, text="Atualizar", command=self.atualizar).grid(row=4, column=1, padx=5, pady=10)
        ctk.CTkButton(frame, text="Excluir", command=self.excluir).grid(row=4, column=2, padx=5, pady=10)
        ctk.CTkButton(frame, text="Limpar", command=self.limpar_campos).grid(row=4, column=3, padx=5, pady=10)

        self.tabela = ttk.Treeview(frame, columns=("id", "nome", "idade", "email", "telefone"), show="headings", height=8)
        self.tabela.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("idade", text="Idade")
        self.tabela.heading("email", text="Email")
        self.tabela.heading("telefone", text="Telefone")

        self.tabela.bind("<ButtonRelease-1>", self.selecionar_linha)
        
        # --- MUDANÇA 6: Adicionar um botão de Logout (opcional, mas recomendado)
        ctk.CTkButton(frame, text="Fazer Logout", fg_color="#c0392b", hover_color="#922b21", command=self.fazer_logout).grid(row=6, column=0, columnspan=4, pady=10)

        self.carregar_dados()

    # --- MUDANÇA 7: Adicionar as funções de fechar e logout ---
    
    def fechar_aplicativo(self):
        """Fecha o aplicativo inteiro quando o 'X' é clicado."""
        print("Fechando aplicativo a partir da TelaInicial...")
        # self.master é a TelaLogin. Destruir ela fecha o app.
        self.master.destroy() 

    def fazer_logout(self):
        """Fecha esta janela (CRUD) e re-exibe a TelaLogin."""
        print("Fazendo logout...")
        self.destroy() # Fecha a si mesma (TelaInicial)
        self.master.deiconify() # Re-exibe a TelaLogin

    # --- O RESTO DAS SUAS FUNÇÕES (conectar, carregar_dados, etc.) ---
    # --- NÃO PRECISAM DE NENHUMA ALTERAÇÃO ---

    def conectar(self):
        return sqlite3.connect("banco.db")

    def carregar_dados(self):
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM pessoas")
        registros = cursor.fetchall()
        conexao.close()

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for linha in registros:
            self.tabela.insert("", "end", values=linha)

    def cadastrar(self):
        nome = self.entry_nome.get()
        idade = self.entry_idade.get()
        email = self.entry_email.get()
        telefone = self.entry_telefone.get()

        if nome == "" or idade == "":
            messagebox.showwarning("Atenção", "Nome e idade são obrigatórios!")
            return

        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO pessoas (nome, idade, email, telefone) VALUES (?, ?, ?, ?)",
                       (nome, idade, email, telefone))
        conexao.commit()
        conexao.close()

        self.carregar_dados()
        self.limpar_campos()

    def atualizar(self):
        try:
            item = self.tabela.selection()[0]
            id_registro = self.tabela.item(item)["values"][0]
        except:
            messagebox.showwarning("Atenção", "Selecione um registro!")
            return

        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            UPDATE pessoas
            SET nome=?, idade=?, email=?, telefone=?
            WHERE id=?
        """, (
            self.entry_nome.get(),
            self.entry_idade.get(),
            self.entry_email.get(),
            self.entry_telefone.get(),
            id_registro
        ))
        conexao.commit()
        conexao.close()

        self.carregar_dados()
        self.limpar_campos()

    def excluir(self):
        try:
            item = self.tabela.selection()[0]
            id_registro = self.tabela.item(item)["values"][0]
        except:
            messagebox.showwarning("Atenção", "Selecione um registro!")
            return

        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM pessoas WHERE id=?", (id_registro,))
        conexao.commit()
        conexao.close()

        self.carregar_dados()
        self.limpar_campos()

    def limpar_campos(self):
        self.entry_nome.delete(0, "end")
        self.entry_idade.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_telefone.delete(0, "end")

    def selecionar_linha(self, event):
        try:
            item = self.tabela.selection()[0]
            dados = self.tabela.item(item)["values"]

            self.entry_nome.delete(0, "end")
            self.entry_idade.delete(0, "end")
            self.entry_email.delete(0, "end")
            self.entry_telefone.delete(0, "end")

            self.entry_nome.insert(0, dados[1])
            self.entry_idade.insert(0, dados[2])
            self.entry_email.insert(0, dados[3])
            self.entry_telefone.insert(0, dados[4])
        except:
            pass