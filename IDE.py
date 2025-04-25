# Tem que estar no mesmo diretório do codigo fonte

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from lark import Lark
from snask_interpreter import SnaskInterpreter
import sys

# Classe que redireciona a saída do print para a área de texto
class RedirectStdout:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.config(state=tk.NORMAL)  # Permite editar o Text
        self.text_widget.insert(tk.END, message)  # Adiciona a mensagem no Text
        self.text_widget.config(state=tk.DISABLED)  # Desabilita a edição

    def flush(self):  # Necessário para compatibilidade
        pass

# Função que chama o interpretador Snask para executar o código
def executar_interpretador(codigo):
    try:
        # Parser que vai usar o arquivo de gramática para gerar a árvore de sintaxe
        parser = Lark.open("C:/Snask/grammar.lark", start='start', parser='lalr')
        # Criando o interpretador
        interpretador = SnaskInterpreter(parser)
        
        # Gerar a árvore de sintaxe para o código fornecido
        tree = parser.parse(codigo)
        
        # Passa a árvore para o interpretador e executa
        interpretador.transform(tree)
        return ""
    except Exception as e:
        return f"Erro: {e}"

# Função que executa o código
def executar_codigo():
    try:
        codigo = editor_texto.get("1.0", tk.END)
        
        # Limpar a área de saída antes de exibir o novo resultado
        resultado_saida.config(state=tk.NORMAL)
        resultado_saida.delete("1.0", tk.END)
        
        # Redireciona o print para o widget de saída
        sys.stdout = RedirectStdout(resultado_saida)
        
        resultado = executar_interpretador(codigo)
        
        # Mostrar o retorno do código na área de resultado
        resultado_saida.config(state=tk.NORMAL)
        resultado_saida.insert(tk.END, resultado + '\n')
        resultado_saida.config(state=tk.DISABLED)
        
    except Exception as e:
        resultado_saida.config(state=tk.NORMAL)
        resultado_saida.insert(tk.END, f"Erro: {e}\n")
        resultado_saida.config(state=tk.DISABLED)

# Função para abrir arquivos
def abrir_arquivo():
    caminho = filedialog.askopenfilename(defaultextension=".snask", filetypes=[("Arquivos Snask", "*.snask"), ("Todos os Arquivos", "*.*")])
    if caminho:
        try:
            with open(caminho, "r") as arquivo:
                editor_texto.delete("1.0", tk.END)
                editor_texto.insert(tk.END, arquivo.read())
            root.title(f"IDE Snask - {caminho}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo: {e}")

# Função para salvar arquivos
def salvar_arquivo():
    caminho = filedialog.asksaveasfilename(defaultextension=".snask", filetypes=[("Arquivos Snask", "*.snask"), ("Todos os Arquivos", "*.*")])
    if caminho:
        try:
            with open(caminho, "w") as arquivo:
                arquivo.write(editor_texto.get("1.0", tk.END))
            messagebox.showinfo("Sucesso", f"Arquivo salvo em: {caminho}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o arquivo: {e}")

# Configuração da interface gráfica com Tkinter
root = tk.Tk()
root.title("IDE Snask")
root.geometry("800x600")

# Estilizando a aplicação com algumas configurações do Tkinter
root.configure(bg="#282c34")  # Cor de fundo
root.option_add("*Font", "Arial 12")
root.option_add("*Background", "#282c34")
root.option_add("*Foreground", "#ffffff")

# Frame para o editor de código
frame_editor = tk.Frame(root, bg="#282c34")
frame_editor.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Editor de código
editor_texto = tk.Text(frame_editor, height=15, width=80, wrap=tk.WORD, font=("Arial", 12), bg="#2e2e2e", fg="#ffffff", insertbackground="white")
editor_texto.pack(fill=tk.BOTH, expand=True)

# Frame para os botões (Executar, Salvar, Abrir)
frame_botoes = tk.Frame(root, bg="#282c34")
frame_botoes.pack(pady=10)

# Botões
botao_executar = tk.Button(frame_botoes, text="Executar Código", command=executar_codigo, bg="#61afef", fg="#ffffff", font=("Arial", 12))
botao_executar.pack(side=tk.LEFT, padx=10)

botao_abrir = tk.Button(frame_botoes, text="Abrir Arquivo", command=abrir_arquivo, bg="#98c379", fg="#ffffff", font=("Arial", 12))
botao_abrir.pack(side=tk.LEFT, padx=10)

botao_salvar = tk.Button(frame_botoes, text="Salvar Arquivo", command=salvar_arquivo, bg="#e06c75", fg="#ffffff", font=("Arial", 12))
botao_salvar.pack(side=tk.LEFT, padx=10)

# Área de saída
resultado_saida = tk.Text(root, height=10, width=80, wrap=tk.WORD, font=("Arial", 12), bg="#1e2127", fg="#ffffff", state=tk.DISABLED)
resultado_saida.pack(pady=10, padx=20)

# Rodar a aplicação
root.mainloop()
