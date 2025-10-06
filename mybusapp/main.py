import ttkbootstrap as ttk
from view.user_view.login.login_view import LoginView
from resources.database.inicializacao import Inicializacao


app = ttk.Window(themename='mybus')
inicializacao = Inicializacao()
LoginView(app)
app.mainloop()