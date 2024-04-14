import sqlite3

connection = sqlite3.connect('database.db')

cur = connection.cursor()

with open('schema.sql') as f:
    script = f.read()
    cur.executescript(script)

cur.execute("INSERT INTO diver (LeadDiverName, LeadDiverEmail) VALUES (?, ?)", ('Test Lead Diver', 'Test.Lead.Diver@dal.ca'))
cur.execute("INSERT INTO prompts (LeadDiverID, DivePlan, Msg) VALUES (?, ?, ?)", (1, 'This is my test cave diving plan. It is the BESTEST and most SAFEST plan ever!', 'This is a test response. It is not as great as you thought.'))


connection.commit()
connection.close()