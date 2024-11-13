import sqlite3
import random
import os
from typing import List, Optional

class LotterySystem:
    def __init__(self, db_path: str = "lottery.db"):
        self.db_path = db_path
        self.setup_database()
    
    def setup_database(self):
        """Initialize the SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create participants table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                selected INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_participant(self, name: str) -> bool:
        """Add a new participant to the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO participants (name) VALUES (?)', (name,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def add_multiple_participants(self, names: str) -> tuple[List[str], List[str]]:
        """
        Add multiple participants at once, separated by spaces.
        Returns tuple of (successful_adds, failed_adds)
        """
        # Split names by spaces and filter out empty strings
        name_list = [name.strip() for name in names.split() if name.strip()]
        
        successful = []
        failed = []
        
        for name in name_list:
            if self.add_participant(name):
                successful.append(name)
            else:
                failed.append(name)
        
        return successful, failed
    
    def get_all_participants(self) -> List[str]:
        """Get all participants from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM participants')
        participants = [row[0] for row in cursor.fetchall()]
        conn.close()
        return participants
    
    def draw_winners(self, count: int) -> List[str]:
        """Draw specified number of winners who haven't been selected yet."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get eligible participants (not selected yet)
        cursor.execute('SELECT id, name FROM participants WHERE selected = 0')
        eligible = cursor.fetchall()
        
        if not eligible:
            conn.close()
            return []
        
        # Select random winners
        winners_count = min(count, len(eligible))
        winners = random.sample(eligible, winners_count)
        
        # Update selected status
        for winner_id, _ in winners:
            cursor.execute('UPDATE participants SET selected = 1 WHERE id = ?', (winner_id,))
        
        conn.commit()
        conn.close()
        
        return [name for _, name in winners]
    
    def reset_selections(self):
        """Reset all selection statuses."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE participants SET selected = 0')
        conn.commit()
        conn.close()

def main():
    lottery = LotterySystem()
    
    while True:
        print("\n=== 抽獎系統 ===")
        print("1. 新增參與者")
        print("2. 批次新增參與者（用空格分隔）")
        print("3. 顯示所有參與者")
        print("4. 抽獎")
        print("5. 重置抽獎狀態")
        print("6. 離開")
        
        choice = input("\n請選擇操作 (1-6): ")
        
        if choice == "1":
            name = input("請輸入參與者姓名: ")
            if lottery.add_participant(name):
                print(f"成功新增 {name}")
            else:
                print("新增失敗，該參與者可能已存在")
        
        elif choice == "2":
            names = input("請輸入多個參與者姓名（用空格分隔）: ")
            successful, failed = lottery.add_multiple_participants(names)
            
            if successful:
                print("\n成功新增:")
                for name in successful:
                    print(f"- {name}")
            
            if failed:
                print("\n新增失敗（已存在）:")
                for name in failed:
                    print(f"- {name}")
            
            if not successful and not failed:
                print("未輸入任何有效名稱")
        
        elif choice == "3":
            participants = lottery.get_all_participants()
            print("\n所有參與者:")
            for i, name in enumerate(participants, 1):
                print(f"{i}. {name}")
        
        elif choice == "4":
            try:
                count = int(input("請輸入要抽出的人數: "))
                winners = lottery.draw_winners(count)
                if winners:
                    print("\n抽獎結果:")
                    for i, winner in enumerate(winners, 1):
                        print(f"{i}. {winner}")
                else:
                    print("沒有合格的參與者可供抽選")
            except ValueError:
                print("請輸入有效的數字")
        
        elif choice == "5":
            lottery.reset_selections()
            print("已重置所有抽獎狀態")
        
        elif choice == "6":
            print("感謝使用，再見！")
            break
        
        else:
            print("無效的選擇，請重試")

if __name__ == "__main__":
    main()
