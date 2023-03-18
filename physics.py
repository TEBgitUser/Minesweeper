from tkinter import *
import main_menu
import random
import send_info
import time

def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

class create():

    all = []
    not_all = []
    bombs = []
    not_bombs = []
    to_delete = []
    click = 1
    win = 0
    flagged = []
    state = False
    cancel_state = None
    i = 0

    def __init__(self, window, grid, size, font):
        self.window = window
        self.grid = grid
        self.size = size
        self.font = font
        self.x = 0
        self.y = 0
        self.chances = [1, 2, 3, 4]
        self.mesh = [(self.x,self.y) for self.x in range(self.grid) for self.y in range(self.grid)]
        if self.grid == 20:
            self.bomb_image = PhotoImage(file=r"C:\Users\Uczeń\PycharmProjects\pythonProject\minesweeper_v2\bomb.png").zoom(3, 3)
        if self.grid == 15:
            self.bomb_image = PhotoImage(file=r"C:\Users\Uczeń\PycharmProjects\pythonProject\minesweeper_v2\bomb.png").zoom(4, 4)
        if self.grid == 10:
            self.bomb_image = PhotoImage(file=r"C:\Users\Uczeń\PycharmProjects\pythonProject\minesweeper_v2\bomb.png").zoom(6, 6)

    def do(self):
        for i in range(self.grid * self.grid):
            button = Button(self.window, bg=rgbtohex(r=200, g=200, b=200), bd=2, activebackground='#d1d1d1')
            button.place(x = self.mesh[i][0] * self.size, y = self.mesh[i][1]* self.size, width=self.size, height=self.size)
            self.restart(button, i)
            self.bind(button)

    def restart(self, button, i):
        create.all.extend([self.mesh[i][0] * self.size, self.mesh[i][1] * self.size, button])
        create.not_all.extend([self.mesh[i][0] * self.size, self.mesh[i][1] * self.size, button])

    def bind(self, button):
        button.bind('<Button-1>', lambda event: self.randomize(button))
        button.bind('<Button-3>', lambda event: self.flag(button))
        button.bind('<Button-2>', lambda event: self.cheat())

    def cheat(self):
        for x in range(int(len(create.bombs) / 3)):
            create.bombs[x * 3 + 2].config(image=self.bomb_image)

    def randomize(self, button):
        if create.click == 1:
            find = create.all.index(button)
            self.first_click(button, find)
            self.makebombs()
        else:
            self.next_click(button)

    def first_click(self, button, find):
        self.window.after(0, lambda: main_menu.update_timer(self.window, 0, 0.1))
        create.cancel_state = False
        create.click-=1
        for x in range(  int(len(create.all)/3)   ):
            if create.all[find-2] in range(int(create.all[x * 3] - (self.size+1)), int(create.all[x*3] + (self.size+1))):
                if create.all[find-1] in range(int(create.all[x * 3 + 1] - (self.size+1)), int(create.all[x * 3 + 1] + (self.size+1))):
                    create.to_delete.extend([x * 3, x * 3 + 1, x * 3 + 2])
        for x in sorted(create.to_delete, reverse=True):
            del create.not_all[x]

    def next_click(self, button):

        if button in create.bombs:
            self.restart_button()

        if button in create.not_bombs:
            button.configure(bg=rgbtohex(r=180, g=180, b=180))
            self.check(button)

    def restart_button(self):
        for x in range(int(len(create.bombs) / 3)):
            create.bombs[x * 3 + 2].config(image=self.bomb_image)
            create.bombs[x * 3 + 2].unbind('<Button-3>')
            create.bombs[x * 3 + 2].unbind('<Button-1>')

            if create.bombs[x * 3 + 2] in create.flagged:
                create.bombs[x * 3 + 2].config(bg = rgbtohex(r=149, g=223, b=173))
            else:
                create.bombs[x * 3 + 2].config(bg = rgbtohex(r=223, g=149, b=149))

        for x in range(int(len(create.not_bombs) / 3)):
            self.check(create.not_bombs[x * 3 + 2])

        create.cancel_state = None
        r_button = Button(self.window, text='Restart', font=('Arial', 35), fg=rgbtohex(r=241, g=191, b=191), bg = rgbtohex(r=223, g=149, b=149), bd=0)
        r_button.bind('<Button-1>', lambda event:self.delete_button(r_button))
        r_button.place(x=1050, y=600, width=300, height=100)

    def delete_button(self, button):
        button.destroy()
        self.lose()

    def check(self, button):
        find = create.all.index(button)
        count = 0
        for x in range(int(len(create.bombs)/3)):
            if create.all[find - 2] in range(int(create.bombs[x * 3] - (self.size+1)), int(create.bombs[x * 3] + (self.size+1))):
                if create.all[find - 1] in range(int(create.bombs[x * 3 + 1] - (self.size+1)), int(create.bombs[x * 3 + 1] + (self.size+1))):
                    count+=1
        self.colors(count, button)

    def flag(self, button):
        if button in create.flagged:
            # untagging box
            button.configure(background=rgbtohex(r=200, g=200, b=200), fg=rgbtohex(r=200, g=200, b=200))
            button.bind('<Button-1>', lambda event: self.randomize(button))
            if button in create.bombs:
                # untagging bomb
                create.win-=1
            else:
                pass
            create.flagged.remove(button)
        else:
            # tagging box
            button.configure(background=rgbtohex(r=150, g=150, b=200), fg=rgbtohex(r=150, g=150, b=200))
            button.unbind('<Button-1>')
            create.flagged.append(button)
            if button in create.bombs:
                # tagging bomb
                create.win+=1
                print(str(create.win) + '/' + str(int(len(create.bombs) / 3)))
                if int(create.win) == int(len(create.bombs)/3):
                    create.cancel_state = True
                    self.success()
            else:
                pass

    def makebombs(self):
        try:
            for x in range(int(len(create.not_all)/3)):
                if random.choice(self.chances) == 1:
                    create.bombs.extend([ create.not_all[x * 3], create.not_all[x * 3 + 1], create.not_all[x * 3 + 2] ])
                else:
                    create.not_bombs.extend([ create.not_all[x * 3], create.not_all[x * 3 + 1], create.not_all[x * 3 + 2] ])

            for y in range(int(len(create.to_delete)/3)):
                create.not_bombs.extend([create.all[create.to_delete[y * 3]], create.all[create.to_delete[y * 3 + 1]], create.all[create.to_delete[y * 3 + 2]]])
                self.next_click(create.all[create.to_delete[y * 3 + 2]])
        except Exception as ex:
            print(ex)

    def toggle(self):
        if create.state == False:
            for x in range(int(len(create.all)/3)):
                create.all[x * 3 + 2].config(bd=0)
                create.state = True
        else:
            for x in range(int(len(create.all)/3)):
                create.all[x * 3 + 2].config(bd=2)
                create.state = False

    def success(self):
        for x in range(int(len(create.bombs) / 3)):
            create.bombs[x * 3 + 2].config(image=self.bomb_image)
            if create.bombs[x * 3 + 2] in create.flagged:
                create.bombs[x * 3 + 2].config(bg = rgbtohex(r=149, g=223, b=173))


    def lose(self):

        create.not_all = []
        for x in range(len(create.all)):
            create.not_all.append(create.all[x])

        create.bombs = []
        create.not_bombs = []
        create.to_delete = []
        create.click = 1
        create.win = 0
        create.flagged = []

        for x in range(int(len(create.all)/3)):
            create.all[x*3+2].unbind('<Button-1>')
            create.all[x*3+2].unbind('<Button-3>')
            create.all[x*3+2].configure(text='', image='',bg=rgbtohex(r=200, g=200, b=200), fg=rgbtohex(r=0, g=0, b=0))
            self.bind(create.all[x*3+2])

    def colors(self, count, button):
        if count == 0:
            button.configure(bg=rgbtohex(r=180, g=180, b=180))
        if count == 1:
            button.configure(text=str(count), font=('Arial', self.font), bg=rgbtohex(r=180, g=180, b=180), fg=rgbtohex(r=20, g=100, b=200))
        if count == 2:
            button.configure(text=str(count), font=('Arial', self.font), bg=rgbtohex(r=180, g=180, b=180), fg=rgbtohex(r=50, g=160, b=80))
        if count == 3:
            button.configure(text=str(count), font=('Arial', self.font), bg=rgbtohex(r=180, g=180, b=180), fg=rgbtohex(r=200, g=40, b=20))
        if count == 4:
            button.configure(text=str(count), font=('Arial', self.font), bg=rgbtohex(r=180, g=180, b=180), fg=rgbtohex(r=140, g=20, b=200))
        if count == 5:
            button.configure(text=str(count), font=('Arial', self.font), bg=rgbtohex(r=180, g=180, b=180), fg=rgbtohex(r=255, g=0, b=24))
        if count == 6:
            button.configure(text=str(count), font=('Arial', self.font), bg=rgbtohex(r=180, g=180, b=180), fg=rgbtohex(r=120, g=200, b=210))
        if count == 7:
            button.configure(text=str(count), font=('Arial', self.font), bg=rgbtohex(r=180, g=180, b=180), fg=rgbtohex(r=255, g=0, b=24))
        if count == 8:
            button.configure(text=str(count), font=('Arial', self.font), bg=rgbtohex(r=180, g=180, b=180), fg=rgbtohex(r=255, g=0, b=24))
        button.unbind("<Button-3>")