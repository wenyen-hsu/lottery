from flask import Flask, jsonify, request
from flask_cors import CORS
from lottery import LotterySystem
import os

app = Flask(__name__)
CORS(app)  # 啟用 CORS 支援跨域請求

# 從環境變數獲取資料庫路徑，如果沒有設定則使用預設路徑
db_path = os.getenv('SQLITE_DB_PATH', os.path.join(os.path.dirname(__file__), 'lottery.db'))
lottery = LotterySystem(db_path=db_path)

@app.route('/')
def index():
    """健康檢查端點"""
    return jsonify({
        'status': 'ok',
        'message': 'Lottery API is running'
    })

@app.route('/participants', methods=['GET'])
def get_participants():
    try:
        participants = lottery.get_all_participants()
        return jsonify({'participants': participants})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_participant', methods=['POST'])
def add_participant():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '無效的請求數據'}), 400
        
        names = data.get('names', '').strip()
        if not names:
            return jsonify({'error': '請輸入參與者姓名'}), 400
        
        successful, failed = lottery.add_multiple_participants(names)
        return jsonify({
            'success': True,
            'successful': successful,
            'failed': failed,
            'participants': lottery.get_all_participants()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/draw', methods=['POST'])
def draw():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '無效的請求數據'}), 400
        
        count = int(data.get('count', 1))
        winners = lottery.draw_winners(count)
        return jsonify({
            'success': True,
            'winners': winners
        })
    except ValueError as e:
        return jsonify({'error': '請輸入有效的數字'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset():
    try:
        lottery.reset_selections()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_all', methods=['POST'])
def clear_all():
    try:
        lottery.clear_all_participants()
        return jsonify({
            'success': True,
            'message': '已清除所有參與者'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # 本地開發時使用
    app.run(host='0.0.0.0', port=5000, debug=True)
