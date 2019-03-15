启动手顺
# linux
1. 使用适当的python
source py36env/bin/activate
2. 使用数据库及表单
python manage.py db migrate
python manage.py db upgrade

3. 在数据库执行下面脚本，生成view
lastest_man_day_id.sql

4. 启动Flask服务器
python start.py