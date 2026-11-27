# 🎓 Student Dashboard (Личный трекер учебы)

![Django](https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge&logo=django)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap)

**Student Dashboard** — это полноценное веб-приложение для студентов, позволяющее централизованно управлять своим учебным процессом. Проект упакован в Docker-контейнеры и готов к развертыванию.

## ✨ Основные возможности

*   **📊 Умный дашборд:** Отслеживание текущего GPA, активных заданий, ближайших дедлайнов и статистики времени учебы с помощью интерактивных графиков (Chart.js).
*   **📚 Управление курсами:** Добавление курсов, привязка преподавателей, цветовая индикация успеваемости.
*   **📦 Архив курсов:** Возможность скрывать завершенные семестры в архив (Soft Delete), сохраняя историю оценок.
*   **📝 Трекер заданий:** Создание задач, смена статусов (Todo/Doing/Done), выставление оценок и ведение истории выполнения через комментарии.
*   **🗓 Расписание:** Просмотр пар по дням недели с указанием аудиторий (офлайн) или ссылок на подключение (онлайн).
*   **👨‍🏫 База преподавателей:** Список преподавателей и закрепленных за ними курсов.
*   **🎯 Подбор курса:** Интерактивный опросник, который рекомендует курсы на основе выбранных студентом критериев (тегов).
*   **👤 Профиль пользователя:** Личный кабинет со статистикой (дата регистрации, пройденные курсы) и формой смены пароля.

## 🐳 Запуск проекта (Docker)

Для запуска проекта вам понадобятся **Docker** и **Docker Compose**.

1. **Клонируйте репозиторий:**
   git clone https://github.com/MyEp1cFa1l/student-dashboard.git
   cd student-dashboard

2. **Создайте файл .env в корневой папке:**
Вам нужно создать файл .env (он есть в .gitignore для безопасности) и добавить туда настройки базы данных:
   Пример содержимого .env
     DEBUG=1
     SECRET_KEY=ваш_секретный_ключ_django
     POSTGRES_DB=students_db
     POSTGRES_USER=students_user
     POSTGRES_PASSWORD=students_password

3. **Соберите и запустите контейнеры:**
   docker compose up --build -d

4. **Примените миграции (создайте таблицы в базе):**
  docker compose exec web python manage.py migrate

5. **Создайте суперпользователя для доступа в админку:**
  docker compose exec web python manage.py createsuperuser

6. **Готово! Перейдите по адресу http://localhost:8000.**

## 🛠 Технологический стек
**Backend:** Python 3.12, Django 6.1, Django ORM
**Database:** PostgreSQL 16
**Frontend:** HTML5, CSS3, Bootstrap 5, Chart.js, JavaScript
**Infrastructure:** Docker, Docker Compose, Gunicorn
**Безопасность:** Окружение на основе переменных .env, встроенная аутентификация Django.
