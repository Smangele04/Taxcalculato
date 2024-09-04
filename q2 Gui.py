import tkinter as tk
from tkinter import messagebox, scrolledtext

class TaxCalculator:
    def __init__(self):
        self.employees = {}

    def add_employee(self, name, income, tax_status):
        self.employees[name] = {"income": income, "tax_status": tax_status}

    def calculate_tax(self, name):
        employee = self.employees[name]
        income = employee["income"]
        tax_status = employee["tax_status"]

        if tax_status == "single":
            if income <= 9875:
                tax = income * 0.10
            elif income <= 40125:
                tax = 987.50 + ((income - 9875) * 0.12)
            elif income <= 85525:
                tax = 4617.50 + ((income - 40125) * 0.22)
            else:
                tax = 14605.00 + ((income - 85525) * 0.24)
        elif tax_status == "married":
            if income <= 19750:
                tax = income * 0.10
            elif income <= 80250:
                tax = 1975.00 + ((income - 19750) * 0.12)
            elif income <= 171050:
                tax = 9227.50 + ((income - 80250) * 0.22)
            else:
                tax = 29207.50 + ((income - 171050) * 0.24)
        else:
            tax = 0

        return tax

    def generate_report(self):
        report = ""
        single_total = 0
        married_total = 0

        for name, employee in self.employees.items():
            income = employee["income"]
            tax = self.calculate_tax(name)
            report += f"Name: {name}\n"
            report += f"Income: ZAR{income:.2f}\n"
            report += f"Tax: ZAR{tax:.2f}\n"
            report += "------------------------\n"

            if employee["tax_status"] == "single":
                single_total += income
            elif employee["tax_status"] == "married":
                married_total += income

        report += f"\nSubtotal for Single: ZAR{single_total:.2f}\n"
        report += f"Subtotal for Married: ZAR{married_total:.2f}\n"
        report += "------------------------\n"

        return report

class TaxCalculatorApp:
    def __init__(self, root):
        self.tax_calculator = TaxCalculator()
        self.root = root
        self.root.title("Tax Calculator")
        self.root.configure(bg="Misty Rose")
        self.create_widgets()

    def create_widgets(self):
        # Define common styles
        label_style = {'bg': 'Misty Rose', 'borderwidth': 10, 'fg': 'Black'}
        entry_style = {'bg': '#FFF0F5', 'borderwidth': 12}
        button_style = {'borderwidth': 12, 'bg': '#FF69B4', 'fg': '#ffffff'}

        # Labels
        tk.Label(self.root, text="Name:", **label_style).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Label(self.root, text="Income (ZAR):", **label_style).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Label(self.root, text="Tax Status:", **label_style).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        # Entry fields with placeholder
        self.name_entry = self.create_entry("Enter employee name")
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.income_entry = self.create_entry("Enter income")
        self.income_entry.grid(row=1, column=1, padx=10, pady=10)

        # Dropdown menu for tax status
        self.tax_status_var = tk.StringVar()
        self.tax_status_var.set("single")
        self.tax_status_dropdown = tk.OptionMenu(self.root, self.tax_status_var, "single", "married")
        self.tax_status_dropdown.config(bg="#FFF0F5", fg="#000000")
        self.tax_status_dropdown.grid(row=2, column=1, padx=10, pady=10)

        # Help buttons
        help_button_color = "#FFB6C1"
        self.create_help_button("name").grid(row=0, column=2, padx=10, pady=10)
        self.create_help_button("income").grid(row=1, column=2, padx=10, pady=10)
        self.create_help_button("tax_status").grid(row=2, column=2, padx=10, pady=10)

        # Action buttons
        tk.Button(self.root, text="Add Employee", command=self.add_employee, **button_style).grid(row=3, column=0, columnspan=3, pady=10)
        tk.Button(self.root, text="Generate Report", command=self.generate_report, **button_style).grid(row=4, column=0, columnspan=3, pady=10)

        # Report text area
        self.report_text = scrolledtext.ScrolledText(self.root, width=50, height=15, bg="#FFE4E1", fg="#000000")
        self.report_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    def create_entry(self, placeholder_text):
        entry = tk.Entry(self.root, **{'bg': '#FFF0F5', 'borderwidth': 12})
        entry.insert(0, placeholder_text)
        entry.bind("<FocusIn>", lambda event: self.on_entry_click(event, placeholder_text))
        entry.bind("<FocusOut>", lambda event: self.on_focus_out(event, placeholder_text))
        return entry

    def on_entry_click(self, event, placeholder_text):
        entry = event.widget
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(self, event, placeholder_text):
        entry = event.widget
        if entry.get() == '':
            entry.insert(0, placeholder_text)
            entry.config(fg='grey')

    def create_help_button(self, field):
        return tk.Button(self.root, text="Help", command=lambda: self.show_help(field), bg="#FFB6C1", borderwidth=10)

    def show_help(self, field):
        help_texts = {
            "name": "Enter the full name of the employee.",
            "income": "Enter the income in ZAR. Ensure it is a numeric value.",
            "tax_status": "Select 'single' or 'married' to indicate the tax status."
        }
        help_message = help_texts.get(field, "No help available.")
        messagebox.showinfo("Help", help_message)

    def add_employee(self):
        name = self.name_entry.get().strip()
        if not name or name == "Enter employee name":
            messagebox.showerror("Invalid input", "Please enter a valid name.")
            return

        try:
            income = float(self.income_entry.get())
            if income < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid non-negative income.")
            return

        tax_status = self.tax_status_var.get().lower()
        if tax_status not in ["single", "married"]:
            messagebox.showerror("Invalid input", "Tax status must be 'single' or 'married'.")
            return

        self.tax_calculator.add_employee(name, income, tax_status)
        messagebox.showinfo("Success", "Employee added successfully.")

    def generate_report(self):
        report = self.tax_calculator.generate_report()
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, report)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaxCalculatorApp(root)
    root.mainloop()
