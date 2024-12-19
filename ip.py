import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import socket
import subprocess

def obter_ip_local():
    try:
        hostname = socket.gethostname()
        endereco_ip = socket.gethostbyname(hostname)
        return endereco_ip
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao obter o endereço IP local: {e}")
        return None
    
def obter_nome_maquina():
    try:
        hostname = socket.gethostname()
        return hostname
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao obter o nome da máquina na rede: {e}")
        return None

def conectar_ao_banco_de_dados():
    try:
        conexao = mysql.connector.connect(
            host="192.168.1.203",
            user="binaural",
            password="binaural@2024",
            database="controle"
        )
        return conexao
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

def carregar_dados_do_banco_de_dados(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM maquinas")
        maquinas = cursor.fetchall()
        cursor.close()
        return maquinas
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao carregar dados do banco de dados: {e}")
        return []

def salvar_dados_no_banco_de_dados(conexao, endereco_ip, nome_maquina, atribuido_para):
    try:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO maquinas (endereco_ip, nome_maquina, atribuido_para) VALUES (%s, %s, %s)", (endereco_ip, nome_maquina, atribuido_para))
        conexao.commit()
        cursor.close()
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso.")
        return True
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao salvar dados no banco de dados: {e}")
        return False

def clique_no_botao_salvar(conexao, entrada_endereco_ip, entrada_nome_maquina, entrada_atribuido_para, arvore):
    endereco_ip = entrada_endereco_ip.get()
    nome_maquina = entrada_nome_maquina.get()
    atribuido_para = entrada_atribuido_para.get()
    if salvar_dados_no_banco_de_dados(conexao, endereco_ip, nome_maquina, atribuido_para):
        recarregar_tabela(conexao, arvore)
        limpar_campos_de_entrada(entrada_endereco_ip, entrada_nome_maquina, entrada_atribuido_para)

def pesquisar_dados_no_banco_de_dados(conexao, termo_pesquisa):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM maquinas WHERE endereco_ip LIKE %s OR nome_maquina LIKE %s OR atribuido_para LIKE %s", (f'%{termo_pesquisa}%', f'%{termo_pesquisa}%', f'%{termo_pesquisa}%'))
        maquinas = cursor.fetchall()
        cursor.close()
        return maquinas
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao pesquisar dados no banco de dados: {e}")
        return []
    
def clique_no_botao_pesquisar(conexao, termo_pesquisa, arvore):
    maquinas = pesquisar_dados_no_banco_de_dados(conexao, termo_pesquisa.get())
    exibir_resultados_pesquisa(maquinas, arvore)

def exibir_resultados_pesquisa(maquinas, arvore):
    arvore.delete(*arvore.get_children())
    for maquina in maquinas:
        arvore.insert("", "end", text=maquina[0], values=maquina)

def recarregar_tabela(conexao, arvore):
    arvore.delete(*arvore.get_children())
    maquinas = carregar_dados_do_banco_de_dados(conexao)
    for maquina in maquinas:
        arvore.insert("", "end", text=maquina[0], values=maquina)

def limpar_campos_de_entrada(*args):
    for entrada in args:
        entrada.delete(0, tk.END)

conexao = conectar_ao_banco_de_dados()
if conexao:
    maquinas = carregar_dados_do_banco_de_dados(conexao)
else:
    maquinas = []

root = tk.Tk()
root.title("Controle de IP das Máquinas")

arvore = ttk.Treeview(root)
arvore["columns"] = ("ID", "Endereço IP", "Nome da Máquina", "Atribuído Para")
arvore.heading("#0", text="ID")
arvore.column("#0", minwidth=0, width=0, stretch=tk.NO)
arvore.heading("ID", text="ID")
arvore.heading("Endereço IP", text="Endereço IP")
arvore.heading("Nome da Máquina", text="Nome da Máquina")
arvore.heading("Atribuído Para", text="Atribuído Para")
arvore.column("ID", minwidth=0, width=50, stretch=tk.NO)
arvore.column("Endereço IP", minwidth=0, width=150, stretch=tk.NO)
arvore.column("Nome da Máquina", minwidth=0, width=150, stretch=tk.NO)
arvore.column("Atribuído Para", minwidth=0, width=150, stretch=tk.NO)
for maquina in maquinas:
    arvore.insert("", "end", text=maquina[0], values=maquina)
arvore.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

tk.Label(root, text="Pesquisar:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
termo_pesquisa = tk.Entry(root)
termo_pesquisa.grid(row=1, column=1, padx=10, pady=5)
botao_pesquisar = tk.Button(root, text="Pesquisar",font="-weight bold -size 9", command=lambda: clique_no_botao_pesquisar(conexao, termo_pesquisa, arvore), fg='black')
botao_pesquisar.grid(row=1, column=2, padx=10, pady=5)

botao_recarregar = tk.Button(root, text="Limpar",font="-weight bold -size 9", command=lambda: recarregar_tabela(conexao, arvore), fg='black')
botao_recarregar.grid(row=2, column=0, columnspan=3, pady=10)

def validar_endereco_ip(entrada):
    if all(c.isdigit() or c == '.' for c in entrada):
        return True
    elif entrada == "":
        return False
    else:
        return False
    
  #C:\\Program Files\\uvnc bvba\\UltraVNC\\vncviewer.exe"  
def iniciar_conexao_vnc(endereco_ip, senha):
    try:
        # Substitua o comando abaixo pelo caminho para o executável do UltraVNC em seu sistema
        subprocess.Popen(["C:\\Program Files\\uvnc bvba\\UltraVNC\\vncviewer.exe", "-password", senha, endereco_ip])
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao iniciar a conexão VNC: {e}")

def abrir_janela_adicionar_maquina():
    janela_adicionar_maquina = tk.Toplevel(root)
    janela_adicionar_maquina.title("Adicionar Nova Máquina")

    tk.Label(janela_adicionar_maquina, text="Endereço IP:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entrada_endereco_ip = tk.Entry(janela_adicionar_maquina)
    entrada_endereco_ip.grid(row=0, column=1, padx=10, pady=5)
    entrada_endereco_ip.config(validate="key", validatecommand=(entrada_endereco_ip.register(validar_endereco_ip), "%P"))

    tk.Label(janela_adicionar_maquina, text="Nome da Máquina:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entrada_nome_maquina = tk.Entry(janela_adicionar_maquina)
    entrada_nome_maquina.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(janela_adicionar_maquina, text="Atribuído Para:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entrada_atribuido_para = tk.Entry(janela_adicionar_maquina)
    entrada_atribuido_para.grid(row=2, column=1, padx=10, pady=5)

    botao_salvar = tk.Button(janela_adicionar_maquina, text="Salvar", command=lambda: clique_no_botao_salvar(conexao, entrada_endereco_ip, entrada_nome_maquina, entrada_atribuido_para, arvore))
    botao_salvar.grid(row=3, column=0, columnspan=2, pady=10)

botao_outras_funcoes = tk.Button(root, text="ADD Maquinas",font="-weight bold -size 9", command=abrir_janela_adicionar_maquina, fg='black')
botao_outras_funcoes.grid(row=5, column=0, columnspan=3, pady=10)

def abrir_janela_editar_maquina():
    selecionado = arvore.selection()
    if not selecionado:
        messagebox.showerror("Erro", "Selecione uma máquina para editar.")
        return
    
    id_maquina = arvore.item(selecionado, "text")
    
    try:
        id_maquina = int(id_maquina)
    except ValueError:
        messagebox.showerror("Erro", "O ID da máquina selecionada não é válido.")
        return
    
    item_selecionado = arvore.item(selecionado)
    valores_maquina = item_selecionado['values']
    
    janela_editar_maquina = tk.Toplevel(root)
    janela_editar_maquina.title("Editar Máquina")

    tk.Label(janela_editar_maquina, text="Endereço IP:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entrada_endereco_ip = tk.Entry(janela_editar_maquina)
    entrada_endereco_ip.insert(0, valores_maquina[1])
    entrada_endereco_ip.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(janela_editar_maquina, text="Nome da Máquina:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entrada_nome_maquina = tk.Entry(janela_editar_maquina)
    entrada_nome_maquina.insert(0, valores_maquina[2])
    entrada_nome_maquina.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(janela_editar_maquina, text="Atribuído Para:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entrada_atribuido_para = tk.Entry(janela_editar_maquina)
    entrada_atribuido_para.insert(0, valores_maquina[3])
    entrada_atribuido_para.grid(row=2, column=1, padx=10, pady=5)

    def salvar_edicao():
        novo_endereco_ip = entrada_endereco_ip.get()
        novo_nome_maquina = entrada_nome_maquina.get()
        novo_atribuido_para = entrada_atribuido_para.get()
        
        try:
            cursor = conexao.cursor()
            cursor.execute("UPDATE maquinas SET endereco_ip = %s, nome_maquina = %s, atribuido_para = %s WHERE id = %s",
                        (novo_endereco_ip, novo_nome_maquina, novo_atribuido_para, id_maquina))
            conexao.commit()
            cursor.close()
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso.")
            recarregar_tabela(conexao, arvore)
            janela_editar_maquina.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao atualizar dados no banco de dados: {e}")
        
    botao_salvar = tk.Button(janela_editar_maquina, text="Salvar Edição", command=salvar_edicao)
    botao_salvar.grid(row=3, column=0, columnspan=2, pady=10)

botao_editar = tk.Button(root, text="Editar",font="-weight bold -size 9", command=abrir_janela_editar_maquina, fg='black')
botao_editar.grid(row=5, column=0, pady=10)

def excluir_maquina_selecionada():
    selecionado = arvore.selection()
    if not selecionado:
        messagebox.showerror("Erro", "Selecione uma máquina para excluir.")
        return
    
    id_maquina = arvore.item(selecionado, "text")
    
    try:
        id_maquina = int(id_maquina)
    except ValueError:
        messagebox.showerror("Erro", "O ID da máquina selecionada não é válido.")
        return
    
    if messagebox.askokcancel("Excluir Máquina", "Tem certeza de que deseja excluir esta máquina?"):
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM maquinas WHERE id = %s", (id_maquina,))
            conexao.commit()
            cursor.close()
            messagebox.showinfo("Sucesso", "Máquina excluída com sucesso.")
            recarregar_tabela(conexao, arvore)
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir máquina do banco de dados: {e}")

botao_excluir = tk.Button(root, text="Excluir",font="-weight bold -size 9", command=excluir_maquina_selecionada, fg='black')

botao_excluir.grid(row=5, column=2, pady=10)

def iniciar_conexao_vnc_selecionada():
    selecionado = arvore.selection()
    if not selecionado:
        messagebox.showerror("Erro", "Selecione uma máquina para iniciar a conexão VNC.")
        return

    endereco_ip = arvore.item(selecionado, "values")[1]
    senha = "9977"  # Substitua "sua_senha_aqui" pela senha desejada
    iniciar_conexao_vnc(endereco_ip, senha)



botao_conectar_vnc = tk.Button(root, text="Conectar VNC",font="-weight bold -size 9", command=iniciar_conexao_vnc_selecionada, bg='light green', fg='black')
botao_conectar_vnc.grid(row=6, column=0, columnspan=3, pady=10)

root.mainloop()
