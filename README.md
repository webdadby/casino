# Анализатор рулетки

Программа для анализа и предсказания чисел в рулетке на основе исторических данных.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Создайте файл `.env` и добавьте в него ваши учетные данные Supabase:
```
SUPABASE_URL=ваш_url
SUPABASE_KEY=ваш_ключ
```

3. Создайте таблицу в Supabase:
```sql
create table roulette_numbers (
  id bigint generated by default as identity primary key,
  number integer not null,
  color text not null,
  timestamp timestamp with time zone default timezone('utc'::text, now()) not null
);
```

## Использование

```python
from main import RouletteAnalyzer

# Создаем анализатор
analyzer = RouletteAnalyzer()

# Добавляем новое выпавшее число
analyzer.add_number(15)

# Получаем анализ
analysis = analyzer.analyze_patterns()

# Получаем предсказание следующего числа
predictions = analyzer.predict_next_number()
```

## Функциональность

- Сохранение истории выпавших чисел в Supabase
- Анализ "горячих" и "холодных" чисел
- Статистика по цветам
- Анализ вероятностей по секторам
- Предсказание следующего числа на основе исторических данных
