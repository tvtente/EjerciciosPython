import tkinter
from tkinter import ttk
from ttkbootstrap import Style


class Application(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.title('Timer')
        self.style = Style()
        # Ahora esta llamada coincide con el nombre de la clase
        self.timer = TimerWidget(self)
        self.timer.pack(fill='both', expand='yes')


# ERROR ORIGINAL: TimerWiget estaba mal escrito y no coincidia con la llamada
# CORRECCION: se corrije el nombre a TimerWidget
class TimerWidget(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # variables
        self.running = tkinter.BooleanVar(value=False)
        self.after_id = tkinter.StringVar()
        self.time_elapsed = tkinter.IntVar()
        self.time_text = tkinter.StringVar(value='00:00:00')

        # timer label
        # ERROR: Labe no existe en ttk
        # CORRECCION: uso Label para mostrar el tiempo
        self.timer_lbl = ttk.Label(self, font='-size 32', anchor='center', textvariable=self.time_text)
        self.timer_lbl.pack(side='top', fill='x', padx=60, pady=20)

        # control buttons
        self.toggle_btn = ttk.Button(self, text='Start', width=10, style='info.TButton', command=self.toggle)
        self.toggle_btn.pack(side='left', fill='x', expand='yes', padx=10, pady=10)

        self.reset_btn = ttk.Button(self, text='Reset', width=10, style='success.TButton', command=self.reset)
        self.reset_btn.pack(side='left', fill='x', expand='yes', pady=10)

        # ERROR ORIGINAL: Buton esta escrito con una sola t
        # CORRECCION: el boton de salida tiene que ser Button
        self.quit_btn = ttk.Button(self, text='Quit', width=10, style='danger.TButton', command=self.quit)
        self.quit_btn.pack(side='left', fill='x', expand='yes', padx=10, pady=10)

    def toggle(self):
        if self.running.get():
            self.pause()
            self.running.set(False)
            self.toggle_btn.configure(text='Start', style='info.TButton')
        else:
            self.start()
            self.running.set(True)
            self.toggle_btn.configure(text='Pause', style='info.Outline.TButton')

    def pause(self):
        # ERROR: aftercancel no lo reconoce Tkinter
        # CORRECCION: after_cancel cancela la llamada que estaba pendiente
        self.after_cancel(self.after_id.get())

    def start(self):
        # Antes la primera llamada esperaba solo 1 ms
        # self.after_id.set(self.after(1, self.increment))
        # CORRECCION: aqui tambien espero 10 ms para el primer incremento
        self.after_id.set(self.after(10, self.increment))

    def increment(self):
        current = self.time_elapsed.get() + 1
        # ERROR ORIGINAL: faltaba un punto entre time_elapsed y set
        # CORRECCION: con .set(current) guardo el valor nuevo
        self.time_elapsed.set(current)
        time_str = '{:02d}:{:02d}:{:02d}'.format((current // 100) // 60, (current // 100) % 60, current % 100)
        self.time_text.set(time_str)
        # ERROR: con 100 ms el contador iba mas lento de lo que marcaba
        # self.after_id.set(self.after(100, self.increment))
        # CORRECCION: cada 10 ms sumo una centesima
        self.after_id.set(self.after(10, self.increment))

    def reset(self):
        self.time_elapsed.set(0)
        self.time_text.set('00:00:00')


if __name__ == '__main__':
    Application().mainloop()