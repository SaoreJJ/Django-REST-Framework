workflow = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, feture/task-01 ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
        ports:
          - 5432:5432
      redis:
        image: redis:7
        ports:
          - 6379:6379
    env:
      SECRET_KEY: test-key
      DEBUG: "True"
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
      DB_HOST: localhost
      DB_PORT: 5432
      REDIS_HOST: localhost
      REDIS_PORT: 6379
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run migrations
        run: python manage.py migrate
      - name: Run tests
        run: python manage.py test

  lint:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install flake8
        run: pip install flake8
      - name: Lint with flake8
        run: flake8 . --count --max-line-length=127 --exclude=migrations,venv,.venv,.git --exit-zero

  build:
    runs-on: ubuntu-latest
    needs: lint
    if: github.event_name == 'push'
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - uses: docker/build-push-action@v5
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
            git pull origin feture/task-01
            echo "${{ secrets.ENV_FILE }}" > .env
            docker compose down
            docker compose up -d --build
            docker compose exec -T app python manage.py migrate
            docker compose exec -T app python manage.py collectstatic --noinput
"""

with open('.github/workflows/ci-cd.yml', 'w') as f:
    f.write(workflow)

