# Исследование влияния методов визуализации программного кода на его понимание (ВКР)

Данный репозиторий содержит программный комплекс, разработанный в рамках выпускной квалификационной работы. Проект состоит из двух ключевых компонентов:
1. **VS Code Extension (vkr-golodyaev)**: Инструмент семантической подсветки синтаксиса Python.
2. **Веб-платформа для тестирования**: Платформа для проведения экспериментов и сбора метрик понимания кода.

---

## Часть 1: VS Code расширение (vkr-golodyaev)

Расширение реализует кастомную семантическую подсветку (Semantic Highlighting) для языка Python, используя собственный парсер и анализатор областей видимости.

### Основные возможности
* **Семантический анализ**: Различение функций, переменных, параметров и литералов.
* **Учет областей видимости**: Корректное определение локальных параметров функций и глобальных переменных.
* **Кастомная тема**: Специально разработанная цветовая схема "VKR Python Colors" для снижения когнитивной нагрузки.
* **Встроенные команды**:
    * `Hello World`: Проверка активации расширения.
    * `Show Current File`: Вывод пути к текущему рабочему файлу.

### Запуск и разработка расширения
Для работы требуется **Node.js** (рекомендуемая версия 20+) и **VS Code**.

1. **Установка зависимостей**:
   ```shell
   npm install
   ```
   Если не сработает, то необходимо скачать Node.js с официального сайта https://nodejs.org/en
    > Во время установки убедитесь, что галочка "Add to PATH" включена.
2. **Компиляция исходного кода**:
   ```shell
   npm run compile
   ```

3. **Запуск**:
   * Откройте папку проекта в VS Code (`code .`).
   * Нажмите `F5` для запуска окна "Extension Development Host".
   * В открывшемся окне откройте любой `.py` файл для проверки подсветки.

### Структура проекта

* **Корень проекта**: Исходный код расширения VS Code (`extension.ts`, `parser.ts`, `analyzer.ts`, `provider.ts`).
* **package.json**: Манифест расширения, описание вкладов (contributes) и семантических токенов.
* **themes/**: Описание цветовой темы `vkr-python-color-theme.json`.
---

## Часть 2: Веб-платформа для тестирования

Платформа предназначена для проведения исследования: респондентам предлагаются различные варианты визуализации кода, а система фиксирует скорость и точность их ответов.

### Технологический стек
* Backend: Python 3.x, Flask.
* Database: SQLite + SQLAlchemy (ORM).
* Frontend: HTML5, Jinja2, CSS3 (адаптивная верстка).

### Быстрый локальный запуск веб-платформы
1. **Установка Python-пакетов**:
   ```bash
   pip install flask flask_sqlalchemy python-dotenv
   ```
2. **Настройка окружения**:
   Создайте файл `.env` в папке веб-приложения:
   ```text
   SECRET_KEY=<необходимо указать ключ>
   DATABASE_URL=sqlite:///<название файла бд>.db
   DEBUG=False
   PORT=5000
   ```
3. **Запуск сервера**:
   ```bash
   python app.py
   ```
   Интерфейс будет доступен по адресу: `http://127.0.0.1:5000`.

### Развертывание веб-платформы на Apache (mod_wsgi)

1. **Установка системных пакетов**:
   Обновите индекс пакетов и установите веб-сервер Apache с модулем WSGI:
   ```bash
   sudo apt update
   sudo apt install apache2 libapache2-mod-wsgi-py3 python3-venv python3-full
   ```
   Стяните репозиторий, также необходимо дать вашему пользователю права на папку /var/www
   ```
   sudo chown $USER:$USER /var/www
   cd /var/www/
   git clone git@github.com:gemcheck/vkr-golodyaev.git
   ```

2. **Настройка конфигурации Apache**:
   Откройте файл конфигурации сайта:
   ```bash
   sudo nano /etc/apache2/sites-available/000-default.conf
   ```
   Замените содержимое или добавьте следующую конфигурацию:
   ```apache
   <VirtualHost *:80>
       ServerName <укажите адрес>

       # WSGI настройки: пути к проекту и виртуальному окружению
       WSGIDaemonProcess my_survey python-path=/var/www/vkr-golodyaev/tests/web/.venv
       WSGIProcessGroup my_survey
       WSGIScriptAlias / /var/www/vkr-golodyaev/tests/web/app.wsgi

       <Directory /var/www/vkr-golodyaev/tests/web>
           Require all granted
       </Directory>

       # Настройка статических файлов
       Alias /static /var/www/vkr-golodyaev/tests/web/static
       <Directory /var/www/vkr-golodyaev/tests/web/static/>
           Require all granted
       </Directory>

       ErrorLog ${APACHE_LOG_DIR}/survey_error.log
       CustomLog ${APACHE_LOG_DIR}/survey_access.log combined
   </VirtualHost>
   ```

3. **Подготовка окружения и зависимостей**:
   Создайте виртуальное окружение и установите необходимые библиотеки:
   ```bash
   cd /var/www/vkr-golodyaev/tests/web
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r req.txt
   ```

4. **Настройка переменных окружения**:
   Создайте файл `.env` для хранения секретов:
   ```bash
   sudo nano .env
   ```
   Пример содержания:
   ```text
   SECRET_KEY=<необходимо указать ключ>
   DATABASE_URL=sqlite:///<название файла бд>.db
   DEBUG=False
   PORT=5000
   ```

5. **Настройка прав доступа**:
   Для корректной работы Apache с базой данных SQLite необходимо настроить права:
   ```bash
   # Права на чтение для папки проекта
   sudo chmod -R 755 /var/www/vkr-golodyaev/tests/web

   # Права на запись для базы данных и папки instance
   cd /var/www/vkr-golodyaev/tests/web/instance/
   sudo chown golodyaev:www-data survey.db .
   sudo chmod 664 survey.db
   sudo chmod 775 .
   ```

6. **Запуск сервера**:
   Активируйте конфигурацию и перезапустите Apache:
   ```bash
   sudo a2ensite 000-default.conf
   sudo systemctl restart apache2
   ```

#### Дополнительно: Копирование БД на локальную машину
Для загрузки файла базы данных с сервера на локальный компьютер (Windows) используйте:
```powershell
scp -i .\cloud <логин>@<адрес сервера>:/var/www/vkr-golodyaev/tests/web/instance/survey.db C:\Users\<пользователь>\Downloads\
```

### Структура проекта

* **tests/web/** (или ваш путь):
    * `app.py` — серверная логика и модели данных.
    * `templates/` — шаблоны страниц (опрос, результаты).
    * `static/` — графические стимулы (скриншоты кода для тестов).
    * `instance/` — папка с базой данных.

---

### Методология сбора данных

Система автоматически аккумулирует данные в таблице `Response` для последующего статистического анализа:
* **Анонимная идентификация**: Привязка ответов к `user_id` сессии.
* **Когнитивные метрики**: Замер `time_taken` (время в секундах между загрузкой задания и отправкой ответа).
* **Качество понимания**: Сверка `answer_text` с `correct_answer`.
* **Контекст**: Хранение индекса вопроса и текста задания для анализа сложности алгоритмов.

## Лицензия и использование
Разработано исключительно в учебных и научно-исследовательских целях в рамках подготовки ВКР.