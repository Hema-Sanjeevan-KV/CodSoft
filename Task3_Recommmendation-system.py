import tkinter as tk
from tkinter import scrolledtext
import random


# MAIN WINDOW

root = tk.Tk()
root.title("🎵 AI Music Recommendation System")
root.geometry("800x850")
root.configure(bg="#0B0B0B")  


# SONG DATABASE

songs = {
    "blinding lights": {"genre":"pop","mood":"happy","artist":"The Weeknd","rating":4.9},
    "shape of you": {"genre":"pop","mood":"happy","artist":"Ed Sheeran","rating":4.8},
    "stay": {"genre":"pop","mood":"happy","artist":"Justin Bieber","rating":4.7},

    "believer": {"genre":"rock","mood":"energetic","artist":"Imagine Dragons","rating":4.8},
    "thunder": {"genre":"rock","mood":"energetic","artist":"Imagine Dragons","rating":4.7},
    "radioactive": {"genre":"rock","mood":"energetic","artist":"Imagine Dragons","rating":4.8},

    "perfect": {"genre":"romantic","mood":"relaxed","artist":"Ed Sheeran","rating":4.9},
    "night changes": {"genre":"romantic","mood":"relaxed","artist":"One Direction","rating":4.8},
    "senorita": {"genre":"romantic","mood":"happy","artist":"Shawn Mendes","rating":4.7},

    "faded": {"genre":"electronic","mood":"sad","artist":"Alan Walker","rating":4.8},
    "alone": {"genre":"electronic","mood":"energetic","artist":"Alan Walker","rating":4.7},
    "animals": {"genre":"electronic","mood":"energetic","artist":"Martin Garrix","rating":4.8},

    "heat waves": {"genre":"indie","mood":"relaxed","artist":"Glass Animals","rating":4.8},
    "505": {"genre":"indie","mood":"sad","artist":"Arctic Monkeys","rating":4.7},

    "unstoppable": {"genre":"motivational","mood":"energetic","artist":"Sia","rating":4.9},
    "hall of fame": {"genre":"motivational","mood":"energetic","artist":"The Script","rating":4.9},
}

favorites = []
history = []


# FUNCTIONS

def recommend_genre(genre):
    result = f"🎵 {genre.upper()} SONGS\n\n"
    found = False

    for song, info in songs.items():
        if info["genre"] == genre:
            found = True
            result += f"• {song.title()} - {info['artist']}\n"

    return result if found else "No songs found for this genre."


def recommend_mood(mood):
    result = f"😊 {mood.upper()} MOOD SONGS\n\n"
    found = False

    for song, info in songs.items():
        if info["mood"] == mood:
            found = True
            result += f"• {song.title()} - {info['artist']}\n"

    return result if found else "No songs found for this mood."


def search_song(name):
    for song, info in songs.items():
        if name.lower() in song:
            return (
                f"🎵 {song.title()}\n\n"
                f"🎤 Artist: {info['artist']}\n"
                f"🎼 Genre: {info['genre'].title()}\n"
                f"😊 Mood: {info['mood'].title()}\n"
                f"⭐ Rating: {info['rating']}"
            )
    return "❌ Song not found."


def top_songs():
    sorted_songs = sorted(songs.items(), key=lambda x: x[1]["rating"], reverse=True)

    result = "🏆 TOP SONGS\n\n"

    for i, (song, info) in enumerate(sorted_songs[:5], start=1):
        result += f"{i}. {song.title()}\n   🎤 {info['artist']} | ⭐ {info['rating']}\n\n"

    return result


def surprise_song():
    song = random.choice(list(songs.keys()))
    return search_song(song)


def add_favorite(song):
    for s in songs:
        if song.lower() == s:
            if s not in favorites:
                favorites.append(s)
                return f"❤️ Added {s.title()} to Favorites."
            return "⚠️ Already in Favorites."
    return "❌ Song not found."


