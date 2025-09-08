import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from banco_setup import criar_banco

def verificar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username=? AND senha=?", (usuario, senha))
    resultado = cursor.fetchone()
    conexao.close()

    if resultado:
        messagebox.showinfo("Login", "Login bem-sucedido!")
        janela_login.destroy()
        abrir_crud()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")

def abrir_crud():
    crud = tk.Tk()
    crud.title("Sistema de Pessoas")
    crud.geometry("700x450")
    crud.configure(bg="#2C2F33")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#23272A",
                    foreground="white",
                    fieldbackground="#23272A",
                    rowheight=25,
                    font=("Arial", 11))
    style.map("Treeview", background=[("selected", "#7289DA")])

    style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#7289DA", foreground="white")

    # Frame formulário
    frame_form = tk.LabelFrame(crud, text="Cadastro", padx=10, pady=10, bg="#2C2F33", fg="white", font=("Arial", 12, "bold"))
    frame_form.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_form, text="Nome:", bg="#2C2F33", fg="white", font=("Arial", 11)).grid(row=0, column=0, sticky="w")
    nome_entry = tk.Entry(frame_form, width=25, font=("Arial", 11))
    nome_entry.grid(row=0, column=1, padx=5)

    tk.Label(frame_form, text="Idade:", bg="#2C2F33", fg="white", font=("Arial", 11)).grid(row=0, column=2, sticky="w")
    idade_entry = tk.Entry(frame_form, width=10, font=("Arial", 11))
    idade_entry.grid(row=0, column=3, padx=5)

    tk.Label(frame_form, text="Email:", bg="#2C2F33", fg="white", font=("Arial", 11)).grid(row=1, column=0, sticky="w")
    email_entry = tk.Entry(frame_form, width=25, font=("Arial", 11))
    email_entry.grid(row=1, column=1, padx=5)

    tk.Label(frame_form, text="Telefone:", bg="#2C2F33", fg="white", font=("Arial", 11)).grid(row=1, column=2, sticky="w")
    telefone_entry = tk.Entry(frame_form, width=15, font=("Arial", 11))
    telefone_entry.grid(row=1, column=3, padx=5)

    def listar():
        for row in tabela.get_children():
            tabela.delete(row)
        conexao = sqlite3.connect("banco.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM pessoas")
        for linha in cursor.fetchall():
            tabela.insert("", "end", values=linha)
        conexao.close()



    def adicionar():
        nome = nome_entry.get()
        idade = idade_entry.get()
        email = email_entry.get()
        telefone = telefone_entry.get()

        if nome and idade.isdigit():
            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO pessoas (nome, idade, email, telefone) VALUES (?, ?, ?, ?)",
                           (nome, int(idade), email, telefone))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Pessoa adicionada!")
            listar()
        else:
            messagebox.showwarning("Erro", "Preencha os campos corretamente!")

    def atualizar():
        selecionado = tabela.selection()
        if selecionado:
            item = tabela.item(selecionado)
            pessoa_id = item["values"][0]

            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("UPDATE pessoas SET nome=?, idade=?, email=?, telefone=? WHERE id=?",
                           (nome_entry.get(), int(idade_entry.get()), email_entry.get(), telefone_entry.get(), pessoa_id))
            conexao.commit()
            conexao.close()
            listar()
        else:
            messagebox.showwarning("Erro", "Selecione uma pessoa na tabela!")

    def deletar():
        selecionado = tabela.selection()
        if selecionado:
            item = tabela.item(selecionado)
            pessoa_id = item["values"][0]

            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM pessoas WHERE id=?", (pessoa_id,))
            conexao.commit()
            conexao.close()
            listar()
        else:
            messagebox.showwarning("Erro", "Selecione uma pessoa na tabela!")

    # Botões
    frame_btn = tk.Frame(crud, bg="#2C2F33")
    frame_btn.pack(fill="x", padx=10, pady=5)

    tk.Button(frame_btn, text="Adicionar", command=adicionar, bg="#43B581", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Atualizar", command=atualizar, bg="#FAA61A", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Deletar", command=deletar, bg="#F04747", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Listar", command=listar, bg="#7289DA", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=5)

    # Tabela (Treeview)
    colunas = ("ID", "Nome", "Idade", "Email", "Telefone")
    tabela = ttk.Treeview(crud, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=120)
    tabela.pack(fill="both", expand=True, padx=10, pady=10)

    listar()
    crud.mainloop()

criar_banco() 
janela_login = tk.Tk()
janela_login.title("Login")
janela_login.geometry("300x150")
janela_login.configure(bg="#2C2F33")

tk.Label(janela_login, text="Usuário:", bg="#2C2F33", fg="white", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_usuario = tk.Entry(janela_login, font=("Arial", 11))
entry_usuario.grid(row=0, column=1, padx=10, pady=5)

tk.Label(janela_login, text="Senha:", bg="#2C2F33", fg="white", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_senha = tk.Entry(janela_login, show="*", font=("Arial", 11))
entry_senha.grid(row=1, column=1, padx=10, pady=5)

tk.Button(janela_login, text="Login", command=verificar_login, bg="#7289DA", fg="white", font=("Arial", 11, "bold")).grid(row=2, column=0, columnspan=2, pady=10)

janela_login.mainloop()