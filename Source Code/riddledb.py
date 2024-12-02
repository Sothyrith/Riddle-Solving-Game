import sqlite3

conn = sqlite3.connect('riddledb.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS riddles (
        id TEXT PRIMARY KEY,
        riddle TEXT NOT NULL,
        choice_1 TEXT NOT NULL,
        choice_2 TEXT NOT NULL,
        choice_3 TEXT NOT NULL,
        choice_4 TEXT NOT NULL,
        correct_answer INTEGER NOT NULL,
        difficulty TEXT NOT NULL
    )
''')

conn.commit()

riddles_data = [
    
    ("1E", "Pick me up and scratch my head. I'll turn red and then black. What am I?", 
     "A match", "Candle", "Caterpillar", "None of the above", 1, "Easy"),
    
    ("2E", "I have a neck, but I don't have a head, and I wear a cap. What am I?", 
     "A ghost", "A bottle", "A snake", "A clam", 2, "Easy"),
    
    ("3E", "If you have it, you want to share it. If you share it, you don't have it anymore. What is it?", 
     "Love", "Talent", "A secret", "None of the above", 3, "Easy"),
    
    ("4E", "Cut me and I won't cry, but you will. What am I?", 
     "Slug", "Spearmint", "A knife", "Onion", 4, "Easy"),
    
    ("5E", "What is always coming but never arrives?", 
     "Tomorrow", "A train", "Your paycheck", "The mail", 1, "Easy"),
    
    ("6E", "The person who made it doesn't want it, the person who paid for it doesn't need it, and the person who needs it doesn't know it. What is it?", 
     "A cake", "A car", "A meal", "A coffin", 4, "Easy"),
    
    ("7E", "It belongs to you, but your friends use it more. What is it?", 
     "Your shoes", "Your name", "Your pants", "Your house", 2, "Easy"),
    
    ("8E", "I have cities but no houses, forests but no trees, and rivers but no water. What am I?", 
    "A blueprint", "A map", "A globe", "A puzzle", 2, "Easy"),
        
    ("9E", "I can fly without wings. I can cry without eyes. Whenever I go, darkness follows me. What am I?", 
    "A shadow", "A cloud", "A storm", "A dream", 2, "Easy"),
        
    ("10E", "In a running race, if you overtake the 2nd person, which place would you find yourself in?", 
    "1st place", "2nd place", "3rd place", "4th place", 2, "Easy"),
        
    ("11E", "What has to be broken before you can use it?", 
    "A seal", "An egg", "A lock", "A promise", 2, "Easy"),
        
    ("12E", "What is full of holes but still holds water?", 
    "A sponge", "A bucket", "A net", "A towel", 1, "Easy"),
        
    ("13E", "What can you catch but cannot throw?", 
    "A tennis ball", "A cold", "Your toys", "A boomerang", 2, "Easy"),
        
    ("14E", "I'm tall when I'm young, and I'm short when I'm old. What am I?", 
    "A candle", "A tree", "A pencil", "A building", 1, "Easy"),
        
    ("1M", "What has 13 hearts, but no other organ?", 
    "A soccer team", "A science lab", "A deck of cards", "An operating theatre", 3, "Medium"),
        
    ("2M", "I often run, but I don’t have legs. I don’t need you, but you need me. What am I?", 
    "Athlete", "Water", "A movie", "Ladder", 2, "Medium"),
        
    ("3M", "What is as light as a feather but can’t be held by anyone for very long?", 
    "Tissue paper", "A baby", "Your word", "Your breath", 4, "Medium"),
        
    ("4M", "I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?", 
    "Fire", "Shadow", "Echo", "Whisper", 3, "Medium"),
        
    ("5M", "I have keys but no locks, I have space but no room, you can enter but you can’t go outside. What am I?", 
    "A map", "A computer keyboard", "A piano", "A door", 2, "Medium"),
        
    ("6M", "The more you take, the more you leave behind. What are they?", 
    "Mistakes", "Footsteps", "Opportunities", "Memories", 2, "Medium"),
        
    ("7M", "A man is 24 years old, and his father is 48 years old. In how many years will the father’s age be double the son’s age?", 
    "12 years", "24 years", "18 years", "48 years", 1, "Medium"),
        
    ("8M", "If two’s company, and three’s a crowd, what are four and five?", 
    "A group", "Nine", "Eleven", "A family", 2, "Medium"),
        
    ("9M", "What can travel around the world while staying in the corner?", 
    "A stamp", "A postcard", "A globe", "A compass", 1, "Medium"),
        
    ("10M", "What comes once in a year, twice in a week, but never in a day?", 
    "The letter 'E'", "The letter 'A'", "A special event", "The letter 'N'", 1, "Medium"),
        
    ("11M", "You can't live without doing this, and we all do it at the same time. Yet many wish it wasn't happening. What is it?", 
    "Breathing", "Aging", "Sleeping", "Eating", 2, "Medium"),
        
    ("12M", "You see a house with four walls, all facing south, and a bear walks past it. What color is the bear?", 
    "White", "Brown", "Black", "Yellow", 1, "Medium"),
        
    ("13M", "I am not alive, but I grow; I don’t have lungs, but I need air; I don’t have a mouth, but water kills me. What am I?", 
    "Fire", "A plant", "A cloud", "A stone", 1, "Medium"),
        
    ("14M", "I am an odd number. Take away one letter, and I become even. What number am I?", 
    "Seven", "Three", "Five", "One", 1, "Medium"),
    
    ("1H", "You see a boat filled with people. It hasn’t sunk, but when you look again, you don’t see a single person on the boat. Why?", 
     "They were below deck.", "Everyone jumped off.", "They were all married.", "The boat moved.", 3, "Hard"),
    
    ("2H", "Two fathers and two sons went fishing. Each caught one fish. In total, they brought home three fish. How is this possible?", 
     "One fish escaped.", "They were not counting.", "There were only three people.", "It’s a mistake.", 3, "Hard"),
    
    ("3H", "A man walks into a room with a briefcase. Inside the room, there is no one else. Ten minutes later, he walks out, but now there are two people in the room. How is this possible?", 
     "The man left his reflection behind.", "The man cloned himself.", "The man left a photograph behind.", "The man left a baby in the room.", 1, "Hard"),
    
    ("4H", "A woman is reading a book in a completely dark room. There is no source of light anywhere, yet she can still read. How is this possible?", 
     "She’s reading a glowing book.", "The book is written in Braille.", "The woman is blind.", "She’s imagining the story.", 2, "Hard"),
    
    ("5H", "A man looks at a painting in a museum and says, ‘Brothers and sisters, I have none, but that man's father is my father’s son.’ Who is in the painting?", 
     "His nephew", "His cousin", "His son", "Himself", 4, "Hard"),
    
    ("6H", "You have three switches in one room and three bulbs in another. You can only enter the room with bulbs once. How do you determine which switch controls which bulb?", 
     "Flip the first switch, wait, flip the second, and enter.", "Flip all switches and enter.", "Flip two switches, leave the room, then enter.", "Flip one switch, enter immediately, and test the bulbs.", 1, "Hard"),
    
    ("7H", "A man was driving his truck. His lights weren’t on, and the moon wasn’t out. A woman was crossing the street in front of him. How did he see her?", 
     "He was driving during the day.", "The street was lit by lampposts.", "The woman was wearing reflective clothing.", "He didn’t need lights; the truck had infrared sensors.", 1, "Hard"),
    
    ("8H", "A girl is sitting in her house at night with no lights on, no candles, and no other source of light. Yet she is reading. How is this possible?", 
     "She’s reading a glowing book.", "She is using a flashlight.", "She is reading in her imagination.", "It’s daylight outside.", 4, "Hard"),
    
    ("9H", "You enter a room that contains a match, a candle, and a kerosene lamp. There is only one matchstick. What do you light first?", 
     "The candle", "The lamp", "The matchstick", "Any of them", 3, "Hard"),
    
    ("10H", "If you drop a glass on the floor and it breaks into pieces, what is the one thing that you cannot do after it breaks?", 
     "Fix the glass.", "Count the pieces.", "Hear the sound.", "See the glass.", 1, "Hard"),
    
    ("11H", "You are given two coins: one is fair (50% heads, 50% tails) and the other is biased (90% heads, 10% tails). You need to select one coin, flip it three times, and get exactly two heads. What coin should you pick to maximize your chances of getting two heads?", 
     "The fair coin", "The biased coin", "It doesn’t matter which coin you pick.", "Flip a coin and decide at random.", 2, "Hard"),
    
    ("12H", "You have 8 balls that look identical, but one is slightly heavier. You have a balance scale and can use it only two times to find the heavier ball. How do you do it?", 
     "Weigh three balls at a time.", "Weigh two balls at a time, keep the heaviest.", "Weigh two groups of 4 balls each.", "Weigh three balls, discard two, and weigh the remaining one.", 1, "Hard"),
    
    ("13H", "You’re standing on one side of a river, and you need to get a wolf, a goat, and a cabbage to the other side. You have a boat, but it can only carry you and one of the items at a time. If you leave the wolf with the goat, the wolf will eat the goat. If you leave the goat with the cabbage, the goat will eat the cabbage. How do you get all three across?", 
     "Take the wolf first, then return and take the goat.", "Take the goat first, then return for the cabbage.", "Take the cabbage first, then return for the wolf.", "Take the goat first, leave it, then take the wolf.", 2, "Hard"),
    
    ("14H", "You have two ropes that each take exactly 60 minutes to burn, but they don’t burn evenly (i.e., they may burn faster in some parts than others). How can you measure exactly 45 minutes using only these ropes?", 
     "Light one rope at both ends and the other at one end.", "Light both ropes at one end and wait.", "Light the first rope and wait for it to burn halfway.", "Light both ropes at both ends.", 1, "Hard"),
    
    ("1MM", "What five-letter word becomes shorter when you add two letters to it?", "Space", "Shorter", "Water", "Sharp", 2, "Medium1"),
    
    ("2MM", "What begins with T, finishes with T, and has T in it?", "Tent", "Teapot", "Ticket", "Target", 2, "Medium1"),
    
    ("3MM", "Three men were in a boat. It capsized, but only two got their hair wet. Why?", "One of them was bald.", "One had a hat on.", "One had a wig on.", "The boat didn’t fully sink.", 1, "Medium1"),
    
    ("4MM", "I fly all day, but I stay in the same spot. What am I?", "A drone", "A cloud", "A flag", "A helicopter", 3, "Medium1"),
    
    ("5MM", "The more that there is of this, the less you see. What is it?", "Fog", "Shadows", "Darkness", "Mist", 3, "Medium1"),
    
    ("6MM", "A girl fell off a 40-foot ladder but still did not get hurt. Why?", "She landed in water.", "She was wearing safety gear.", "She held on tightly.", "She was only on the first step.", 4, "Medium1"),
    
    ("7MM", "Tommy throws the ball as hard as he can, and it comes back to him, without anything or anybody touching it. How?", "He used a trampoline.", "He threw it into a wall.", "He spun it with a trick.", "He threw it straight up.", 4, "Medium1"),
    
    ("8MM", "How far can a fox run into the woods?", "As far as it wants to go.", "Until it finds the deepest spot.", "Halfway, then it’s running out.", "Until it gets tired.", 3, "Medium1"),
    
    ("9MM", "It’s been around for millions of years but is never more than a month old. What is it?", "A shadow", "A calendar", "The moon", "A newborn star", 3, "Medium1"),
    
    ("10MM", "What is the last thing you take off before bed?", "Your shoes", "Your feet off the floor", "Your glasses", "Your socks", 2, "Medium1"),
    
    ("11MM", "What flies when it's born, lies when it's alive, and runs when it's dead?", "A clock", "A bird", "A snowflake", "A leaf", 3, "Medium1"),
    
    ("12MM", "What is greater than God, more evil than the devil, the poor have it, the rich need it, and if you eat it you’ll die?", "Money", "Nothing", "Time", "Love", 2, "Medium1"),
    
    ("13MM", "I can travel from there to here by disappearing, and here to there by reappearing. What am I?", "A thought", "A shadow", "The letter T", "A dream", 3, "Medium1"),
    
    ("14MM", "What do we see every day, kings see rarely, and God never sees?", "The moon", "The equality", "The sun", "Time", 2, "Medium1"),
    
    ("15MM", "A man walks out of a house that has four walls all facing north. A bird walks past him. What is it?", "A crow", "A seagull", "A penguin", "An ostrich", 3, "Medium1"),
    
    ("16MM", "What is as big as you are and yet does not weigh anything?", "Your reflection", "Your image", "Your shadow", "Your thoughts", 3, "Medium1"),
    
    ("17MM", "Who spends the day at the window, goes to the table for meals, and hides at night?", "A bird", "A fly", "A cat", "A mouse", 2, "Medium1"),
    
    ("18MM", "If you are a man, then your best friend will eat this for dinner. What is it?", "A steak", "A bone", "A sandwich", "A fish", 2, "Medium1"),
    
    ("19MM", "Sometimes I am liked, sometimes I am hated. Usually I am old, usually I am dated. What am I?", "A movie", "A song", "History", "A book", 3, "Medium1"),
    
    ("20MM", "This sparkling globe can float on water. It is light as a feather, but ten giants can't pick it up. What is it?", "A star", "A bubble", "A raindrop", "A cloud", 2, "Medium1")
]

# c.executemany('''
#     INSERT INTO riddles (id, riddle, choice_1, choice_2, choice_3, choice_4, correct_answer, difficulty)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
# ''', riddles_data)

# conn.commit()

c.execute('SELECT * FROM riddles')
riddles = c.fetchall()

for riddle in riddles:
    print(f"ID: {riddle[0]}")
    print(f"Riddle: {riddle[1]}")
    print(f"Choices: {riddle[2]}, {riddle[3]}, {riddle[4]}, {riddle[5]}")
    print(f"Correct Answer: {riddle[6]}")
    print(f"Difficulty: {riddle[7]}")
    print('-' * 50)

conn.close()