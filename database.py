import sqlite3
import uuid

class ChatDatabase:
    def __init__(self, db_name='databases\chats.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def create_table(self):
        self.connect()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY,
                file_name TEXT,
                title_chat TEXT
            )
        ''')
        self.conn.commit()
        self.disconnect()

    def add_chat(self, chat_id, title_chat):
        file_name = self.generate_file_name()
        self.connect()
        self.cursor.execute('INSERT INTO chats (id, file_name, title_chat) VALUES (?, ?, ?)', (chat_id, file_name, title_chat))
        self.conn.commit()
        self.disconnect()

    def get_file_name(self, chat_id):
        self.connect()
        self.cursor.execute('SELECT file_name FROM chats WHERE id = ?', (chat_id,))
        result = self.cursor.fetchone()
        self.disconnect()
        if result:
            return result[0]
        else:
            return None
        
    def get_chats(self):
        self.connect()
        self.cursor.execute('SELECT id, title_chat FROM chats')
        rows = self.cursor.fetchall()
        self.disconnect()
        return [[row[0], row[1]] for row in rows]
    
    def generate_file_name(self):
        return str(uuid.uuid4()) + ".txt"
    
    def append_to_file(self, file_path, text):
        """
        Функция, которая добавляет строку text в конец файла file_path.

        :param file_path: путь к файлу
        :param text: текст, который нужно добавить в конец файла
        :return: None
        """
        with open(file_path, mode='a', encoding='utf-8') as file:
            file.write(text)