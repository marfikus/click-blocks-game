
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
            "matrix_coords": (h, w),
        }
        matrix[h][w] = block
        x += block_size

    x = 0
    y += block_size

selected_blocks = []


def remove_selected_blocks():
    for block in selected_blocks:
        y, x = block["matrix_coords"]
        matrix[y][x] = None
        c.delete(block["rect"])

    selected_blocks.clear()


def is_siblings(new_block):
    new_block_y, new_block_x = new_block["matrix_coords"]
    for block in selected_blocks:
        block_y, block_x = block["matrix_coords"]
        if block_y == new_block_y:
            if (block_x == new_block_x - 1) or (block_x == new_block_x + 1):
                return True
        elif block_x == new_block_x:
            if (block_y == new_block_y - 1) or (block_y == new_block_y + 1):
                return True
    return False


def select_block(event):
    block_found = False

    for string in matrix:
        for block in string:
            if block is None:
                continue

            rect = block["rect"]
            coords = c.coords(rect)
            if (coords[0] <= event.x <= coords[2]) and (coords[1] <= event.y <= coords[3]):
                if block["selected"]:
                    c.itemconfig(rect, fill=colors[block["color"]][0])
                    block["selected"] = False
                    selected_blocks.remove(block)
                else:
                    if len(selected_blocks) == 0:
                        c.itemconfig(rect, fill=colors[block["color"]][1])
                        block["selected"] = True
                        selected_blocks.append(block)
                    elif (block["color"] == selected_blocks[0]["color"]) and (is_siblings(block)):
                        # также нужно добавить проверку соседства блоков
                        c.itemconfig(rect, fill=colors[block["color"]][1])
                        block["selected"] = True
                        selected_blocks.append(block)

                        if len(selected_blocks) == 3:
                            remove_selected_blocks()

                block_found = True
                break
        if block_found:
            break


c.bind("<Button-1>", select_block)
# c.tag_bind("rect", "<Button-1>", select_block)

root.mainloop()

