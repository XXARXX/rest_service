## иструкция:

из каталога проекта выполнить в командной строке

1. python -m venv venv
2. ./venv/Scripts/activate
2. python -m pip install -r requirements.txt
3. python run\.py config -b {директория-поиска-файлов}
4. python run\.py server [-ip] [-p]


## команды:

* Создание конфига: python run\.py config -b {директория-поиска-файлов}

    Файл 'config.xml' будет создан в рабочем каталоге программы с корректно заполненной структурой

* Помощь: python run\.py {server, config} -h

* Запуск сервера в тестовом режиме: python run\.py server -d [-ip] [-p]

* Запуск сервера в обычном режиме: python run\.py server [-ip] [-p]

    Сервер может вызвать ошибку в случае не существующего пути до директории поиска файлов
    или в случае если конфиг заполнен не правильно

* Запуск тестов: python -m unittest

* Добавлен опциональный параметр запроса ashtml для переноса строк в вэб браузерe (просто оборачивает строки в \<p>\</p> тэги).

    > Пример: /api/show_file_content?filename=file&filter=00:03&ashtml=1