# Coffee Recipes — Flask App ☕

## Кратко
**Coffee Recipes** — небольшой и аккуратный учебный проект на Flask: веб-интерфейс + REST API для обмена рецептами приготовления кофе.

- Учебная цель: понятная структура, авторизация, загрузка изображений, теги, лайки/сохранение рецептов.
- Подходит для локальной разработки и как основа для расширений.

---

## Основные возможности ✅
- CRUD для рецептов (REST API)
- Поиск по заголовку и фильтр по тегам
- Лайки и сохранение (save) рецептов
- Загрузка изображений для рецепта
- Регистрация / вход (Flask-Login)
- Swagger UI для работы с API (Flasgger)
- Набор базовых тестов (pytest)

---

## Быстрый старт (Windows PowerShell) 🚀
1) Создайте и активируйте виртуальное окружение:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) (Опционально) Создайте `.env` на основе `.env.example` и измените параметры (например, `SECRET_KEY`, `DATABASE_URL`, `FLASK_DEBUG`, `FLASK_RUN_PORT`).

3) Запустите приложение (автоматически создаст SQLite БД при первом запуске, если это указано в `DATABASE_URL`):

```powershell
python run.py
```

При успешном старте вы увидите в консоли строку вида:

```
Starting Coffee Recipes app on http://127.0.0.1:5000 (debug=False)
```

4) Откройте в браузере:
- Веб UI — http://127.0.0.1:5000/
- Swagger UI — http://127.0.0.1:5000/apidocs

---

## Тесты 🧪
Запуск:

```powershell
pytest -q
```

---

## Структура проекта 📁
- `run.py` — запуск приложения
- `requirements.txt` — зависимости
- `app/` — пакет приложения (модели, маршруты, шаблоны, статика)
- `tests/` — тесты (pytest)
- `swagger.yml` — OpenAPI спецификация

---

## Устранение проблем (Quick Troubleshooting)
- Убедитесь, что виртуальное окружение активировано
- Если сервер не запускается, проверьте, что у вас правильно введена команда `python run.py` (иногда в PowerShell случайно вводят похожие символы, например `сpython` с кириллической буквой "с").
- Для локальной разработки приложение автоматически создаст SQLite базу, если `DATABASE_URL` указывает на файл, которого ещё нет.

---

Если хотите — могу сократить README до минимума или добавить дополнительные примеры API-запросов и бейджи (badges).

---

## Deploy & connect a domain 🌐

Below are concise steps and options to deploy the app and connect a domain.

### Quick checklist
- Choose a hosting provider: VPS (DigitalOcean, Hetzner), PaaS (Render, Railway), or shared hosting.
- Ensure you have an IP address or hosting control panel where you can add a domain.
- Configure environment variables: `SECRET_KEY`, `DATABASE_URL`, and `FLASK_ENV`/`FLASK_DEBUG`.
- Set up TLS (Let's Encrypt) for HTTPS.

### Example: simple VPS + Nginx (recommended for control)
1. Provision a VM and install Python 3.10+, pip, and virtualenv.
2. Push project to the server (git clone) and create a virtualenv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Set environment variables (e.g. in systemd service file or export in a shell):
   - `SECRET_KEY`, `DATABASE_URL=sqlite:////path/to/app.db` (or a production DB URI)
4. Run the app with Gunicorn behind Nginx:
   ```bash
   gunicorn -w 3 -b 127.0.0.1:8000 run:app
   ```
5. Configure Nginx as a reverse proxy and set server_name to your domain. Example snippet:
   ```nginx
   server {
     listen 80;
     server_name example.com www.example.com;

     location /static/ {
       alias /path/to/your/project/app/static/;
     }

     location / {
       proxy_pass http://127.0.0.1:8000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
     }
   }
   ```
6. Enable HTTPS with Certbot (Let's Encrypt) or a provider-managed certificate.

### Example: Render / Heroku / Railway (easier)
- Create a new web service, connect your Git repository, set build and run commands (e.g. `gunicorn run:app`).
- Add environment variables in the service settings (`SECRET_KEY`, `DATABASE_URL`).
- Add the domain in the platform UI and follow their DNS instructions (usually CNAME or A record).
- Platforms typically manage TLS automatically.

### DNS notes
- To point your domain to a server, add an **A** record (domain root) pointing to the server IP, and a **CNAME** for subdomains to the service hostname when required.
- TTL edits may take a few minutes to propagate, sometimes hours.

### Final checklist
- App runs under a process manager (systemd or platform-managed service).
- Nginx (or platform) serves static files and proxies dynamic requests.
- TLS certificate is valid and auto-renewing (Let's Encrypt + Certbot or platform-managed).
- Environment variables are set and secret values are not committed to the repo.

If you'd like, I can add a `deploy.md` with an example systemd unit file and an Nginx config tailored to this project, or scaffold a `Dockerfile`+`docker-compose.yml` for container deployment.