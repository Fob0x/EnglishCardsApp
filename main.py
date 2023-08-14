import tkinter as tk
import random
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json

class EnglishCardsApp: # Класс самой моей программы
    def __init__(self, root):
        # self.root = root # Сохраняем объект основного окна Tkinter в атрибуте
        # self.root.title("Изучений английских слов по карточкам") # Заголовок (название приложения)
        # self.root.resizable(False, False) # Отключение возможности собственноручного масштабирования окна
        # self.root.iconbitmap("Serg.ico") # Изменяем иконку окна (пасхал'очка) c расширением .ico
        #
        # # Создание и настройка виджета Frame (рамки) внутри основного окна
        # self.menu_frame = tk.Frame(self.root)
        # self.menu_frame.pack(pady = 20)
        #
        # # Создание кнопки "Карточки" внутри menu_frame, при нажатии на которую будет вызываться метод self.open_cards
        # self.cards_button = tk.Button(self.menu_frame, text = "Карточки", command = self.open_cards)
        # self.cards_button.grid(row = 0, column=0, padx = 10)
        #
        # # Создание кнопки "Настройки" внутри menu_frame, при нажатии на которую будет вызываться метод self.open_settings
        # self.settings_button = tk.Button(self.menu_frame, text = "Настройки", command = self.open_settings)
        # self.settings_button.grid(row = 0, column = 1, padx = 10)
        #
        # # Создание кнопки "Тест" внутри menu_frame, при нажатии на которую будет вызываться метод self.open_tests
        # self.tests_button = tk.Button(self.menu_frame, text = "Тесты", command = self.open_test)
        # self.tests_button.grid(row = 0, column = 2, padx = 10)

        self.root = root # Сохраняем объект основного окна Tkinter в атрибуте
        self.root.title("Изучений английских слов по карточкам") # Заголовок (название приложения)
        self.root.resizable(False, False) # Отключение возможности собственноручного масштабирования окна
        self.root.iconbitmap("Serg.ico") # Изменяем иконку окна (пасхал'очка) c расширением .ico
        self.root.geometry("300x400")

##################################

        self.background_image = tk.PhotoImage(file="bgm.png")  # Укажите путь к вашей картинке
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

