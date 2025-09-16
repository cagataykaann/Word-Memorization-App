import tkinter as tk
from tkinter import messagebox
import random
from difflib import SequenceMatcher

data = {
 
    "dominate": "baskin olmak",
    "donate": "bagis",
    "contribute": "bagis",
    "dowry": "ceyiz",
    "dramatic": "cok hizli",
    "drastic": "cok hizli",
    "draw": "cizmek",
    "drug addict": "uyusturucu bagimlisi",
    "drug dealer": "uyusturucu saticisi",
    "dustbin": "cop kutusu",
    "trash can": "cop kutusu",
    "edit": "duzenleme",
    "edition": "basim",
    "educate": "egitmek",
    "effect": "etki",
    "impact": "etki",
    "elect": "secmek",
    "eliminate": "elemek",
    "vote for": "secmek",
    "elimination": "ortadan kaldirmak",
    "embarrass": "utandirma",
    "humiliate": "utandirma",
    "embrace": "hug",
    "emerge": "ortaya cikmak",
    "come out": "ortaya cikmak",
    "emphasize": "vurgulamak",
    "employ": "ise almak",
    "empty": "bos",
    "emulate": "taklit etmek",
    "enable": "olanak tanimak",
    "enclose": "cevrelemek",
    "encounter": "karsilasma",
    "encourage": "tesvik etmek",
    "endure": "dayanikli",
    "enhance": "buyulemek",
    "enhancement": "improvement",
    "enrich": "zenginlestirmek",
    "enlarge": "buyutmek",
    "enquire": "sorusturmak",
    "enslave": "kolelestirmek",
    "ensure": "teminat vermek",
    "entertain": "eglendirmek",
    "entirely": "tamamen",
    "entrance": "giris",
    "envy": "kiskanmak",
    "epic": "destan",
    "equal": "esit",
    "equate": "esitlemek",
    "equip": "donatmak",
    "parity": "esitlik",
    "erode": "yipratmak",
    "fairness": "esitlik"

}

unasked_words = list(data.items())
wrong_words = []

class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Çeviri Oyunu")
        self.root.geometry("600x500")
        self.mode = None
        self.current_word = None
        self.previous_word = None  
        self.score_correct = 0
        self.score_wrong = 0

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(pady=20)

        self.label_mode = tk.Label(self.main_frame, text="Hangi modu kullanmak istiyorsunuz?", font=("Arial", 16))
        self.label_mode.pack()

        self.btn_turk_to_eng = tk.Button(self.main_frame, text="Türkçe → İngilizce", font=("Arial", 14),
                                         command=lambda: self.set_mode("TR_TO_EN"))
        self.btn_turk_to_eng.pack(pady=10)

        self.btn_eng_to_turk = tk.Button(self.main_frame, text="İngilizce → Türkçe", font=("Arial", 14),
                                         command=lambda: self.set_mode("EN_TO_TR"))
        self.btn_eng_to_turk.pack(pady=10)

        self.quiz_frame = tk.Frame(root)

        self.label_question = tk.Label(self.quiz_frame, text="", font=("Arial", 16))
        self.label_question.pack(pady=20)

        self.entry_frame = tk.Frame(self.quiz_frame, bg="black", padx=2, pady=2)
        self.entry_frame.pack(pady=10)

        self.entry_answer = tk.Entry(self.entry_frame, font=("Arial", 14), width=30, bg="#3b3b3b", fg="white")
        self.entry_answer.pack()

        self.entry_answer.bind("<Return>", self.check_answer)

        self.btn_submit = tk.Button(self.quiz_frame, text="Gönder", font=("Arial", 14), command=self.check_answer)
        self.btn_submit.pack(pady=10)

        self.label_feedback = tk.Label(self.quiz_frame, text="", font=("Arial", 12), fg="blue")
        self.label_feedback.pack(pady=5)

        self.label_score = tk.Label(self.quiz_frame, text="Doğru: 0, Yanlış: 0", font=("Arial", 14))
        self.label_score.pack(pady=10)

        self.label_last_word = tk.Label(self.quiz_frame, text="", font=("Arial", 12), fg="green")  
        self.label_last_word.pack(pady=10)

        self.end_frame = tk.Frame(root)

    def set_mode(self, mode):
        self.mode = mode
        self.main_frame.pack_forget()
        self.start_game()

    def start_game(self):
        self.quiz_frame.pack(pady=20)
        self.ask_question()

    def ask_question(self):
        global unasked_words, wrong_words

        words_to_ask = unasked_words + wrong_words
        if not words_to_ask:
            self.finish_game()
            return

        self.previous_word = self.current_word  
        self.current_word = random.choice(words_to_ask)
        if self.mode == "TR_TO_EN":
            self.label_question.config(text=f"Türkçe: {self.current_word[1]}")
        else:
            self.label_question.config(text=f"İngilizce: {self.current_word[0]}")

        self.entry_answer.delete(0, tk.END)
        self.label_feedback.config(text="")

        
        if self.previous_word:
            self.label_last_word.config(text=f"Önceki Kelime: {self.previous_word[0]} → {self.previous_word[1]}")
        else:
            self.label_last_word.config(text="")

    def check_answer(self, event=None):
        global unasked_words, wrong_words
        user_answer = self.entry_answer.get().strip().lower()
        correct_answer = (self.current_word[0] if self.mode == "TR_TO_EN" else self.current_word[1]).lower()

        if self.is_close_enough(user_answer, correct_answer):
            self.score_correct += 1
            if self.current_word in unasked_words:
                unasked_words.remove(self.current_word)
            if self.current_word in wrong_words:
                wrong_words.remove(self.current_word)

            self.label_feedback.config(text=f"Doğru: {self.current_word[0]} → {self.current_word[1]}", fg="green")
        else:
            self.score_wrong += 1
            if self.current_word not in wrong_words:
                wrong_words.append(self.current_word)

            self.label_feedback.config(text=f"Yanlış! Doğru: {self.current_word[0]} → {self.current_word[1]}", fg="red")

        self.label_score.config(text=f"Doğru: {self.score_correct}, Yanlış: {self.score_wrong}")
        self.ask_question()

    def is_close_enough(self, user, correct):
        return self.levenshtein_distance(user, correct) <= 2

    def levenshtein_distance(self, a, b):
        return len(a) + len(b) - 2 * int(SequenceMatcher(None, a, b).ratio() * min(len(a), len(b)))

    def finish_game(self):
        self.quiz_frame.pack_forget()
        self.end_frame.pack(pady=20)

        end_message = tk.Label(self.end_frame, text="Tebrikler! Oyun bitti.", font=("Arial", 16))
        end_message.pack(pady=20)

        final_score = tk.Label(self.end_frame, text=f"Doğru: {self.score_correct}, Yanlış: {self.score_wrong}",
                               font=("Arial", 14))
        final_score.pack(pady=10)

        restart_button = tk.Button(self.end_frame, text="Tekrar Başla", font=("Arial", 14), command=self.restart_game)
        restart_button.pack(pady=20)

    def restart_game(self):
        global unasked_words, wrong_words
        unasked_words = list(data.items())
        wrong_words = []
        self.score_correct = 0
        self.score_wrong = 0

        self.end_frame.pack_forget()
        self.label_score.config(text="Doğru: 0, Yanlış: 0")
        self.start_game()


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()
