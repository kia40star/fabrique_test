# fabrique_test
Django-DRF

## Установка и запуск:
- docker-compose up -d --build db 
- Дождаться инициализации Postgres
- docker-compose up -d --build web

http://127.0.0.1:8000/

## Описание API:
### Доступно всем
    [POST] "login": "login/" 
        {
            "username": "",
            "password": ""
        }
    [GET] "logout": "logout/"
    
    [GET/POST]"polls": "polls/{id}/questions/{id}/answer/"
        {
            "choices": [] | "choice": id:int | "choice_text": ""
        }
    
### Только для администратора:
    [GET/POST] "polls": "polls/{id}"
        {
            "title": "",
            "started_at": null,
            "finish_at": null,
            "description": "",
            "questions": [],
            "is_active": false
        }
        
    [GET/POST] "questions": "questions/{id}"
        {
            "title": "",
            "question_type": null,
            "choices": [],
            "is_active": false
        }
        
    [GET/POST] "choices": "choices/{id}"
        {
            "questions": [],
            "title": ""
        }
        
    [GET] "answers": "answers/{id}"
        
        
