from flask import Flask, request, jsonify, send_from_directory
from lottery import LotterySystem
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='frontend')
CORS(app)  # Enable CORS for all routes
lottery = LotterySystem(db_path=os.path.join(os.path.dirname(__file__), 'lottery.db'))

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/add_participant', methods=['POST'])
def add_participant():
    data = request.get_json()
    names = data.get('names', '').strip()
    if not names:
        return jsonify({'error': '請輸入參與者姓名'})
    
    successful, failed = lottery.add_multiple_participants(names)
    return jsonify({
        'success': True,
        'successful': successful,
        'failed': failed,
        'participants': lottery.get_all_participants()
    })

@app.route('/participants', methods=['GET'])
def get_participants():
    return jsonify({
        'participants': lottery.get_all_participants()
    })

@app.route('/draw', methods=['POST'])
def draw():
    try:
        data = request.get_json()
        count = int(data.get('count', 1))
        winners = lottery.draw_winners(count)
        return jsonify({
            'success': True,
            'winners': winners
        })
    except ValueError:
        return jsonify({'error': '請輸入有效的數字'})

@app.route('/reset', methods=['POST'])
def reset():
    lottery.reset_selections()
    return jsonify({'success': True})

@app.route('/clear_all', methods=['POST'])
def clear_all():
    try:
        lottery.clear_all_participants()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
