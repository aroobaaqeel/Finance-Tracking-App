# ---------- main.py ----------
from tkinter import Tk
from db import init_db
from gui import FinanceApp

if __name__ == "__main__":
    init_db()
    root = Tk()
    app = FinanceApp(root)
    root.mainloop()
