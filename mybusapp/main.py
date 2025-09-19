import ttkbootstrap as ttk
from view.user_view.login.login_view import LoginView
#from view.user_view.linha.home_linha import HomeLinhaView

app = ttk.Window(themename='mybus')
LoginView(app)
#HomeLinhaView(app)
app.mainloop()