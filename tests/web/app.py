import os
import time
from datetime import datetime  
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv 

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- МОДЕЛЬ ----------------
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False) 
    question_index = db.Column(db.Integer)
    question_text = db.Column(db.Text)
    answer_text = db.Column(db.Text)
    correct_answer = db.Column(db.Text)
    time_taken = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# ---------------- ДАННЫЕ ----------------
questions = [
    {
        "code": """Кратко:
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

Нажимая кнопку «Далее», Вы подтверждаете ознакомление с правилами и даете согласие на участие в исследовании."""
    },
    {   
        "code": "Укажите Ваш курс или должность. Все ответы вводятся внизу страницы!\nОбычно исследования ориентируются только на грейд, в нынешнем исследовании хотелось бы проследить корреляцию в зависимости от возраста.",
        "questions": [
            "Для студентов номер курса, для работников грейд(джуниор, мидл, синьор)", "Укажите Ваш возраст"
        ]
    },


    {   
        "code": """Этап 1: Базовый уровень сложности. 
Вам будет предложено два листинга кода. К каждому из них составлено по два вопроса. Для удобства анализа текст кода и вопрос к нему представлены на одной странице."""
    },
    {   "image": "que11.png",
        "questions": [
            "1. Какое значение имеет итоговая переменная?\nОтвет введите числом"
        ],
        "correct_answers": ["10"]
    },
    {   "image": "que11.png",
        "questions": [
            "2. Какая переменная используется для хранения результата внутри функции?"
        ],
        "correct_answers": ["result"]
    },
    {   "image": "que1.png",
        "questions": [
            "1. Какое значение имеет итоговая переменная?\nОтвет введите числом"
        ],
        "correct_answers": ["15"]
    },
    {   "image": "que1.png",
        "questions": [
            "2. Какая переменная используется для хранения результата внутри функции?"
        ],
        "correct_answers": ["output"]
    },


    {   
        "code": """Этап 2: Средний уровень сложности. 
Данный этап включает в себя два листинга кода повышенной сложности. К каждому фрагменту прилагается по два вопроса. Обратите внимание: структура кода и логика вычислений на данном этапе требуют более детального анализа."""
    },
    {   "image": "que21.png",
        "questions": [
            "1. Какое название имеет параметр функции?\nОтвет введите буквой"
        ],
        "correct_answers": ["n"]
    },
    {   "image": "que21.png",
        "questions": [
            "2. Какая переменная используется в цикле (счетчик)?"
        ],
        "correct_answers": ["i"]
    },
    {   "image": "que2.png",
        "questions": [
            "1. Какое название имеет параметр функции?\nОтвет введите буквой"
        ],
        "correct_answers": ["k"]
    },
    {   "image": "que2.png",
        "questions": [
            "2. Какая переменная используется в цикле (счетчик)?"
        ],
        "correct_answers": ["j"]
    },


    {   
        "code": """Этап 3: Высокий уровень сложности. 
Заключительный этап тестирования. Вам будет предложено два комплексных фрагмента кода. К каждому из них составлено по ЧЕТЫРЕ контрольных вопроса. Данный блок направлен на проверку глубокого понимания алгоритмической логики и взаимосвязей внутри программы."""
    },
    {   "image": "que31.png",
        "questions": [
            "1. Сколько раз вызывается основная вычислительная функция (square / cube)?\nОтвет введите числом"
        ],
        "correct_answers": ["3"]
    },
    {   "image": "que31.png",
        "questions": [
            "2. Какой параметр у функции?\nОтвет введите одной буквой латинского алфавита"
        ],
        "correct_answers": ["x"]
    },
    {   "image": "que31.png",
        "questions": [
            "3. Какая переменная используется в цикле?"
        ],
        "correct_answers": ["res"]
    },
    {   "image": "que31.png",
        "questions": [
            "4. Что возвращает основная функция?"
        ],
        "correct_answers": ["True"]
    },
    {   "image": "que3.png",
        "questions": [
            "1. Сколько раз вызывается основная вычислительная функция (square / cube)?\nОтвет введите числом"
        ],
        "correct_answers": ["3"]
    },
    {   "image": "que3.png",
        "questions": [
            "2. Какой параметр у функции?\nОтвет введите одной буквой латинского алфавита"
        ],
        "correct_answers": ["a"]
    },
    {   "image": "que3.png",
        "questions": [
            "3. Какая переменная используется в цикле?"
        ],
        "correct_answers": ["result"]
    },
    {   "image": "que3.png",
        "questions": [
            "4. Что возвращает основная функция?"
        ],
        "correct_answers": ["False"]
    },

    {
        "type": "comparison",
        "code": "Выберите вариант подсветки кода, который кажется вам наиболее удобным и читаемым:",
        "images": ["que41.png", "que42.png", "que43.png"],
        "questions": ["Какой вариант вам нравится больше всего? (1, 2 или 3)", "Расскажите подробнее"]
    }
]

