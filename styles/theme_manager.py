import sqlite3
from enum import Enum

class ThemeType(Enum):
    LIGHT = "light"
    DARK = "dark"


class ThemeManager:
    def __init__(self, db_file="tools.db"):
        self.db_file = db_file
        self.current_theme = ThemeType.LIGHT
        self.load_theme()
    
    def load_theme(self):
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute('SELECT config_value FROM config WHERE config_key = ?', ('theme',))
            result = c.fetchone()
            conn.close()
            
            if result:
                theme_name = result[0]
                self.current_theme = ThemeType(theme_name)
            else:
                self.current_theme = ThemeType.LIGHT
                self.save_theme()
        except Exception:
            self.current_theme = ThemeType.LIGHT
    
    def save_theme(self):
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            
            c.execute('SELECT COUNT(*) FROM config WHERE config_key = ?', ('theme',))
            exists = c.fetchone()[0] > 0
            
            if exists:
                c.execute('UPDATE config SET config_value = ? WHERE config_key = ?', 
                         (self.current_theme.value, 'theme'))
            else:
                c.execute('INSERT INTO config (config_key, config_value) VALUES (?, ?)', 
                         ('theme', self.current_theme.value))
            
            conn.commit()
            conn.close()
        except Exception:
            pass
    
    def switch_theme(self):
        if self.current_theme == ThemeType.LIGHT:
            self.current_theme = ThemeType.DARK
        else:
            self.current_theme = ThemeType.LIGHT
        
        self.save_theme()
        return self.current_theme
    
    def get_current_theme(self):
        return self.current_theme
    
    def set_theme(self, theme):
        self.current_theme = theme
        self.save_theme()
    
    def is_dark_theme(self):
        return self.current_theme == ThemeType.DARK
