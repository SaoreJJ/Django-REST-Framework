import os

os.makedirs('.github/workflows', exist_ok=True)

workflow = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, feature/task-01 ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    env:
      SECRET_KEY: test-secret-key
      DEBUG: "True"
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
      DB_HOST: localhost
      DB_PORT: 5432
      REDIS_HOST: localhost
      REDIS_PORT: 6379

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: python manage.py test

  lint:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install flake8
        run: pip install flake8

      - name: Lint with flake8
        run: flake8 . --count --max-line-length=127 --statistics --exclude=migrations,venv,.venv,.git

  build:
    runs-on: ubuntu-latest
    needs: lint
    if: github.event_name == 'push'
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/drf-learning:latest

  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'push'
    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /opt/drf-project
            if [ -d ".git" ]; then
              git pull origin feature/task-01
            else
              git clone -b feature/task-01 https://github.com/SaoreJJ/Django-REST-Framework.git .
            fi
            echo "${{ secrets.ENV_FILE }}" > .env
            docker compose down
            docker compose up -d --build
            docker compose exec -T app python manage.py migrate
            docker compose exec -T app python manage.py collectstatic --noinput
"""

with open('.github/workflows/ci-cd.yml', 'w') as f:
    f.write(workflow)

print("Workflow создан для ветки feature/task-01!")