from collections import OrderedDict
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import tkinter

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from turing_pattern import GrayScott

matplotlib.use('TkAgg')


contrast_factor = 2.5
draw_skip: int = 1

def contrast_fcn(a: np.ndarray):
    x = a * contrast_factor
    return (np.exp(2*x) - 1) / (np.exp(2*x) + 1)

def set_contrast_factor(x):
    global contrast_factor
    contrast_factor = float(x)

def set_draw_skip(skip: int):
    global draw_skip
    draw_skip = int(skip)

m = GrayScott(height=256, width=256)

fig, ax = plt.subplots(figsize=(6, 6))
plt.subplots_adjust(wspace=0, hspace=0.1, left=0, bottom=0.0, top=1.0, right=1)

im = ax.imshow(contrast_fcn(m.v), cmap="jet", vmin=0.0, vmax=1.0)
root = tkinter.Tk()
root.title("Gray Scott Reaction")

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=0)

config_pannel = tkinter.Frame(master=root, padx=5)
config_pannel.grid(column=1, row=0)

config_sliders = OrderedDict({
            #min, max, resolution, default, command
    "F": (0.001, 0.3, 0.001, m.F, m.set_F),
    "k": (0.001, 0.3, 0.001, m.k, m.set_k),
    "Du": (0.0, 0.3, 0.001, m.Du, m.set_Du),
    "Dv": (0.0, 0.3, 0.001, m.Dv, m.set_Dv),
    "draw_skip": (1, 100, 1, draw_skip, set_draw_skip),
    "contrast_factor": (0.1, 10, 0.1, contrast_factor, set_contrast_factor)
})

for i, k in enumerate(config_sliders):
    label = tkinter.Label(master=config_pannel, text=k)
    label.grid(column=0, row=i)

    vmin, vmax, res, default_value, cmd = config_sliders[k]

    slider = tkinter.Scale(master=config_pannel,
                            from_=vmin,
                            to=vmax,
                            resolution=res,
                            command=cmd,
                            orient="horizontal")
    slider.grid(column=1, row=i)
    slider.set(default_value)

msg = tkinter.Label(master=config_pannel, text="Hit <space> bar to reset".format(m.dt), pady=30)
msg.grid(column=0, row=len(config_sliders))


reset_flag = False
after_id = None
def update_ani():
    global after_id, reset_flag
    if reset_flag:
        m.reset()
        reset_flag = False

    m.update()
    if m.cnt % draw_skip == 0:
        im.set_array(contrast_fcn(m.v))
        canvas.draw()
    after_id = root.after(3, update_ani)

def on_reset(event=None):
    global reset_flag
    reset_flag = True

def on_destroy(event):
    global after_id
    if event.widget is not root:
        return
    if after_id:
        root.after_cancel(after_id)
        after_id = None
    root.destroy()
    root.quit()

root.bind("<space>", on_reset)
root.bind("<Destroy>", on_destroy)
update_ani()
tkinter.mainloop()
