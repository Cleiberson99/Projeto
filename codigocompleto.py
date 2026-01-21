import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


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


carrinho = []           
usuario_logado = None   


def limpar_carrinho():
    global carrinho
    carrinho = []

def calcular_total_carrinho():
    return sum(preco for _, preco in carrinho)


def verificar_login():
    global usuario_logado
    
    usuario = entry_usuario.get().strip()
    senha = entry_senha.get()

    if not usuario or not senha:
        messagebox.showwarning("Atenção", "Preencha usuário e senha!")
        return

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario = ? AND senha = ?",
        (usuario, senha)
    )
    if cursor.fetchone():
        usuario_logado = usuario
        janela.withdraw()
        abrir_tela_inicial()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")


def abrir_criar_conta():
    criar = tk.Toplevel(janela)
    criar.title("Criar Conta")
    criar.geometry("400x300")
    criar.grab_set()

    frm = ttk.Frame(criar, padding=20)
    frm.pack(expand=True)

    ttk.Label(frm, text="Criar nova conta", font=("Arial", 16)).pack(pady=10)

    ttk.Label(frm, text="Novo usuário:").pack()
    entry_user = ttk.Entry(frm)
    entry_user.pack(pady=4)

    ttk.Label(frm, text="Nova senha:").pack()
    entry_pass = ttk.Entry(frm, show="*")
    entry_pass.pack(pady=4)

    def salvar():
        u = entry_user.get().strip()
        p = entry_pass.get()
        if not u or not p:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        try:
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (u, p))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Conta criada!")
            criar.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Este usuário já existe!")

    ttk.Button(frm, text="Salvar", command=salvar).pack(pady=20)


def atualizar_senha():
    global usuario_logado
    
    if usuario_logado is None:
        messagebox.showwarning("Aviso", "Faça login primeiro!")
        return

    att = tk.Toplevel(janela)
    att.title("Alterar Senha")
    att.geometry("420x380")
    att.grab_set()

    frm = ttk.Frame(att, padding=20)
    frm.pack(expand=True)

    ttk.Label(frm, text="Alterar Senha", font=("Arial", 16)).pack(pady=10)

    ttk.Label(frm, text="Senha atual:").pack()
    entry_atual = ttk.Entry(frm, show="*")
    entry_atual.pack(pady=4)

    ttk.Label(frm, text="Nova senha:").pack()
    entry_nova = ttk.Entry(frm, show="*")
    entry_nova.pack(pady=4)

    ttk.Label(frm, text="Confirmar nova senha:").pack()
    entry_conf = ttk.Entry(frm, show="*")
    entry_conf.pack(pady=4)

    def salvar():
        atual = entry_atual.get()
        nova = entry_nova.get()
        conf = entry_conf.get()

        if not all([atual, nova, conf]):
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        if nova != conf:
            messagebox.showerror("Erro", "As senhas novas não coincidem!")
            return

        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario = ? AND senha = ?",
            (usuario_logado, atual)
        )
        if not cursor.fetchone():
            messagebox.showerror("Erro", "Senha atual incorreta!")
            return

        cursor.execute(
            "UPDATE usuarios SET senha = ? WHERE usuario = ?",
            (nova, usuario_logado)
        )
        conexao.commit()
        messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
        att.destroy()

    ttk.Button(frm, text="Alterar senha", command=salvar).pack(pady=20)


def deletar_conta():
    global usuario_logado
    
    if usuario_logado is None:
        messagebox.showwarning("Aviso", "Faça login primeiro!")
        return

    if not messagebox.askyesno("Confirmação", "Deseja realmente excluir sua conta?\nEsta ação não pode ser desfeita!"):
        return

    cursor.execute("DELETE FROM usuarios WHERE usuario = ?", (usuario_logado,))
    conexao.commit()

    messagebox.showinfo("Sucesso", "Conta excluída permanentemente.")
    usuario_logado = None
    limpar_carrinho()

    tela_inicial.destroy()
    janela.deiconify()


tela_inicial = None
tree_carrinho = None
label_total = None
var_pagamento = None

