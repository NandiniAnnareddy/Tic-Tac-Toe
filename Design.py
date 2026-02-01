from tkinter import *
import logic  

root = Tk()
root.geometry("400x500")
root.title("Tic Tac Toe")

# ---------------- Global Variables ----------------
current_symbol = None
other_symbol = None
player1_name = ""
player2_name = ""
game_mode = None
computer_symbol = None
start_turn = IntVar()
symbol = StringVar()
game_over = False
current_player_name = ""

# ---------------- Screens ----------------
screen1 = Frame(root)
screen2 = Frame(root)
screen3 = Frame(root)
screen_board = Frame(root)

for screen in [screen1, screen2, screen3, screen_board]:
    screen.place(relheight=1, relwidth=1)

def show_screen(frame):
    frame.tkraise()

# ---------------- Board Drawing ----------------
canvas = Canvas(screen_board, width=300, height=300, bg="#F1F1F1")
canvas.grid(row=2, column=0, padx=20, pady=20)

def draw_lines():
    canvas.delete("all")
    for i in range(1, 3):
        canvas.create_line(100*i, 0, 100*i, 300, width=2)
        canvas.create_line(0, 100*i, 300, 100*i, width=2)

draw_lines()

status_label = Label(screen_board, text="", font=("Times New Roman", 14, "bold"), fg="blue")
status_label.grid(row=0, column=0, pady=10)
player_label = Label(screen_board, text="", font=("Times New Roman", 12, "bold"))
player_label.grid(row=1, column=0)

# ---------------- Draw Symbol ----------------
def draw_symbol(row, col, sym):
    x = col * 100 + 50
    y = row * 100 + 50
    canvas.create_text(x, y, text=sym, font=("Times New Roman", 40, "bold"))

def update_labels():
    player_label.config(text=f"{player1_name} vs {player2_name}")
    if game_over:
        return
    status_label.config(text=f"{current_player_name}'s turn", fg="blue")

# ---------------- Board Click Handler ----------------
def click_board(event):
    global current_symbol, other_symbol, game_over, current_player_name

    if game_over:
        return

    row = event.y // 100
    col = event.x // 100

    # Player move
    if logic.board[row][col] == "" and current_player_name != "Computer":
        logic.board[row][col] = current_symbol
        draw_symbol(row, col, current_symbol)

        # Check winner
        if logic.check_winner(current_symbol):
            status_label.config(text=f"{current_player_name} won!", fg="green")
            game_over = True
            return

        # Check draw
        if logic.check_draw():
            status_label.config(text="Draw!", fg="orange")
            game_over = True
            return

        # Switch turn
        if game_mode == 1:  # Two players
            if current_player_name == player1_name:
                current_player_name = player2_name
            else:
                current_player_name = player1_name
            current_symbol = other_symbol if current_symbol == symbol.get() else symbol.get()
            update_labels()
        else:  # Computer vs Player
            current_player_name = "Computer"
            current_symbol = computer_symbol
            update_labels()
            computer_move()

# ---------------- Computer Move ----------------
def computer_move():
    global current_symbol, current_player_name, game_over

    if game_over:
        return

    r, c = logic.computer_move(symbol=current_symbol, player_symbol=symbol.get())
    logic.board[r][c] = current_symbol
    draw_symbol(r, c, current_symbol)

    # Check winner
    if logic.check_winner(current_symbol):
        status_label.config(text="Computer won!", fg="green")
        game_over = True
        return

    # Check draw
    if logic.check_draw():
        status_label.config(text="Draw!", fg="orange")
        game_over = True
        return

    # Switch back to player
    current_player_name = player1_name
    current_symbol = symbol.get()
    update_labels()

canvas.bind("<Button-1>", click_board)

# ---------------- Game Setup ----------------
def choose_two_players():
    global game_mode
    game_mode = 1
    show_screen(screen2)

def choose_computer_vs_player():
    global game_mode
    game_mode = 2
    show_screen(screen3)

def send_names():
    if game_mode == 1:
        return entry1.get() or "Player 1", entry2.get() or "Player 2"
    else:
        return entry3.get() or "Player", "Computer"

def start_game_gui():
    global player1_name, player2_name, current_symbol, other_symbol, game_over, computer_symbol, current_player_name

    player1_name, player2_name = send_names()
    logic.reset_board()
    draw_lines()
    game_over = False

    if game_mode == 1:  # Two players
        if start_turn.get() == 1:
            current_player_name = player1_name
        else:
            current_player_name = player2_name
        current_symbol = symbol.get()
        other_symbol = "O" if symbol.get() == "X" else "X"
        update_labels()
        show_screen(screen_board)

    else:  # Computer vs Player
        # Assign symbols
        if start_turn.get() == 1:  # Player starts
            current_player_name = player1_name
            current_symbol = symbol.get()
            computer_symbol = "O" if symbol.get() == "X" else "X"
            update_labels()
            show_screen(screen_board)
        else:  # Computer starts
            current_player_name = "Computer"
            computer_symbol = "O" if symbol.get() == "X" else "X"
            current_symbol = computer_symbol
            update_labels()
            show_screen(screen_board)
            computer_move()  # Computer makes first move

