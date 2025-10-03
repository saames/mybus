import ttkbootstrap as ttk
from tkinter import TclError

class Utils:
    # Centraliza janela
    def centraliza(self, master):
        """
        Centraliza uma janela no centro da tela.
        """
        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        master.update_idletasks()
        largura_janela = master.winfo_width()
        altura_janela = master.winfo_height()
        x = largura_monitor // 2 - largura_janela // 2
        y = altura_monitor //2 - altura_janela // 2
        master.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

    # Placeholder
    def add_placeholder(self, entry, texto):
        """
        Adiciona a funcionalidade de placeholder a uma janela Entry do ttkbootstrap.
        Esta função também configura o estilo 'Placeholder.TEntry' necessário.
        """
        estilo = ttk.Style()
        estilo.configure('Placeholder.TEntry', foreground='gray')

        if len(entry.get()) == 0:
            entry.insert(0, texto)
            entry.configure(style='Placeholder.TEntry')

        def ativar(event):
            # Limpa o placeholder quando a entry recebe foco.
            if entry.cget('style') == 'Placeholder.TEntry':
                entry.delete(0, 'end')
                entry.configure(style='TEntry')

        def desativar(event):
            # Restaura o placeholder se a entry perder o foco e estiver vazio."""
            if not entry.get():
                entry.insert(0, texto)
                entry.configure(style='Placeholder.TEntry')
        
        # Associa as funções (event handlers) aos eventos de foco do widget
        entry.bind("<FocusIn>", ativar)
        entry.bind("<FocusOut>", desativar)


    def call_top_view(self, master, tl):
        janela = master
        janela.withdraw()  # Oculta janela, iconify() para apenas minimizar.
        janela.wait_window(tl)  # .wait_window() aguarda o fechamento da janela_cadastro para rodar o deiconify.
        try:
            janela.deiconify()
        except TclError as tcl:
            pass