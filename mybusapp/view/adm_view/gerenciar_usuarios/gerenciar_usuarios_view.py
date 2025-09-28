from tkinter import messagebox
import ttkbootstrap as ttk
import tkintermapview as tkmap
from control.gerenciar_usuarios_control import GerenciarUsuariosControl
from view.adm_view.onibus_forms.onibus_form import OnibusForm
from resources.utils import Utils
from view.user_view.cadastro.cadastro_user import CadastroUserView


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
        self.btn_voltar.grid(column=0, row=0)
        self.btn_voltar.bind('<ButtonRelease-1>')

        # Título da janela
        self.lbl_titulo = ttk.Label(self.frm_center, text='Gerenciar Usuários', bootstyle='primary-inverse', padding=(339, 11))
        self.lbl_titulo.grid(column=1, row=0, columnspan=2)

        # Tabela (cabeçalho + corpo)
        colunas = ['id', 'nome', 'email', 'telefone', 'papel', 'status']
        self.tvw = ttk.Treeview(self.frm_center, height=8, columns=colunas, show='headings', selectmode='browse')
        self.tvw.heading('id', text='ID')
        self.tvw.heading('nome', text='NOME')
        self.tvw.heading('email', text='EMAIL')
        self.tvw.heading('telefone', text='TELEFONE')
        self.tvw.heading('papel', text='PAPEL')
        self.tvw.heading('status', text='STATUS')
        self.tvw.grid(column=0, row=1, columnspan=2, pady=6, sticky='we')

        # Alinha o campo com a coluna
        self.tvw.column('id', anchor='center', width=60, minwidth=60)
        self.tvw.column('nome', anchor='center', width=180, minwidth=180)
        self.tvw.column('email', anchor='center', width=225, minwidth=225)
        self.tvw.column('telefone', anchor='center', width=170, minwidth=170)
        self.tvw.column('papel', anchor='center', width=100, minwidth=100)
        self.tvw.column('status', anchor='center', width=100, minwidth=100)

        # Configura cor para status
        self.tvw.tag_configure("ativo", background="#002B5C")
        self.tvw.tag_configure("inativo", background="#001F44")

        # Scrollbar da Tabela
        self.brl = ttk.Scrollbar(self.frm_center, command=self.tvw.yview)
        self.brl.grid(column=2, row=1, sticky='ns', pady=6)
        self.tvw.configure(yscrollcommand=self.brl.set)

        # Gerando tuplas
        self.atualizar_tabela()

        # Verifica se existe uma linha selecionada
        self.tvw.bind('<KeyRelease>', self.validar_botoes)
        self.tvw.bind('<ButtonRelease-1>', self.validar_botoes)

        # Botões
        self.frm_menu = ttk.Frame(self.frm_center)
        self.frm_menu.grid(column=0, row=2, columnspan=3) 

        self.entr_busca_value = ttk.StringVar()
        self.entr_busca = ttk.Entry(self.frm_menu, textvariable=self.entr_busca_value)
        self.entr_busca.grid(column=0, row=0, columnspan=2, sticky='ew')
        self.btn_buscar = ttk.Button(self.frm_menu, text='Buscar')
        self.btn_buscar.bind('<ButtonRelease-1>', self.pesquisar_usuario)
        self.btn_buscar.grid(column=2, row=0, padx=(5, 0)) 

        self.btn_promover = ttk.Button(self.frm_menu, text='Promover Administrador', bootstyle='success', state='disabled')
        self.btn_promover.grid(column=0, row=1, padx=2, pady=(10, 0), sticky='ew')
        self.btn_promover.bind('<ButtonRelease-1>', self.promover_adm)

        self.btn_editar = ttk.Button(self.frm_menu, text='Editar', bootstyle='warning', state='disabled')
        self.btn_editar.grid(column=1, row=1, padx=2, pady=(10, 0), sticky='ew')
        self.btn_editar.bind('<ButtonRelease-1>', self.editar_usuario)

        self.btn_excluir = ttk.Button(self.frm_menu, text='Inativar', bootstyle='danger', state='disabled')
        self.btn_excluir.grid(column=2, row=1, padx=2, pady=(10, 0), sticky='ew')
        self.btn_excluir.bind('<ButtonRelease-1>', self.excluir)

        self.utils.centraliza(self.janela)

    def validar_botoes(self, *event):
        linha = item = self.tvw.selection()
        if linha: # Se uma linha for selecionada
            self.btn_promover.config(state='enable')
            self.btn_editar.config(state='enable')
            self.btn_excluir.config(state='enable')
            return True
        else:
            self.btn_promover.config(state='disabled')
            self.btn_editar.config(state='disabled')
            self.btn_excluir.config(state='disabled')
            return False

    def atualizar_tabela(self, tuplas=None):
        dados = self.tvw.get_children()
        for item in dados:
            self.tvw.delete(item)
        if tuplas == None:
            tuplas = self.ge_usuarios.listar_usuarios()
        for item in tuplas:
            valores = list(item) # Converte para lista
            tag_inativo = tuple()
            tag_ativo = tuple()

            if valores[3] == 'adm':
                valores[3] = 'Administrador'
            elif valores[3] == 'user':
                valores[3] = 'Usuário'

            if valores[4] == 'A':
                valores[4] = 'Ativo'
                tag_ativo = ('ativo',)
            elif valores[4] == 'I':
                valores[4] = 'Inativo'
                tag_inativo = ('inativo',)


            self.tvw.insert('', 'end', values=valores, tags=[tag_inativo, tag_ativo])
        
    def promover_adm(self, event):
        item = self.tvw.selection()
        if item:
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
                    messagebox.showinfo('Informação', 'Usuário foi promovido a administrador')
        else:
            messagebox.showerror('Erro','Selecione um usuário para promover a administrador.')
        
        # elif len(item) > 0:
        #     messagebox.showwarning('Aviso', 'Selecione apenas 1 usuário')
        
        # else:
        #     messagebox.showwarning('Aviso', 'Selecione 1 usuário')

    def pesquisar_usuario(self, event):
        termobusca = self.entr_busca_value.get()
        result = self.ge_usuarios.pesquisar_usuario(termobusca)
        self.atualizar_tabela(result)

    def editar_usuario(self, event):
        item = self.tvw.selection()
        if self.tvw.selection():
            usuario_id = self.tvw.item(item)['values'][0]
            usuario = self.ge_usuarios.buscar_usuario_id(usuario_id)[0]
            self.tl = ttk.Toplevel(self.janela)
            CadastroUserView(self.tl, usuario)
            self.utils.call_top_view(self.janela, self.tl)
            self.atualizar_tabela()
        else:
            messagebox.showwarning("Error", "Selecione um usuário para editar.")

    def excluir(self, event):
        item = self.tvw.selection()
        if item:
            item_id = item[0] 
            
            dados_linha = self.tvw.item(item_id, 'values') #pegando todos os dados da linha
            nome_use = dados_linha[1]
            id_use = dados_linha[0]
            status_atual = dados_linha[4]
            
            if status_atual == 'Inativo':
                 messagebox.showinfo('Informação', f'O usuário {nome_use} já esta inativo.')
                 return
            
            res = messagebox.askquestion('Confirmar', f'Tem certeza que deseja tornar o usuário {nome_use} inativo?')
            
            if res == 'yes':
                self.ge_usuarios.deletar_usuario(id_use)
                self.atualizar_tabela()
                messagebox.showinfo('Informação', 'Usuário inativado com sucesso!')
        else:
            messagebox.showwarning("Error", "Selecione um usuário para inativar.")
        # elif len(item) > 0:
        #     messagebox.showwarning('Aviso', 'Selecione apenas 1 usuário')
        
        # else:
        #     messagebox.showwarning('Aviso', 'Selecione 1 usuário')

    def voltar(self):
            self.janela.destroy() 
            self.janela_origem.deiconify() 

