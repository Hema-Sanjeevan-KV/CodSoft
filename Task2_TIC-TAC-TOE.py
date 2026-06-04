import tkinter as tk
from tkinter import messagebox


# TIC TAC TOE

root = tk.Tk()
root.title("⚡AI Tic-Tac-Toe")
root.geometry("900x760")
root.configure(bg="#090B1A")
root.resizable(False, False)

board = [""] * 9
player_score = 0
ai_score = 0
draw_score = 0
difficulty = tk.StringVar(value="Impossible")

CELL = 140
BOARD_SIZE = CELL * 3


# UI

title = tk.Label(
    root,
    text="⚡ AI TIC-TAC-TOE",
    font=("Segoe UI", 26, "bold"),
    bg="#090B1A",
    fg="#FFFFFF"
)
title.pack(pady=10)

top_frame = tk.Frame(root, bg="#090B1A")
top_frame.pack()

score_var = tk.StringVar()
score_label = tk.Label(
    top_frame,
    textvariable=score_var,
    font=("Segoe UI", 14, "bold"),
    bg="#1A1040",
    fg="white",
    padx=20,
    pady=10
)
score_label.pack(side="left", padx=10)

difficulty_menu = tk.OptionMenu(
    top_frame, difficulty, "Easy", "Medium", "Impossible"
)
difficulty_menu.config(
    bg="#7A1FFF",
    fg="white",
    font=("Segoe UI", 11, "bold")
)
difficulty_menu.pack(side="left")

status_var = tk.StringVar(value="😊 Your Turn (X)")
status = tk.Label(
    root,
    textvariable=status_var,
    font=("Segoe UI", 16, "bold"),
    bg="#090B1A",
    fg="#00FF99"
)
status.pack(pady=10)

canvas = tk.Canvas(
    root,
    width=BOARD_SIZE,
    height=BOARD_SIZE,
    bg="#13002B",
    highlightthickness=0
)
canvas.pack(pady=10)


# DRAW

def update_score():
    score_var.set(
        f"😊 Player: {player_score}    🤖 AI: {ai_score}    🤝 Draws: {draw_score}"
    )

def draw_grid():
    canvas.delete("grid")

    for i in range(1, 3):
        x = i * CELL

        # glow effect
        canvas.create_line(x, 0, x, BOARD_SIZE,
                           fill="#7A1FFF", width=10, tags="grid")
        canvas.create_line(0, x, BOARD_SIZE, x,
                           fill="#7A1FFF", width=10, tags="grid")

        canvas.create_line(x, 0, x, BOARD_SIZE,
                           fill="#FF4DFF", width=4, tags="grid")
        canvas.create_line(0, x, BOARD_SIZE, x,
                           fill="#FF4DFF", width=4, tags="grid")

def draw_x(index):
    row, col = divmod(index, 3)
    x1 = col * CELL + 35
    y1 = row * CELL + 35
    x2 = x1 + 70
    y2 = y1 + 70

    canvas.create_line(x1, y1, x2, y2,
                       fill="#66B3FF", width=8)
    canvas.create_line(x2, y1, x1, y2,
                       fill="#66B3FF", width=8)

def draw_o(index):
    row, col = divmod(index, 3)
    x = col * CELL + 35
    y = row * CELL + 35

    canvas.create_oval(
        x, y, x + 70, y + 70,
        outline="#FF7B39",
        width=8
    )


# GAME LOGIC

def check_winner(brd):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for a,b,c in wins:
        if brd[a] == brd[b] == brd[c] and brd[a] != "":
            return brd[a], (a,b,c)

    if "" not in brd:
        return "Draw", None

    return None, None

def minimax(brd, maximizing):
    result, _ = check_winner(brd)

    if result == "O":
        return 1
    if result == "X":
        return -1
    if result == "Draw":
        return 0

    if maximizing:
        best = -999
        for i in range(9):
            if brd[i] == "":
                brd[i] = "O"
                best = max(best, minimax(brd, False))
                brd[i] = ""
        return best
    else:
        best = 999
        for i in range(9):
            if brd[i] == "":
                brd[i] = "X"
                best = min(best, minimax(brd, True))
                brd[i] = ""
        return best

def draw_win_line(combo):
    coords = {
        0:(70,70),1:(210,70),2:(350,70),
        3:(70,210),4:(210,210),5:(350,210),
        6:(70,350),7:(210,350),8:(350,350)
    }

    x1,y1 = coords[combo[0]]
    x2,y2 = coords[combo[2]]

    canvas.create_line(
        x1,y1,x2,y2,
        fill="#00FF99",
        width=10
    )

def reset_board():
    global board
    board = [""] * 9
    canvas.delete("all")
    draw_grid()
    status_var.set("😊 Your Turn (X)")

def end_game(result, combo):
    global player_score, ai_score, draw_score

    if combo:
        draw_win_line(combo)

    if result == "X":
        player_score += 1
        update_score()
        messagebox.showinfo("Winner", "🎉 You Won!")

    elif result == "O":
        ai_score += 1
        update_score()
        messagebox.showinfo("Winner", "🤖 AI Wins!")

    else:
        draw_score += 1
        update_score()
        messagebox.showinfo("Draw", "🤝 Match Draw!")

    reset_board()

def ai_move():
    status_var.set("🤖 AI Thinking...")
    root.update()

    level = difficulty.get()

    if level == "Easy":
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                draw_o(i)
                break

    else:
        best = -999
        move = None

        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = ""

                if score > best:
                    best = score
                    move = i

        if move is not None:
            board[move] = "O"
            draw_o(move)

    result, combo = check_winner(board)

    if result:
        end_game(result, combo)
    else:
        status_var.set("😊 Your Turn (X)")

def click(event):
    col = event.x // CELL
    row = event.y // CELL

    idx = row * 3 + col

    if idx > 8:
        return

    if board[idx] == "":
        board[idx] = "X"
        draw_x(idx)

        result, combo = check_winner(board)

        if result:
            end_game(result, combo)
            return

        root.after(300, ai_move)

canvas.bind("<Button-1>", click)

draw_grid()
update_score()

tk.Button(
    root,
    text="🔄 NEW GAME",
    font=("Segoe UI", 14, "bold"),
    bg="#7A1FFF",
    fg="white",
    padx=25,
    pady=10,
    relief="flat",
    command=reset_board
).pack(pady=15)

tk.Label(
    root,
    text="CodSoft AI Internship Project • Cyberpunk Edition",
    bg="#090B1A",
    fg="#AAB8FF",
    font=("Segoe UI", 10)
).pack()

root.mainloop()