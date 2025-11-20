# main.py
from pathlib import Path

from diary import DiaryManager  # Импортируем наши классы


def get_valid_mood() -> int:
    """Вспомогательная функция для валидации ввода (оставляем процедурной)."""
    while True:
        try:
            val = int(input("Настроение (1-5): "))
            if 1 <= val <= 5:
                return val
            print("Число должно быть от 1 до 5.")
        except ValueError:
            print("Введите целое число.")


def main():
    print("--- СУЦН v0.5 (ООП Версия) ---")

    # 1. Инициализация
    # Мы просто говорим менеджеру, где файл. Он сам загрузит данные.
    manager = DiaryManager(Path("diary.json"))

    print(f"Загружено записей: {len(manager.entries)}")

    # 2. Цикл работы
    while True:
        date = input("\nВведите дату (или 'stop'): ")
        if date == "stop":
            break

        mood = get_valid_mood()
        notes = input("Заметки: ")

        # 3. Делегирование
        # Main не знает, как сохранять. Он просто просит менеджера "добавить".
        manager.add_entry(date, mood, notes)
        print("Запись добавлена!")

    # 4. Аналитика
    avg = manager.get_average_mood()
    print(f"\nСреднее настроение: {avg:.2f}")


if __name__ == "__main__":
    main()
