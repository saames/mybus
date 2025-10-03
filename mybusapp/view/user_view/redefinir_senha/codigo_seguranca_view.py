import ttkbootstrap as ttk
from resources.utils import Utils
from tkinter import messagebox
import random
import string
import yagmail
from datetime import datetime, timedelta
from view.user_view.redefinir_senha.definir_nova_senha_view import DefinirNovaSenhaView

class CodigoSegurancaView:
    def __init__(self, master, janela_origem, email_usuario = 'marcos.manuares@sou.ufac.br'):
        # Ajustes na janela
        self.janela = master
        self.janela_origem = janela_origem
        self.janela.title("Código de Segurança - MyBus")
        self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.pack(expand=True, padx=10, pady=10)

        self.email_usuario = email_usuario
        
        self.codigo_enviado = None
        self.timestamp_envio = None 
        self.horario_fim_contagem = None

        # Criação de Instâncias
        self.utils = Utils()

        # Título
        self.lbl_title = ttk.Label(self.frm_center, text='Código de Segurança', bootstyle='primary-inverse', padding=(96, 11))
        self.lbl_title.grid(column=0,row=0, columnspan=2, pady=(0,30))

        email_censurado = self.censurar_email(self.email_usuario)
        self.lbl_info = ttk.Label(self.frm_center, text=f"Um código de segurança foi enviado para o email:\n{email_censurado}",  justify='center')
        self.lbl_info.grid(column=0, row=1, columnspan=2, pady=(0,30))

        self.lbl_codigo = ttk.Label(self.frm_center, text='CÓDIGO', bootstyle='inverse-secondary', 
                                                              borderwidth=7, 
                                                              padding=(39,0),
                                                              font=('TkDefaultFont', 10, 'bold'))
        self.lbl_codigo.grid(column=0, row=2, sticky='w', pady=(0,5))
        self.ent_codigo_value = ttk.StringVar()
        self.ent_codigo = ttk.Entry(self.frm_center, textvariable=self.ent_codigo_value)
        self.ent_codigo.grid(column=1, row=2, sticky='ew', pady=(0, 5))
        self.ent_codigo.bind('<KeyRelease>', self.validar_campos)
        self.utils.add_placeholder(self.ent_codigo,'XXXXXX')

        self.lbl_tempo_restante = ttk.Label(self.frm_center, text="")
        self.lbl_tempo_restante.grid(column=0, row=3, columnspan=2, pady=(30,0))

        # Frame dos botões
        self.frm_buttons = ttk.Frame(self.frm_center)
        self.frm_buttons.grid(column=0, row=4, columnspan=2, pady=(10, 0))

        # Botão Solicitar novo código
        self.btn_solicitar = ttk.Button(self.frm_buttons, text='SOLICITAR NOVO CÓDIGO', bootstyle='warning', state='disabled')
        self.btn_solicitar.grid(column=0, row=0, columnspan=2, sticky='ew', pady=(0,45))
        self.btn_solicitar.bind('<ButtonRelease-1>', self.enviar_codigo)

        # Botão Cancelar 
        self.btn_cancel = ttk.Button(self.frm_buttons, text='CANCELAR', bootstyle='danger')
        self.btn_cancel.grid(column=0, row=1, padx=(0,5))
        self.btn_cancel.bind('<ButtonRelease-1>', self.cancelar)

        # Botão Continuar
        self.btn_continuar = ttk.Button(self.frm_buttons, text='CONTINUAR', bootstyle='success', state='disabled')
        self.btn_continuar.grid(column=1, row=1)
        self.btn_continuar.bind('<ButtonRelease-1>', self.continuar)

        self.enviar_codigo()

        self.utils.centraliza(self.janela)

    def censurar_email(self, email):
        try:
            usuario, dominio = email.split('@')
            if len(usuario) > 3:
                return f"{usuario[:3]}{'*'*6}@{dominio}"
            return email
        except ValueError:
            return "E-mail inválido"

    def enviar_codigo(self, *event):
        self.btn_solicitar.config(state='disabled')
        self.codigo_enviado = ''.join(random.choices(string.digits, k=6))
        
        try:
            yag = yagmail.SMTP("mybusrb@gmail.com","ahsgqehojefovvhl")
            yag.send(
                to=self.email_usuario,
                subject="Código de redefinição de senha MyBus",
                contents=f"Seu código de segurança é: {self.codigo_enviado}"
            )
            
            self.timestamp_envio = datetime.now() 

            self.horario_fim_contagem = datetime.now() + timedelta(seconds=60)
            self.lbl_tempo_restante.grid()
            self.atualizar_contador()
        except Exception as e:
            messagebox.showerror('Erro de Envio', f'Falha ao enviar e-mail.\nTente novamente.', parent=self.janela)
            print({e})
            self.btn_solicitar.config(state='enabled')

    def atualizar_contador(self):
        agora = datetime.now()
        if agora < self.horario_fim_contagem:
            tempo_restante = self.horario_fim_contagem - agora
            segundos_restantes = int(tempo_restante.total_seconds())
            self.lbl_tempo_restante.config(text=f"Solicite novamente em {segundos_restantes} segundos.")
            self.janela.after(1000, self.atualizar_contador)
        else:
            self.lbl_tempo_restante.grid_remove()
            self.btn_solicitar.config(state='enabled')

    def validar_campos(self, *event):
        codigo = self.ent_codigo_value.get()
        if len(codigo) == 6:
            self.btn_continuar.config(state='enable')
            return True
        else:
            self.btn_continuar.config(state='disabled')
            return False

    def cancelar(self, *event):
        self.janela.destroy()
        self.janela_origem.deiconify()

    def continuar(self, *event):
        if self.validar_campos():
            # 3. Verificar se o código expirou
            tempo_limite = timedelta(minutes=2)
            if self.timestamp_envio and (datetime.now() - self.timestamp_envio) > tempo_limite:
                messagebox.showerror("Expirado", "O código de segurança expirou. Por favor, solicite um novo.", parent=self.janela)
                self.ent_codigo_value.set("") # Limpa o campo
                self.btn_continuar.config(state='disabled')
                return # Interrompe a função

            if self.ent_codigo_value.get() == self.codigo_enviado:
                messagebox.showinfo("Sucesso", "Código validado com sucesso!", parent=self.janela)
                self.tl = ttk.Toplevel(self.janela)
                DefinirNovaSenhaView(self.tl, self.janela) 
                self.utils.call_top_view(self.janela, self.tl)
                self.janela.destroy()
            else:
                messagebox.showerror("Erro", "Código de segurança inválido.", parent=self.janela)