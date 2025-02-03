from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import urllib.parse
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Добавляем секретный ключ для работы с flash-сообщениями
TEXTGEARS_API_KEY = 'ZQTSFYJHtGSENitV'  # Замените на ваш API ключ
TEXTGEARS_GRAMMAR_URL = 'https://api.textgears.com/grammar'
TEXTGEARS_SPELLING_URL = 'https://api.textgears.com/spelling'
TEXTGEARS_CORRECT_URL = 'https://api.textgears.com/correct'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_text = request.form['text']
        if not original_text.strip():
            flash('Пожалуйста, введите текст для проверки', 'error')
            return redirect(url_for('index'))
        
        # Проверяем грамматику, орфографию и получаем исправленный текст
        grammar_errors = check_grammar(original_text)
        spelling_errors = check_spelling(original_text)
        corrected_text = get_corrected_text(original_text)
        
        if grammar_errors is None and spelling_errors is None:
            flash('Произошла ошибка при проверке текста. Проверьте API ключ.', 'error')
            return redirect(url_for('index'))
        
        return render_template('index.html', 
                            original_text=original_text,
                            grammar_errors=grammar_errors,
                            spelling_errors=spelling_errors,
                            corrected_text=corrected_text)
    
    return render_template('index.html')

def check_grammar(text):
    """Проверка грамматики текста"""
    params = {
        'key': TEXTGEARS_API_KEY,
        'text': text,
        'language': 'ru-RU',
        'ai': '1'
    }
    try:
        response = requests.get(TEXTGEARS_GRAMMAR_URL, params=params)
        result = response.json()
        print("Grammar API Response:", result)  # Отладка
        
        if result['status']:
            return result['response'].get('errors', [])
        return None
    except Exception as e:
        print(f"Grammar check error: {str(e)}")
        return None

def check_spelling(text):
    """Проверка орфографии текста"""
    params = {
        'key': TEXTGEARS_API_KEY,
        'text': text,
        'language': 'ru-RU',
        'ai': '1'
    }
    try:
        response = requests.get(TEXTGEARS_SPELLING_URL, params=params)
        result = response.json()
        print("Spelling API Response:", result)  # Отладка
        
        if result['status']:
            return result['response'].get('errors', [])
        return None
    except Exception as e:
        print(f"Spelling check error: {str(e)}")
        return None

def get_corrected_text(text):
    """Получение исправленного текста"""
    params = {
        'key': TEXTGEARS_API_KEY,
        'text': text,
        'language': 'ru-RU'
    }
    try:
        response = requests.get(TEXTGEARS_CORRECT_URL, params=params)
        result = response.json()
        print("Correction API Response:", result)
        
        if result['status']:
            return result['response'].get('corrected')
        return None
    except Exception as e:
        print(f"Text correction error: {str(e)}")
        return None

if __name__ == '__main__':
    app.run(debug=True) 