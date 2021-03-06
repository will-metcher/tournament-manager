import random

tournament = 0

class Tournament:
   
    def __init__(self, name):
        self.name = name
        self.players = []
        self.games = []

    def addPlayer(self, name, played, points):
        self.players.append(Player(name, played, points))

    def recordGame(self, p1, p2, result):
        self.games.append(Game(p1, p2, result))

    def getPlayerByName(self, name):
        for i in range(len(self.players)):
            if(self.players[i].name == name):
                return self.players[i]
        return 0

    def sortPlayersByPoints(self):
        self.players.sort(key=lambda x : x.points, reverse=True)

    def unplayedMatches(self, name):
        #convert games played to str arr
        _games = []
        for y in range(len(self.games)):
            _games.append(str(self.games[y].p1) + "," +str(self.games[y].p2))

        played = []
        for i in range(len(_games)):
            if name in _games[i]:
                if name != _games[i].split(",")[1]:
                    played.append(_games[i].split(",")[1])
                else:
                    played.append(_games[i].split(",")[0])

        unplayed = []
        for j in range(len(self.players)):
            if self.players[j].name not in played and self.players[j].name != name:
                unplayed.append(self.players[j].name)

        return unplayed

    def generateMatches(self):
        #sorted by games played desc
        players = []
        self.players.sort(key=lambda x : x.played, reverse=True)

        #remove completed players
        for i in range(len(self.players)):
            if self.players[i].played != len(self.players) - 1:
                players.append(self.players[i].name)

        #gen matches from players
        #odd num players
        if len(players) % 2 != 0:
            players.pop(random.randrange(0,len(players) - 1))
            
        print(players)
        
class Player:
    def __init__(self, name, played, points):
        self.name = name
        self.played = int(played)
        self.points = int(points)

    def calcRatio(self):
        if(self.played == 0):
            return "0%"
        return str((self.points / self.played) * 50) + "%"

class Game:
    def __init__(self,p1,p2,result):
        self.p1 = p1
        self.p2 = p2
        self.result = result

choice = ""

def menu():
    print("\na. Create new Tournament \nb. Add Player \nc. Record Game \nd. Generate Matchups \ne. View Results \nf. Save Data \ng. Load Data \nh. List unplayed \nx. Exit")
    choice = input(">>> ")
    if choice == "a":
        createTournament()
    elif choice == "b":
        createPlayer()
    elif choice == "c":
        recordGame()
    elif choice == "d":
        tournament.generateMatches()
    elif choice == "e" or choice == "results":
        showResults()
    elif choice == "f":
        saveData()
    elif choice == "g" or choice == "load":
        loadData()
    elif choice == "x":
        exit(0)
    elif choice == "h":
        name = input("Give unplayed players for: ")
        print(tournament.unplayedMatches(name))
    else:
        print("Unknown command: "+choice)

def isTournamentActive():
    if tournament == 0:
        print("You need to create a Tournament first.")
        return False
    return True
 
def createTournament():
    global tournament
    name = input("Tournament Name: ")
    tournament = Tournament(name)

def createPlayer():
    if not isTournamentActive():
        return
    
    name = input("Player Name: ")
    tournament.addPlayer(name,0,0)
    saveData()

def recordGame():
    if not isTournamentActive():
        return

    p1 = input("Player 1: ")
    p2 = input("Player 2: ")
    res = input("result (beat, tied): ")
    mult = 1
    
    if p1 == "Will" or p2 == "Will":
        mult = 2

    p1_obj = tournament.getPlayerByName(p1)
    p2_obj = tournament.getPlayerByName(p2)
   
    if p1_obj == 0:
        print("No player called "+p1 + " found.")
        return
    
    if p2_obj == 0:
        print("No player called "+p2 + " found.")
        return

    #check for rematch
    for i in range(len(tournament.games)):
        players = tournament.games[i].p1 + tournament.games[i].p2
        if p1 in players and p2 in players:
            #rematch

            print("That was a rematch, both players have been subtracted a game and the previous result ("+p1+" " + tournament.games[i].result + " " + p2+") was removed.")
            
            p1_obj.played -= 1
            p2_obj.played -= 1
            
            if tournament.games[i].result == "beat":
                tournament.getPlayerByName(tournament.games[i].p1).points -= 2 * mult
            else:
                p1_obj.points -= 1 * mult
                p2_obj.points -= 1 * mult
            tournament.games.pop(i)
            break
   
    tournament.recordGame(p1, p2, res)
    p1_obj.played += 1
    p2_obj.played += 1

    if res == "beat":
        p1_obj.points += 2 * mult
    else:
        p1_obj.points += 1 * mult
        p2_obj.points += 1 * mult
       
    saveData()
    

def showResults():
    if not isTournamentActive():
        return
    
    tournament.sortPlayersByPoints()
   
    longest = 0
    for j in range(len(tournament.players)):
        if len(tournament.players[j].name) > longest:
            longest = len(tournament.players[j].name)
   
    for i in range(len(tournament.players)):
        string = tournament.players[i].name + (" " * (longest - len(tournament.players[i].name))) + "   "
        print(string + str(tournament.players[i].played) + "    " + str(tournament.players[i].points))
       
def saveData():
    file = open(tournament.name+"_data.txt", "w")
    save = ""
    for i in range(len(tournament.players)):
        save += tournament.players[i].name + ":" + str(tournament.players[i].played) + ":" + str(tournament.players[i].points) + ","
    save = save[:-1] + "\n"
    for j in range(len(tournament.games)):
        save += tournament.games[j].p1 + " " + tournament.games[j].result + " " + tournament.games[j].p2 + "\n"
   
    file.write(save)
    file.close()

def loadData():
    global tournament
    #filename = input("File: ") + ".txt"
    filename = "ftp_data.txt"
    lines = open(filename).read().splitlines()
    tournament = Tournament(filename.split("_")[0])

    if len(lines) == 0:
        print(filename + " is empty.")
        return

    players = lines[0]
   
    games = []

    for j in range(1, len(lines )):
        line = lines[j].split(" ")
        tournament.recordGame(line[0], line[2], line[1])
   
    players = players.split(",")

    for i in range(len(players)):
        player = players[i].split(":")
        tournament.addPlayer(player[0], player[1], player[2])

    tournament.sortPlayersByPoints()

    print(filename + " loaded.")

while not choice == "x":
    menu()
