import tkinter as tk
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import animation as anm
from matplotlib.figure import Figure
from tkinter import ttk
from scipy import stats

matplotlib.use("TkAgg")

class App:
    def __init__(self):
        self.window = tk.Tk("Ley Normal de Fallas")
        self.f = Figure(figsize=(5,3.5), dpi=100)
        self.a = self.f.add_subplot(111)
        self.showerror = tk.StringVar(self.window, "0")
        self.Media = tk.StringVar(self.window, "0")
        self.Dst = tk.StringVar(self.window, "1")
        self.Func = tk.StringVar(self.window, "1")
        self.Limite = tk.StringVar(self.window, "0%")
        self.failfunc = tk.StringVar(self.window, "La probalilidad de que el componente falle es:")
        self.setUI()
        self.ani = anm.FuncAnimation(self.f, self.calc, interval=500)
        self.window.mainloop()
    
    def setUI(self):
        self.sidePanel = tk.Frame(self.window, width=200, background="#EDEDED", borderwidth=5)
        self.sidePanel.pack_propagate(0)
        self.sidePanel.pack(side=tk.RIGHT, fill=tk.Y)

        self.LTitle = tk.Label(self.window, text = "Probabilidad de que un componente falle o continue funcionando")
        self.LTitle.pack()

        canvas = FigureCanvasTkAgg(self.f, self.window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.CLabel = ttk.Label(self.sidePanel, text="\n¿Que desea calcular?:")
        self.CLabel.pack(side=tk.TOP, anchor="w")

        self.CRadioF = ttk.Radiobutton(self.sidePanel, text= " La probabilidad de que\n continue en funcionamiento", variable=self.showerror, value = "0")
        self.CRadioF.pack(side=tk.TOP, anchor="w")

        self.CRadioE = ttk.Radiobutton(self.sidePanel, text= " La probabilidad de que\n falle", variable=self.showerror, value = "1")
        self.CRadioE.pack(side=tk.TOP, anchor="w")

        self.MLabel = ttk.Label(self.sidePanel, text="Vida media del componente:", width=10)
        self.MLabel.pack(side=tk.TOP, anchor="w")

        self.MBox = tk.Entry(self.sidePanel, textvariable=self.Media, width=10)
        self.MBox.pack(side=tk.TOP, anchor="w")

        self.DLabel = ttk.Label(self.sidePanel, text="Variacion en la vida componente:", width=15, wraplength= 200)
        self.DLabel.pack(side=tk.TOP, anchor="w")

        self.DBox = ttk.Entry(self.sidePanel, textvariable=self.Dst, width=10)
        self.DBox.pack(side=tk.TOP, anchor="w")

        self.FLabel = ttk.Label(self.sidePanel, text="Uso del componente:", width=15, wraplength= 200)
        self.FLabel.pack(side=tk.TOP, anchor="w")

        self.FBox = ttk.Entry(self.sidePanel, textvariable=self.Func, width=10)
        self.FBox.pack(side=tk.TOP, anchor="w")

        self.LLabel = ttk.Label(self.sidePanel, textvariable=self.failfunc , width=20, wraplength= 150)
        self.LLabel.pack(side=tk.TOP, anchor="w")

        self.LRes = ttk.Label(self.sidePanel, textvariable=self.Limite , width=20, wraplength= 150)
        self.LRes.pack(side=tk.TOP, anchor="w")

    def calc(self, i):
        media = 0
        dst = 1
        lim = 1
        try:
            media = float(self.Media.get())
            dst = float(self.Dst.get())
            if self.showerror.get() == "1":
                lim = stats.norm(media, dst).cdf(float(self.Func.get()))
            else:
                lim = stats.norm(media, dst).sf(float(self.Func.get()))
            self.Limite.set(str('%.3f'%(lim*100)) + "%")

            pl = np.linspace(media - 3*dst, media + 3*dst, 100)
            A1 = np.linspace(media - 3*dst - ((media - 3*dst) + 6*dst*lim), media + 3*dst - ((media - 3*dst) + 6*dst*lim), 100)
            A2 = np.linspace(media - 3*dst - ((media + 3*dst) - 6*dst*lim), media + 3*dst - ((media + 3*dst) - 6*dst*lim), 100)

            self.a.clear()
            self.a.plot(pl, stats.norm.pdf(pl, media, dst))

            if self.showerror.get() == "1":
                self.failfunc.set("La probalilidad de que el componente falle es:")
                self.a.fill_between(pl, 0.000001/(A1), stats.norm.pdf(pl, media, dst),where=(0.01/A1>0))
            else:
                self.failfunc.set("La probalilidad de que el componente continue funcionando es:")
                self.a.fill_between(pl, 0.000001/(A2), stats.norm.pdf(pl, media, dst),where=(0.01/A2<0))
        except:
            pass


program = App()