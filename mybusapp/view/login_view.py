import ttkbootstrap as ttk
from mybusapp.control.login_control import LoginControl

class LoginView:
    def __init__(self, master):
        self.janela = master
        self.janela.title('MyBus')
        self.janela.geometry('640x480')
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.pack()

        
        self.img_logo = ttk.PhotoImage(file='../mybusapp/resources/media/mybus_logo_128.png')
        #self.img_logo = self.img_logo.subsample(1,1)
        self.lbl_logo = ttk.Label(self.frm_center, image=self.img_logo)
        self.lbl_logo.image = self.img_logo
        self.lbl_logo.grid(column=0, row=0, columnspan=2, pady=20)

        self.lbl_username = ttk.Label(self.frm_center, text='CPF', bootstyle='inverse-secondary', 
                                                                   borderwidth=7, 
                                                                   padding=(13,0),
                                                                   font=('TkDefaultFont', 10, 'bold'))
        self.lbl_username.grid(column=0, row=1)
        self.ent_username = ttk.Entry(self.frm_center, validate='key', validatecommand=LoginControl.validar_campos)
        self.ent_username.grid(column=1, row=1)

        self.lbl_password = ttk.Label(self.frm_center, text='SENHA', bootstyle='inverse-secondary', 
                                                                     borderwidth=7, 
                                                                     padding=(2,0),
                                                                     font=('TkDefaultFont', 10, 'bold'))
        self.lbl_password.grid(column=0, row=2)
        self.ent_password = ttk.Entry(self.frm_center, show='*', validate='key', validatecommand=LoginControl.validar_campos)
        self.ent_password.grid(column=1, row=2, pady=5)

        self.btn_acessar = ttk.Button(self.frm_center, text='ACESSAR', state='disabled')
        self.btn_acessar.grid(column=0, row=3, columnspan=2, sticky='we', pady=5)