# Инструкция по настройке и запуску проекта на сервере

## Шаг 1: Установка Git

```bash
sudo apt update
sudo apt install git
```

---

## Шаг 2: Установка Python и активация последней версии

1. Обновляем список пакетов:

```bash
sudo apt update
```

2. Устанавливаем зависимости:

```bash
sudo apt install software-properties-common
```

3. Добавляем репозиторий с последними версиями Python:

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
```

4. Устанавливаем последнюю стабильную версию Python (например, 3.11):

```bash
sudo apt install python3.11 python3.11-venv python3.11-dev python3.11-distutils
```

5. Проверяем установленную версию:

```bash
python3.11 --version
```



## Шаг 3: Установка Docker и Docker Compose

1. Устанавливаем Docker:

```bash
curl -sSL https://get.docker.com/ | sh
```

2. Устанавливаем Docker Compose:

```bash
sudo curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

```

3. Проверяем установки:

```bash
docker --version
docker-compose --version
```

---

## Шаг 4: Создание папки с проектом

```bash
mkdir my_project
cd my_project
```

---

## Шаг 5: Клонирование проекта из GitHub

```bash
git clone <URL_РЕПОЗИТОРИЯ>
```

---

## Шаг 6: Добавление файла `.env`

Создаём файл `.env` и добавляем в него переменные окружения:

```bash
nano .env
```

Пример содержимого файла `.env`:
```
PRIVATE_KEY=
PUBLIC_KEY=

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
DATABASE_URL=
```

Сохраняем файл: `Ctrl + O`, выходим: `Ctrl + X`.

---

## Шаг 7: Создание и активация виртуального окружения (venv)

1. Создаём виртуальное окружение:

```bash
python3.11 -m venv venv
```

2. Активируем его:

```bash
source venv/bin/activate
```

---

## Шаг 8: Сборка и запуск Docker Compose

1. Собираем контейнеры:

```bash
docker-compose build
```

2. Запускаем контейнеры:

```bash
docker-compose up -d
```

3. Проверяем работающие контейнеры:

```bash
docker ps
```

---

## Шаг 9: Готово!

Проект успешно запущен и доступен для использования.
