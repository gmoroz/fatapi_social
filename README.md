## Запуск приложения

    git clone https://github.com/gmoroz/fatapi_social
    cd fatapi_social
    docker-compose up --build -d

root url приложения: `localhost:8000`

## Документация

Можно посмотреть по адресу `localhost:8000/docs`
Или ниже:

## Эндпоинты для пользователей

| Эндпоинт       | Метод | Описание                                      | Аутентификация |
| -------------- | ----- | --------------------------------------------- | -------------- |
| /register      | POST  | Регистрация нового пользователя               | Нет            |
| /login         | POST  | Получение JWT токена по данным аутентификации | Multipart Form |
| /refresh-token | POST  | Обновление JWT токена                         | JWT токен      |

## Эндпоинты для постов:

| Эндпоинт                 | Метод  | Описание                              | Аутентификация |
| ------------------------ | ------ | ------------------------------------- | -------------- |
| /posts                   | POST   | Создать новый пост                    | JWT токен      |
| /posts/{post_id}         | GET    | Получить пост по его id               | Нет            |
| /posts/{post_id}         | PUT    | Обновить информацию о посте по его id | JWT токен      |
| /posts/{post_id}         | DELETE | Удалить пост по его id                | JWT токен      |
| /posts/{post_id}/like    | POST   | Поставить лайк посту по его id        | JWT токен      |
| /posts/{post_id}/dislike | POST   | Поставить дизлайк посту по его id     | JWT токен      |

Схема базы данных:

![Схема бд](https://i.ibb.co/wR7nWn5/db-diagram.png)
