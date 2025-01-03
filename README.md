# 效果展示
![image](https://github.com/user-attachments/assets/1b88a0a7-385e-47dc-a9e4-92848c0d6951)
![image](https://github.com/user-attachments/assets/f6b009df-908b-415e-9362-4b24a67173a4)
![image](https://github.com/user-attachments/assets/175b4103-802b-41f8-857c-f286b6d9bb92)
![image](https://github.com/user-attachments/assets/474f658b-a47c-4541-a3b9-fb6eb11f1a2c)
![image](https://github.com/user-attachments/assets/289d14a5-f0a6-4b49-87e6-8dabca633067)
![image](https://github.com/user-attachments/assets/428a1881-8a23-4782-9ce4-afbe1e439458)
![image](https://github.com/user-attachments/assets/58767848-555c-431f-9086-b159f3522889)
# 部署过程

部署前准备

```
# 在服务器上创建项目目录
mkdir -p /opt/uric/logs
cd /opt/uric

# 确保目录权限正确
chown -R root:root /opt/uric
chmod -R 755 /opt/uric
chmod -R 777 /opt/uric/logs
```

启动前检查

```
cd /opt/uric

# 检查 Docker 和 Docker Compose 是否安装
docker --version
docker-compose --version

# 如果没有安装，需要先安装：
curl -fsSL https://get.docker.com | bash -s docker
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

启动服务

```
# 构建并启动所有服务
docker-compose up -d --build

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

验证部署

```
# 检查端口是否正常监听
netstat -tunlp | grep -E '8080'

# 检查容器日志
docker-compose logs backend
docker-compose logs frontend
```

数据库初始化检查

```
# 进入后端容器
docker-compose exec backend bash

# 检查数据库迁移
python manage.py showmigrations

# 如果需要，手动创建超级用户
python manage.py createsuperuser
```

安全检查

```
# 检查防火墙规则
firewall-cmd --list-all

# 检查端口是否可访问（在其他机器上执行）
telnet 47.99.160.215 8080
telnet 47.99.160.215 8000
```

备份策略

```
# 创建备份目录
mkdir -p /opt/uric/backups

# 数据库备份脚本（可以添加到 crontab）
docker-compose exec mysql mysqldump -u root -p123456 uric > /opt/uric/backups/uric_$(date +%Y%m%d).sql
```

故障恢复流程

```
# 如果服务出现问题，可以重启：
docker-compose restart

# 如果需要完全重建：
docker-compose down
docker-compose up -d --build

# 如果需要清理数据重来：
docker-compose down -v  # 注意：这会删除所有数据
```