##################
        self.menu_frame = tk.Frame(root)
        self.menu_frame.place(x=-150, y=0, relwidth=0.5, relheight=1.0)
        self.menu_expanded = False

        self.expand_button = tk.Button(root, text=">", command=self.toggle_menu)
        self.expand_button.place(x=0, y=0, width=30, height=400)

        # Создаем Label с фоновым изображением в menu_frame
        self.background_bar_image = tk.PhotoImage(file="bg.png")  # Укажите путь к вашей картинке
        self.background_label = tk.Label(self.menu_frame, image=self.background_bar_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Добавляем кнопки внутри выдвигающегося бара
        button_font = ("Helvetica", 12)  # Измените на нужный вам шрифт и размер
        self.cards_button = tk.Button(self.menu_frame, text="Карточки", font=button_font, command=self.open_cards)
        self.cards_button.pack(fill=tk.X, expand=True, pady=(10, 0))

        self.settings_button = tk.Button(self.menu_frame, text="Настройки", font=button_font, command=self.open_settings)
        self.settings_button.pack(fill=tk.X, expand=True, pady=(0, 5))

        self.tests_button = tk.Button(self.menu_frame, text="Тесты", font=button_font, command=self.open_test)
        self.tests_button.pack(fill=tk.X, expand=True, pady=(0, 10))

    def toggle_menu(self):
        if not self.menu_expanded:
            self.menu_frame.place(x=0)
        else:
            self.menu_frame.place(x=-150)
        self.menu_expanded = not self.menu_expanded


        # Инициализация списка, хранящего данные карточек
        self.card_list = []

        self.load_cards()  # Загрузка карточек при запуске

    def open_settings(self):
        # Создание нового окна для настроек (хм, а можно ли как-то открывать в этом же окне, либо поверх его..?)
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Настройки")
        self.root.resizable(False, False)
        self.root.iconbitmap("Serg.ico")  # Изменяем иконку окна (пасхал'очка) c расширением .ico

        def set_background_color(color):
            self.root.configure(bg = color) # Изменение цвета фона основного окна
            settings_window.configure(bg=color)
            settings_window.destroy() # Закрытие окна настроек

        # Создание кнопок для выбора цвета фона и привязка к ниф ф-ции color
        white_button = tk.Button(settings_window, text = "Белый", command=lambda: set_background_color("white"))
        white_button.pack()
        black_button = tk.Button(settings_window, text = "Чёрный", command=lambda: set_background_color("black"))
        black_button.pack()
        grey_button = tk.Button(settings_window, text = "Серый", command=lambda: set_background_color("grey"))
        grey_button.pack()

    """С 33-ей по 50-ую строчку создаётся окно настроек с 3-мя кнопками для выбора цвета фона основного окна
    Каждая кнопка связана с ф-цией set_background_color, изменяющей цвет основого окна и затем закрывающей окно настроек"""

    def save_cards(self):
        # Сохранение списка карточек в JSON файл
        with open("cards.json", "w") as file:
            json.dump(self.card_list, file)

    def load_cards(self):
        try:
            # Загрузка списка карточек из JSON файла, если файл существует
            with open("cards.json", "r") as file:
                self.card_list = json.load(file)
        except FileNotFoundError:
            pass # Если файл не найден - игнорим

    """В этих функциях save_cards и load_cards выполняют сохранение и загрузку списка карточек в/из JSON файл.
        save_cards открывает файл для записи ("w" - write mode) и использует функцию json.dump() для сохранения списка карточек в файл.
        load_cards пытается открыть файл для чтения ("r" - read mode), используя json.load() для загрузки данных из файла в список карточек.
        Если файл не существует (обработка исключения FileNotFoundError), функция просто проходит мимо (используя pass)."""

    def open_cards(self):
        # Создание нового окна для карточек
        cards_window = tk.Toplevel(self.root)
        cards_window.title("Карточки")
        cards_window.iconbitmap("Serg.ico")

        # Ф-ция для добавления карточки
        def add_card():
            card = \
                {
                    "English": english_entry.get(),
                    "Russian": russian_entry.get(),
                    "Image": self.image_path
                }
            self.card_list.append(card) # Добавление карточки в список
            english_entry.delete(0, tk.END) # Очистка ввода английского слова
            russian_entry.delete(0, tk.END) # Очистка ввода перевода
            self.image_path = "" # Сброс пути к изображению
            self.save_cards() # Сохраняем карточки после обновления
            update_word_list() # обновляем список карточек

        def delete_card():
            selected_index = word_list.curselection()
            if selected_index:
                index = selected_index[0]
                del self.card_list[index]
                self.save_cards()  # Сохраняем карточки после удаления
                update_word_list()  # Обновляем список карточек

        def update_word_list():
            word_list.delete(0, tk.END) #
            for i, card in enumerate(self.card_list):
                word_list.insert(tk.END, card['English']) # Добавляем английские слова в список

        # Ф-ция для открытия окна с подробной
        def choose_image():
            self.image_path = filedialog.askopenfilename() # Получаем путь к изображению
            if self.image_path:
                img = Image.open(self.image_path)
                img.thumbnail((150, 100)) # задаём размер изображения
                img = ImageTk.PhotoImage(img)
                img_label.config(image = img) # обновляем изображение
                img_label.image = img

        # Ф-ция для открытия окна с подробной инф-цией о карточке
        def open_card_window(index):
            card = self.card_list[index]
            card_window = tk.Toplevel(self.root)
            card_window.title(card['English'])

            english_label = tk.Label(card_window, text = "Английское слово:")
            english_label.pack()
            eng_value = tk.Label(card_window, text = card['English'])
            eng_value.pack()

            rus_label = tk.Label(card_window, text="Перевод на русский:")
            rus_label.pack()
            rus_value = tk.Label(card_window, text=card['Russian'])
            rus_value.pack()

            if card['Image']:
                img = Image.open(card['Image'])
                img.thumbnail((150, 100))  # Задаем размер изображения
                img = ImageTk.PhotoImage(img)
                img_label = tk.Label(card_window, image=img)
                img_label.image = img
                img_label.pack()

        # Создание интерфейса для добавления, отображения и удаления карточек
        english_label = tk.Label(cards_window, text = "Английское слово:")
        english_label.pack()
        english_entry = tk.Entry(cards_window)
        english_entry.pack()

        russian_label = tk.Label(cards_window, text = "Перевод на русский:")
        russian_label.pack()
        russian_entry = tk.Entry(cards_window)
        russian_entry.pack()

        choose_image_button = tk.Button(cards_window, text = "Выбрать картинку", command = choose_image)
        choose_image_button.pack()

        img_label = tk.Label(cards_window) # Метка для отображения изображения
        img_label.pack()

        add_button = tk.Button(cards_window, text = "Добавить карточку", command=add_card)
        add_button.pack()

        delete_button = tk.Button(cards_window, text = "Удалить карточку", command=delete_card)
        delete_button.pack()

        word_list = tk.Listbox(cards_window)
        word_list.pack()
        word_list.bind("<Double-Button-1>", lambda event: open_card_window(word_list.curselection()[0]))

        update_word_list() # Обновляем список карточек

    def open_test(self):
        # Создание окна выбора типа теста
        test_mode_window = tk.Toplevel(self.root)
        test_mode_window.title("Выберите тип теста")

        # Создание метки для выбора теста
        test_mode_label = tk.Label(test_mode_window, text = "Выберите тип теста:")
        test_mode_label.pack()

        # Создание кнопки для выбора теста на правильное написание
        spelling_test_button = tk.Button(test_mode_window, text="Правильное написание", command=lambda: self.start_test(test_mode_window, 1))
        spelling_test_button.pack(pady=(20, 0))

        # Создание кнопки для выбора теста вариантов
        multiple_choice_test_button = tk.Button(test_mode_window, text = "Выбор из вариантов", command = lambda: self.start_test(test_mode_window, 2))
        multiple_choice_test_button.pack( pady=(20, 0))

        # Создание кнопки для выбора теста карточек на время
        time_cards_set_test_button = tk.Button(test_mode_window, text = "Карточки на время", command = lambda: self.start_test(test_mode_window, 3))
        time_cards_set_test_button.pack( pady=(20, 0))

        guess_the_words_on_time_test_button = tk.Button(test_mode_window, text = "Слова на время", command=lambda: self.start_test(test_mode_window, 4))
        guess_the_words_on_time_test_button.pack(pady=(20, 0))

        """Этот код создает интерфейс для выбора типа теста. 
        Он включает в себя создание окна с меткой и тремя кнопками для выбора типа теста "Правильное написание", "Выбор из вариантов" и "Карточки на время". 
        При нажатии на кнопку запускается метод self.start_test с соответствующим параметром типа теста."""

    def start_test(self, test_mode_window, test_type):
        test_mode_window.destroy() # Закрываем окно выбора типа теста

        # Создание окна для тестирования
        test_window = tk.Toplevel(self.root)
        test_window.title("Тестирование")
        test_window.iconbitmap("Serg.ico")

        # Определение типа теста и вызов соотв-щей ф-ции
        if test_type == 1:
            self.start_spelling_test(test_window)
        elif test_type == 2:
            self.start_multiple_choice_test(test_window)
        elif test_type == 3:
            self.start_time_cards_set_test(test_window)
        else:
            self.start_guess_the_words_on_time_test(test_window)
        # else:
        #     messagebox.showerror("Ошибка", "Неверный тип теста")

    """Я вот что думаю. Надо бы сделать так, чтобы сохранялись неправильные ответы и их прогоняли по новой, пока пользователь не выполнит тест безошибочно.
    Вопрос только в том, как это сделать в python? В Плюсах я бы въебал while с флагом, а для карточек создал либо отдельный массив bool, с привязкой по индексу к массиву карт, либо пару..."""

    def start_spelling_test(self, test_window):
        current_card_index = 0

        def display_next_card():
            nonlocal current_card_index
            if current_card_index < len(self.card_list):
                current_card = self.card_list[current_card_index]
                question_label.config(text = f"Как переводится '{current_card['English']}'?")
                answer_entry.delete(0, tk.END)
                check_button.config(state = tk.NORMAL)
                result_label.config(text = "", fg="black")
                current_card_index += 1
            else:
                question_label.config(text = "Тест завершён", font = ("Helvetica", 14, "bold"), )
                answer_entry.destroy()
                check_button.destroy()
                result_label.destroy()
                next_button.destroy()

        def check_answer():
            user_answer = answer_entry.get().strip().lower()
            correct_answer = self.card_list[current_card_index - 1]['Russian'].lower()
            if user_answer == correct_answer:
                result_label.config(text = "Правильно!", fg = "green")
            else:
                result_label.config(text = f"Неправильно! Правильный ответ: {correct_answer}", fg = "red")

        # Создание метки для выбора перевода текста с англйиского языка
        question_label = tk.Label(test_window, text = "", font = ("Helvetica", 16))
        question_label.pack()

        # Создание окна для ввода ответа (перевода слова)
        answer_entry = tk.Entry(test_window, font = ("Helvetica", 14))
        answer_entry.pack()

        # Кнопка проверки ответа
        check_button = tk.Button(test_window, text = "Проверить", command = check_answer, font = ("Helvetica", 14), state = tk.DISABLED)
        check_button.pack()

        # Создание метки с выводом правильности ответа
        result_label = tk.Label(test_window, text = "", font=("Helvetica", 14))
        result_label.pack()

        # Кнопка для перехода на следующий вопрос
        next_button = tk.Button(test_window, text = "Следующий вопрос", comman = display_next_card, font = ("Helvetica", 14))
        next_button.pack()

        display_next_card()

    """Этот код начинает тестирование типа "Правильное написание". 
        Он создает окно тестирования, содержащее метку для вопроса, поле ввода для ответа, кнопку "Проверить", 
        метку для отображения результата проверки и кнопку "Следующий вопрос". 
        Функции display_next_card и check_answer управляют отображением нового вопроса и проверкой ответа.
        Эти функции являются основой для создания тестового режима в вашем приложении. 
        В зависимости от выбранного типа теста, интерфейс и логика тестирования будут различаться."""

    def start_guess_the_words_on_time_test(self, test_window):
        time_left = 30
        current_card_index = 0
        correct_answer = 0

        question_label = tk.Label(self.root, text="", font=("Helvetica", 16))
        question_label.pack()

        timer_label = tk.Label(self.root, text=str(time_left), font=("Helvetica", 20))
        timer_label.pack()

        def display_question():
            if current_card_index < len(self.card_list):
                current_card = self.card_list[current_card_index]
                question_label.config(text = f"Как пеереводится: '{current_card['English']}'?")
                #answer_button(current_card['Russian'])

        def update_timer():
            nonlocal time_left
            timer_label.config(text = str(time_left))
            if time_left > 0:
                time_left -= 1
                root.after(1000, update_timer)






    # def start_time_cards_set_test(self, test_window):
    #
    #     english_button_one = tk.Button(test_window, text = "")
    #     english_button_one.grid(row = 0, column = 0, padx=10, pady=10)
    #
    #     english_button_two = tk.Button(test_window, text="")
    #     english_button_two.grid(row = 1, column=0, padx=10, pady=10)
    #
    #     english_button_three = tk.Button(test_window, text="")
    #     english_button_three.grid(row = 2, column=0, padx=10, pady=10)
    #
    #     english_button_four = tk.Button(test_window, text="")
    #     english_button_four.grid(row = 3, column=0, padx=10, pady=10)
    #
    #     ##################################################
    #
    #     russian_button_one = tk.Button(test_window, text="")
    #     russian_button_one.grid(row = 0, column=1)
    #
    #     russian_button_two = tk.Button(test_window, text="")
    #     russian_button_two.grid(row = 1, column=1)
    #
    #     russian_button_three = tk.Button(test_window, text="")
    #     russian_button_three.grid(row = 2, column=1)
    #
    #     russian_button_four = tk.Button(test_window, text="")
    #     russian_button_four.grid(row = 3, column=1)

    # В место этого можно самой последней строчкой написать root.mainloop() Для запуска цикла обработки событий Tkinter

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk() # Создаем основное окно Tkinter
    app = EnglishCardsApp(root) # Создаем объект EnglishLearningApp, передавая ему созданное окно root
    app.run() # Запускаем главный цикл обработки событий Tkinter