from tkinter import messagebox
import ttkbootstrap as ttk
import tkintermapview as tkmap
from control.gerenciar_usuarios_control import GerenciarUsuariosControl
from view.adm_view.onibus_forms.onibus_form import OnibusForm
from resources.utils import Utils


class GerenciarUsuariosView:
    def __init__(self,master, janela_origem):
        self.janela = master
        self.janela_origem = janela_origem
        self.janela.title('Gerenciar Usuários - MyBus')
        #self.janela.geometry('700x500')
        #self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.grid(column=0, row=0, padx=10, pady=10)

        # Criação de Instâncias
        self.utils = Utils()
        self.ge_usuarios = GerenciarUsuariosControl()

        # Botão voltar
        self.style = ttk.Style()
        self.style.configure('large.TButton', font=('TkDefaultFont', 18, 'bold'))
        self.btn_voltar = ttk.Button(self.frm_center, text='⬅', style='large.TButton', command=self.voltar)
        self.btn_voltar.grid(column=0, row=0, sticky='wn')
        self.btn_voltar.bind('<ButtonRelease-1>')

        # Título da janela
        self.lbl_titulo = ttk.Label(self.frm_center, text='Gerenciar Usuários', bootstyle='primary-inverse', padding=(229, 11))
        self.lbl_titulo.grid(column=0, row=0, columnspan=2)

        # Tabela (cabeçalho + corpo)
        colunas = ['id', 'nome', 'telefone', 'papel', 'status']
        self.tvw = ttk.Treeview(self.frm_center, height=8, columns=colunas, show='headings')
        self.tvw.heading('id', text='ID')
        self.tvw.heading('nome', text='NOME')
        self.tvw.heading('telefone', text='TELEFONE')
        self.tvw.heading('papel', text='PAPEL')
        self.tvw.heading('status', text='STATUS')
        self.tvw.grid(column=0, row=1, columnspan=2, pady=6, sticky='we')

        # Alinha o campo com a coluna
        self.tvw.column('id', anchor='center', width=200, minwidth=100)
        self.tvw.column('nome', anchor='center', width=200, minwidth=100)
        self.tvw.column('telefone', anchor='center', width=200, minwidth=200)
        self.tvw.column('papel', anchor='center', width=200, minwidth=200)
        self.tvw.column('status', anchor='center', width=300, minwidth=200)

        # Scrollbar da Tabela
        self.brl = ttk.Scrollbar(self.frm_center, command=self.tvw.yview)
        self.brl.grid(column=2, row=1, sticky='ns', pady=6)
        self.tvw.configure(yscrollcommand=self.brl.set)

        # Gerando tuplas
        self.atualizar_tabela()

        # Botões
        self.frm_menu = ttk.Frame(self.frm_center)
        self.frm_menu.grid(column=0, row=2, columnspan=3) 

        self.entr_busca_value = ttk.StringVar()
        self.entr_busca = ttk.Entry(self.frm_menu, textvariable=self.entr_busca_value)
        self.entr_busca.grid(column=0, row=0, columnspan=2, sticky='ew')
        self.btn_buscar = ttk.Button(self.frm_menu, text='Buscar')
        self.btn_buscar.bind('<ButtonRelease-1>', self.pesquisar_usuario)
        self.btn_buscar.grid(column=2, row=0, padx=(5, 0)) 

        self.btn_cadastrar = ttk.Button(self.frm_menu, text='Cadastrar Administrador', bootstyle='success', command=self.cadastrar_adm)
        self.btn_cadastrar.grid(column=0, row=1, padx=2, pady=(10, 0), sticky='ew')
        self.btn_cadastrar.bind('<ButtonRelease-1>')

        self.btn_editar = ttk.Button(self.frm_menu, text='Editar', bootstyle='warning')
        self.btn_editar.grid(column=1, row=1, padx=2, pady=(10, 0), sticky='ew')
        self.btn_editar.bind('<ButtonRelease-1>')

        self.btn_excluir = ttk.Button(self.frm_menu, text='Excluir', bootstyle='danger', command=self.excluir)
        self.btn_excluir.grid(column=2, row=1, padx=2, pady=(10, 0), sticky='ew')
        self.btn_excluir.bind('<ButtonRelease-1>')

        self.utils.centraliza(self.janela)

    def atualizar_tabela(self, tuplas=None):
        dados = self.tvw.get_children()
        for item in dados:
            self.tvw.delete(item)
        if tuplas == None:
            tuplas = self.ge_usuarios.listar_usuarios()
        for item in tuplas:
            valores = list(item) # Converte para lista

            if valores[3] == 'adm':
                valores[3] = 'Administrador'
            elif valores[3] == 'user':
                valores[3] = 'Usuário'

            if valores[4] == 'A':
                valores[4] = 'Ativo'
            elif valores[4] == 'I':
                valores[4] = 'Inativo'


            self.tvw.insert('', 'end', values=valores)
        
    def cadastrar_adm(self):
        item = self.tvw.selection()

        if len(item) == 1:
            item_id = item[0] 
            
            dados_linha = self.tvw.item(item_id, 'values') # Pegando todos os dados da linha
            nome_use = dados_linha[1]
            id_use = dados_linha[0]
            papel_atual = dados_linha[3]
            
            if papel_atual == 'Administrador':
                 messagebox.showinfo('Informação', f'O usuário {nome_use} já é administrador')
                 return
            
            res = messagebox.askquestion('Confirmar', f'Tem certeza da promoção do usuário {nome_use}, para o papel de administrador?')
            
            if res == 'yes':
                self.ge_usuarios.promover_usuario(id_use)
                self.atualizar_tabela()
                messagebox.showinfo('Informação', 'Usuário foi promovido')
        
        elif len(item) > 0:
            messagebox.showwarning('Aviso', 'Selecione apenas 1 usuário')
        
        else:
            messagebox.showwarning('Aviso', 'Selecione 1 usuário')

    def pesquisar_usuario(self, event):
        termobusca = self.entr_busca_value.get()
        result = self.ge_usuarios.pesquisar_usuario(termobusca)
        self.atualizar_tabela(result)
    
    def excluir(self):
        item = self.tvw.selection()
        if len(item) == 1:
            item_id = item[0] 
            
            dados_linha = self.tvw.item(item_id, 'values') #pegando todos os dados da linha
            nome_use = dados_linha[1]
            id_use = dados_linha[0]
            status_atual = dados_linha[4]
            
            if status_atual == 'Inativo':
                 messagebox.showinfo('Informação', f'O usuário {nome_use} já esta inativo')
                 return
            
            res = messagebox.askquestion('Confirmar', f'Tem certeza da exclusão do usuário {nome_use}?')
            
            if res == 'yes':
                self.ge_usuarios.deletar_usuario(id_use)
                self.atualizar_tabela()
                messagebox.showinfo('Informação', 'Usuário está inativo')
        
        elif len(item) > 0:
            messagebox.showwarning('Aviso', 'Selecione apenas 1 usuário')
        
        else:
            messagebox.showwarning('Aviso', 'Selecione 1 usuário')

    def voltar(self):
            self.janela.destroy() 
            self.janela_origem.deiconify() 

