import tkinter as tk
from simulator import AntSimulationApp

if __name__ == "__main__":
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - 600) // 2
    y = (screen_height - 850) // 2

    root.geometry(f"{600}x{850}+{x}+{y}")
    root.update()

    app = AntSimulationApp(root)
    root.mainloop()