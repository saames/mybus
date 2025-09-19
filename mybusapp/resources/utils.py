import ttkbootstrap as ttk

class Utils:
    # Placeholder
    def add_placeholder(entry, texto):
        """
        Adiciona a funcionalidade de placeholder a uma janela Entry do ttkbootstrap.
        Esta função também configura o estilo 'Placeholder.TEntry' necessário.
        """
        estilo = ttk.Style()
        estilo.configure('Placeholder.TEntry', foreground='gray')

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