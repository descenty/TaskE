from tkinter import *
import tkinter.ttk as ttk
import matplotlib
import matplotlib.pyplot as plt
from currency import *

months = ["янв", "фев", "март", "апр", "май", "июнь", "июль", "авг", "сен", "окт", "ноя", "дек"]


class TkinterManager:

    def __init__(self, currencies: list[Currency]):
        self.tab1 = None
        self.tab2 = None
        self.tab_control = None
        self.plot_widget = None
        self.output_lbl = None
        self.currency_combo1 = None
        self.currency_combo2 = None
        self.currency1_name: StringVar = None
        self.currency2_name: StringVar = None
        self.input_text: StringVar = None
        self.output_text: StringVar = None
        self.currencies: StringVar = currencies

    def create_window(self):
        # WINDOW PROPERTIES
        window = Tk()
        window.title('Конвертер валют')
        window.geometry('600x250')

        # INIT VARIABLES
        self.currency1_name = StringVar()
        self.currency2_name = StringVar()
        self.input_text = StringVar()
        self.output_text = StringVar()

        # ADD TABS
        tab_control = ttk.Notebook(window)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        tab_control.add(self.tab1, text='Калькулятор валют')
        tab_control.add(self.tab2, text='Динамика курса')
        tab_control.pack(expand=1, fill='both')

        # ADD COMPONENTS
        currency_combo1 = ttk.Combobox(self.tab1, width=25, textvariable=self.currency1_name)
        currency_combo1['values'] = [currency.name for currency in self.currencies]
        currency_combo1.grid(column=0, row=0, padx=20, pady=20)

        currency_combo2 = ttk.Combobox(self.tab1, width=25, textvariable=self.currency2_name)
        currency_combo2['values'] = [currency.name for currency in self.currencies]
        currency_combo2.grid(column=0, row=1)

        input_box = Entry(self.tab1, textvariable=self.input_text)
        input_box.grid(column=1, row=0)

        output_lbl = Label(self.tab1, textvariable=self.output_text)
        output_lbl.grid(column=1, row=1)

        convert_btn = Button(self.tab1, text='Конвертировать', command=self.convert_button_clicked)
        convert_btn.grid(column=2, row=0)

        # CREATE MATPLOTLIB CANVAS
        matplotlib.use('TkAgg')
        fig = plt.figure()
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=self.tab2)
        plot_widget = canvas.get_tk_widget()
        plot_widget.grid(row=0, column=0)
        plt.grid()

        self.draw_graph()
        window.mainloop()

    def convert_button_clicked(self):
        currency1: Currency = [x for x in self.currencies if x.name == self.currency1_name.get()][0]
        currency2: Currency = [x for x in self.currencies if x.name == self.currency2_name.get()][0]
        self.output_text.set(str(round((currency1.value / currency2.value) * float(self.input_text.get()), 2)))
        print('huy')

    def draw_graph(self):
        plt.plot(['январь', 'февраль', 'март', 'апрель'], [1, 2, 3, 4])