# ---------------- Screens ----------------
# Screen 1
Label(screen1, text="Tic Tac Toe", font=("Times New Roman", 20, "bold")).pack(pady=30)
Button(screen1, text="Two Players", font=("Times New Roman", 15, "bold"), bg="violet", command=choose_two_players).pack(pady=10)
Button(screen1, text="Computer vs Player", font=("Times New Roman", 15, "bold"), bg="violet", command=choose_computer_vs_player).pack(pady=10)
show_screen(screen1)

# Screen 2: Two Player Mode
start_turn.set(1)
symbol.set("X")

Label(screen2,text="Two Player Mode", font=("Times New Roman",20,"bold")).grid(row=0,column=0,columnspan=3,padx=20,pady=20)
Label(screen2,text="Player 1 : ", font=("Times New Roman",15,"bold")).grid(row=1,column=0,padx=10,pady=10, sticky="e")
Label(screen2,text="Player 2 : ", font=("Times New Roman",15,"bold")).grid(row=2,column=0,padx=10,pady=10, sticky="e")
entry1 = Entry(screen2); entry1.grid(row=1,column=1,pady=10, padx=5)
entry2 = Entry(screen2); entry2.grid(row=2,column=1,pady=10, padx=5)

Label(screen2, text="Who starts first :", font=("Times New Roman",12,"bold")).grid(row=3,column=0,padx=10, pady=10, sticky="e")
Radiobutton(screen2, text="Player 1", variable=start_turn,value=1).grid(row=3,column=1, sticky="w", padx=5)
Radiobutton(screen2, text="Player 2", variable=start_turn,value=2).grid(row=3,column=2, sticky="w", padx=5)

Label(screen2, text="Choose Symbol :", font=("Times New Roman",12,"bold")).grid(row=4,column=0,padx=10, pady=10, sticky="e")
Radiobutton(screen2, text="X", variable=symbol,value="X").grid(row=4,column=1, sticky="w", padx=5)
Radiobutton(screen2, text="O", variable=symbol,value="O").grid(row=4,column=2, sticky="w", padx=5)

Button(screen2,text="Start Game", font=("Times New Roman",10,"bold"), bg="violet", command=start_game_gui).grid(row=5,column=0,columnspan=3,pady=20)

# Screen 3: Computer vs Player
start_turn.set(1)
symbol.set("X")

Label(screen3,text="Computer vs Player Mode", font=("Times New Roman",20,"bold")).grid(row=0,column=0,columnspan=3,padx=20,pady=20)
Label(screen3,text="Player : ", font=("Times New Roman",15,"bold")).grid(row=1,column=0,padx=10,pady=10, sticky="e")
entry3 = Entry(screen3)
entry3.grid(row=1, column=1, columnspan=2, pady=10, padx=5, sticky="w")

Label(screen3,text="Game starts with : ", font=("Times New Roman",12,"bold")).grid(row=2,column=0,padx=10,pady=10, sticky="e")
Radiobutton(screen3,text="Player", variable=start_turn,value=1).grid(row=2,column=1, sticky="w", padx=5)
Radiobutton(screen3,text="Computer", variable=start_turn,value=2).grid(row=2,column=2, sticky="w", padx=5)

Label(screen3,text="Choose Player Symbol : ", font=("Times New Roman",12,"bold")).grid(row=3,column=0,padx=10,pady=10, sticky="e")
Radiobutton(screen3,text="X", variable=symbol,value="X").grid(row=3,column=1, sticky="w", padx=5)
Radiobutton(screen3,text="O", variable=symbol,value="O").grid(row=3,column=2, sticky="w", padx=5)

Button(screen3,text="Start Game", font=("Times New Roman",10,"bold"), bg="violet", command=start_game_gui).grid(row=4,column=0,columnspan=3,pady=20)

# ---------------- Restart Button ----------------
def restart_game():
    global current_symbol, other_symbol, player1_name, player2_name, game_over, computer_symbol
    current_symbol = None
    other_symbol = None
    player1_name = ""
    player2_name = ""
    computer_symbol = None
    game_over = False
    logic.reset_board()
    draw_lines()
    show_screen(screen1)

restart_button = Button(screen_board, text="Restart", font=("Times New Roman", 12, "bold"), bg="red", fg="white", command=restart_game)
restart_button.grid(row=3, column=0, pady=20)

root.mainloop()
