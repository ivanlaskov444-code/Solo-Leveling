import sqlite3
import os

class Database:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "database.db")
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()

    def register_player(self, login, password):
        try:
            self.cur.execute(
                "INSERT INTO players (login, password, credits, level) VALUES (?, ?, ?, ?)",
                (login, password, 100, 1)
            )
            self.con.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login(self, login, password):
        self.cur.execute(
            "SELECT id, login, credits, level FROM players WHERE login = ? AND password = ?",
            (login, password)
        )
        return self.cur.fetchone()

    def add_credits_goblin(self, login):
        self.cur.execute(
            "UPDATE players SET credits = credits + 20 WHERE login = ?",
            (login,)
        )
        self.con.commit()

    def add_credits_mucus(self, login):
        self.cur.execute(
            "UPDATE players SET credits = credits + 10 WHERE login = ?",
            (login,)
        )
        self.con.commit()

    def restart(self, login):
        self.cur.execute(
            "SELECT id, login, credits, level FROM players WHERE login = ?",
            (login,)
        )
        return self.cur.fetchone()

    def up_level(self, login):
        self.cur.execute(
            "UPDATE players SET level = level + 1 WHERE login = ?",
            (login,)
        )
        self.con.commit()


