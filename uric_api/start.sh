#!/bin/bash

# 等待MySQL服务启动
echo "Waiting for MySQL to start..."
while ! nc -z mysql 3306; do
    sleep 1
done
echo "MySQL started"

# 等待Redis服务启动
echo "Waiting for Redis to start..."
while ! nc -z redis 6379; do
    sleep 1
done
echo "Redis started"

# 执行数据库迁移
echo "Applying database migrations..."
python manage.py migrate

# 创建超级用户（如果不存在）
echo "Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', '123456')
    print("Superuser created successfully")
else:
    print("Superuser already exists")
EOF

# 启动Django服务
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 