readme = """# Платформа онлайн-обучения (DRF)

REST API для платформы онлайн-обучения на Django REST Framework с автоматическим CI/CD и деплоем на сервер.

## Технологический стек

- **Backend:** Python 3.11, Django 4.2, Django REST Framework
- **База данных:** PostgreSQL 15
- **Кеш/Брокер:** Redis 7
- **Фоновые задачи:** Celery
- **Web-сервер:** Nginx + Gunicorn
- **Контейнеризация:** Docker, Docker Compose
- **CI/CD:** GitHub Actions

## Структура сервисов

| Сервис | Технология | Внутренний порт | Внешний порт |
|--------|------------|-----------------|--------------|
| app | Django + Gunicorn | 8000 | - |
| db | PostgreSQL 15 | 5432 | - |
| redis | Redis 7 | 6379 | - |
| celery | Celery worker | - | - |
| nginx | Nginx | 80 | 80 |

## Быстрый старт (локально)

### Предварительные требования

- Docker и Docker Compose
- Git

### 1. Клонирование репозитория

```bash
git clone https://github.com/SaoreJJ/Django-REST-Framework.git
cd Django-REST-Framework
