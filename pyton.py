import math
import random

class Board:
    def __init__(self,row,column):
        if row != column :
            raise ValueError("Liczby muszą być sobie równe!")
        if row < 2 or column < 2:
            raise ValueError("Plansza wieksza niz 2na2")
        self.row=row
        self.column=column
        self.slownik = {}
        for a in range(row):
            self.slownik[65+a]= a

    def generate_board(self):
        # gracz podaje dlugosc i wysokosc planszy, plansza tworzy się jako macierz
        if (self.row !=self.column):
            return False
        else:
            self.board = [[0 for x in range(self.row)] for x in range(self.column)]
            self.mapa = [["O" for x in range(self.row)] for x in range(self.column)]

    # mechanizm pokazywania planszy wraz ze stakami
    def show_board(self):
        print(" ", end="")
        for x in range(self.column):
            print(" ", chr(65 + x), end="")
        print()
        for ind, a in enumerate(self.board):
            print(ind, end=" ")
            print(a)
    #mechanizm do pokazywania mapy tam gdzie ty strzelales
    def show_mapa(self):

        for x in range(self.column):
            print("   ", chr(65 + x), end="")
        print()
        for ind, a in enumerate(self.mapa):
            print(ind, end=" ")
            print(a)


    # czy wszystkie statki zostaly zatopione
    def check_board(self):
        end = all(znak != 1 for wiersz in self.board for znak in wiersz)
        punktow_do_traf = sum(znak == 1 for wiersz in self.board for znak in wiersz)
        return punktow_do_traf

    # algorytm do losowania statkow i ich ilosci
    def generate_ships(self):
        d = math.floor(self.row**2*0.4)
        slowniczek = {}
        while 1:
            lista = []
            for a in range(self.row+1):
                lista.append(random.randint(1,self.row-2))
            if sum(lista) == d and self.row-2 in lista:
                break
            else:
                continue
        for a in range(self.row-2):
            slowniczek[a+1] = lista.count(a+1)
        return slowniczek



class Player():
    # gracz podaje swoja nazwe
    def __init__(self,name,board,przeciwnik):
        self.name=name
        self.board = board
        self.slownik = self.board.slownik
        self.statki = self.board.generate_ships()
        self.przeciwnik = przeciwnik
        # self.punkty = Board.check_board(board.board)

    # gracz wybiera pole do ostrzalu statku
    def attack(self):
        pole = str(input("Podaj pole, które chcesz zaatakować format(A0, B5)"))
        pole = list(pole)
        self.przeciwnik.board[int(pole[1])][self.slownik[ord(pole[0])]] -=2
        self.trafienie = self.board.board[int(pole[1])][self.slownik[ord(pole[0])]]
        self.board.mapa[int(pole[1])][self.slownik[ord(pole[0])]] = "X"

    def check_attack(self):
        if self.trafienie == -1:
            return "trafiony"
        elif self.trafienie < -1:
            return "już tam strzelałeś"
        else:
            return "nie trafiles"

    # gracz wybiera pole na ktorym stawia swoj statek
    def plant_ship(self):
        pole = str(input("Podaj pole, na którym chcesz postawic statek format(A0, B5)"))
        pole = list(pole)
        print(self.statki)
        statek = int(input("Wybierz ktory statek chcesz umiescic wpisujac jego dlugość"))
        if statek == 1 and self.statki[statek]>0:
            self.board.board[int(pole[1])][self.slownik[ord(pole[0])]] += 1
            self.statki[1] -= 1
        elif statek >= 2 and self.statki[statek]>0:
            jak = input("Czy chcesz umieścić statek pionowo czy poziomo 1 - poziomo 2 - pionowo: ")
            if jak == "1":
                for i in range(statek):
                    print(i)
                    self.board.board[int(pole[1])][self.slownik[ord(pole[0])] + i] += 1
            elif jak == "2":
                for i in range(statek):
                    print(i)
                    self.board.board[int(pole[1]) + i][self.slownik[ord(pole[0])]] += 1
            self.statki[statek] -= 1
        else:
            print("nie masz juz tych statkow")

    # jeszcze dodac mape trafien w przeciwnika jak wyglada


    # ile jeszcze statkow zyje / ile ma punktow do ostrzelenia
    def count_ships(self):
        return self.board.check_board()
    def gui(self):
        x = int(input("Wybierz co chcesz zrobic 1-pokaz swoja mape 2- pokaz mape ostrzalow 3- zaatakuj przeciwnika"))
        match x:
            case 1:
                self.board.show_board()
            case 2:
                self.board.show_mapa()
            case 3:
                self.attack()
                return False
            case default:
                print("essa")
        return True
class Bot(Player):
    attaki = []
    def __int__(self,board):
        self.board = board

    def randomize_ships(self):
        list = []
        while len(list) < math.floor(self.board.row**2*0.4):
            x  = random.randint(0,self.board.row-1)
            y  = random.randint(0,self.board.row-1)
            if [x,y] not in list:
                list.append([x,y])
                self.board.board[x][y] +=1
            else:
                continue
    def random_attack(self):
        while True:
            x  = random.randint(0,self.board.row-1)
            y  = random.randint(0,self.board.row-1)
            if [x,y] in self.attaki:
                continue
            else:
                self.attaki.append([x,y])
                self.przeciwnik.board[x][y] -=2
                break




class Game:
    def start(self):
        x = int(input("Podaj wielkosc planszy: "))
        plansza = Board(x,x)
        plansza.generate_board()
        plansza.show_board()

        bota_plansza = Board(x, x)
        bota_plansza.generate_board()
        bocik = Bot("bot",bota_plansza, plansza)
        bocik.randomize_ships()
        bota_plansza.show_board()

        gracz = Player("gracz1", plansza, bota_plansza)


        while not all(wartosc == 0 for wartosc in gracz.statki.values()):
            gracz.plant_ship()
            plansza.show_board()

        while(self.check_winner(gracz,bocik)):
            while gracz.gui():
                gracz.gui()
            bocik.random_attack()
            plansza.show_board()

    # mechanizm okreslania zwyciezy
    def check_winner(self,player1,player2):
        if (player1.count_ships() == 0):
            print(f"{player2.name} wygrywa!")
        elif (player2.count_ships() == 1):
            print(f"{player1.name} wygrywa!")
        else:
            return True
        return False

    pass
def main():
    print("Ahoj kamracie, Gra w statki!")
    game = Game()
    game.start()

if __name__ == "__main__":
    main()
