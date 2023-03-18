from tkinter import *
import main_menu

def rgbtohex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

game = Tk()
game.title("Basic Minesweeper")
game.geometry('1400x1000')
game.configure(bg=rgbtohex(r=88, g=88, b=88))

main_menu.game_menu(game)

game.mainloop()