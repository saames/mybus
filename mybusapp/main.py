import ttkbootstrap as ttk
from view.user_view.login.login_view import LoginView


app = ttk.Window(themename='mybus')

LoginView(app)
app.mainloop()