# ---------------- РОУТЫ ----------------

@app.route("/", methods=["GET", "POST"])
def survey():
    # Идентификация уникальной сессии без сбора персональных данных (анонимизация)
    if "user_id" not in session:
        session["user_id"] = int(time.time() * 1000)
    
    if "current_index" not in session:
        session["current_index"] = 0
        session["q_start_time"] = time.time()

    index = session["current_index"]

    # Предотвращение ошибок выхода за границы списка при завершении теста
    if index >= len(questions):
        return redirect(url_for("finish"))

    current_q = questions[index]

    if request.method == "POST":
        q_list = current_q.get("questions", [])
        correct_list = current_q.get("correct_answers", [])
        
        # Вычисление когнитивной нагрузки через затраченное время
        duration = round(time.time() - session.get("q_start_time", time.time()), 2)

        if q_list:
            # Валидация: все вопросы на странице должны иметь ответ
            for i, _ in enumerate(q_list):
                ans = request.form.get(f"answer_{i}", "").strip()
                if not ans:
                    return render_template("survey.html", question=current_q, index=index, error="Ответ обязателен")
            
            # Атомарное сохранение каждого ответа для детального анализа
            for i, qtext in enumerate(q_list):
                ans = request.form.get(f"answer_{i}", "").strip()
                c_ans = correct_list[i] if i < len(correct_list) else "N/A"
                new_resp = Response(
                    user_id=session["user_id"],
                    question_index=index + 1,
                    question_text=qtext,
                    answer_text=ans,
                    correct_answer=c_ans,
                    time_taken=duration
                )
                db.session.add(new_resp)
        else:
            # Логирование просмотра информационных блоков
            new_resp = Response(
                user_id=session["user_id"],
                question_index=index + 1,
                question_text="Инфо-страница",
                answer_text="Просмотрено",
                correct_answer="N/A",
                time_taken=duration
            )
            db.session.add(new_resp)

        db.session.commit()
        
        session["current_index"] = index + 1
        session["q_start_time"] = time.time()
        
        if session["current_index"] >= len(questions):
            return redirect(url_for("finish"))
            
        return redirect(url_for("survey"))

    return render_template("survey.html", question=current_q, index=index)

@app.route("/finish")
def finish():
    uid = session.get("user_id")
    if not uid: 
        return redirect(url_for("survey"))
    
    user_responses = Response.query.filter_by(user_id=uid).order_by(Response.id).all()
    
    # Группировка по тексту вопроса для сравнительного анализа ответов на разных этапах
    grouped_results = {}
    for r in user_responses:
        q_key = r.question_text.strip()
        
        if q_key not in grouped_results:
            grouped_results[q_key] = {
                "question": q_key,
                "attempts": []
            }
        
        grouped_results[q_key]["attempts"].append({
            "answer": r.answer_text,
            "correct": r.correct_answer,
            "time": r.time_taken,
            "page_index": r.question_index
        })
    
    return render_template("result.html", 
                            grouped_results=grouped_results.values(), 
                            user_id=uid)

@app.route("/restart")
def restart():
    session.pop("current_index", None)
    session.pop("q_start_time", None)
    return redirect(url_for("survey"))

if __name__ == "__main__":
    app.run(
        debug=os.getenv("DEBUG", "False"),
        port=int(os.getenv("PORT", 5000))
    )