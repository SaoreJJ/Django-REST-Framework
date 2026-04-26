# Проект онлайн-обучения

## Запуск

1. Клонировать репозиторий
2. `cp .env.example .env` и заполнить SECRET_KEY и пароли
3. `docker-compose up -d --build`
4. `docker-compose exec app python manage.py createsuperuser`
5. Открыть http://localhost

## Команды

- Логи: `docker-compose logs -f`
- Остановить: `docker-compose down`
