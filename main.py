from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime
from database import save_number, get_last_numbers

app = Flask(__name__)
CORS(app)

# Словарь с цветами чисел в рулетке
ROULETTE_COLORS = {
    0: 'green',
    **{num: 'red' if num in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36] else 'black' 
       for num in range(1, 37)}
}

class RouletteAnalyzer:
    def __init__(self):
        self.numbers = []
        self.load_history()

    def load_history(self):
        """Загрузить историю из базы данных"""
        numbers = get_last_numbers(50)  # Получаем последние 50 чисел
        if numbers:
            print(f"Loading history from database: {numbers}")
            # Преобразуем данные в нужный формат
            self.numbers = [(item['number'], item['color']) for item in numbers]
            print(f"Loaded numbers: {self.numbers}")
        else:
            print("No history data found")
            self.numbers = []

    def analyze_patterns(self):
        """Анализ паттернов в последних числах"""
        if not self.numbers:
            return {}

        numbers = [n[0] for n in self.numbers]
        df = pd.DataFrame(numbers, columns=['number'])
        
        analysis = {
            'hot_numbers': self.get_hot_numbers(df),
            'cold_numbers': self.get_cold_numbers(df),
            'color_stats': self.get_color_stats(),
            'sector_probability': self.calculate_sector_probability(df)
        }
        
        return analysis

    def get_hot_numbers(self, df, top_n=5):
        """Получить числа, которые выпадали чаще всего"""
        return df['number'].value_counts().head(top_n).to_dict()

    def get_cold_numbers(self, df, bottom_n=5):
        """Получить числа, которые выпадали реже всего"""
        all_numbers = set(range(37))
        appeared_numbers = set(df['number'].unique())
        never_appeared = list(all_numbers - appeared_numbers)
        
        if never_appeared:
            return {num: 0 for num in never_appeared[:bottom_n]}
        return df['number'].value_counts().tail(bottom_n).to_dict()

    def get_color_stats(self):
        """Получить статистику по цветам"""
        colors = [n[1] for n in self.numbers]
        color_counts = pd.Series(colors).value_counts()
        total = len(colors)
        return {color: count/total for color, count in color_counts.items()}

    def calculate_sector_probability(self, df):
        """Рассчитать вероятность выпадения чисел по секторам"""
        if df.empty:
            return {'1-12': 1/3, '13-24': 1/3, '25-36': 1/3}
            
        sectors = {
            '1-12': (1, 12),
            '13-24': (13, 24),
            '25-36': (25, 36)
        }
        
        probabilities = {}
        total_numbers = len(df)
        
        for sector_name, (start, end) in sectors.items():
            sector_count = df[df['number'].between(start, end)].shape[0]
            probabilities[sector_name] = sector_count / total_numbers if total_numbers > 0 else 1/3
            
        return probabilities

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/add_number', methods=['POST'])
def add_number():
    try:
        data = request.get_json()
        print(f"Received request data: {data}")
        
        if not data or 'number' not in data:
            return jsonify({'error': 'No number provided'}), 400
            
        number = data['number']
        if not isinstance(number, int) or number < 0 or number > 36:
            return jsonify({'error': 'Invalid number'}), 400
            
        # Сохраняем число в базу данных
        if save_number(number):
            # Обновляем историю в анализаторе
            analyzer.load_history()
            return jsonify({
                'success': True,
                'message': f'Number {number} added successfully'
            })
        else:
            return jsonify({'error': 'Failed to save number'}), 500
            
    except Exception as e:
        print(f"Error in add_number: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze')
def analyze():
    try:
        # Получаем анализ
        analysis = analyzer.analyze_patterns()
        
        # Добавляем историю с цветами
        return jsonify({
            'hot_numbers': analysis['hot_numbers'],
            'cold_numbers': analysis['cold_numbers'],
            'color_stats': analysis['color_stats'],
            'sector_probability': analysis['sector_probability'],
            'history': analyzer.numbers
        })
    except Exception as e:
        print(f"Error analyzing data: {e}")
        return jsonify({'error': str(e)}), 500

analyzer = RouletteAnalyzer()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