def abrir_tela_inicial():
    global tela_inicial, tree_carrinho, label_total, var_pagamento

    tela_inicial = tk.Toplevel(janela)
    tela_inicial.title("Mega Swag Video Games")
    tela_inicial.geometry("1000x700")
    tela_inicial.protocol("WM_DELETE_WINDOW", lambda: [limpar_carrinho(), tela_inicial.destroy(), janela.deiconify()])

    ttk.Label(tela_inicial, text="Mega Swag Video Games", font=("Arial", 22, "bold")).pack(pady=10)
    ttk.Label(tela_inicial, text=f"Bem-vindo, {usuario_logado}!", font=("Arial", 12)).pack()

    frm_botoes = ttk.Frame(tela_inicial)
    frm_botoes.pack(anchor="ne", padx=20, pady=5)
    ttk.Button(frm_botoes, text="Alterar senha", command=atualizar_senha).pack(side="left", padx=5)
    ttk.Button(frm_botoes, text="Excluir conta", command=deletar_conta).pack(side="left", padx=5)

    pane = ttk.PanedWindow(tela_inicial, orient=tk.HORIZONTAL)
    pane.pack(fill="both", expand=True, padx=10, pady=10)

    frm_catalogo = ttk.LabelFrame(pane, text="Catálogo de Jogos")
    pane.add(frm_catalogo, weight=3)

    jogos = [
        ("The Witcher 3", 129.90),
        ("Red Dead Redemption 2", 299.90),
        ("DOOM Eternal", 149.00),
        ("Minecraft", 79.90),
        ("Cyberpunk 2077", 199.90),
        ("Elden Ring", 249.90),
    ]

    for nome, preco in jogos:
        frm_jogo = ttk.Frame(frm_catalogo)
        frm_jogo.pack(fill="x", pady=6, padx=8)
        ttk.Label(frm_jogo, text=nome, font=("Arial", 11, "bold")).pack(side="left")
        ttk.Label(frm_jogo, text=f"R$ {preco:,.2f}", foreground="dark green").pack(side="left", padx=20)
        ttk.Button(frm_jogo, text="Adicionar", command=lambda n=nome, p=preco: adicionar_ao_carrinho(n, p)).pack(side="right")

    frm_carrinho = ttk.LabelFrame(pane, text="Carrinho de Compras")
    pane.add(frm_carrinho, weight=2)

    tree_carrinho = ttk.Treeview(frm_carrinho, columns=("Jogo", "Preço"), show="headings", height=10)
    tree_carrinho.heading("Jogo", text="Jogo")
    tree_carrinho.heading("Preço", text="Preço")
    tree_carrinho.column("Jogo", width=180)
    tree_carrinho.column("Preço", width=80, anchor="e")
    tree_carrinho.pack(fill="both", expand=True, padx=5, pady=5)

    label_total = ttk.Label(frm_carrinho, text="Total: R$ 0,00", font=("Arial", 12, "bold"))
    label_total.pack(pady=8)

    ttk.Button(frm_carrinho, text="Remover selecionado", command=remover_item_carrinho).pack(pady=5)
    ttk.Button(frm_carrinho, text="Limpar carrinho", command=atualizar_carrinho).pack(pady=5)

    frm_pagamento = ttk.LabelFrame(tela_inicial, text="Finalizar Compra")
    frm_pagamento.pack(fill="x", padx=10, pady=10)

    var_pagamento = tk.StringVar(value="pix")
    ttk.Radiobutton(frm_pagamento, text="PIX", variable=var_pagamento, value="pix").pack(side="left", padx=20)
    ttk.Radiobutton(frm_pagamento, text="Cartão de Crédito", variable=var_pagamento, value="credito").pack(side="left", padx=20)
    ttk.Radiobutton(frm_pagamento, text="Boleto", variable=var_pagamento, value="boleto").pack(side="left", padx=20)

    ttk.Button(frm_pagamento, text="FINALIZAR COMPRA", command=finalizar_compra).pack(pady=15)

def adicionar_ao_carrinho(nome, preco):
    carrinho.append((nome, preco))
    atualizar_carrinho()

def remover_item_carrinho():
    selecionado = tree_carrinho.selection()
    if not selecionado:
        return
    index = tree_carrinho.index(selecionado)
    carrinho.pop(index)
    atualizar_carrinho()

def atualizar_carrinho():
    for item in tree_carrinho.get_children():
        tree_carrinho.delete(item)

    for nome, preco in carrinho:
        tree_carrinho.insert("", "end", values=(nome, f"R$ {preco:,.2f}"))

    total = calcular_total_carrinho()
    label_total.config(text=f"Total: R$ {total:,.2f}")

def finalizar_compra():
    if not carrinho:
        messagebox.showwarning("Carrinho vazio", "Adicione itens ao carrinho primeiro!")
        return

    total = calcular_total_carrinho()
    forma = var_pagamento.get().upper()

    msg = f"Compra finalizada com sucesso!\n\n"
    msg += f"Cliente: {usuario_logado}\n"
    msg += f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
    msg += f"Forma de pagamento: {forma}\n"
    msg += f"Total: R$ {total:,.2f}\n\nItens:\n"
    msg += "\n".join(f"• {nome} - R$ {preco:,.2f}" for nome, preco in carrinho)

    messagebox.showinfo("Compra Concluída", msg)
    limpar_carrinho()
    atualizar_carrinho()


janela = tk.Tk()
janela.title("Mega Swag Video Games - Login")
janela.geometry("600x500")

frm = ttk.Frame(janela, padding=30)
frm.pack(expand=True)

ttk.Label(frm, text="Mega Swag Video Games", font=("Arial", 24, "bold")).pack(pady=30)

ttk.Label(frm, text="Usuário:").pack()
entry_usuario = ttk.Entry(frm, width=35)
entry_usuario.pack(pady=5)

ttk.Label(frm, text="Senha:").pack()
entry_senha = ttk.Entry(frm, show="*", width=35)
entry_senha.pack(pady=5)

botoes = ttk.Frame(frm)
botoes.pack(pady=30)

ttk.Button(botoes, text="Entrar", command=verificar_login,width=15).pack(side="left", padx=10)
ttk.Button(botoes, text="Criar conta", command=abrir_criar_conta, width=15).pack(side="left", padx=10)
ttk.Button(botoes, text="Sair", command=janela.destroy, width=15).pack(side="left", padx=10)

janela.mainloop()


conexao.close()
