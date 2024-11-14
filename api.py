from flask import Flask, jsonify, request
from flask_cors import CORS
from lottery import LotterySystem
import os
import sqlite3

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
        class_id = request.args.get('class')
        if not class_id:
            return jsonify({'error': '未指定班級'}), 400
        participants = lottery.get_all_participants(class_id)
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
        class_id = data.get('class')
        if not names:
            return jsonify({'error': '請輸入參與者姓名'}), 400
        if not class_id:
            return jsonify({'error': '未指定班級'}), 400
        
        successful, failed = lottery.add_multiple_participants(names, class_id)
        return jsonify({
            'success': True,
            'successful': successful,
            'failed': failed,
            'participants': lottery.get_all_participants(class_id)
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
        class_id = data.get('class')
        if not class_id:
            return jsonify({'error': '未指定班級'}), 400
        
        winners = lottery.draw_winners(count, class_id)
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
        data = request.get_json()
        class_id = data.get('class')
        if not class_id:
            return jsonify({'error': '未指定班級'}), 400
        
        lottery.reset_selections(class_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_all', methods=['POST'])
def clear_all():
    try:
        data = request.get_json()
        class_id = data.get('class')
        if not class_id:
            return jsonify({'error': '未指定班級'}), 400
        
        lottery.clear_all_participants(class_id)
        return jsonify({
            'success': True,
            'message': '已清除所有參與者'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/classes', methods=['GET'])
def get_classes():
    try:
        classes = lottery.get_all_classes()
        return jsonify({'classes': classes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_class', methods=['POST'])
def add_class():
    """新增班級的路由處理函數"""
    try:
        # 檢查請求內容
        data = request.get_json()
        print(f"收到的數據: {data}")  # 加入日誌
        
        if not data:
            return jsonify({
                'success': False,
                'error': '無效的請求數據 - 未收到 JSON 數據'
            }), 400
        
        if 'className' not in data:
            return jsonify({
                'success': False,
                'error': '無效的請求數據 - 缺少 className 欄位'
            }), 400
        
        class_name = data['className'].strip()
        if not class_name:
            return jsonify({
                'success': False,
                'error': '請輸入班級名稱'
            }), 400
        
        # 嘗試新增班級
        try:
            success = lottery.add_class(class_name)
            if success:
                print(f"成功新增班級: {class_name}")  # 加入日誌
                return jsonify({
                    'success': True,
                    'message': f'已新增班級：{class_name}'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': '班級已存在'
                }), 400
        except Exception as e:
            print(f"新增班級時發生錯誤: {str(e)}")  # 加入日誌
            return jsonify({
                'success': False,
                'error': f'新增班級失敗: {str(e)}'
            }), 500
            
    except Exception as e:
        print(f"處理請求時發生錯誤: {str(e)}")  # 加入日誌
        return jsonify({
            'success': False,
            'error': f'伺服器錯誤: {str(e)}'
        }), 500

@app.route('/delete_class', methods=['POST'])
def delete_class():
    try:
        data = request.get_json()
        if not data or 'class' not in data:
            return jsonify({'error': '無效的請求數據'}), 400
        
        class_id = data['class']
        success = lottery.delete_class(class_id)
        if success:
            return jsonify({
                'success': True,
                'message': '已刪除班級'
            })
        else:
            return jsonify({'error': '刪除班級失敗'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 本地開發時使用
    app.run(host='0.0.0.0', port=5000, debug=True)
