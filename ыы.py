workflow = """name: Deploy Only

on:
  push:
    branches: [ deploy-trigger ]

jobs:
  deploy:
    runs-on: ubuntu-latest
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

with open('.github/workflows/deploy.yml', 'w') as f:
    f.write(workflow)

print("Создан deploy workflow. Выполни:")
print("git add .")
print("git commit -m 'Add deploy trigger'")
print("git push origin feture/task-01")
print("")
print("Затем:")
print("git checkout -b deploy-trigger")
print("git push origin deploy-trigger")