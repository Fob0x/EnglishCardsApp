
import sqlite3
import tkinter as tk
import random
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import customtkinter as CTk

class EnglishCardsApp: # Класс самой моей программы
    def __init__(self, root):

        self.root = root # Сохраняем объект основного окна Tkinter в атрибуте
        self.root.title("Изучений английских слов по карточкам") # Заголовок (название приложения)
        self.root.resizable(False, False) # Отключение возможности собственноручного масштабирования окна
        self.root.iconbitmap("Serg.ico") # Изменяем иконку окна (пасхал'очка) c расширением .ico
        self.root.geometry("300x400")


##################################

        self.background_image = CTk.CTkImage(dark_image=Image.open("bgm.png"), size = (300,400))
        self.background_label = CTk.CTkLabel(self.root, image=self.background_image, text="")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

##################

        self.menu_frame = CTk.CTkFrame(root)
        self.menu_frame.place(x=-150, y=0, relwidth=0.5, relheight=1.0)
        self.menu_expanded = False

        self.expand_button = CTk.CTkButton(root, text=">", command=self.toggle_menu, width=30, height=400)
        self.expand_button.place(x=0, y=0)

        # Создаем Label с фоновым изображением в menu_frame
        self.background_bar_image = CTk.CTkImage(dark_image=Image.open("bg.png"), size = (500,400))  # Укажите путь к вашей картинке
        self.background_label = CTk.CTkLabel(self.menu_frame, image=self.background_bar_image)
        self.background_label.place(x = 0, y = 0)

        # Добавляем кнопки внутри выдвигающегося бара
        button_font = ("Helvetica", 12)  # Измените на нужный вам шрифт и размер
        self.cards_button = CTk.CTkButton(self.menu_frame, text="Карточки", font=button_font, command=self.open_cards)
        self.cards_button.pack(fill=tk.X, expand=True, pady=(10, 0))

        self.tests_button = CTk.CTkButton(self.menu_frame, text="Тесты", font=button_font, command=self.open_test)
        self.tests_button.pack(fill=tk.X, expand=True, pady=(0, 5))

        # Создание кнопок для выбора цвета фона
        self.appearance_mode_option_menu = CTk.CTkOptionMenu(
            self.menu_frame,
            values=["light", "Dark", "System"],
            command=self.change_appearance_mode_event, anchor="center"
        )
        self.appearance_mode_option_menu.pack(fill=tk.X, expand=True, pady=(0, 10))

        # Подключение к базе данных (создание файла или подключение к существующему)
        self.conn = sqlite3.connect('cards.db')
        self.cursor = self.conn.cursor()

        '''sqlite3.connect('cards.db'):
        Эта строка создает подключение к базе данных SQLite с именем 'cards.db'. Если файл базы данных не существует, он будет создан.
        Если файл уже существует, будет установлено подключение к нему. Важно, чтобы вы указали корректный путь к файлу базы данных.
        В данном случае, 'cards.db' - это имя файла базы данных. Вы можете изменить это имя на другое, если хотите.

        self.cursor = self.conn.cursor():
        После установления подключения к базе данных, создается объект курсора.
        Курсор используется для выполнения SQL-запросов к базе данных и получения результатов запросов.
        Курсор позволяет вам взаимодействовать с базой данных, выполнять операции добавления, изменения, удаления и извлечения данных.

        Итак, вместе эти строки кода создают подключение к базе данных и курсор для выполнения операций.
        Вы можете использовать этот курсор для выполнения запросов SQL к базе данных, как, например, для создания таблицы или вставки данных.'''

        # Создание таблицы cards, если она еще не существует
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS cards (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        english TEXT NOT NULL,
                        russian TEXT NOT NULL,
                        image_path TEXT
                    )
                ''')
        self.conn.commit()

        """Этот код выполняет создание таблицы cards в базе данных SQLite, если она еще не существует. Давайте разберем, что делают эти функции и как они работают:

        self.cursor.execute(...):
        Эта строка выполняет SQL-запрос для создания таблицы в базе данных. Метод execute() курсора позволяет выполнить SQL-запрос на базе данных. В данном случае, SQL-запрос является многострочной строкой, которая определяет структуру таблицы cards. Здесь используется SQL-запрос CREATE TABLE, который создает таблицу в базе данных.

        В структуре таблицы указаны следующие поля:

        id: Первичный ключ таблицы. Он будет автоматически инкрементироваться при добавлении новых записей.
        english: Текстовое поле для хранения английского слова.
        russian: Текстовое поле для хранения русского перевода.
i       mage_path: Текстовое поле для хранения пути к изображению (опционально).
        self.conn.commit():
        После выполнения SQL-запроса для создания таблицы, необходимо "зафиксировать" изменения в базе данных с помощью метода commit(). Это позволяет сохранить изменения в базе данных навсегда.

        Обратите внимание, что CREATE TABLE IF NOT EXISTS это конструкция SQL, которая создает таблицу только в случае, если она еще не существует. 
        Это полезно, чтобы избежать ошибок при повторном выполнении кода. Если таблица уже существует, запрос игнорируется.

        Таким образом, эти строки кода создают таблицу cards с определенной структурой (столбцами) в базе данных, и эта таблица будет использоваться для хранения карточек в вашем приложении."""

    def change_appearance_mode_event(self, new_appearance_mode):
        CTk.set_appearance_mode(new_appearance_mode)
    def toggle_menu(self):
        if not self.menu_expanded:
            self.menu_frame.place(x=0)
        else:
            self.menu_frame.place(x=-150)
        self.menu_expanded = not self.menu_expanded


        # Инициализация списка, хранящего данные карточек
        self.card_list = []

        self.load_cards()  # Загрузка карточек при запуске


    """С 33-ей по 50-ую строчку создаётся окно настроек с 3-мя кнопками для выбора цвета фона основного окна
    Каждая кнопка связана с ф-цией set_background_color, изменяющей цвет основого окна и затем закрывающей окно настроек"""

    def save_cards(self):
        # Очистка таблицы перед сохранением (опционально, в зависимости от моего случая (А может вообще убрать?))
        self.cursor.execute('DELETE FROM cards')
        self.conn.commit()

        # Вставка карточек в таблицу
        for card in self.card_list:
            self.cursor.execute('''
                INSERT INTO cards (english, russian, image_path)
                VALUES (?, ?, ?)
            ''', (card['English'], card['Russian'], card['Image']))
            self.conn.commit()

    '''self.cursor.execute('DELETE FROM cards'):
    Эта строка выполняет SQL-запрос для удаления всех записей из таблицы cards. Этот шаг может быть опциональным, в зависимости от вашей логики приложения. Если вы хотите полностью перезаписать таблицу новыми данными при каждом сохранении, это удаление может быть полезным.

    self.conn.commit():
    После выполнения SQL-запроса для удаления записей, метод commit() сохраняет изменения в базе данных.

    Вставка карточек в таблицу:
    Далее происходит итерация по списку self.card_list, который хранит карточки. Для каждой карточки выполняется SQL-запрос для вставки данных в таблицу. 
    Запрос использует параметризованный формат для вставки значений в соответствующие столбцы таблицы.
     В данном случае, в значения столбцов english, russian и image_path будут подставлены соответствующие значения из каждой карточки.
    После выполнения каждой операции вставки, метод commit() вызывается снова, чтобы сохранить изменения в базе данных.

    Таким образом, эти строки кода осуществляют удаление старых данных из таблицы (если это требуется), а затем вставляют новые карточки из списка self.card_list в таблицу cards базы данных.'''

    def load_cards(self):
        self.card_list = []  # Очищаем список карточек

        self.cursor.execute('SELECT english, russian, image_path FROM cards')
        rows = self.cursor.fetchall()

        for row in rows:
            card = {
                'English': row[0],
                'Russian': row[1],
                'Image': row[2]
            }
            self.card_list.append(card)

    '''Эти функции выполняют загрузку карточек из базы данных SQLite в список self.card_list, который используется вашим приложением для работы с карточками.
     Давайте разберем, что делают эти функции и как они работают:

    self.card_list = []:
    Эта строка просто очищает список self.card_list, чтобы в случае загрузки карточек из базы данных, он был пустым и готов к заполнению новыми данными.

    self.cursor.execute('SELECT english, russian, image_path FROM cards'):
    Эта строка выполняет SQL-запрос для извлечения данных из таблицы cards. 
    SQL-запрос SELECT выбирает определенные столбцы (english, russian, image_path) из таблицы cards.

    rows = self.cursor.fetchall():
    После выполнения SQL-запроса с помощью метода execute(), метод fetchall() извлекает все строки, соответствующие результатам запроса, и сохраняет их в переменной rows. 
    Каждая строка представляется в виде кортежа, где элементы кортежа соответствуют столбцам таблицы.

    Заполнение списка карточек:
    Далее выполняется итерация по кортежам в rows. Для каждого кортежа создается словарь card, где ключи English, Russian и Image связаны с соответствующими значениями из кортежа. 
    Эти значения представляют собой данные английского слова, русского перевода и пути к изображению.

    Добавление карточек в список:
    Словарь card добавляется в список self.card_list, что в конечном итоге заполняет список карточек из базы данных.

    Итак, эти строки кода выполняют извлечение данных из таблицы cards в базе данных и заполняют список self.card_list
    этими данными для дальнейшей работы вашего приложения с карточками.'''

    def open_cards(self):
        # Создание нового окна для карточек
        cards_window = tk.Toplevel(self.root)
        cards_window.title("Карточки")
        cards_window.iconbitmap("Serg.ico")

        # Ф-ция для добавления карточки
        def add_card():
            card = {
                "English": english_entry.get(),
                "Russian": russian_entry.get(),
                "Image": self.image_path
            }
            self.card_list.append(card)  # Сохраняем в общий список карт, продемонстрированный пользователю

            self.cursor.execute('''
                INSERT INTO cards (english, russian, image_path)
                VALUES (?, ?, ?)
            ''', (card['English'], card['Russian'], card['Image']))
            self.conn.commit()

            english_entry.delete(0, tk.END)
            russian_entry.delete(0, tk.END)
            self.image_path = ""
            update_word_list()

            '''def open_cards(self):
    Эта функция вызывается для открытия нового окна, где пользователь может работать с карточками.

    Создание нового окна:
    В начале функции создается новое окно с помощью tk.Toplevel(self.root). Это окно будет содержать элементы для добавления и просмотра карточек.

    Установка заголовка и иконки окна:
    Затем устанавливаются заголовок окна и иконка с помощью методов title() и iconbitmap().

    def add_card():
    Эта внутренняя функция вызывается при нажатии на кнопку для добавления новой карточки. Она выполняет следующие действия:

    Создание словаря card:
    Создается словарь card с данными, которые пользователь вводит в поля ввода английского слова (english_entry) и перевода (russian_entry). Также в этот словарь добавляется путь к изображению (self.image_path), который предполагается, что был выбран пользователем.

    Сохранение в общий список:
    Созданный словарь card добавляется в общий список карточек self.card_list. Это нужно для того, чтобы новая карточка сразу отобразилась в интерфейсе и была доступна для последующего сохранения в базу данных.

    Вставка данных в базу данных:
    Затем выполняется SQL-запрос для вставки данных из словаря card в таблицу cards в базе данных. После вставки, вызывается метод commit() для сохранения изменений.

    Очистка полей ввода:
    Поля ввода английского слова и перевода (english_entry и russian_entry) очищаются, чтобы быть готовыми для ввода следующей карточки.

    Обновление списка:
    Вызывается функция update_word_list(), которая обновляет список карточек в интерфейсе, чтобы отразить добавленную карточку.

    Эти функции позволяют пользователю добавлять новые карточки в приложение, как в интерфейсе, так и в базе данных.'''

        def delete_card():
            selected_index = word_list.curselection()
            if selected_index:
                index = selected_index[0]
                card_to_delete = self.card_list[index]
                self.card_list.pop(index)

                self.cursor.execute('DELETE FROM cards WHERE english = ?', (card_to_delete['English'],))
                self.conn.commit()

                update_word_list()

        '''def delete_card():
            Эта функция вызывается при нажатии на кнопку удаления карточки.

            selected_index = word_list.curselection():
            Эта строка получает индекс выделенной пользователем карточки в списке word_list. word_list представляет собой элемент интерфейса, в котором отображаются английские слова карточек.

            if selected_index::
            Этот блок if выполняется, если пользователь действительно выделил какую-либо карточку в списке.

            Получение индекса и карточки для удаления:
            Из переменной selected_index получается индекс выделенной карточки. Далее, по этому индексу, из списка self.card_list получается словарь, представляющий карточку, которую пользователь хочет удалить.

            Удаление из списка:
            Выделенная карточка удаляется из списка self.card_list с помощью метода pop(index).

            Удаление из базы данных:
            Затем выполняется SQL-запрос для удаления карточки из таблицы cards в базе данных. 
            SQL-запрос DELETE FROM cards WHERE english = ? удаляет строку, где значение столбца english совпадает с английским словом выделенной карточки. 
            Передача (card_to_delete['English'],) вторым аргументом метода execute() является кортежем, который заменяет ? в запросе.

            self.conn.commit():
            После выполнения SQL-запроса для удаления, метод commit() сохраняет изменения в базе данных.

            Обновление списка:
            Наконец, вызывается функция update_word_list(), чтобы обновить список карточек в интерфейсе после удаления.

            Таким образом, эта функция обеспечивает удаление выбранной карточки как из списка, так и из базы данных.'''

        def update_word_list():
            word_list.delete(0, tk.END) #
            for i, card in enumerate(self.card_list):
                word_list.insert(tk.END, card['English']) # Добавляем английские слова в список


        # Ф-ция для открытия окна с подробной
        def choose_image(): # Да я, блять, просто не понимаю как эту хуйню фиксить. Хуй инфы есть, сука.  UserWarning: CTkLabel Warning: Given image is not CTkImage but <class 'PIL.ImageTk.PhotoImage'>. Image can not be scaled on HighDPI displays, use CTkImage instead. warnings.warn(f"{type(self).__name__} Warning: Given image is not CTkImage but {type(image)}. Image can not be scaled on HighDPI displays, use CTkImage instead.\n")
            self.image_path = filedialog.askopenfilename() # Получаем путь к изображению
            if self.image_path:
                img = Image.open(self.image_path)
                img.thumbnail((150, 100)) # задаём размер изображения
                img = ImageTk.PhotoImage(img)
                img_label.configure(image = img) # обновляем изображение
                img_label.image = img

        # Ф-ция для открытия окна с подробной инф-цией о карточке
        def open_card_window(index):
            card = self.card_list[index]
            card_window = CTk.CTkToplevel(self.root)
            card_window.title(card['English'])

            english_label = CTk.CTkLabel(card_window, text = "Английское слово:")
            english_label.pack()
            eng_value = CTk.CTkLabel(card_window, text = card['English'])
            eng_value.pack()

            rus_label = CTk.CTkLabel(card_window, text="Перевод на русский:")
            rus_label.pack()
            rus_value = CTk.CTkLabel(card_window, text=card['Russian'])
            rus_value.pack()

            if card['Image']:
                img = Image.open(card['Image'])
                img.thumbnail((150, 100))  # Задаем размер изображения
                img = ImageTk.PhotoImage(img)
                img_label = CTk.CTkLabel(card_window, image=img, text="")
                img_label.image = img
                img_label.pack()

        # Создание интерфейса для добавления, отображения и удаления карточек
        english_label = CTk.CTkLabel(cards_window, text = "Английское слово:", text_color="Black")
        english_label.pack()

        english_entry = CTk.CTkEntry(cards_window)
        english_entry.pack()

        russian_label = CTk.CTkLabel(cards_window, text = "Перевод на русский:", text_color="Black")
        russian_label.pack()
        russian_entry = CTk.CTkEntry(cards_window)
        russian_entry.pack()

        choose_image_button = CTk.CTkButton(cards_window, text = "Выбрать картинку", command = choose_image )
        choose_image_button.pack()

        img_label = CTk.CTkLabel(cards_window, text="") # Метка для отображения изображения
        img_label.pack()

        add_button = CTk.CTkButton(cards_window, text = "Добавить карточку", command=add_card)
        add_button.pack()

        delete_button = CTk.CTkButton(cards_window, text = "Удалить карточку", command=delete_card )
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
        check_button.bind()

        # Создание метки с выводом правильности ответа
        result_label = tk.Label(test_window, text = "", font=("Helvetica", 14))
        result_label.pack()

        # Кнопка для перехода на следующий вопрос
        next_button = tk.Button(test_window, text = "Следующий вопрос", comman = display_next_card, font = ("Helvetica", 14))
        next_button.pack()

        answer_entry.bind("<Return>", check_answer)

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

    def __del__(self): # Закрываю соединение с БД при закрытии приложения
        self.conn.close()


if __name__ == "__main__":

    root = CTk.CTk() # Создаем основное окно Tkinter
    app = EnglishCardsApp(root) # Создаем объект EnglishLearningApp, передавая ему созданное окно root
    app.run() # Запускаем главный цикл обработки событий Tkinter