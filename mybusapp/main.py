import ttkbootstrap as ttk
from view.login_view import LoginView

app = ttk.Window(themename='mybus')
LoginView(app)
app.mainloop()