from tkinter import *
import tkinter.ttk as ttk
import send_info
import physics

def rgbtohex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def game_menu(root):

    menu_frame = Frame(root, bg=rgbtohex(r=88, g=88, b=88), width=1400, height=1000)
    menu_frame.pack()

    title = Label(menu_frame, bg=rgbtohex(r=88, g=88, b=88), text='Minesweeper', font=('Arial', 65), fg='white')
    title.pack(pady=60)

    easy = Button(menu_frame, bd=0, bg=rgbtohex(r=137, g=208, b=153), width=20, height=3, activebackground='#31fc5f')
    easy.config(text='EASY', font=('Arial', 35), fg=rgbtohex(r=171, g=250, b=189))
    easy.bind('<Button-1>', lambda event: running_game(root, menu_frame, 1))
    easy.pack()

    medium = Button(menu_frame, bd=0, bg=rgbtohex(r=128, g=130, b=210), width=20, height=3, activebackground='#314cfc')
    medium.config(text='MEDIUM', font=('Arial', 35), fg=rgbtohex(r=172, g=174, b=255))
    medium.bind('<Button-1>', lambda event: running_game(root, menu_frame, 2))
    medium.pack(pady=10)

    hard = Button(menu_frame, bd=0, bg=rgbtohex(r=210, g=128, b=128), width=20, height=3, activebackground='#fc3131')
    hard.config(text='HARD', font=('Arial', 35), fg=rgbtohex(r=255, g=168, b=168))
    hard.bind('<Button-1>', lambda event: running_game(root, menu_frame, 3))
    hard.pack()

    quit = Button(menu_frame, bd=0, bg=rgbtohex(r=60, g=60, b=60), activebackground='#636363', width=10, height=1)
    quit.config(text='Quit', font=('Arial', 35), fg=rgbtohex(r=30, g=30, b=30))
    quit.bind('<Button-1>', lambda event: quit_game(root))
    quit.pack(side='right', pady=40)

def quit_game(root):
    root.destroy()

def previous(root, game_frame, menu_frame, x, y, z):
    physics.create.all = []
    physics.create(game_frame, x, y, z).lose()
    game_frame.pack_forget()
    game_frame.destroy()
    menu_frame.pack_forget()
    menu_frame.destroy()
    game_menu(root)

count = 0
time_loop = None

def running_game(root, menu_frame, difficulty):

    global count

    game_frame = Frame(root, bg=rgbtohex(r=88, g=88, b=88), width=1400, height=1000)
    game_frame.pack()

    menu_frame.pack_forget()
    menu_frame.destroy()

    quit = Button(game_frame, bd=0, bg=rgbtohex(r=60, g=60, b=60))
    quit.config(text='Main Menu', font=('Arial', 35), fg=rgbtohex(r=30, g=30, b=30))
    quit.place(x=1050, y=870, width=300, height=100)

    toggle_grid = Button(game_frame, bd=0, bg=rgbtohex(r=60, g=60, b=60))
    toggle_grid.config(text='Grid', font=('Arial', 25), fg=rgbtohex(r=30, g=30, b=30))
    toggle_grid.place(x=1050, y=800, width=300, height=60)

    if difficulty == 1:
        physics.create(game_frame, 10, 100, 40).do()
        easy = Label(game_frame, bd=0, bg=rgbtohex(r=137, g=208, b=153))
        easy.config(text='EASY', font=('Arial', 35), fg=rgbtohex(r=171, g=250, b=189))
        easy.place(x=1050, y=30, width=300, height=100)
        quit.bind('<Button-1>', lambda event: previous(root, game_frame, menu_frame, 10, 100, 40))
        toggle_grid.bind('<Button-1>', lambda event: physics.create(root, 10, 100, 40).toggle())

    if difficulty == 2:
        physics.create(game_frame, 15, 67, 30).do()
        medium = Label(game_frame, bd=0, bg=rgbtohex(r=128, g=130, b=210))
        medium.config(text='MEDIUM', font=('Arial', 35), fg=rgbtohex(r=172, g=174, b=255))
        medium.place(x=1050, y=30, width=300, height=100)
        quit.bind('<Button-1>', lambda event: previous(root, game_frame, menu_frame, 15, 67, 30))
        toggle_grid.bind('<Button-1>', lambda event: physics.create(root, 15, 67, 30).toggle())

    if difficulty == 3:
        physics.create(game_frame, 20, 50, 25).do()
        hard = Label(game_frame, bd=0, bg=rgbtohex(r=210, g=128, b=128))
        hard.config(text='HARD', font=('Arial', 35), fg=rgbtohex(r=255, g=168, b=168))
        hard.place(x=1050, y=30, width=300, height=100)
        quit.bind('<Button-1>', lambda event: previous(root, game_frame, menu_frame, 20, 50, 25))
        toggle_grid.bind('<Button-1>', lambda event: physics.create(root, 20, 50, 25).toggle())

def update_timer(game_frame, count, seconds):
    stage = physics.create
    global time_loop
    if count < 1000:
        print(stage.cancel_state)
        timer = Label(game_frame)
        if stage.cancel_state == False:
            count = count + seconds
            timer.config(text=round(float(count), 1), font=('Arial', 20), fg=rgbtohex(r=255, g=255, b=255), bd=0,bg=rgbtohex(r=88, g=88, b=88))
            timer.place(x=1050, y=700, width=300, height=100)
            time_loop = game_frame.after(100, lambda: update_timer(game_frame, count, 0.1))
        if stage.cancel_state == True:
            game_frame.after_cancel(time_loop)
            send_info.send_count()
        if stage.cancel_state == None:
            count = 0
            timer.config(text=round(float(count), 1), font=('Arial', 20), fg=rgbtohex(r=255, g=255, b=255), bd=0, bg=rgbtohex(r=88, g=88, b=88))
            game_frame.after_cancel(time_loop)
