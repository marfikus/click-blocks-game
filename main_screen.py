
from tkinter import Tk, Canvas, Menu
import random


colors = {
    "red": ["#ff0000", "#900000"],
    "green": ["#00ff00", "#009000"],
    "blue": ["#0000ff", "#000090"],
}

class MainScreen:
    def __init__(self, settings):
        self.settings = settings
        self.settings_screen = None
        self.root = None
        self.mainmenu = None
        self.width = None
        self.height = None
        self.matrix = None
        self.c = None
        self.selected_blocks = None
        self.game_is_active = False


    def link_to_mainmenu(self, settings_screen):
        self.settings_screen = settings_screen


    def start_game(self):
        if self.game_is_active:
            self.root.destroy()
            self.game_is_active = False
            self.settings_screen.settings_screen_is_active = False

        self.root = Tk()
        self.root.title("Three identical")
        self.root.resizable(False, False)

        self.mainmenu = Menu(self.root)
        self.root.config(menu=self.mainmenu)
        self.mainmenu.add_command(label="New game", command=self.start_game)
        self.mainmenu.add_command(label="Settings", command=self.show_settings)

        self.width = self.settings.block_size * self.settings.matrix_size
        self.height = self.settings.block_size * self.settings.matrix_size

        self.matrix = [
            [None for _ in range(self.settings.matrix_size)] for _ in range(self.settings.matrix_size)
        ]

        self.c = Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.c.pack()

        x = 0
        y = 0
        for h in range(len(self.matrix)):
            for w in range(len(self.matrix[0])):
                color = random.choice(list(colors.keys()))
                rect = self.c.create_rectangle(x, y, 
                    x + self.settings.block_size, 
                    y + self.settings.block_size, 
                    fill=colors[color][0]
                )
                block = {
                    "rect": rect,
                    "selected": False,
                    "color": color,
                    "matrix_coords": (h, w),
                }
                self.matrix[h][w] = block
                x += self.settings.block_size

            x = 0
            y += self.settings.block_size

        self.selected_blocks = []

        self.c.bind("<Button-1>", self.click_block)
        self.c.bind("<Button-3>", self.add_new_blocks)

        self.game_is_active = True
        self.root.mainloop()


    def show_settings(self):
        self.settings_screen.show()


    def remove_blocks(self, blocks):
        for block in blocks:
            y, x = block["matrix_coords"]
            self.matrix[y][x] = None
            self.c.delete(block["rect"])


    def is_siblings(self, new_block):
        new_block_y, new_block_x = new_block["matrix_coords"]
        for block in self.selected_blocks:
            block_y, block_x = block["matrix_coords"]
            if block_y == new_block_y:
                if (block_x == new_block_x - 1) or (block_x == new_block_x + 1):
                    return True
            elif block_x == new_block_x:
                if (block_y == new_block_y - 1) or (block_y == new_block_y + 1):
                    return True
        return False


    def fall_blocks(self):
        for i in range(len(self.matrix) - 1, 0, -1):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] is None:
                    for k in range(i - 1, -1, -1):
                        if self.matrix[k][j] is not None:
                            block = self.matrix[k][j]
                            self.matrix[k][j] = None
                            block["matrix_coords"] = (i, j)
                            self.c.move(block["rect"], 0, self.settings.block_size * (i - k))
                            self.matrix[i][j] = block
                            break


    def click_block(self, event):
        block_found = False

        for string in self.matrix:
            for block in string:
                if block is None:
                    continue

                rect = block["rect"]
                coords = self.c.coords(rect)
                if (coords[0] <= event.x <= coords[2]) and (coords[1] <= event.y <= coords[3]):

                    if self.settings.remove_all_siblings:
                        siblings = self.find_siblings(block)
                        if len(siblings) >= 3:
                            self.remove_blocks(siblings)
                            self.fall_blocks()
                    else:
                        if block["selected"]:
                            self.c.itemconfig(rect, fill=colors[block["color"]][0])
                            block["selected"] = False
                            self.selected_blocks.remove(block)
                        else:
                            if len(self.selected_blocks) == 0:
                                self.c.itemconfig(rect, fill=colors[block["color"]][1])
                                block["selected"] = True
                                self.selected_blocks.append(block)
                            elif (block["color"] == self.selected_blocks[0]["color"]) and (self.is_siblings(block)):
                                self.c.itemconfig(rect, fill=colors[block["color"]][1])
                                block["selected"] = True
                                self.selected_blocks.append(block)

                                if len(self.selected_blocks) == 3:
                                    self.remove_blocks(self.selected_blocks)
                                    self.selected_blocks.clear()
                                    self.fall_blocks()

                    block_found = True
                    break
            if block_found:
                break


    def add_new_block(self):
        max_attempts = 50
        attempt = 0
        success = False

        h = None
        w = None
        while True:
            attempt += 1
            h = random.randint(0, len(self.matrix) - 1)
            w = random.randint(0, len(self.matrix[0]) - 1)
            if self.matrix[h][w] is None:
                success = True
                break
            if attempt == max_attempts:
                print("Max attempts for adding random block!")
                break

        if not success:
            return False

        color = random.choice(list(colors.keys()))
        x = w * self.settings.block_size
        y = h * self.settings.block_size
        rect = self.c.create_rectangle(x, y, 
            x + self.settings.block_size, 
            y + self.settings.block_size, 
            fill=colors[color][0]
        )
        block = {
            "rect": rect,
            "selected": False,
            "color": color,
            "matrix_coords": (h, w),
        }
        self.matrix[h][w] = block
        return True


    def add_new_blocks(self, event):
        if self.settings.add_multiple_blocks:
            new_blocks_num = random.randint(1, 3)
            for _ in range(new_blocks_num):
                if not self.add_new_block():
                    break
        else:
            self.add_new_block()
        self.fall_blocks()


    def find_siblings(self, block, all_siblings=None):
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

            if (x < 0) or (x > len(self.matrix[0]) - 1):
                continue
            if (y < 0) or (y > len(self.matrix) - 1):
                continue
            if self.matrix[y][x] is None:
                continue
            if self.matrix[y][x]["color"] != block["color"]:
                continue
            if exist_in_all_siblings(self.matrix[y][x]):
                continue

            new_siblings += self.find_siblings(self.matrix[y][x], all_siblings)
        return new_siblings

