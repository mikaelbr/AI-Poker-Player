import sqlite3
import hashlib


class DB_Con ():

    def __init__ (self):
        self.conn = sqlite3.connect('db_file')
        self.c = self.conn.cursor()
        self.c.executescript("""
            CREATE table IF NOT EXISTS opponent_modeling (
                context,
                player,
                action,
                strength,
                num_vals
            );
        """)


    # returns a context based on what round, num players remaining, number of total raises in game
    # and the pot odds (C/(C+P))
    def generate_context(self, betting_round, players_remaining, num_raises, pot_odds):

        # OK To just use md5 for this - not to many collisions.
        # Also a fast hashing - positive in this context. 
        #return hashlib.md5("%s:%s:%s:%s" % (betting_round, players_remaining, num_raises, pot_odds)).hexdigest()
        return "%s:%s:%s:%s" % (betting_round, players_remaining, num_raises, pot_odds)


    # returns a float value
    def get_hand_strength(self, context, player, action):
        self.c.execute("SELECT strength FROM opponent_modeling WHERE context = ? AND action = ? AND player = ?", (context, action, player))

        ret = self.c.fetchone();

        if ret == None:
            return False

        return ret[0]

    def get_dump(self):
        self.c.execute("SELECT * FROM opponent_modeling")
        return self.c.fetchall()

    # in form of [[context, action], [context, action], ... ]
    def insert_data(self, data, player, strength):

        for c in data:
            prev_value = self.get_hand_strength(c[0],c[1],c[2])
            if prev_value:
                # update value
                self.c.execute("UPDATE opponent_modeling SET strength = (strength+?)/2, num_raises = num_raises + 1", (c[3]))
                pass
            else: # Insert new
                self.c.execute("INSERT INTO opponent_modeling VALUES (?, ?, ?, ?, ?)", (c[0],c[1],c[2],c[3],1))

        self.conn.commit()


db = DB_Con()
db = DB_Con()

contexts = [
    [db.generate_context(1, 3, 1, float(30.0/(45.0+30.0))), "Mikael", "call", 0.8531],
    [db.generate_context(4, 3, 1, float(30.0/(45.0+30.0))), "Mikael", "raise", 0.3331],
    [db.generate_context(3, 3, 1, float(30.0/(45.0+30.0))), "Mikael", "call", 0.8531],
    [db.generate_context(2, 3, 1, float(30.0/(45.0+30.0))), "Mikael", "raise", 0.6531]
]

#db.insert_data(contexts)


print("Strength: %s" % db.get_hand_strength(db.generate_context(1, 3, 1, float(30.0/(45.0+30.0))), "Mikael", "call"))


print(db.get_dump())