def show_favorites():
    if not favorites:
        return "❤️ No favorites yet."

    result = "❤️ FAVORITES\n\n"
    for s in favorites:
        result += f"• {s.title()}\n"
    return result


def show_history():
    if not history:
        return "🕒 No history yet."

    result = "🕒 HISTORY\n\n"
    for i, h in enumerate(history, start=1):
        result += f"{i}. {h}\n"
    return result


# BOT LOGIC

def get_reply(msg):
    m = msg.lower().strip()

    genres = ["pop","rock","romantic","electronic","indie","motivational"]
    moods = ["happy","sad","energetic","relaxed"]

    if m in genres:
        history.append(f"{m} genre")
        return recommend_genre(m)

    if m in moods:
        history.append(f"{m} mood")
        return recommend_mood(m)

    if "top" in m:
        history.append("top songs")
        return top_songs()

    if "surprise" in m:
        history.append("surprise song")
        return surprise_song()

    if m == "favorites":
        return show_favorites()

    if m == "history":
        return show_history()

    if m.startswith("add "):
        return add_favorite(m[4:])

    if "hello" in m or "hi" in m:
        return (
            "👋 Welcome to AI Music Recommender!\n\n"
            "Try:\n"
            "• pop\n• rock\n• happy\n• energetic\n"
            "• top songs\n• surprise\n• add believer\n"
            "• favorites\n• history"
        )

    return search_song(msg)


# SEND MESSAGE

def send_message():
    msg = entry.get().strip()
    if not msg:
        return

    chat.config(state=tk.NORMAL)

    chat.insert(tk.END, f"\n👤 YOU:\n{msg}\n\n", "user")

    reply = get_reply(msg)

    chat.insert(tk.END, f"🤖 AI:\n{reply}\n\n", "bot")

    chat.config(state=tk.DISABLED)
    chat.yview(tk.END)
    entry.delete(0, tk.END)


# TITLE

title = tk.Label(
    root,
    text="🎵 MUSIC RECOMMENDATION SYSTEM",
    font=("Segoe UI", 20, "bold"),
    bg="#0B0B0B",
    fg="#FACC15"   # YELLOW
)

title.pack(pady=15)


# CHAT AREA

chat = scrolledtext.ScrolledText(
    root,
    font=("Segoe UI", 11),
    bg="#1A1A1A",      # DARK GRAY
    fg="#F5F5F5",
    insertbackground="#FACC15",
    relief="flat",
    bd=5
)

chat.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

chat.tag_config("user", foreground="#FACC15", font=("Segoe UI", 11, "bold"))
chat.tag_config("bot", foreground="#FFFFFF")

chat.insert(
    tk.END,
"""
💛 AI MUSIC BOT 

━━━━━━━━━━━━━━━━━━━━━━

🎵 Welcome!

🎼 GENRES:
• pop
• rock
• romantic
• motivational

😊 MOODS:
• happy
• sad
• energetic
• relaxed

⭐ FEATURES:
• top songs
• surprise me
• favorites
• history

━━━━━━━━━━━━━━━━━━━━━━
"""
)

chat.config(state=tk.DISABLED)


# INPUT SECTION

frame = tk.Frame(root, bg="#0B0B0B")
frame.pack(fill=tk.X, padx=20, pady=20)

entry = tk.Entry(
    frame,
    font=("Segoe UI", 12),
    bg="#1A1A1A",
    fg="#FACC15",
    insertbackground="#FACC15",
    relief="flat",
    bd=5
)

entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12)


btn = tk.Button(
    frame,
    text="🎵 Send",
    command=send_message,
    bg="#FACC15",
    fg="#0B0B0B",
    activebackground="#EAB308",
    activeforeground="#000000",
    font=("Segoe UI", 11, "bold"),
    relief="flat",
    padx=18,
    pady=8,
    cursor="hand2"
)

btn.pack(side=tk.RIGHT, padx=10)


# ENTER KEY SUPPORT

root.bind("<Return>", lambda e: send_message())


# RUN

root.mainloop()