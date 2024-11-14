import sqlite3
import random

class LotterySystem:
    def __init__(self, db_path='lottery.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """初始化資料庫，創建必要的表格"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 創建班級表
        c.execute('''CREATE TABLE IF NOT EXISTS classes
                    (id TEXT PRIMARY KEY,
                     name TEXT UNIQUE)''')
        
        # 創建參與者表（加入班級關聯）
        c.execute('''CREATE TABLE IF NOT EXISTS participants
                    (name TEXT,
                     class_id TEXT,
                     selected INTEGER DEFAULT 0,
                     PRIMARY KEY (name, class_id),
                     FOREIGN KEY (class_id) REFERENCES classes(id))''')
        
        conn.commit()
        conn.close()

    def get_all_classes(self):
        """獲取所有班級"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT id, name FROM classes')
        classes = [{'id': row[0], 'name': row[1]} for row in c.fetchall()]
        conn.close()
        return classes

    def add_class(self, class_name):
        """新增班級"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            class_id = f"class_{len(self.get_all_classes()) + 1}"
            c.execute('INSERT INTO classes (id, name) VALUES (?, ?)',
                     (class_id, class_name))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def delete_class(self, class_id):
        """刪除班級及其所有參與者"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            # 先刪除該班級的所有參與者
            c.execute('DELETE FROM participants WHERE class_id = ?', (class_id,))
            # 再刪除班級
            c.execute('DELETE FROM classes WHERE id = ?', (class_id,))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    def get_all_participants(self, class_id=None):
        """獲取指定班級的所有參與者"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        if class_id:
            c.execute('SELECT name FROM participants WHERE class_id = ?', (class_id,))
        else:
            c.execute('SELECT name FROM participants')
            
        participants = [row[0] for row in c.fetchall()]
        conn.close()
        return participants

    def add_participant(self, name, class_id):
        """新增單個參與者到指定班級"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute('INSERT INTO participants (name, class_id) VALUES (?, ?)',
                     (name, class_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def add_multiple_participants(self, names, class_id):
        """新增多個參與者到指定班級"""
        names = [name.strip() for name in names.split() if name.strip()]
        successful = []
        failed = []
        
        for name in names:
            if self.add_participant(name, class_id):
                successful.append(name)
            else:
                failed.append(name)
                
        return successful, failed

    def draw_winners(self, count, class_id):
        """從指定班級中抽取指定數量的得獎者"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 獲取未被選中的參與者
        c.execute('''SELECT name FROM participants 
                    WHERE class_id = ? AND selected = 0''', (class_id,))
        available = [row[0] for row in c.fetchall()]
        
        # 如果可用參與者數量小於要抽取的數量，調整抽取數量
        count = min(count, len(available))
        winners = random.sample(available, count) if available else []
        
        # 更新已選中的參與者狀態
        for winner in winners:
            c.execute('''UPDATE participants SET selected = 1 
                        WHERE name = ? AND class_id = ?''', (winner, class_id))
        
        conn.commit()
        conn.close()
        return winners

    def reset_selections(self, class_id):
        """重置指定班級的抽獎狀態"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('UPDATE participants SET selected = 0 WHERE class_id = ?', (class_id,))
        conn.commit()
        conn.close()

    def clear_all_participants(self, class_id):
        """清除指定班級的所有參與者"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM participants WHERE class_id = ?', (class_id,))
        conn.commit()
        conn.close()
