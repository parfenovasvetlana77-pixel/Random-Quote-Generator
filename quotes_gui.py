import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import json
import os
from datetime import datetime

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Настройка цветовой темы
        self.root.configure(bg='#f0f0f0')
        
        # Загрузка предопределенных цитат
        self.predefined_quotes = self.load_predefined_quotes()
        
        # Загрузка истории из JSON
        self.history_file = "quotes_history.json"
        self.history = self.load_history()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление отображения
        self.update_history_display()
        self.update_filter_options()
    
    def load_predefined_quotes(self):
        """Загрузка предопределенных цитат"""
        return [
            {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", 
             "author": "Джон Леннон", 
             "theme": "жизнь"},
            {"text": "Будь изменением, которое ты хочешь видеть в мире.", 
             "author": "Махатма Ганди", 
             "theme": "мотивация"},
            {"text": "Сложнее всего начать действовать, все остальное зависит от упорства.", 
             "author": "Амелия Эрхарт", 
             "theme": "мотивация"},
            {"text": "Ваше время ограничено, не тратьте его, живя чужой жизнью.", 
             "author": "Стив Джобс", 
             "theme": "успех"},
            {"text": "Воображение важнее знания.", 
             "author": "Альберт Эйнштейн", 
             "theme": "творчество"},
            {"text": "Кто не двигается, тот не замечает своих цепей.", 
             "author": "Роза Люксембург", 
             "theme": "свобода"},
            {"text": "Лучший способ предсказать будущее — изобрести его.", 
             "author": "Алан Кей", 
             "theme": "будущее"},
            {"text": "Счастье — это когда то, что ты думаешь, говоришь и делаешь, находится в гармонии.", 
             "author": "Махатма Ганди", 
             "theme": "счастье"},
            {"text": "Единственный способ делать великую работу — любить то, что ты делаешь.", 
             "author": "Стив Джобс", 
             "theme": "работа"},
            {"text": "Не судите о моем успехе по тому, как высоко я поднялся, а по тому, как высоко я отскочил, когда упал.", 
             "author": "Джордж Вашингтон", 
             "theme": "успех"}
        ]
    
    def create_widgets(self):
        # Главный контейнер
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Заголовок
        title_label = tk.Label(main_container, text="✨ Генератор случайных цитат ✨", 
                               font=("Arial", 18, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # --- Панель генерации цитаты ---
        generate_frame = tk.LabelFrame(main_container, text="🎲 Генерация цитаты", 
                                       font=("Arial", 12, "bold"), bg='#f0f0f0', fg='#34495e')
        generate_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.quote_text_label = tk.Label(generate_frame, text="Нажмите кнопку, чтобы сгенерировать цитату", 
                                         wraplength=700, font=("Arial", 11, "italic"), 
                                         bg='#f0f0f0', fg='#7f8c8d', height=4)
        self.quote_text_label.pack(pady=(15, 5), padx=15)
        
        self.quote_author_label = tk.Label(generate_frame, text="", font=("Arial", 10), 
                                           bg='#f0f0f0', fg='#95a5a6')
        self.quote_author_label.pack(pady=(0, 10))
        
        generate_button = tk.Button(generate_frame, text="🎲 Сгенерировать цитату", 
                                   command=self.generate_quote, bg='#3498db', fg='white',
                                   font=("Arial", 11, "bold"), padx=20, pady=10,
                                   cursor="hand2", relief=tk.FLAT)
        generate_button.pack(pady=(0, 15))
        
        # --- Панель добавления новой цитаты ---
        add_frame = tk.LabelFrame(main_container, text="➕ Добавить новую цитату", 
                                  font=("Arial", 12, "bold"), bg='#f0f0f0', fg='#34495e')
        add_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Текст цитаты
        tk.Label(add_frame, text="Текст:", font=("Arial", 10), bg='#f0f0f0').pack(anchor=tk.W, padx=10, pady=(10, 0))
        self.quote_entry = scrolledtext.ScrolledText(add_frame, height=3, width=80, font=("Arial", 10))
        self.quote_entry.pack(padx=10, pady=(0, 10), fill=tk.X)
        
        # Автор
        author_frame = tk.Frame(add_frame, bg='#f0f0f0')
        author_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        tk.Label(author_frame, text="Автор:", font=("Arial", 10), bg='#f0f0f0', width=10, anchor=tk.W).pack(side=tk.LEFT)
        self.author_entry = tk.Entry(author_frame, font=("Arial", 10), width=50)
        self.author_entry.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        # Тема
        theme_frame = tk.Frame(add_frame, bg='#f0f0f0')
        theme_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        tk.Label(theme_frame, text="Тема:", font=("Arial", 10), bg='#f0f0f0', width=10, anchor=tk.W).pack(side=tk.LEFT)
        self.theme_entry = tk.Entry(theme_frame, font=("Arial", 10), width=50)
        self.theme_entry.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        add_button = tk.Button(add_frame, text="💾 Добавить цитату", 
                              command=self.add_quote, bg='#27ae60', fg='white',
                              font=("Arial", 10, "bold"), padx=15, pady=5)
        add_button.pack(pady=(0, 10))
        
        # --- Панель фильтрации ---
        filter_frame = tk.LabelFrame(main_container, text="🔍 Фильтрация истории", 
                                     font=("Arial", 12, "bold"), bg='#f0f0f0', fg='#34495e')
        filter_frame.pack(fill=tk.X, pady=(0, 15))
        
        filter_content = tk.Frame(filter_frame, bg='#f0f0f0')
        filter_content.pack(padx=10, pady=10, fill=tk.X)
        
        # Фильтр по автору
        tk.Label(filter_content, text="Автор:", font=("Arial", 10), bg='#f0f0f0').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.author_filter = ttk.Combobox(filter_content, state="readonly", width=30)
        self.author_filter.grid(row=0, column=1, padx=5, pady=5)
        self.author_filter.bind("<<ComboboxSelected>>", lambda e: self.update_history_display())
        
        # Фильтр по теме
        tk.Label(filter_content, text="Тема:", font=("Arial", 10), bg='#f0f0f0').grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.theme_filter = ttk.Combobox(filter_content, state="readonly", width=30)
        self.theme_filter.grid(row=0, column=3, padx=5, pady=5)
        self.theme_filter.bind("<<ComboboxSelected>>", lambda e: self.update_history_display())
        
        clear_filter_button = tk.Button(filter_content, text="❌ Сбросить фильтры", 
                                       command=self.clear_filters, bg='#e74c3c', fg='white',
                                       font=("Arial", 9), padx=10, pady=3)
        clear_filter_button.grid(row=0, column=4, padx=10)
        
        # --- Панель истории ---
        history_frame = tk.LabelFrame(main_container, text="📜 История цитат", 
                                      font=("Arial", 12, "bold"), bg='#f0f0f0', fg='#34495e')
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Список с прокруткой
        list_frame = tk.Frame(history_frame, bg='#f0f0f0')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, 
                                         font=("Arial", 9), height=12, selectmode=tk.SINGLE)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Статистика
        self.stats_label = tk.Label(history_frame, text="Всего цитат: 0", 
                                   font=("Arial", 9, "italic"), bg='#f0f0f0', fg='#7f8c8d')
        self.stats_label.pack(pady=(0, 5))
    
    def generate_quote(self):
        """Генерация случайной цитаты"""
        if self.predefined_quotes:
            quote = random.choice(self.predefined_quotes).copy()
            self.quote_text_label.config(text=f"«{quote['text']}»", fg='#2c3e50', font=("Arial", 11, "bold"))
            self.quote_author_label.config(text=f"— {quote['author']} (тема: {quote['theme']})", fg='#34495e')
            
            # Добавляем в историю с меткой времени
            quote['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history.append(quote)
            self.save_history()
            self.update_history_display()
            self.update_filter_options()
            
            messagebox.showinfo("Успех", "Цитата добавлена в историю!")
        else:
            messagebox.showwarning("Нет цитат", "Нет доступных предопределенных цитат")
    
    def add_quote(self):
        """Добавление новой цитаты пользователем"""
        text = self.quote_entry.get("1.0", tk.END).strip()
        author = self.author_entry.get().strip()
        theme = self.theme_entry.get().strip()
        
        # Проверка на пустые строки
        if not text:
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
            return
        if not author:
            messagebox.showerror("Ошибка", "Автор не может быть пустым!")
            return
        if not theme:
            messagebox.showerror("Ошибка", "Тема не может быть пустой!")
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
        self.quote_entry.delete("1.0", tk.END)
        self.author_entry.delete(0, tk.END)
        self.theme_entry.delete(0, tk.END)
        
        messagebox.showinfo("Успех", "Цитата успешно добавлена в историю!")
    
    def update_filter_options(self):
        """Обновление опций в выпадающих списках"""
        authors = sorted(set(quote["author"] for quote in self.history))
        themes = sorted(set(quote["theme"] for quote in self.history))
        
        self.author_filter['values'] = [''] + authors
        self.theme_filter['values'] = [''] + themes
    
    def clear_filters(self):
        """Сброс фильтров"""
        self.author_filter.set('')
        self.theme_filter.set('')
        self.update_history_display()
    
    def update_history_display(self):
        """Обновление отображения истории"""
        self.history_listbox.delete(0, tk.END)
        
        # Применяем фильтры
        filtered_history = self.history
        author_filter = self.author_filter.get()
        theme_filter = self.theme_filter.get()
        
        if author_filter:
            filtered_history = [q for q in filtered_history if q["author"] == author_filter]
        if theme_filter:
            filtered_history = [q for q in filtered_history if q["theme"] == theme_filter]
        
        # Отображаем отфильтрованные цитаты
        for quote in reversed(filtered_history):
            display_text = f"[{quote['timestamp']}] {quote['author']}: {quote['text'][:100]}... (Тема: {quote['theme']})"
            self.history_listbox.insert(tk.END, display_text)
        
        # Обновляем статистику
        self.stats_label.config(text=f"Всего цитат: {len(self.history)} | Отфильтровано: {len(filtered_history)}")
    
    def load_history(self):
        """Загрузка истории из JSON файла"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Ошибка при загрузке истории: {e}")
                return []
        return []
    
    def save_history(self):
        """Сохранение истории в JSON файл"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as file:
                json.dump(self.history, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Ошибка при сохранении истории: {e}")
            messagebox.showerror("Ошибка", "Не удалось сохранить историю!")

def main():
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
