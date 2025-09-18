from tkinter import END
import ttkbootstrap as ttk

class PlaceHolder:
    def add_placeholder(entry, texto):
        """
        Adiciona a funcionalidade de placeholder a uma janela Entry do ttkbootstrap.
        Esta função também configura o estilo 'Placeholder.TEntry' necessário, (pelas minhas pesquisas, parece que n é recomendando fazer isso, mas bora ver no que da).
        """
        estilo = ttk.Style()
        estilo.configure('Placeholder.TEntry', foreground='gray')

        entry.insert(0, texto)
        entry.configure(style='Placeholder.TEntry')

        def passa_por_cima(event):
            # Limpa o placeholder quando a entry recebe foco.
            if entry.cget('style') == 'Placeholder.TEntry':
                entry.delete(0, END)
                entry.configure(style='TEntry')

        def sai_de_cima(event):
            # Restaura o placeholder se a entry perder o foco e estiver vazio."""
            if not entry.get():
                entry.insert(0, texto)
                entry.configure(style='Placeholder.TEntry')
        
        # Associa as funções (event handlers) aos eventos de foco do widget
        entry.bind("<FocusIn>", passa_por_cima)
        entry.bind("<FocusOut>", sai_de_cima)
