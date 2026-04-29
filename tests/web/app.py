import os
import time
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_session import Session
from data import listings_pool

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


# ---------------- ЛОГИКА ГЕНЕРАЦИИ ТЕСТА ----------------
def generate_test_flow():
    pool = listings_pool.copy()
    random.shuffle(pool)
    
    selected = pool[:18]
    styles = ["none"] * 6 + ["standard"] * 6 + ["custom"] * 6
    random.shuffle(styles)
    
    flow = []
    # 1. Инфо-страница
    flow.append({"type": "info", "code": "Кратко:\n\nТестирование в рамках ВКР, необходимо ответить на вопросы по листингам кода на языке программирования Python3, на страницу назад возвращаться нельзя.\n\nВсе ответы анонимизированы.\n\nРазвернуто:\n\nИНФОРМАЦИЯ ОБ ИССЛЕДОВАНИИ И СОГЛАСИЕ\n\nДанное исследование проводится в рамках подготовки выпускной квалификационной работы (ВКР) и направлено на изучение влияния различных способов визуализации программного кода на скорость его понимания и качество запоминания информации.\n\nПорядок проведения:\n    * Вам будет предложено проанализировать фрагменты кода на языке Python и ответить на вопросы по их структуре и результатам выполнения.\n    * В ходе тестирования фиксируется время решения, корректность ответов и технические параметры сессии.\n    * Важно, выполняйте задания последовательно, не используйте кнопку «Назад» в браузере.\n\nЮридическая информация и конфиденциальность:\n    1. Сбор данных осуществляется в анонимном виде. Исследование не предполагает сбор персональных данных, позволяющих идентифицировать вашу личность (ФИО, номер телефона, e-mail).\n\n    2. Для технического обеспечения процесса тестирования (сохранения текущего прогресса и идентификации сессии без привязки к личности) сайт использует файлы cookie и локальное хранилище.\n\n    3. Нажимая кнопку «Далее», Вы даете свое согласие на автоматизированную обработку предоставляемых вами данных (включая технические параметры сессии и использование файлов cookie) в соответствии с ФЗ №152-ФЗ «О персональных данных».\n\n    4. Все полученные результаты будут использованы исключительно в научных и исследовательских целях в обобщенном виде.\n\nПожалуйста, старайтесь отвечать максимально точно и работать в комфортном для вас темпе.\n\nНажимая кнопку «Далее», Вы подтверждаете ознакомление с правилами и даете согласие на участие в исследовании."})
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
        
        res = {
            "question_index": index,
            "listing_id": page.get("listing_id"),
            "category": page.get("category", "info"),
            "image": page.get("image") if page.get("type") == "question" else None,
            "images": page.get("images") if page.get("type") == "comparison" else None,
            "question_text": page.get("question", "Инфо"),
            "answer_text": final_ans,
            "correct_answer": page.get("correct", "N/A"),
            "time_taken": duration,
            "completed_at": datetime.now()
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
                time_taken=item["time_taken"],
                created_at=item.get("completed_at", datetime.now())
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
