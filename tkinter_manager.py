from tkinter import *
import tkinter.ttk as ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from currency import *

months = ["янв", "фев", "март", "апр", "май", "июнь", "июль", "авг", "сен", "окт", "ноя", "дек"]


class TkinterManager:

    def __init__(self, currencies: list[Currency]):
        self.window = None
        self.tab1 = None
        self.tab2 = None
        self.tab_control = None
        self.plot_widget = None
        self.output_lbl = None
        self.currency_combo1 = None
        self.currency_combo2 = None
        self.plot = None

        self.window_size1 = (650, 250)
        self.window_size2 = (650, 500)
        self.currencies = currencies
        self.tab_index = 0

        # WINDOW PROPERTIES
        self.window = Tk()
        self.window.title('Конвертер валют')
        self.window.geometry('650x250')

        # INIT VARIABLES
        self.currency1_name = StringVar()
        self.currency2_name = StringVar()
        self.currency3_name = StringVar()
        self.input_text = StringVar()
        self.output_text = StringVar()

        self.graph_period = IntVar()
        self.graph_period.trace('w', self.on_graph_period_change)

        # ADD TABS
        tab_control = ttk.Notebook(self.window)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        tab_control.add(self.tab1, text='Калькулятор валют')
        tab_control.add(self.tab2, text='Динамика курса')
        tab_control.pack(expand=1, fill='both')
        tab_control.bind('<<NotebookTabChanged>>', self.resize_window)

        # TAB 1
        # ADD COMPONENTS
        currency_combo1 = ttk.Combobox(self.tab1, width=25, textvariable=self.currency1_name)
        currency_combo1['values'] = [currency.name for currency in self.currencies]
        currency_combo1.grid(column=0, row=0, padx=20, pady=20)

        currency_combo2 = ttk.Combobox(self.tab1, width=25, textvariable=self.currency2_name)
        currency_combo2['values'] = [currency.name for currency in self.currencies]
        currency_combo2.grid(column=0, row=1)

        input_box1 = Entry(self.tab1, textvariable=self.input_text)
        input_box1.grid(column=1, row=0, padx=20, pady=20)

        output_lbl = Label(self.tab1, textvariable=self.output_text)
        output_lbl.grid(column=1, row=1)

        convert_btn = Button(self.tab1, text='Конвертировать', command=self.convert_button_clicked)
        convert_btn.grid(column=2, row=0)

        # TAB 2
        # ADD COMPONENTS
        lbl1 = Label(self.tab2, text='Валюта')
        lbl1.grid(column=0, row=0, pady=10)

        currency_combo3 = ttk.Combobox(self.tab2, width=25, textvariable=self.currency3_name)
        currency_combo3['values'] = [currency.name for currency in self.currencies]
        currency_combo3.grid(column=0, row=1)

        draw_graph_btn = Button(self.tab2, text='Построить график', command=self.draw_graph)
        draw_graph_btn.grid(column=0, row=4)

        lbl2 = Label(self.tab2, text='Период')
        lbl2.grid(column=1, row=0)

        # GRAPH PERIOD
        # RADIOBUTTONS
        radio_button1 = Radiobutton(self.tab2, text='Неделя', value=0, variable=self.graph_period)
        radio_button1.grid(column=1, row=1)

        radio_button2 = Radiobutton(self.tab2, text='Месяц', value=1, variable=self.graph_period)
        radio_button2.grid(column=1, row=2)

        radio_button3 = Radiobutton(self.tab2, text='Квартал', value=2, variable=self.graph_period)
        radio_button3.grid(column=1, row=3)

        radio_button4 = Radiobutton(self.tab2, text='Год', value=3, variable=self.graph_period)
        radio_button4.grid(column=1, row=4)

        # COMBOS
        lbl3 = Label(self.tab2, text='Выбор периода')
        lbl3.grid(column=2, row=0)

        week_combo = ttk.Combobox(self.tab2, width=15, textvariable='')
        week_combo['values'] = [currency.name for currency in self.currencies]
        week_combo.grid(column=2, row=1)

        month_combo = ttk.Combobox(self.tab2, width=15, textvariable='')
        month_combo['values'] = [currency.name for currency in self.currencies]

        quarter_combo = ttk.Combobox(self.tab2, width=15, textvariable='')
        quarter_combo['values'] = [currency.name for currency in self.currencies]

        year_combo = ttk.Combobox(self.tab2, width=15, textvariable='')
        year_combo['values'] = [currency.name for currency in self.currencies]

        self.graph_period_combos = [week_combo, month_combo, quarter_combo, year_combo]

        # CREATE MATPLOTLIB CANVAS
        matplotlib.use('TkAgg')
        figure = Figure(figsize=(6, 2), dpi=100)
        self.plot = figure.add_subplot(1, 1, 1)
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(figure, master=self.tab2)
        canvas.get_tk_widget().grid(row=5, column=0, columnspan=3, padx=20, pady=20)

        self.draw_graph()
        self.window.mainloop()

    def convert_button_clicked(self):
        currency1: Currency = [x for x in self.currencies if x.name == self.currency1_name.get()][0]
        currency2: Currency = [x for x in self.currencies if x.name == self.currency2_name.get()][0]
        self.output_text.set(str(round((currency1.value / currency2.value) * float(self.input_text.get()), 2)))
        print('huy')

    def draw_graph(self):
        self.plot.plot(['январь', 'февраль', 'март', 'апрель'], [1, 2, 3, 4])

    def resize_window(self, event):
        if self.tab_index % 2 == 0:
            self.window.geometry('{}x{}'.format(self.window_size1[0], self.window_size1[1]))
        else:
            self.window.geometry('{}x{}'.format(self.window_size2[0], self.window_size2[1]))
        self.tab_index += 1

    def on_graph_period_change(self, index, value, op):
        [combo.grid_forget() for combo in self.graph_period_combos]
        self.graph_period_combos[self.graph_period.get()].grid(column=2, row=self.graph_period.get() + 1)
        print(self.graph_period.get())

