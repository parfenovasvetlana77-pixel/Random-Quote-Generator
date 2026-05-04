import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

# Предопределённые цитаты
PREDEFINED_QUOTES = [
    {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "theme": "жизнь"},
    {"text": "Будь изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "theme": "мотивация"},
    {"text": "Сложнее всего начать действовать, все остальное зависит от упорства.", "author": "Амелия Эрхарт", "theme": "мотивация"},
    {"text": "Ваше время ограничено, не тратьте его, живя чужой жизнью.", "author": "Стив Джобс", "theme": "успех"},
    {"text": "Воображение важнее знания.", "author": "Альберт Эйнштейн", "theme": "творчество"},
    {"text": "Кто не двигается, тот не замечает своих цепей.", "author": "Роза Люксембург", "theme": "свобода"},
    {"text": "Лучший способ предсказать будущее — изобрести его.", "author": "Алан Кей", "theme": "будущее"},
    {"text": "Счастье — это когда то, что ты думаешь, говоришь и делаешь, находится в гармонии.", "author": "Махатма Ганди", "theme": "счастье"},
    {"text": "Код — это поэзия.", "author": "Редькин Никита", "theme": "программирование"},
]

HISTORY_FILE = "quotes_history.json"

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator - Редькин Никита")
        self.root.geometry("700x650")
        self.root.resizable(True, True)

        # Загружаем историю
        self.history = self.load_history()

        # Текущая цитата
        self.current_quote = None

        # Создаём интерфейс
        self.create_widgets()

        # Обновляем список истории и фильтры
        self.update_history_display()
        self.update_filter_options()

    def create_widgets(self):
        # --- Верхняя панель: отображение цитаты ---
        self.quote_frame = tk.LabelFrame(self.root, text="Случайная цитата", padx=10, pady=10)
        self.quote_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.quote_label = tk.Label(self.quote_frame, text="Нажмите 'Сгенерировать'", wraplength=650, font=("Arial", 12), justify="center")
        self.quote_label.pack(pady=10)

        self.author_label = tk.Label(self.quote_frame, text="", font=("Arial", 10, "italic"), fg="gray")
        self.author_label.pack()

        self.generate_btn = tk.Button(self.quote_frame, text="🎲 Сгенерировать цитату", command=self.generate_quote, bg="lightblue", font=("Arial", 10))
        self.generate_btn.pack(pady=10)

        # --- Панель добавления новой цитаты ---
        self.add_frame = tk.LabelFrame(self.root, text="Добавить новую цитату", padx=10, pady=10)
        self.add_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(self.add_frame, text="Текст:").grid(row=0, column=0, sticky="w")
        self.text_entry = tk.Text(self.add_frame, height=3, width=50)
        self.text_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.add_frame, text="Автор:").grid(row=1, column=0, sticky="w")
        self.author_entry = tk.Entry(self.add_frame, width=40)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.add_frame, text="Тема:").grid(row=2, column=0, sticky="w")
        self.theme_entry = tk.Entry(self.add_frame, width=40)
        self.theme_entry.grid(row=2, column=1, padx=5, pady=2)

        self.add_btn = tk.Button(self.add_frame, text="➕ Добавить в историю", command=self.add_quote, bg="lightgreen")
        self.add_btn.grid(row=3, column=1, pady=5, sticky="e")

        # --- Фильтрация ---
        self.filter_frame = tk.LabelFrame(self.root, text="Фильтрация истории", padx=10, pady=10)
        self.filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(self.filter_frame, text="Фильтр по автору:").grid(row=0, column=0, sticky="w")
        self.author_filter_combo = ttk.Combobox(self.filter_frame, state="readonly", width=30)
        self.author_filter_combo.grid(row=0, column=1, padx=5)
        self.author_filter_combo.bind("<<ComboboxSelected>>", lambda e: self.update_history_display())

        tk.Label(self.filter_frame, text="Фильтр по теме:").grid(row=1, column=0, sticky="w")
        self.theme_filter_combo = ttk.Combobox(self.filter_frame, state="readonly", width=30)
        self.theme_filter_combo.grid(row=1, column=1, padx=5)
        self.theme_filter_combo.bind("<<ComboboxSelected>>", lambda e: self.update_history_display())

        self.clear_filter_btn = tk.Button(self.filter_frame, text="❌ Сбросить фильтры", command=self.clear_filters)
        self.clear_filter_btn.grid(row=2, column=1, pady=5, sticky="e")

        # --- История ---
        self.history_frame = tk.LabelFrame(self.root, text="История цитат", padx=10, pady=10)
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.history_listbox = tk.Listbox(self.history_frame, height=12)
        self.history_listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.history_frame, orient="vertical", command=self.history_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=self.scrollbar.set)

    def generate_quote(self):
        """Генерирует случайную цитату (из предопределённых)"""
        if PREDEFINED_QUOTES:
            self.current_quote = random.choice(PREDEFINED_QUOTES).copy()
            self.quote_label.config(text=f"«{self.current_quote['text']}»")
            self.author_label.config(text=f"— {self.current_quote['author']} (тема: {self.current_quote['theme']})")
            
            # Добавляем в историю с временем
            quote_copy = self.current_quote.copy()
            quote_copy["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history.append(quote_copy)
            self.save_history()
            self.update_history_display()
            self.update_filter_options()
        else:
            messagebox.showwarning("Нет цитат", "Нет доступных предопределённых цитат")

    def add_quote(self):
        """Добавляет новую цитату от пользователя"""
        text = self.text_entry.get("1.0", tk.END).strip()
        author = self.author_entry.get().strip()
        theme = self.theme_entry.get().strip()

        if not text:
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым")
            return
        if not author:
            messagebox.showerror("Ошибка", "Автор не может быть пустым")
            return
        if not theme:
            messagebox.showerror("Ошибка", "Тема не может быть пустой")
            return

        new_quote = {
            "text": text,
            "author": author,
            "theme": theme,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(new_quote)
        self.save_history()
        self.update_history_display()
        self.update_filter_options()

        # Очищаем поля
        self.text_entry.delete("1.0", tk.END)
        self.author_entry.delete(0, tk.END)
        self.theme_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", "Цитата добавлена в историю")

    def update_filter_options(self):
        """Обновляет списки для фильтрации"""
        authors = sorted(set(q["author"] for q in self.history))
        themes = sorted(set(q["theme"] for q in self.history))
        
        self.author_filter_combo["values"] = [""] + authors
        self.theme_filter_combo["values"] = [""] + themes

    def clear_filters(self):
        """Сбрасывает фильтры"""
        self.author_filter_combo.set("")
        self.theme_filter_combo.set("")
        self.update_history_display()

    def update_history_display(self):
        """Отображает историю с учётом фильтров"""
        self.history_listbox.delete(0, tk.END)
        
        selected_author = self.author_filter_combo.get()
        selected_theme = self.theme_filter_combo.get()

        filtered = self.history
        if selected_author:
            filtered = [q for q in filtered if q["author"] == selected_author]
        if selected_theme:
            filtered = [q for q in filtered if q["theme"] == selected_theme]

        for quote in reversed(filtered):  # свежие сверху
            display = f"{quote['timestamp']} — {quote['author']}: {quote['text'][:80]}... (тема: {quote['theme']})"
            self.history_listbox.insert(tk.END, display)

    def load_history(self):
        """Загружает историю из JSON"""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        """Сохраняет историю в JSON"""
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()