import datetime
from tkinter import *
import tkinter.ttk as ttk
import matplotlib
import matplotlib.pyplot as plt
from currency import *

months = ["янв", "фев", "март", "апр", "май", "июнь", "июль", "авг", "сен", "окт", "ноя", "дек"]


class TkinterManager:
    def __init__(self, currencies: list[Currency]):
        self.tab_control = None
        self.currencies = currencies

    def create_window(self):
        window = Tk()
        window.title('Конвертер валют')
        window.geometry('600x200')

        self.tab_control = ttk.Notebook(window)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Калькулятор валют')
        self.tab_control.add(self.tab2, text='Динамика курса')

        combo = ttk.Combobox(self.tab1)
        combo['values'] = ['раз', 'два', 'три']
        combo.grid(column=0, row=0)

        txt = Entry(self.tab1)
        btn = Button(self.tab1, text='Действие', command='clicked')
        lbl = Label(self.tab1, text='')

        self.tab_control.pack(expand=1, fill='both')
        self.draw_graph()
        window.mainloop()

    def draw_graph(self):
        matplotlib.use('TkAgg')
        fig = plt.figure()
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=self.tab2)
        plot_widget = canvas.get_tk_widget()
        fig.clear()
        plt.plot(['январь', 'февраль', 'март', 'апрель'], [1, 2, 3, 4])
        plt.grid()
        plot_widget.grid(row=0, column=0)