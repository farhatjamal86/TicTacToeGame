import tkinter as tk
from tkinter import messagebox
import pygame
import os
from gtts import gTTS
import tempfile

# Initialize pygame mixer for sounds
pygame.mixer.init()

# Load sound effects (ensure these .wav files are in the same folder)
click_sound = pygame.mixer.Sound(r"c:\Users\jamal\Downloads\click.wav")
win_sound = pygame.mixer.Sound(r"c:\Users\jamal\Downloads\win.wav")
draw_sound = pygame.mixer.Sound(r"c:\Users\jamal\Downloads\draw.wav")

# Initialize main window
root = tk.Tk()
root.title("Tic Tac Toe - Farhat vs AI (with Sound + Voice)")
root.geometry("400x500")
root.resizable(False, False)

board = [" " for _ in range(9)]
buttons = []

# Flag for voice feedback on/off
voice_on = tk.BooleanVar(value=True)

def speak(text):
    if voice_on.get():
        try:
            tts = gTTS(text=text, lang='hi')
            with tempfile.NamedTemporaryFile(delete=True) as fp:
                tmpfile = fp.name + ".mp3"
                tts.save(tmpfile)
                pygame.mixer.music.load(tmpfile)
                pygame.mixer.music.play()
        except Exception as e:
            print("Voice Error:", e)

def check_winner(player):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    return any(all(board[i] == player for i in combo) for combo in wins)

def is_full():
    return all(cell != " " for cell in board)

def minimax(is_maximizing):
    if check_winner("O"):
        return 1
    if check_winner("X"):
        return -1
    if is_full():
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == " ": 
                board[i] = "O"
                score = minimax(False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -float("inf")
    best_move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
    if best_move is not None:
        board[best_move] = "O"
        buttons[best_move].config(text="O", state="disabled", disabledforeground="red")
        pygame.mixer.Sound.play(click_sound)
        if check_winner("O"):
            pygame.mixer.Sound.play(win_sound)
            speak("बधाई हो! AI जीत गया!")
            messagebox.showinfo("Game Over", " AI Jeet gaya! Try again!")
            reset_game()
        elif is_full():
            pygame.mixer.Sound.play(draw_sound)
            speak("मैच ड्रॉ हो गया!")
            messagebox.showinfo("Game Over", "🤝 Match Draw!")
            reset_game()

def on_click(i): 
    if board[i] == " ":
        board[i] = "X"
        buttons[i].config(text="X", state="disabled", disabledforeground="green")
        pygame.mixer.Sound.play(click_sound)
        if check_winner("X"):
            pygame.mixer.Sound.play(win_sound)
            speak("शाबाश! तुम जीत गई, Farhat!")
            messagebox.showinfo("Game Over", "🎉 Tum jeet gayi, Farhat! Super Move!")
            reset_game()
        elif is_full():
            pygame.mixer.Sound.play(draw_sound)
            speak("मैच ड्रॉ हो गया!")
            messagebox.showinfo("Game Over", "🤝 Match Draw!")
            reset_game()
        else:
            ai_move()

def reset_game():
    global board
    board = [" " for _ in range(9)]
    for btn in buttons:
        btn.config(text=" ", state="normal")

def toggle_voice():
    if voice_on.get():
        speak("वॉइस ऑन कर दिया गया है। चलो खेलते हैं!")
    else:
        pygame.mixer.music.stop()

# GUI layout for buttons
for i in range(9):
    btn = tk.Button(root, text=" ", font=("Arial", 32), width=4, height=2, command=lambda i=i: on_click(i))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

# Reset button
reset_btn = tk.Button(root, text="🔄 Restart Game", font=("Arial", 14), command=reset_game)
reset_btn.grid(row=3, column=0, columnspan=3, pady=10)

# Voice toggle
voice_toggle = tk.Checkbutton(root, text="🗣️ Voice ON/OFF", font=("Arial", 12), variable=voice_on, command=toggle_voice)
voice_toggle.grid(row=4, column=0, columnspan=3)

root.mainloop()
