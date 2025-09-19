import ttkbootstrap as ttk
from view.user_view.login.login_view import LoginView
from view.user_view.linha.visualizar_linha import VisualizarLinhaView
from view.user_view.home.home_view import HomeLinhaView

app = ttk.Window(themename='mybus')
VisualizarLinhaView(app)
#LoginView(app)
#HomeLinhaView(app)
app.mainloop()