from flask import Flask, render_template, request, jsonify
from lottery import LotterySystem
import os

app = Flask(__name__)
lottery = LotterySystem(db_path=os.path.join(os.path.dirname(__file__), 'lottery.db'))

@app.route('/')
def index():
    participants = lottery.get_all_participants()
    return render_template('index.html', participants=participants)

@app.route('/add_participant', methods=['POST'])
def add_participant():
    names = request.form.get('names', '').strip()
    if not names:
        return jsonify({'error': '請輸入參與者姓名'})
    
    successful, failed = lottery.add_multiple_participants(names)
    return jsonify({
        'success': True,
        'successful': successful,
        'failed': failed,
        'participants': lottery.get_all_participants()
    })

@app.route('/draw', methods=['POST'])
def draw():
    try:
        count = int(request.form.get('count', 1))
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
