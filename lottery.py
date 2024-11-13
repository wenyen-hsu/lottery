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

    def clear_all_participants(self) -> bool:
        """Clear all participants from the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM participants')
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False
