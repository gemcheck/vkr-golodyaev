import os
import time
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_session import Session

load_dotenv()

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SESSION_FILE_DIR'] = os.path.join(basedir, 'flask_session')
app.secret_key = os.getenv("SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Session(app)
db = SQLAlchemy(app)

# ---------------- МОДЕЛЬ ДАННЫХ ----------------
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    question_index = db.Column(db.Integer)
    listing_id = db.Column(db.Integer)       
    category = db.Column(db.String(20))      
    question_text = db.Column(db.Text)
    answer_text = db.Column(db.Text)
    correct_answer = db.Column(db.Text)
    time_taken = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

listings_pool = [
    {
        "id": 1,
        "image_base": "que1",
        "questions": [
            {"text": "Сколько раз в коде вызывается метод append?", "correct": "2"},
            {"text": "Как называется входной параметр функции merge_sort?", "correct": "arr"},
            {"text": "С каким значением сравнивается список в первый раз?", "correct": "1"},
            {"text": "Является ли left_half входным параметром или локальной переменной? напишите (parametr/local)", "correct": "local"},
            {"text": "Используются ли в этом коде строковые литералы? Ответ на английском yes/no", "correct": "no"}
        ]
    },
    {
        "id": 2,
        "image_base": "que2",
        "questions": [
            {"text": "Сколько вызовов методов (pop, get, append, add) в цикле while?", "correct": "5"},
            {"text": "Как называется параметр, обозначающий начальную точку поиска?", "correct": "start"},
            {"text": "Какое специальное значение возвращается, если путь не найден?", "correct": "None"},
            {"text": "Какое название имеет переменная итератор?", "correct": "neighbor"},
            {"text": "Инициализируется ли переменная queue как список? Ответ на английском yes/no", "correct": "yes"}
        ]
    },
    {
        "id": 3,
        "image_base": "que3",
        "questions": [
            {"text": "Какая функция используется для преобразования корня в целое число?", "correct": "int"},
            {"text": "Как называется входной параметр, ограничивающий поиск?", "correct": "limit"},
            {"text": "Какое булево значение чаще упоминается в коде?", "correct": "False"},
            {"text": "Является ли primes входным параметром? Ответ на английском yes/no", "correct": "no"},
            {"text": "Используется ли в коде оператор возведения в степень **? Ответ на английском yes/no", "correct": "yes"}
        ]
    },
    {
        "id": 4,
        "image_base": "que4",
        "questions": [
            {"text": "Сколько разных методов is... (например, isupper) в коде?", "correct": "3"},
            {"text": "Какое значение длины (min_len) установлено по умолчанию?", "correct": "8"},
            {"text": "Какое булево значение возвращается в самом конце функции?", "correct": "True"},
            {"text": "Что написано в строке, возвращаемой при ошибке длины?", "correct": "Too short"},
            {"text": "Является ли password первым и единственным параметром? Ответ на английском yes/no", "correct": "no"}
        ]
    },
    {
        "id": 5,
        "image_base": "que5",
        "questions": [
            {"text": "Найдите вызов метода strip. Сколько раз он встречается?", "correct": "2"},
            {"text": "Какой символ используется в параметре delimiter по умолчанию?", "correct": ","},
            {"text": "Используются ли в коде целые числовые константы? Ответ на английском yes/no", "correct": "no"},
            {"text": "Какой строковый литерал (кавычка) используется в параметре quote?", "correct": "\""},
            {"text": "Является ли in_quotes переменной логического типа (bool)? Ответ на английском yes/no", "correct": "yes"}
        ]
    },
    {
        "id": 6,
        "image_base": "que6",
        "questions": [
            {"text": "Какой метод используется для приведения текста к верхнему регистру?", "correct": "upper"},
            {"text": "Как называется параметр, отвечающий за версию API?", "correct": "version"},
            {"text": "Какое числовое значение сравнивается со score?", "correct": "50"},
            {"text": "Какое строковое значение принимает статус, если payload пуст?", "correct": "empty"},
            {"text": "Используется ли в коде f-строка для формирования результата? Ответ на английском yes/no", "correct": "no"}
        ]
    },
    {
        "id": 7,
        "image_base": "que7",
        "questions": [
            {"text": "Сколько методов определено внутри класса ShoppingCart?", "correct": "4"},
            {"text": "Какой параметр метода add_item имеет значение по умолчанию?", "correct": "qty"},
            {"text": "Какое числовое значение скидки устанавливается при сумме > 1000?", "correct": "0.1"},
            {"text": "Как называется ключ для имени товара в словаре items?", "correct": "name"},
            {"text": "Передается ли user_id в конструктор __init__? Ответ на английском yes/no", "correct": "yes"}
        ]
    },
    {
        "id": 8,
        "image_base": "que8",
        "questions": [
            {"text": "Какой метод используется для записи данных в файл?", "correct": "write"},
            {"text": "Как называется параметр метода log, отвечающий за текст?", "correct": "message"},
            {"text": "Чему равно начальное значение logs_count?", "correct": "0"},
            {"text": "Какое значение level установлено по умолчанию?", "correct": "INFO"},
            {"text": "Используется ли в коде метод close() для файла? Ответ на английском yes/no", "correct": "no"}
        ]
    },
    {
        "id": 9,
        "image_base": "que9",
        "questions": [
            {"text": "Назовите метод, который принимает параметр factor.", "correct": "scale"},
            {"text": "Как называется параметр, задающий высоту прямоугольника?", "correct": "height"},
            {"text": "С каким числом сравнивается factor в условии if?", "correct": "0"},
            {"text": "Какой цвет задан в коде по умолчанию?", "correct": "red"},
            {"text": "Как называется метод который возвращает площать?", "correct": "area"}
        ]
    },
    {
        "id": 10,
        "image_base": "que10",
        "questions": [
            {"text": "Сколько раз в коде встречается конкатенация +=?", "correct": "1"},
            {"text": "Как называется булев параметр, разрешающий цифры?", "correct": "allow_numbers"},
            {"text": "Какое число используется как предел длины строки?", "correct": "50"},
            {"text": "Что возвращает функция, если итоговая строка пуста?", "correct": "n/a"},
            {"text": "Является ли char переменной цикла (итератором)? Ответ на английском yes/no", "correct": "yes"}
        ]
    },
    {
        "id": 11,
        "image_base": "que11",
        "questions": [
            {"text": "Какая называется переменная которая хранит отсортированные значения?", "correct": "sorted_nums"},
            {"text": "Как называется входной список чисел?", "correct": "numbers"},
            {"text": "Является ли median входным параметром? Ответ на английском yes/no", "correct": "no"},
            {"text": "Как называется ключ для среднего значения в итоговом словаре?", "correct": "mean"},
            {"text": "Используется ли в коде метод sorted()? Ответ на английском yes/no", "correct": "yes"}
        ]
    },
    {
        "id": 12,
        "image_base": "que12",
        "questions": [
            {"text": "Сколько раз в коде встречается функция print?", "correct": "2"},
            {"text": "Как называется параметр, ограничивающий время ожидания?", "correct": "timeout"},
            {"text": "Сколько попыток (retries) задано по умолчанию?", "correct": "3"},
            {"text": "Какое слово ищется в url для имитации ошибки?", "correct": "error"},
            {"text": "Импортируется ли в коде библиотека requests? Ответ на английском yes/no", "correct": "yes"}
        ]
    },
    {
        "id": 13,
        "image_base": "que13",
        "questions": [
            {"text": "Какая функция используется для округления результата?", "correct": "round"},
            {"text": "Какой параметр отвечает за процент комиссии?", "correct": "fee_percent"},
            {"text": "На какое число делится fee_percent в формуле?", "correct": "100"},
            {"text": "Какой входной параметр сравнивается с 0?", "correct": "amount"},
            {"text": "Является ли rate входным параметром? Ответ на английском yes/no", "correct": "yes"}
        ]
    },
    {
        "id": 14,
        "image_base": "que14",
        "questions": [
            {"text": "Какая функция вызывается из модуля random?", "correct": "choice"},
            {"text": "Какая длина ID (length) установлена по умолчанию?", "correct": "12"},
            {"text": "С каким числом (в виде строки) сравнивается начало ID?", "correct": "0"},
            {"text": "Какой префикс добавляется к каждому ID?", "correct": "ID_"},
            {"text": "Используется ли в коде функция range()? Ответ на английском yes/no", "correct": "yes"}
        ]
    },
    {
        "id": 15,
        "image_base": "que15",
        "questions": [
            {"text": "Какой метод используется для разделения строки лога?", "correct": "split"},
            {"text": "Как называется входной список строк?", "correct": "logs"},
            {"text": "Чему равно начальное значение error_count?", "correct": "0"},
            {"text": "Какое строковое значение соответствует критической ошибке?", "correct": "CRITICAL"},
            {"text": "Является ли status локальной переменной внутри цикла? Ответ на английском yes/no", "correct": "yes"}
        ]
    },
    {
        "id": 16,
        "image_base": "que16",
        "questions": [
            {"text": "Какой метод вызывается для сортировки итогового списка?", "correct": "sort"},
            {"text": "Как называется входной список элементов?", "correct": "items"},
            {"text": "С каким числом сравнивается count в финальном цикле?", "correct": "1"},
            {"text": "Используются ли в этом коде строковые литералы? Ответ на английском yes/no", "correct": "no"},
            {"text": "Создается ли в коде пустой словарь seen? Ответ на английском yes/no", "correct": "yes"}
        ]
    },
    {
        "id": 17,
        "image_base": "que17",
        "questions": [
            {"text": "Сколько раз вызывается функция len?", "correct": "4"},
            {"text": "Как называются два входных параметра-матрицы? Ответ введите через запятую", "correct": "mat_a, mat_b"},
            {"text": "Какое значение возвращается, если размеры матриц не совпадают?", "correct": "None"},
            {"text": "Есть ли в коде строковые переменные? Ответ на английском yes/no", "correct": "no"},
            {"text": "В какой переменной хранится результат?", "correct": "result"}
        ]
    },
    {
        "id": 18,
        "image_base": "que18",
        "questions": [
            {"text": "Какой метод используется для удаления первого элемента из списка order?", "correct": "pop"},
            {"text": "Какой лимит кэша задан по умолчанию?", "correct": "5"},
            {"text": "Является ли key параметром метода set? Ответ на английском yes/no", "correct": "yes"},
            {"text": "Используются ли строки в теле методов? Ответ на английском yes/no", "correct": "no"},
            {"text": "Инициализируется ли self.store как словарь? Ответ на английском yes/no", "correct": "yes"}
        ]
    },
    {
        "id": 19,
        "image_base": "que19",
        "questions": [
            {"text": "Как называется входной параметр функции?", "correct": "seconds"},
            {"text": "Используется ли в коде цикл for? Ответ на английском yes/no", "correct": "no"},
            {"text": "Сколько раз в коде встречается вызов функции?", "correct": "3"},
            {"text": "Возвращает ли функция список (list)? Ответ на английском yes/no", "correct": "no"},
            {"text": "Является ли res локальной переменной? Ответ на английском yes/no", "correct": "yes"}
        ]
    },
    {
        "id": 20,
        "image_base": "que20",
        "questions": [
            {"text": "Какой метод используется для извлечения задачи из списка queue?", "correct": "pop"},
            {"text": "Как называется входной параметр-очередь?", "correct": "queue"},
            {"text": "На какое число делится task_id для получения остатка?", "correct": "2"},
            {"text": "С какой строкой сравнивается приоритет задачи?", "correct": "high"},
            {"text": "Извлекается ли в коде элемент из списка? Ответ на английском yes/no", "correct": "yes"}
        ]
    }
]

# ---------------- ЛОГИКА ГЕНЕРАЦИИ ТЕСТА ----------------
def generate_test_flow():
    pool = listings_pool.copy()
    random.shuffle(pool)
    
    selected = pool[:18]
    styles = ["none"] * 6 + ["standard"] * 6 + ["custom"] * 6
    random.shuffle(styles)
    
    flow = []
    # 1. Инфо-страница
    flow.append({"type": "info", "code": 
"""Кратко:
Тестирование в рамках ВКР, необходимо ответить на вопросы по листингам кода на языке программирования Python3, на страницу назад возвращаться нельзя.
        
Все ответы анонимизированы.

Развернуто:
ИНФОРМАЦИЯ ОБ ИССЛЕДОВАНИИ И СОГЛАСИЕ

Данное исследование проводится в рамках подготовки выпускной квалификационной работы (ВКР) и направлено на изучение влияния различных способов визуализации программного кода на скорость его понимания и качество запоминания информации.

Порядок проведения:
    * Вам будет предложено проанализировать фрагменты кода на языке Python и ответить на вопросы по их структуре и результатам выполнения.
    * В ходе тестирования фиксируется время решения, корректность ответов и технические параметры сессии.
    * Важно, выполняйте задания последовательно, не используйте кнопку «Назад» в браузере.

Юридическая информация и конфиденциальность:
    1. Сбор данных осуществляется в анонимном виде. Исследование не предполагает сбор персональных данных, позволяющих идентифицировать вашу личность (ФИО, номер телефона, e-mail).

    2. Для технического обеспечения процесса тестирования (сохранения текущего прогресса и идентификации сессии без привязки к личности) сайт использует файлы cookie и локальное хранилище.

    3. Нажимая кнопку «Далее», Вы даете свое согласие на автоматизированную обработку предоставляемых вами данных (включая технические параметры сессии и использование файлов cookie) в соответствии с ФЗ №152-ФЗ «О персональных данных».

    4. Все полученные результаты будут использованы исключительно в научных и исследовательских целях в обобщенном виде.

Пожалуйста, старайтесь отвечать максимально точно и работать в комфортном для вас темпе.

Нажимая кнопку «Далее», Вы подтверждаете ознакомление с правилами и даете согласие на участие в исследовании.
"""})
    # 2. Демография
    flow.append({
        "type": "profile", 
        "code": "Укажите Ваш курс или должность. Все ответы вводятся внизу страницы! Переход между страницами можно осуществлять через нажатие Enter.\nОбычно исследования ориентируются только на грейд, в нынешнем исследовании хотелось бы проследить корреляцию в зависимости от возраста.",
        "inputs": [
            {"name": "grade", "label": "Для студентов номер курса, для работников грейд(джуниор, мидл, синьор)"},
            {"name": "age", "label": "Ваш возраст"}
        ]
    })

    # 3. Основные блоки
    for i, listing in enumerate(selected):
        style = styles[i]
        image_name = f"{listing['image_base']}_{style}.png"
        
        for q in listing['questions']:
            flow.append({
                "type": "question",
                "image": image_name,
                "question": q['text'],
                "correct": q['correct'],
                "category": style,
                "listing_id": listing['id']
            })
            
    # 4. Финальное сравнение
    flow.append({
        "type": "comparison",
        "title": "Сравнительный анализ",
        "images": ["que9_none.png", "que9_custom.png", "que9_standard.png"],
        "questions": [
            "Какой вариант вам нравится больше всего? (1, 2 или 3)", 
            "Почему именно он?"
        ]
    })
    return flow

# ---------------- РОУТЫ ----------------
@app.route("/", methods=["GET", "POST"])
def survey():
    if "flow" not in session or "user_id" not in session:
        session["user_id"] = int(time.time() * 1000)
        session["flow"] = generate_test_flow()
        session["current_index"] = 0
        session["temp_responses"] = []
        session["q_start_time"] = time.time()
        session.modified = True
    
    flow = session["flow"]
    index = session["current_index"]

    if index >= len(flow):
        return redirect(url_for("finish"))

    page = flow[index]

    if request.method == "POST":
        duration = round(time.time() - session.get("q_start_time", time.time()), 2)
        final_ans = ""

        # Логика сбора ответов в зависимости от типа страницы
        if page.get("type") == "profile":
            ans_parts = []
            for inp in page["inputs"]:
                val = request.form.get(inp["name"], "").strip()
                if not val:
                    return render_template("survey.html", page=page, index=index, error="Заполните все поля")
                ans_parts.append(f"{inp['label']}: {val}")
            final_ans = " | ".join(ans_parts)

        elif page.get("type") == "comparison":
            ans_parts = []
            for i, q_text in enumerate(page.get("questions", [])):
                val = request.form.get(f"comp_{i}", "").strip()
                if not val:
                    return render_template("survey.html", page=page, index=index, error="Ответьте на все вопросы")
                ans_parts.append(f"{q_text}: {val}")
            final_ans = " | ".join(ans_parts)

        elif page.get("type") == "question":
            final_ans = request.form.get("answer", "").strip()
            if not final_ans:
                return render_template("survey.html", page=page, index=index, error="Ответ обязателен")
        
        else:
            # Для типа 'info' или других страниц без полей ввода
            final_ans = "Просмотрено"
        is_empty = False
        if page.get("type") in ["profile", "comparison"]:
            if any(not part.split(": ")[1].strip() for part in final_ans.split(" | ")):
                is_empty = True
        elif page.get("type") == "question":
            if not final_ans:
                is_empty = True
        if is_empty:
            return render_template("survey.html", page=page, index=index, error="Пожалуйста, заполните все поля перед переходом.")
        
        # Сохраняем результат в временный список
        res = {
            "question_index": index,
            "listing_id": page.get("listing_id"),
            "category": page.get("category", "info"),
            "image": page.get("image") if page.get("type") == "question" else None,
            "images": page.get("images") if page.get("type") == "comparison" else None,
            "question_text": page.get("question", "Инфо"),
            "answer_text": final_ans,
            "correct_answer": page.get("correct", "N/A"),
            "time_taken": duration
        }
        
        temp = session.get("temp_responses", [])
        temp.append(res)
        session["temp_responses"] = temp
        session["current_index"] = index + 1
        session["q_start_time"] = time.time()
        session.modified = True

        if session["current_index"] >= len(flow):
            save_all_to_db()
            return redirect(url_for("finish"))

        return redirect(url_for("survey"))
    
    return render_template("survey.html", page=page, index=index)

def save_all_to_db():
    try:
        for item in session["temp_responses"]:
            new_resp = Response(
                user_id=session["user_id"],
                question_index=item["question_index"],
                listing_id=item["listing_id"],
                category=item["category"],
                question_text=item["question_text"],
                answer_text=item["answer_text"],
                correct_answer=item["correct_answer"],
                time_taken=item["time_taken"]
            )
            db.session.add(new_resp)
        db.session.commit()
        session.pop("temp_responses", None)
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")

@app.route("/finish")
def finish():
    user_id = session.get("user_id", "Unknown")
    
    db_results = Response.query.filter_by(user_id=user_id).order_by(Response.id).all()
    
    flat_results = []
    for r in db_results:
        flat_results.append({
            "question": r.question_text,       
            "listing_id": r.listing_id,        
            "image": r.question_index,           
            "category": r.category,
            "answer": r.answer_text,
            "correct": r.correct_answer,
            "time": r.time_taken
        })

    if not flat_results:
        temp_responses = session.get("temp_responses", [])
        for r in temp_responses:
            flat_results.append({
                "question": r.get("question_text"),
                "listing_id": r.get("listing_id"),
                "image": r.get("image"),
                "category": r.get("category"),
                "answer": r.get("answer_text"),
                "correct": r.get("correct_answer"),
                "time": r.get("time_taken")
            })

    return render_template("result.html", 
                           user_id=user_id, 
                           results=flat_results)

@app.route("/restart")
def restart():
    session.clear()
    return redirect(url_for("survey"))

if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG"))
