Запуск проекта:

1. Клонировать репозиторий и зайти в него  
    git clone https://github.com/Tisot-studio/simple-blog-app.git
    cd simple-blog-app


2. Создать виртуальное окружение и запустить его, например: 
    python -m venv testenv 

    # Windows
    testenv\Scripts\activate
    # Linux and Mac
    source testenv/bin/activate

3. Установить все необходимые пакеты:  
    pip install -r requirements.txt


4. В файле settings.py настроить отправку электронной почты приложения, используется gmail как хост. 
    EMAIL_HOST_USER = 'электронный_адрес'
    EMAIL_HOST_PASSWORD = 'пароль'


5. Создать БД и администратора  
    python manage.py migrate
    python manage.py createsuperuser


6. Запустить сервер
    python manage.py runserver

7. Через администратора создать несколько пользователей, указать для них электронные почты, куда будут приходить оповещения о новых постах в блогах на которые они подписаны

8. Можно создавать посты через админку либо через личный кабинет

