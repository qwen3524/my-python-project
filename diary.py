class DiaryEntry:
    # __init__ - это Конструктор. Он запускается, когда мы создаем новый объект.
    # self - это ссылка на КОНКРЕТНЫЙ объект (конкретное печенье), который создается прямо сейчас.
    def __init__(self, date: str, mood: int, notes: str):
        self.date = date  # Мы сохраняем данные ВНУТРИ объекта
        self.mood = mood
        self.notes = notes

    # Метод - это функция внутри класса. Она умеет работать с данными объекта (self).
    def to_dict(self) -> dict:
        """Превращает объект обратно в словарь для сохранения в JSON."""
        return {
            "date": self.date,
            "mood": self.mood,
            "notes": self.notes,
        }


import json
from pathlib import Path
from typing import List

# ... (тут ваш класс DiaryEntry)


class DiaryManager:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.entries: List[DiaryEntry] = []  # Список хранит ОБЪЕКТЫ, а не словари
        self._load()  # Автоматически загружаем при старте

    def _load(self):
        """Внутренний (приватный) метод загрузки."""
        if not self.file_path.exists():
            return
        try:
            data = json.loads(self.file_path.read_text(encoding="utf-8"))
            # МАГИЯ ООП: Мы превращаем сырые словари (dict) в умные объекты (DiaryEntry)
            # Использование list comprehension (генератора списка)
            self.entries = [DiaryEntry(d["date"], d["mood"], d["notes"]) for d in data]
        except (json.JSONDecodeError, KeyError):
            self.entries = []

    def save(self):
        """Сохранение всех записей."""
        # Превращаем объекты обратно в словари для JSON
        data_to_save = [entry.to_dict() for entry in self.entries]
        self.file_path.write_text(
            json.dumps(data_to_save, indent=4, ensure_ascii=False), encoding="utf-8"
        )

    def add_entry(self, date: str, mood: int, notes: str):
        """Создает запись и сразу сохраняет."""
        new_entry = DiaryEntry(date, mood, notes)
        self.entries.append(new_entry)
        self.save()

    def get_average_mood(self) -> float:
        """Аналитика инкапсулирована внутри менеджера."""
        if not self.entries:
            return 0.0
        total = sum(entry.mood for entry in self.entries)
        return total / len(self.entries)
