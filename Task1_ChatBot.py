import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai


# GEMINI AI SETUP

genai.configure(api_key="YOUR_API_KEY_HERE")

model = genai.GenerativeModel("gemini-2.5-flash")

chat = model.start_chat(history=[])


# AI RESPONSE FUNCTION

def get_ai_response(message):
    try:
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        return f"Error: {e}"


# MAIN WINDOW

root = tk.Tk()

root.title("AI Chatbot")

root.geometry("500x650")

root.configure(bg="#0f172a")


# HEADER

header = tk.Label(

    root,

    text="🤖 AI Chatbot",

    bg="#2563eb",

    fg="white",

    font=("Arial", 18, "bold"),

    pady=15
)

header.pack(fill=tk.X)


# CHAT AREA

chat_area = scrolledtext.ScrolledText(

    root,

    wrap=tk.WORD,

    font=("Arial", 12),

    bg="#1e293b",

    fg="white",

    insertbackground="white",

    bd=0
)

chat_area.pack(

    padx=15,

    pady=15,

    fill=tk.BOTH,

    expand=True
)

chat_area.insert(
    tk.END,
    "Bot: Hello 👋 I am your AI assistant. Ask me anything.\n\n"
)

chat_area.config(state=tk.DISABLED)


# INPUT FRAME

input_frame = tk.Frame(root, bg="#0f172a")

input_frame.pack(fill=tk.X, padx=10, pady=10)


# USER INPUT

user_input = tk.Entry(

    input_frame,

    font=("Arial", 12),

    bg="#334155",

    fg="white",

    insertbackground="white",

    relief=tk.FLAT
)

user_input.pack(

    side=tk.LEFT,

    fill=tk.X,

    expand=True,

    ipady=10,

    padx=(0, 10)
)


# SEND MESSAGE

def send_message():

    message = user_input.get().strip()

    if not message:
        return

    chat_area.config(state=tk.NORMAL)


    # User Message

    chat_area.insert(
        tk.END,
        f"You: {message}\n\n"
    )


    # AI Reply

    reply = get_ai_response(message)

    chat_area.insert(
        tk.END,
        f"Bot: {reply}\n\n"
    )

    chat_area.config(state=tk.DISABLED)

    chat_area.yview(tk.END)

    user_input.delete(0, tk.END)


# SEND BUTTON

send_button = tk.Button(

    input_frame,

    text="Send",

    command=send_message,

    bg="#2563eb",

    fg="white",

    font=("Arial", 11, "bold"),

    relief=tk.FLAT,

    padx=20,

    pady=10,

    cursor="hand2"
)

send_button.pack(side=tk.RIGHT)


# ENTER KEY SUPPORT

root.bind(

    "<Return>",

    lambda event: send_message()
)


# RUN APP

root.mainloop()