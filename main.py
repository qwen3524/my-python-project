# main.py
import json  # <- Импортируем JSON
from pathlib import Path  # <- Импортируем pathlib

# --- БЛОК 0: КОНСТАНТЫ ---
# Определяем "имя" нашего файла данных.
# Path() создает объект пути.
DATA_FILE = Path("diary.json")
# --- БЛОК 1: ОПРЕДЕЛЕНИЕ ИНСТРУМЕНТОВ (ФУНКЦИЙ) ---


def load_entries(path: Path) -> list:
    """
    (Инструмент 0 - НОВЫЙ)
    Загружает записи из файла 'path'.
    Возвращает список словарей.
    """
    if not path.exists():
        return []  # Если файла нет, возвращаем пустой список
    try:
        # (Навык Дня 5) Используем .read_text() - шорткат pathlib
        json_data = path.read_text(encoding="utf-8")
        # (Навык Дня 5) Используем json.loads() для парсинга строки
        entries = json.loads(json_data)
        return entries
    except json.JSONDecodeError:
        # (Навык Дня 3) Если файл есть, но он "битый" (не JSON)
        print(f"Ошибка: Не удалось прочитать{path}. Создан новый дневник.")
        return []


def save_entries(path: Path, entries: list) -> None:
    """
    (Инструмент 1 - НОВЫЙ)
    Сохраняет список 'entries' в файл 'path'.
    """
    # (Навык Дня 5) Используем json.dumps() для превращения списка в строку
    # indent=4 делает JSON "красивым" (с отступами)
    json_data = json.dumps(entries, indent=4, ensure_ascii=False)
    # (Навык Дня 5) Используем .write_text() - шорткат pathlib
    path.write_text(json_data, encoding="utf-8")


def get_mood_input() -> int:
    """
    (Инструмент 2 - из Дня 4)
    Запрашивает настроение, пока ввод не станет корректным.
    """
    while True:
        mood_str = input("Настроение (1-5):")
        try:
            mood_int = int(mood_str)
            if 1 <= mood_int <= 5:
                return mood_int
            else:
                print("Ошибка: Настроение должно быть от 1 до 5.")
        except ValueError:
            print("Ошибка: Введите, пожалуйста, ЧИСЛО (1, 2, 3, 4 или 5).")


def analize_entries(entries: list) -> None:
    """
    (Инструмент 3 - из Дня 4)
    Принимает список, печатает анализ.
    """
    if not entries:
        print("\nВы не сделали ни одной записи. Анализировать нечего.")
        return
    print("\n===============================")
    print("Анализ Вашего Дневника:")
    total_entries = len(entries)
    print(f"Всего записей:{total_entries}")
    total_mood = sum(entry["mood"] for entry in entries)  # (Более 'питоничный' способ)
    average_mood = total_mood / total_entries
    print(f"Среднее настроение:{average_mood:.1f}/5")


# --- БЛОК 2: ГЛАВНАЯ ЛОГИКА (ДИРИЖЕР) ---
def main():
    """
    (Дирижер - из Дня 4)
    Главная функция, которая запускает программу.
    """
    print("--- Система Учета Настроения (СУЦН) v0.4 ---")
    print("Введите 'stop' в поле 'дата', чтобы закончить и получить анализ.")
    # --- ИЗМЕНЕНИЕ ДНЯ 5 ---
    # Мы больше не создаем пустой список.
    # Мы ЗАГРУЖАЕМ его из файла!
    diary_entries = load_entries(DATA_FILE)

    while True:
        date = input("\nДата (гггг-мм-дд):")
        if date == "stop":
            break

        mood = get_mood_input()
        notes = input("Заметки: ")

        entry = {
            "date": date,
            "mood": mood,
            "notes": notes,
        }
        diary_entries.append(entry)

        # --- ИЗМЕНЕНИЕ ДНЯ 5 ---
        # Сразу ПОСЛЕ добавления в список,
        # мы СОХРАНЯЕМ ВЕСЬ список обратно в файл.
        save_entries(DATA_FILE, diary_entries)
        print("--- Запись добавлена и СОХРАНЕНА! ---")
        # Анализ работает как и раньше,
    # но теперь он анализирует ВСЕ записи
    analize_entries(diary_entries)
    print("\n--- Работа программы завершена. ---")


# --- БЛОК 3: ТОЧКА ВХОДА ---
if __name__ == "__main__":
    main()
