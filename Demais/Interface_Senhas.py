import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
from random import choice
import re

class GeradorSenhasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Senhas Seguras")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Configurar estilo
        self.root.configure(bg="#f0f0f0")
        style = ttk.Style()
        style.theme_use('clam')
        
        # Lista de caracteres
        self.alfanumerica = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F', 'g', 'G', 'h','H', 'i', 'I', 'j', 'J',
                        'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 
                        'u', 'U', 'v', 'V', 'w', 'W', 'y', 'Y', 'z', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                        '@', '$', '&', '#', '*', '%', '!']
        
        self.historico = []
        self.senha_atual = ""
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="🔐 Gerador de Senhas", font=("Helvetica", 18, "bold"))
        titulo.pack(pady=10)
        
        # Frame para a senha
        senha_frame = ttk.LabelFrame(main_frame, text="Senha Gerada", padding="10")
        senha_frame.pack(fill=tk.X, pady=10)
        
        self.senha_var = tk.StringVar()
        self.senha_entry = ttk.Entry(senha_frame, textvariable=self.senha_var, font=("Courier", 12), state="readonly")
        self.senha_entry.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(0, 10))
        
        btn_copiar = ttk.Button(senha_frame, text="📋 Copiar", command=self.copiar_senha, width=10)
        btn_copiar.pack(side=tk.LEFT)
        
        # Frame para configurações
        config_frame = ttk.LabelFrame(main_frame, text="Configurações", padding="10")
        config_frame.pack(fill=tk.X, pady=10)
        
        # Comprimento da senha
        ttk.Label(config_frame, text="Comprimento da senha:").pack(anchor=tk.W, pady=5)
        self.comprimento_var = tk.IntVar(value=16)
        comprimento_scale = ttk.Scale(config_frame, from_=8, to=32, orient=tk.HORIZONTAL, 
                                      variable=self.comprimento_var, command=self.atualizar_comprimento)
        comprimento_scale.pack(fill=tk.X, pady=5)
        
        self.comprimento_label = ttk.Label(config_frame, text="16 caracteres", font=("Helvetica", 10))
        self.comprimento_label.pack(anchor=tk.W)
        
        # Opções de caracteres
        self.usar_maiusculas = tk.BooleanVar(value=True)
        self.usar_numeros = tk.BooleanVar(value=True)
        self.usar_especiais = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(config_frame, text="Incluir MAIÚSCULAS", variable=self.usar_maiusculas).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(config_frame, text="Incluir números", variable=self.usar_numeros).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(config_frame, text="Incluir caracteres especiais", variable=self.usar_especiais).pack(anchor=tk.W, pady=2)
        
        # Botões de ação
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.pack(fill=tk.X, pady=15)
        
        btn_gerar = ttk.Button(botoes_frame, text="🔄 Gerar Senha", command=self.gerar_senha_gui, width=20)
        btn_gerar.pack(side=tk.LEFT, padx=5)
        
        btn_limpar = ttk.Button(botoes_frame, text="🗑️ Limpar", command=self.limpar, width=15)
        btn_limpar.pack(side=tk.LEFT, padx=5)
        
        # Frame para histórico
        historico_frame = ttk.LabelFrame(main_frame, text="Histórico de Senhas", padding="10")
        historico_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Listbox com scrollbar
        scrollbar = ttk.Scrollbar(historico_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.historico_listbox = tk.Listbox(historico_frame, yscrollcommand=scrollbar.set, font=("Courier", 10), height=8)
        self.historico_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.historico_listbox.yview)
        
        # Bind para clicar no histórico
        self.historico_listbox.bind('<<ListboxSelect>>', self.selecionar_do_historico)
        
        # Rodapé com informações
        info_label = ttk.Label(main_frame, text="Dica: Clique em um item do histórico para restaurá-lo", font=("Helvetica", 9, "italic"), foreground="gray")
        info_label.pack(pady=5)
    
    def atualizar_comprimento(self, valor):
        """Atualiza a label do comprimento"""
        comp = int(float(valor))
        self.comprimento_label.config(text=f"{comp} caracteres")
    
    def gerar_senha_gui(self):
        """Gera nova senha com validações"""
        comprimento = self.comprimento_var.get()
        
        # Construir lista de caracteres permitidos
        caracteres = []
        alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
                   'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
        numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        especiais = ['@', '$', '&', '#', '*', '%', '!']
        
        # Adicionar letras minúsculas
        caracteres.extend(alfabeto)
        caracteres.extend([c.upper() for c in alfabeto])
        
        if self.usar_numeros.get():
            caracteres.extend(numeros)
        
        if self.usar_especiais.get():
            caracteres.extend(especiais)
        
        if not caracteres:
            messagebox.showwarning("Aviso", "Selecione pelo menos uma opção de caracteres!")
            return
        
        # Gerar senha válida
        tentativas = 0
        max_tentativas = 100
        
        while tentativas < max_tentativas:
            nova_senha = ''.join(choice(caracteres) for _ in range(comprimento))
            
            # Validar se tem caractere especial (se habilitado)
            if self.usar_especiais.get():
                padrao = re.compile(r'[@#$%^&+=!*]')
                caractere_especial = padrao.search(nova_senha)
                comeca_caractere_especial = padrao.match(nova_senha)
                
                if caractere_especial and not comeca_caractere_especial:
                    self.senha_atual = nova_senha
                    self.senha_var.set(nova_senha)
                    self.adicionar_ao_historico(nova_senha)
                    break
            else:
                self.senha_atual = nova_senha
                self.senha_var.set(nova_senha)
                self.adicionar_ao_historico(nova_senha)
                break
            
            tentativas += 1
        
        if tentativas >= max_tentativas and self.usar_especiais.get():
            messagebox.showwarning("Aviso", "Não foi possível gerar uma senha válida. Tente com diferentes configurações.")
    
    def adicionar_ao_historico(self, senha):
        """Adiciona senha ao histórico"""
        if senha not in self.historico:
            self.historico.insert(0, senha)
            
            # Limitar a 10 itens no histórico
            if len(self.historico) > 10:
                self.historico.pop()
        
        self.atualizar_historico_display()
    
    def atualizar_historico_display(self):
        """Atualiza a exibição do histórico"""
        self.historico_listbox.delete(0, tk.END)
        for i, senha in enumerate(self.historico, 1):
            self.historico_listbox.insert(tk.END, f"{i}. {senha}")
    
    def selecionar_do_historico(self, event):
        """Seleciona uma senha do histórico"""
        selection = self.historico_listbox.curselection()
        if selection:
            idx = selection[0]
            senha = self.historico[idx]
            self.senha_var.set(senha)
            self.senha_atual = senha
    
    def copiar_senha(self):
        """Copia a senha para a área de transferência"""
        if self.senha_atual:
            try:
                pyperclip.copy(self.senha_atual)
                messagebox.showinfo("Sucesso", "Senha copiada para a área de transferência!")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível copiar: {e}")
                # Fallback: usar clipboard do tkinter
                self.root.clipboard_clear()
                self.root.clipboard_append(self.senha_atual)
                messagebox.showinfo("Sucesso", "Senha copiada (usando método alternativo)")
        else:
            messagebox.showwarning("Aviso", "Gere uma senha primeiro!")
    
    def limpar(self):
        """Limpa a senha atual"""
        self.senha_var.set("")
        self.senha_atual = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = GeradorSenhasApp(root)
    root.mainloop()
