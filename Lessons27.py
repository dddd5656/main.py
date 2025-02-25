import tkinter as tk

# Conversion data
conversion_data = {
    'length': {
        'meters': 1,
        'centimeters': 100,
        'millimeters': 1000,
        'feet': 3.28084,
        'inches': 39.3701
    },
    'mass': {
        'kilograms': 1,
        'grams': 1000,
        'milligrams': 1e6,
        'pounds': 2.20462,
        'ounces': 35.274
    },
    'time': {
        'seconds': 1,
        'minutes': 1 / 60,
        'hours': 1 / 3600,
        'days': 1 / 86400
    },
    'temperature change': {
        'celsius': 1,
        'fahrenheit': 1.8,
        'kelvin': 1
    },
    'electric current': {
        'amperes': 1,
        'milliamperes': 1000,
        'microamperes': 1e6
    },
    'amount of substance': {
        'moles': 1,
        'kilomoles': 1e-3
    },
    'luminous intensity': {
        'candelas': 1
    },
    'speed': {
        'meters per second': 1,
        'kilometers per hour': 3.6,
        'miles per hour': 2.23694
    },
    'area': {
        'square meters': 1,
        'square kilometers': 1e-6,
        'square feet': 10.7639,
        'acres': 0.000247105,
        'hectares': 1e-4
    },
    'volume': {
        'cubic meters': 1,
        'liters': 1000,
        'milliliters': 1e6,
        'cubic feet': 35.3147,
        'gallons': 264.172
    },
    'pressure': {
        'pascals': 1,
        'atmospheres': 9.86923e-6,
        'bars': 0.00001,
        'torr': 0.00750062
    },
    'energy': {
        'joules': 1,
        'kilowatt-hours': 2.77778e-7,
        'calories': 0.239006,
        'BTUs': 0.000947817
    },
    'power': {
        'watts': 1,
        'kilowatts': 0.001,
        'horsepower': 0.00134102
    },
    'frequency': {
        'hertz': 1,
        'kilohertz': 0.001,
        'megahertz': 1e-6
    },
    'digital storage': {
        'bytes': 1,
        'kilobytes': 0.001,
        'megabytes': 1e-6,
        'gigabytes': 1e-9,
        'terabytes': 1e-12
    }
}

class UnitConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter")

        self.unit_type_var = tk.StringVar()
        self.unit_type_var.set('length')

        self.from_unit_var = tk.StringVar()
        self.to_unit_var = tk.StringVar()

        self.unit_label = tk.Label(root, text="Select Unit Category:")
        self.unit_label.grid(row=0, column=0)

        self.unit_menu = tk.OptionMenu(root, self.unit_type_var, *conversion_data.keys())
        self.unit_menu.grid(row=0, column=1)

        self.from_unit_label = tk.Label(root, text="From:")
        self.from_unit_label.grid(row=1, column=0)

        self.from_unit_menu = tk.OptionMenu(root, self.from_unit_var, "")
        self.from_unit_menu.grid(row=1, column=1)

        self.to_unit_label = tk.Label(root, text="To:")
        self.to_unit_label.grid(row=2, column=0)

        self.to_unit_menu = tk.OptionMenu(root, self.to_unit_var, "")
        self.to_unit_menu.grid(row=2, column=1)

        self.input_label = tk.Label(root, text="Input:")
        self.input_label.grid(row=3, column=0)

        self.input_entry = tk.Entry(root)
        self.input_entry.grid(row=3, column=1)

        self.convert_button = tk.Button(root, text="Convert", command=self.convert)
        self.convert_button.grid(row=3, column=2)

        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=4, columnspan=3)

        self.unit_type_var.trace('w', self.update_unit_menus)

    def update_unit_menus(self, *args):
        selected_category = self.unit_type_var.get()
        from_units = list(conversion_data.get(selected_category, {}).keys())
        to_units = from_units[:]
        self.from_unit_menu['menu'].delete(0, 'end')
        self.to_unit_menu['menu'].delete(0, 'end')

        for unit in from_units:
            self.from_unit_menu['menu'].add_command(label=unit, command=lambda value=unit: self.from_unit_var.set(value))

        for unit in to_units:
            self.to_unit_menu['menu'].add_command(label=unit, command=lambda value=unit: self.to_unit_var.set(value))

        self.from_unit_var.set(from_units[0])
        self.to_unit_var.set(to_units[0])

    def convert(self):
        try:
            unit_type = self.unit_type_var.get()
            from_unit = self.from_unit_var.get()
            to_unit = self.to_unit_var.get()
            input_value = float(self.input_entry.get())
            conversions = conversion_data.get(unit_type, {})

            if from_unit in conversions and to_unit in conversions:
                result = (input_value * conversions[to_unit]) / conversions[from_unit]
                result_text = f"{input_value} {from_unit} = {result:.4f} {to_unit}"
                self.result_label.config(text=result_text)
            else:
                self.result_label.config(text="Invalid units")

        except ValueError:
            self.result_label.config(text="Invalid input")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnitConverterApp(root)
    root.mainloop()