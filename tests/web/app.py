from flask import Flask, render_template, request, redirect, session, url_for
import time

app = Flask(__name__)
# app.secret_key = "secret_key_123"

# ---------------- ДАННЫЕ ----------------
questions = [
    {
        "code": """Кратко:\nТестирование в рамках ВКР, необходимо ответить на вопросы по листингам кода, на страницу назад возвращаться нельзя.
        
Все ответы анонимизированны.

Развернуто:
В рамках данного исследования изучается влияние различных способов визуализации программного кода на скорость его понимания и качество запоминания информации.
Вам будет предложено выполнить несколько заданий, связанных с анализом небольших фрагментов кода на языке Python.
Задания предполагают определение результатов выполнения кода и ответы на вопросы по его структуре.
В ходе выполнения фиксируется время решения и корректность ответов. Важно выполнять задания последовательно и не возвращаться к предыдущим вопросам.
После завершения основной части будет предложен небольшой блок вопросов на запоминание, направленный на оценку того, какая информация сохранилась после работы с кодом.
Пожалуйста, старайтесь отвечать максимально точно и работать в комфортном для вас темпе.
Полученные данные будут использованы исключительно в исследовательских целях в рамках выпускной квалификационной работы."""
    },
    {   
        "code": "Укажите ваш курс или должность.\n",
        "questions": [
            "Для студентов номер курса, для работников грейд(джуниор, мидл, синьор)"
        ]
    },
    {
        "image": "que1.png",
        "code": "Запомните код, на следующих страницах Вас ждут небольшие вопросы по коду"
    },
    {
        "questions": [
            "1. Какое значение имеет переменная z?"
        ]
    },
    {
        "questions": [
            "2. Какая переменная используется для вычисления y?"
        ]
    }
    # {
    #     "code": "def square(n): return n*n",
    #     "questions": [
    #         "1. Что возвращает square(4)?",
    #         "2. Назовите переменную внутри функции."
    #     ]
    # }
]

# ---------------- Состояние сессии ----------------
survey_state = {
    "start_time": None,
    "user_id": None,
    "answers": [],
    "timestamps": []
}

# ---------------- Роуты ----------------
@app.route("/", methods=["GET", "POST"])
def survey():
    global user
    index = len(survey_state["answers"])

    # Если опрос только начинается, создаем user_id
    if survey_state["start_time"] is None:
        survey_state["start_time"] = time.time()
        survey_state["user_id"] = int(time.time() * 1000)
        user = survey_state["user_id"]
        print(f"User ID: {survey_state['user_id']}")

    # Инициализируем время начала вопроса, если это первый раз на странице
    if "question_start_time" not in survey_state:
        survey_state["question_start_time"] = time.time()

    if request.method == "POST":
        current_q = questions[index]
        user_answers = []

        for i, qtext in enumerate(current_q.get("questions", [])):
            ans = request.form.get(f"answer_{i}", "").strip()
            if not ans:
                return render_template("survey.html", question=current_q, index=index, error="Ответ обязателен")
            user_answers.append(ans)

        # Время прохождения текущего вопроса
        time_for_question = time.time() - survey_state["question_start_time"]
        survey_state["answers"].append(user_answers)
        survey_state["timestamps"].append(time_for_question)

        index += 1
        if index >= len(questions):
            return redirect(url_for("finish"))

        # Обновляем время начала следующего вопроса
        survey_state["question_start_time"] = time.time()

    if index < len(questions):
        return render_template("survey.html", question=questions[index], index=index, error=None)
    else:
        return redirect(url_for("finish"))

@app.route("/finish")
def finish():
    results = []
    for i, q in enumerate(questions):
        ans_list = survey_state["answers"][i] if i < len(survey_state["answers"]) else []
        q_texts = q.get("questions", ["(Только текст/изображение)"])
        # Составляем список кортежей (вопрос, ответ)
        qa_pairs = list(zip(q_texts, ans_list + ["(нет)"]*len(q_texts)))
        results.append({
            "assignment": i + 1,
            "code": q.get("code", ""),
            "image": q.get("image", ""),
            "qa_pairs": qa_pairs,
            "time": survey_state["timestamps"][i] if i < len(survey_state["timestamps"]) else 0
        })
    return render_template("result.html", results=results, user_id=survey_state["user_id"])

# ---------------- Запуск ----------------
if __name__ == "__main__":
    # Для доступа через интернет: host="0.0.0.0"
    app.run(debug=True, host="0.0.0.0", port=5000)

# Running on http://127.0.0.1:5000
# Running on http://192.168.31.99:5000