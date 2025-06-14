
from tkinter import *
import random
from settings import Settings
from settings_screen import SettingsScreen


colors = {
    "red": ["#ff0000", "#900000"],
    "green": ["#00ff00", "#009000"],
    "blue": ["#0000ff", "#000090"],
}

root = Tk()
root.title("Three identical")
root.resizable(False, False)

settings = Settings()
settings_screen = SettingsScreen(settings)

width = settings.block_size * settings.matrix_size
height = settings.block_size * settings.matrix_size
matrix = [[None for _ in range(settings.matrix_size)] for _ in range(settings.matrix_size)]

c = Canvas(root, width=width, height=height, bg="white")
c.pack()

x = 0
y = 0
for h in range(len(matrix)):
    for w in range(len(matrix[0])):
        color = random.choice(list(colors.keys()))
        rect = c.create_rectangle(x, y, x + settings.block_size, y + settings.block_size, fill=colors[color][0])
        block = {
            "rect": rect,
            "selected": False,
            "color": color,
            "matrix_coords": (h, w),
        }
        matrix[h][w] = block
        x += settings.block_size

    x = 0
    y += settings.block_size

selected_blocks = []


def remove_blocks(blocks):
    for block in blocks:
        y, x = block["matrix_coords"]
        matrix[y][x] = None
        c.delete(block["rect"])


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


def fall_blocks():
    for i in range(len(matrix) - 1, 0, -1):
        for j in range(len(matrix[0])):
            if matrix[i][j] is None:
                for k in range(i - 1, -1, -1):
                    if matrix[k][j] is not None:
                        block = matrix[k][j]
                        matrix[k][j] = None
                        block["matrix_coords"] = (i, j)
                        c.move(block["rect"], 0, settings.block_size * (i - k))
                        matrix[i][j] = block
                        break


def click_block(event):
    block_found = False

    for string in matrix:
        for block in string:
            if block is None:
                continue

            rect = block["rect"]
            coords = c.coords(rect)
            if (coords[0] <= event.x <= coords[2]) and (coords[1] <= event.y <= coords[3]):

                if settings.remove_all_siblings:
                    siblings = find_siblings(block)
                    if len(siblings) >= 3:
                        remove_blocks(siblings)
                        fall_blocks()
                else:
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
                            c.itemconfig(rect, fill=colors[block["color"]][1])
                            block["selected"] = True
                            selected_blocks.append(block)

                            if len(selected_blocks) == 3:
                                remove_blocks(selected_blocks)
                                selected_blocks.clear()
                                fall_blocks()

                block_found = True
                break
        if block_found:
            break


def add_new_block():
    max_attempts = 50
    attempt = 0
    success = False

    h = None
    w = None
    while True:
        attempt += 1
        h = random.randint(0, len(matrix) - 1)
        w = random.randint(0, len(matrix[0]) - 1)
        if matrix[h][w] is None:
            success = True
            break
        if attempt == max_attempts:
            print("Max attempts for adding random block!")
            break

    if not success:
        return False

    color = random.choice(list(colors.keys()))
    x = w * settings.block_size
    y = h * settings.block_size
    rect = c.create_rectangle(x, y, x + settings.block_size, y + settings.block_size, fill=colors[color][0])
    block = {
        "rect": rect,
        "selected": False,
        "color": color,
        "matrix_coords": (h, w),
    }
    matrix[h][w] = block
    return True


def add_new_blocks(event):
    if settings.add_multiple_blocks:
        new_blocks_num = random.randint(1, 3)
        for _ in range(new_blocks_num):
            if not add_new_block():
                break
    else:
        add_new_block()
    fall_blocks()


def find_siblings(block, all_siblings=None):
    directions = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1)
    ]

    if all_siblings is None:
        all_siblings = []
    new_siblings = []

    def exist_in_all_siblings(check_block):
        for block in all_siblings:
            if check_block["rect"] == block["rect"]:
                return True
        return False


    all_siblings.append(block)
    new_siblings.append(block)

    for direction in directions:
        x = block["matrix_coords"][1] + direction[1]
        y = block["matrix_coords"][0] + direction[0]

        if (x < 0) or (x > len(matrix[0]) - 1):
            continue
        if (y < 0) or (y > len(matrix) - 1):
            continue
        if matrix[y][x] is None:
            continue
        if matrix[y][x]["color"] != block["color"]:
            continue
        if exist_in_all_siblings(matrix[y][x]):
            continue

        new_siblings += find_siblings(matrix[y][x], all_siblings)
    return new_siblings


def start_game():
    print("start_game")


c.bind("<Button-1>", click_block)
c.bind("<Button-3>", add_new_blocks)

mainmenu = Menu(root)
root.config(menu=mainmenu)
mainmenu.add_command(label="New game", command=start_game)
mainmenu.add_command(label="Settings", command=settings_screen.show)

root.mainloop()

