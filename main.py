
from tkinter import *
import random


colors = {
    "red": ["#ff0000", "#900000"],
    "green": ["#00ff00", "#009000"],
    "blue": ["#0000ff", "#000090"],
}

root = Tk()
root.title("Test")
root.resizable(False, False)

matrix_size = 5
block_size = 40
width = block_size * matrix_size
height = block_size * matrix_size
matrix = [[None for _ in range(matrix_size)] for _ in range(matrix_size)]

c = Canvas(root, width=width, height=height, bg="white")
c.pack()

x = 0
y = 0
for h in range(len(matrix)):
    for w in range(len(matrix[0])):
        color = random.choice(list(colors.keys()))
        rect = c.create_rectangle(x, y, x + block_size, y + block_size, fill=colors[color][0])
        block = {
            "rect": rect,
            "selected": False,
            "color": color,
        }
        matrix[h][w] = block
        x += block_size

    x = 0
    y += block_size


def change_bg(event):
    block_found = False
    for string in matrix:
        for block in string:
            rect = block["rect"]
            coords = c.coords(rect)
            if (coords[0] <= event.x <= coords[2]) and (coords[1] <= event.y <= coords[3]):
                if block["selected"]:
                    c.itemconfig(rect, fill=colors[block["color"]][0])
                else:
                    c.itemconfig(rect, fill=colors[block["color"]][1])
                block["selected"] = not block["selected"]
                block_found = True
                break
        if block_found:
            break


c.bind("<Button-1>", change_bg)
# c.tag_bind("rect", "<Button-1>", change_bg)

root.mainloop()

