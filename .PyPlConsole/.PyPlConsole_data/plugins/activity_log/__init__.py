import sqlite3
from time import strftime
class main:
    def __init__(self, pluginDir, startDir,*a) -> None:
        self.db = sqlite3.connect(pluginDir+"/logging.sqlite")
        self.cursor = self.db.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS starts (start_id INTEGER PRIMARY KEY, time text)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS ends (end_id INTEGER PRIMARY KEY, time text)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS commands (command_id INTEGER PRIMARY KEY, time_at_execution text, command text)")

        self.cursor.execute(f"INSERT INTO starts VALUES (NULL, '{strftime('%-d:%-m:%y %H:%M:%S')}')")
        self.db.commit()


    def _bye(self):
        self.cursor.execute(f"INSERT INTO ends VALUES (NULL, '{strftime('%-d:%-m:%y %H:%M:%S')}')")
        self.db.commit()
        self.db.close()

    def oncmd(self,cmd):
        self.cursor.execute(f"INSERT INTO commands VALUES (NULL, '{strftime('%-d:%-m:%y %H:%M:%S')}', '{cmd}')")
        self.db.commit()

    def view_logs(self,cmd:str):
        cmd = cmd.split()
        if not len(cmd) == 2:
            print("Please provide only on of these as argument:")
            print("starts\nends\ncommands")
            return

        if cmd[-1] == "starts":
            starts = self.cursor.execute("SELECT start_id, time FROM starts").fetchall()
            for start in starts:
                print(f"{start[0]} {start[1]}")
        elif cmd[-1] == "exits":
            ends = self.cursor.execute("SELECT end_id, time FROM ends").fetchall()
            for end in ends:
                print(f"{end[0]} {end[1]}")
        elif cmd[-1] == "commands":
            commands = self.cursor.execute("SELECT command_id, time_at_execution, command FROM commands").fetchall()
            for command in commands:
                print(f"{command[0]} {command[1]} {command[2]}")
        else:
            print("Please provide only on of these as argument:")
            print("starts\nends\ncommands")
    
    def delete_logs(self,cmd:str):
        cmd = cmd.split()
        if cmd[-1]=="all":
            self.cursor.execute("DELETE FROM starts")
            self.cursor.execute("DELETE FROM ends")
            self.cursor.execute("DELETE FROM commands")
            self.db.commit()
            print("Deleted all logs!")
        else:
            print("You can only delete all entries at once, \nsingle deletions are not possible in this version.\nFor that enter delete_logs all")

