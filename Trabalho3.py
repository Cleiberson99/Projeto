import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import funcoes
from PIL import Image, ImageTk

conexao = sqlite3.connect("usuarios.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
""")
conexao.commit()


def verificar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=? AND senha=?",
        (usuario, senha)
    )

    if cursor.fetchone():
        janela.withdraw()          
        abrir_tela_inicial(usuario)
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")



def abrir_criar_conta():
    criar = tk.Toplevel(janela)
    criar.title("Criar Conta")
    criar.geometry("400x300")

    frm_criar = ttk.Frame(criar, padding=10)
    frm_criar.pack(expand=True)

    ttk.Label(frm_criar, text="Criar nova conta", font=("Arial", 16)).pack(pady=10)

    tk.Label(frm_criar, text="Novo usuário:").pack()
    entry_novo_usuario = tk.Entry(frm_criar)
    entry_novo_usuario.pack()

    tk.Label(frm_criar, text="Nova senha:").pack()
    entry_nova_senha = tk.Entry(frm_criar, show="*")
    entry_nova_senha.pack()

    def salvar_conta():
        novo_usuario = entry_novo_usuario.get()
        nova_senha = entry_nova_senha.get()

        if novo_usuario == "" or nova_senha == "":
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        try:
            cursor.execute(
                "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
                (novo_usuario, nova_senha)
            )
            conexao.commit()
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            criar.destroy()

        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Usuário já existe!")

    tk.Button( frm_criar,text="Salvar",bg="Green",fg="White",activebackground="Dark green", activeforeground="Black", command=salvar_conta).pack(pady=10)

def abrir_tela_inicial(usuario_logado):

    tela = tk.Toplevel(janela)
    tela.title("Tela Inicial")
    tela.geometry("900x600")

    frm_tela = ttk.Frame(tela, padding=10)
    frm_tela.pack(expand=True, fill="both")

    ttk.Label(frm_tela,text="Mega Swag Video Games",font=("Arial", 20)).pack(pady=20)
    ttk.Label(frm_tela,text=f"Bem-vindo, {usuario_logado}!",font=("Arial", 14)).pack(pady=10)

janela = tk.Tk()
janela.title("Sistema de Login")
janela.geometry("800x600")

frm = ttk.Frame(janela, padding=10)
frm.pack(expand=True)

ttk.Label(frm, text="Mega Swag Video Games", font=("Arial", 26)).pack(pady=20)

tk.Label(frm, text="Usuário:").pack()
entry_usuario = tk.Entry(frm)
entry_usuario.pack()

tk.Label(frm, text="Senha:").pack()
entry_senha = tk.Entry(frm, show="*")
entry_senha.pack()

tk.Button(frm, text="Entrar", command=verificar_login, bg="Green", fg="white", activebackground="Dark Green", activeforeground="Black").pack(pady=10)
tk.Button(frm, text="Sair", command=janela.destroy, bg="Red", fg="White", activebackground="Dark Red", activeforeground="Black").pack(pady=11)
tk.Button(frm, text="Criar conta",command=abrir_criar_conta).pack(pady=11)

janela.mainloop()

conexao.close()

