# ---------- gui.py ----------
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import insert_transaction, delete_transaction, get_transactions, get_summary

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker")
        self.root.geometry("700x500")

        entry_frame = tk.Frame(root)
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Date (YYYY-MM-DD)").grid(row=0, column=0)
        self.date_entry = tk.Entry(entry_frame)
        self.date_entry.grid(row=1, column=0)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

        tk.Label(entry_frame, text="Description").grid(row=0, column=1)
        self.desc_entry = tk.Entry(entry_frame)
        self.desc_entry.grid(row=1, column=1)

        tk.Label(entry_frame, text="Amount").grid(row=0, column=2)
        self.amount_entry = tk.Entry(entry_frame)
        self.amount_entry.grid(row=1, column=2)

        self.type_var = tk.StringVar(value='expense')
        tk.OptionMenu(entry_frame, self.type_var, 'income', 'expense').grid(row=1, column=3, padx=10)

        tk.Button(entry_frame, text="Add", command=self.add_transaction).grid(row=1, column=4, padx=10)

        self.tree = ttk.Treeview(root, columns=("ID", "Date", "Desc", "Amount", "Type"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=20, fill="x")

        tk.Button(root, text="Delete Selected", command=self.delete_selected).pack()

        summary_frame = tk.Frame(root)
        summary_frame.pack(pady=10)

        tk.Button(summary_frame, text="Daily Summary", command=lambda: self.show_summary('daily')).grid(row=0, column=0)
        tk.Button(summary_frame, text="Weekly Summary", command=lambda: self.show_summary('weekly')).grid(row=0, column=1)
        tk.Button(summary_frame, text="Monthly Summary", command=lambda: self.show_summary('monthly')).grid(row=0, column=2)

        self.summary_label = tk.Label(root, text="Summary will appear here")
        self.summary_label.pack(pady=5)

        self.load_data()

    def add_transaction(self):
        try:
            date = self.date_entry.get()
            desc = self.desc_entry.get()
            amount = float(self.amount_entry.get())
            t_type = self.type_var.get()
            insert_transaction(date, desc, amount, t_type)
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_selected(self):
        selected = self.tree.selection()
        if selected:
            tid = self.tree.item(selected[0])["values"][0]
            delete_transaction(tid)
            self.load_data()
        else:
            messagebox.showinfo("Select a row", "Please select a row to delete.")

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for txn in get_transactions():
            self.tree.insert("", "end", values=txn)

    def show_summary(self, period):
        data = get_summary(period)
        income = data.get("income", 0)
        expense = data.get("expense", 0)
        balance = income - expense
        self.summary_label.config(text=f"Income: {income:.2f} | Expense: {expense:.2f} | Balance: {balance:.2f}")

