from flask import Flask, render_template, request, jsonify
import os
import re
from collections import Counter
import string


app = Flask(__name__, static_folder='static')


def analyze_text(text):
    """Analyze text and return word count, character count, line count and word frequency"""
  
    lines = text.split('\n')
    line_count = len(lines)
    
    translator = str.maketrans('', '', string.punctuation)
    words = text.translate(translator).split()
    word_count = len(words)
    
    char_count_with_spaces = len(text)
    char_count_without_spaces = len(text.replace(' ', ''))
    
    word_freq = Counter(words)
    most_common_words = word_freq.most_common(10)
    
    sentence_count = len(re.split(r'[.!?]+', text)) - 1
    
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    paragraph_count = len(paragraphs)
    
    avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
    
    reading_time = word_count / 200
    
    return {
        'word_count': word_count,
        'line_count': line_count,
        'char_count_with_spaces': char_count_with_spaces,
        'char_count_without_spaces': char_count_without_spaces,
        'sentence_count': sentence_count,
        'paragraph_count': paragraph_count,
        'avg_word_length': round(avg_word_length, 2),
        'reading_time': round(reading_time, 2),
        'most_common_words': most_common_words
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                text = file.read().decode('utf-8')
            else:
                text = request.form.get('text', '')
        else:
            text = request.form.get('text', '')
        
        if not text.strip():
            return jsonify({'error': 'Please provide some text to analyze.'})
        
        
        results = analyze_text(text)        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
