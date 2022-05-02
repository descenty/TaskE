import datetime

from currencies_manager import *
from tkinter import *
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from currency import *

months = ["январь", "февраль", "март",
          "апрель", "май", "июнь",
          "июль", "август", "сентябрь",
          "октябрь", "ноябрь", "декабрь"]

quarters = ['01.01.#-31.03.#', '01.04.#-30.06.#', '01.07.#-30.09.#', '01.10.#-31.12.#']


class TkinterManager:

    def __init__(self):
        self.window = None
        self.tab1 = None
        self.tab2 = None
        self.tab_control = None
        self.plot_widget = None
        self.output_lbl = None
        self.currency_combo1 = None
        self.currency_combo2 = None
        self.plot = None

        self.window_size1 = '650x200'
        self.window_size2 = '650x450'
        self.tab_index = 0

        # PARSE CURRENCIES
        self.currencies = CurrenciesManager.parse_currencies_by_date(datetime.date.today())

        # WINDOW PROPERTIES
        self.window = Tk()
        self.window.title('Конвертер валют')
        self.window.geometry(self.window_size1)
        self.window.resizable(False, False)

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
        currency_combo1 = ttk.Combobox(self.tab1, width=25, state='readonly', textvariable=self.currency1_name)
        currency_combo1['values'] = [currency.name for currency in self.currencies]
        currency_combo1.grid(column=0, row=0, padx=20, pady=20)

        currency_combo2 = ttk.Combobox(self.tab1, width=25, state='readonly', textvariable=self.currency2_name)
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

        currency_combo3 = ttk.Combobox(self.tab2, width=25, state='readonly', textvariable=self.currency3_name)
        currency_combo3['values'] = [currency.name for currency in self.currencies]
        currency_combo3.grid(column=0, row=1)

        draw_graph_btn = Button(self.tab2, text='Построить график', command=self.draw_graph_btn_clicked)
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

        # GET TIME PERIODS
        date_today = datetime.date.today()
        isocalendar = datetime.date.today().isocalendar()

        self.week_periods: list[(datetime.date, datetime.date)] = \
            [((date_today - datetime.timedelta(days=isocalendar.weekday + 7 * x - 1)),
              (date_today + datetime.timedelta(days=7 - isocalendar.weekday) - datetime.timedelta(days=7 * x))) for x in range(4)]


        self.month_periods: list[(datetime.date, datetime.date)] = \
            [(date_today.replace(month=date_today.month - x, day=1),
              (date_today.replace(month=date_today.month - x + 1, day=1) -
               datetime.timedelta(days=1))) for x in range(4)]

        self.quarter_periods = \
            [quarters[(date_today.month - 1) // 3 - x]
                 .replace('#', str(date_today.year if (date_today.month - 1) // 3 - x > 0 else date_today.year - 1))
                 .split('-') for x in range(4)]

        self.quarter_periods: list[(datetime.date, datetime.date)] = \
            [(datetime.datetime.strptime(x[0], '%d.%m.%Y'), datetime.datetime.strptime(x[1], '%d.%m.%Y'))
             for x in self.quarter_periods]

        self.year_periods: list[(datetime.date, datetime.date)] = \
            [(datetime.datetime.strptime(f'01.01.{date_today.year - x}', '%d.%m.%Y'),
              datetime.datetime.strptime(f'31.12.{date_today.year - x}', '%d.%m.%Y')) for x in range(4)]

        # PERIOD COMBOS
        week_combo = ttk.Combobox(self.tab2, width=20, state='readonly', textvariable='')
        week_combo['values'] = ['{}-{}'.format(x[0].strftime('%d.%m.%Y'), x[1].strftime('%d.%m.%Y')) for x in
                                self.week_periods]
        week_combo.grid(column=2, row=1)

        month_combo = ttk.Combobox(self.tab2, width=20, state='readonly', textvariable='')
        month_combo['values'] = [f'{months[x[0].month - 1]} {x[0].year}' for x in self.month_periods]
        month_combo.grid(column=2, row=2)

        quarter_combo = ttk.Combobox(self.tab2, width=20, state='readonly', textvariable='')
        quarter_combo['values'] = \
            [f'{range(1, 5)[(date_today.month - 1) // 3 - x]} ' \
             f'квартал {date_today.year if (date_today.month - 1) // 3 - x + 1 > 0 else date_today.year - 1}'
             for x in range(4)]
        quarter_combo.grid(column=2, row=3)

        year_combo = ttk.Combobox(self.tab2, width=20, state='readonly', textvariable='')
        year_combo['values'] = [x[0].year for x in self.year_periods]
        year_combo.grid(column=2, row=4)

        self.graph_period_combos = [week_combo, month_combo, quarter_combo, year_combo]

        # CREATE MATPLOTLIB CANVAS
        figure = Figure(figsize=(6, 2), dpi=100)
        self.f_plot = figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(figure, self.tab2)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=6, column=0, columnspan=3, padx=20, pady=20)

        self.window.mainloop()

    def convert_button_clicked(self):
        currency1: Currency = [x for x in self.currencies if x.name == self.currency1_name.get()][0]
        currency2: Currency = [x for x in self.currencies if x.name == self.currency2_name.get()][0]
        self.output_text.set(str(round((currency1.value / currency2.value) * float(self.input_text.get()), 2)))

    def draw_graph_btn_clicked(self):
        match self.graph_period.get():
            case 0:
                self.draw_graph(
                    dict(zip(TkinterManager.get_days_in_period(self.week_periods[self.graph_period.get()]), CurrenciesManager.parse_currency_at_period([x.char_code for x in self.currencies if x.name == self.currency3_name.get()][0], self.week_periods[self.graph_period.get()], 1))))
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass

    def draw_graph(self, keys_values: dict):
        print(keys_values.keys(), keys_values.values())
        self.f_plot.clear()
        self.f_plot.plot(keys_values.keys(), keys_values.values())
        self.canvas.draw()

    def resize_window(self, event):
        self.window.geometry(self.window_size1 if self.tab_index % 2 == 0 else self.window_size2)
        self.tab_index += 1

    def on_graph_period_change(self, index, value, op):
        [combo.grid_forget() for combo in self.graph_period_combos]
        self.graph_period_combos[self.graph_period.get()].grid(column=2, row=self.graph_period.get() + 1)
        print(self.graph_period.get())

    @staticmethod
    def get_days_in_period(period: tuple[datetime.date, datetime.date]) -> list[str]:
        period = list(period)
        days = []
        while (period[1] - period[0]).days != -1:
            days.append(period[0].strftime('%d/%m'))
            period[0] += datetime.timedelta(days=1)
        return days
