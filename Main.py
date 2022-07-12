#!/usr/bin/env python3

import sys
import random
import time

from PyQt5.QtCore import Qt, QEvent, QAbstractTableModel, QRect, QPoint, QObject, QThread, pyqtSignal, QSize
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QWidget):
    '''Main window of the Yahtzee application'''
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.dict = {'aces' : 0, 
                     'twos' : 0, 
                     'threes' : 0,
                     'fours' : 0,
                     'fives' : 0,
                     'sixes' : 0,
                     'threeofakind' : 0,
                     'fourofakind' : 0,
                     'fullhouse' : 0,
                     'smstraight' : 0,
                     'lgstraight' : 0,
                     'yahtzee' : 0,
                     'chance' : 0,
                     'bonus' : 0
                     }

        self.upper_tot = 0
        self.lower_tot = 0

        self.extra_yahtzee = 0

        self.max_val = 7

        self.initUI()




    def initUI(self):

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        '''Short Cuts'''

        self.quit_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self.quit_shortcut.activated.connect(self.exit_program)

        '''Upper labels'''

        self.upper_section_lab = QLabel("UPPER SECTION")

        self.aces_btn   = QPushButton("ACES")
        self.twos_btn   = QPushButton("TWOS")
        self.threes_btn = QPushButton("THREES")
        self.fours_btn  = QPushButton("FOURS")
        self.fives_btn  = QPushButton("FIVES")
        self.sixes_btn  = QPushButton("SIXES")

        self.bonus_btn  = QPushButton("BONUS")
        self.bonus_val  = QLabel("0")

        for btn in [self.aces_btn, self.twos_btn, 
                    self.threes_btn, self.fours_btn, 
                    self.fives_btn, self.sixes_btn, 
                    self.bonus_btn]:
            btn.setFixedWidth(125)
            btn.setFlat(True)

        self.bonus_btn.setEnabled(False)
        self.bonus_btn.setStyleSheet("color : black")

        self.aces_btn.clicked.connect(self.ChangeAces)
        self.twos_btn.clicked.connect(self.ChangeTwos)
        self.threes_btn.clicked.connect(self.ChangeThrees)
        self.fours_btn.clicked.connect(self.ChangeFours)
        self.fives_btn.clicked.connect(self.ChangeFives)
        self.sixes_btn.clicked.connect(self.ChangeSixes)


        self.aces_val   = QLabel('')
        self.twos_val   = QLabel('')
        self.threes_val = QLabel('')
        self.fours_val  = QLabel('')
        self.fives_val  = QLabel('')
        self.sixes_val  = QLabel('')

        self.bonus_val        = QLabel('')
        
        for lab in [self.aces_val, self.twos_val,
                    self.threes_val, self.fours_val, 
                    self.fives_val, self.sixes_val, 
                    self.bonus_val]:
            lab.setFixedWidth(50)
            lab.setStyleSheet("border : solid black; border-width : 0px 0px 1px 0px")



        '''Lower Labels'''

        self.lower_section_lab = QLabel("LOWER SECTION")

        self.threeofakind_btn = QPushButton("3 of a kind (all)")
        self.fourofakind_btn  = QPushButton("4 of a kind (all)")
        self.fullhouse_btn    = QPushButton("Full House (25)")
        self.smstraight_btn   = QPushButton("Sm. Straight (30)")
        self.lgstraight_btn   = QPushButton("Lg. Straigt (40)")
        self.yahtzee_btn      = QPushButton("YAHTZEE (50)")
        self.chance_btn       = QPushButton("Chance (all)")
        self.yahtzee_b_btn    = QPushButton("YAHTZEE\nBONUS (100+)")

        for btn in [self.threeofakind_btn, self.fourofakind_btn,
                    self.fullhouse_btn, self.smstraight_btn,
                    self.lgstraight_btn, self.yahtzee_btn,
                    self.chance_btn, self.yahtzee_b_btn]:
            btn.setFixedWidth(125)
            btn.setFlat(True)

        self.threeofakind_btn.clicked.connect(self.ChangeThreeOfAKind)
        self.fourofakind_btn.clicked.connect(self.ChangeFourOfAKind)
        self.fullhouse_btn.clicked.connect(self.ChangeFullHouse)
        self.smstraight_btn.clicked.connect(self.ChangeSmallStraight)
        self.lgstraight_btn.clicked.connect(self.ChangeLargeStraight)
        self.yahtzee_btn.clicked.connect(self.ChangeYahtzee)
        self.chance_btn.clicked.connect(self.ChangeChance)
        self.yahtzee_b_btn.clicked.connect(self.ChangeYahtzeeBonus)


        self.threeofakind_val = QLabel('')
        self.fourofakind_val  = QLabel('')
        self.fullhouse_val    = QLabel('')
        self.smstraight_val   = QLabel('')
        self.lgstraight_val   = QLabel('')
        self.yahtzee_val      = QLabel('')
        self.chance_val       = QLabel('')
        self.yahtzee_b_val    = QLabel('')

        for lab in [self.threeofakind_val, self.fourofakind_val,
                    self.fullhouse_val, self.smstraight_val,
                    self.lgstraight_val, self.yahtzee_val,
                    self.chance_val, self.yahtzee_b_val]:
            lab.setFixedWidth(50)
            lab.setStyleSheet("border : solid black; border-width : 0px 0px 1px 0px")


        '''Final Labels'''

        self.upper_total_btn = QPushButton("TOTAL (LOWER)")
        self.lower_total_btn  = QPushButton("TOTAL (UPPER)")
        self.grand_total_btn  = QPushButton("GRAND TOTAL")

        for btn in [self.upper_total_btn, self.lower_total_btn, self.grand_total_btn]:
            btn.setFixedWidth(125)
            btn.setFlat(True)
            btn.setEnabled(False)
            btn.setStyleSheet("color : black")

        self.upper_total_val = QLabel('')
        self.lower_total_val = QLabel('')
        self.grand_total_val = QLabel('')

        for lab in [self.upper_total_val, self.lower_total_val, self.grand_total_val]:
            lab.setFixedWidth(50)
            lab.setStyleSheet("border : solid black; border-width : 0px 0px 1px 0px")


        '''Dice'''

        self.dice_vals = []

        self.dice1 = QPushButton()
        self.dice2 = QPushButton()
        self.dice3 = QPushButton()
        self.dice4 = QPushButton()
        self.dice5 = QPushButton()

        for j, lab in enumerate([self.dice1, self.dice2, self.dice3, self.dice4, self.dice5]):
            self.dice_vals.append(random.randrange(1, self.max_val, 1))
            lab.setIcon(QIcon(str(self.dice_vals[j]) + ".png"))

            lab.setFixedWidth(50)
            lab.setFixedHeight(50)
            lab.setCheckable(True)
            lab.setIconSize(QSize(50, 50))

        '''Game Buttons'''

        self.number_of_rolls = 0

        self.roll_btn     = QPushButton("Roll")
        self.newgame_btn  = QPushButton("New\nGame")

        for lab in [self.roll_btn, self.newgame_btn]:
            lab.setFixedWidth(50)
            lab.setFixedHeight(50)


        self.newgame_btn.clicked.connect(self.NewGame)
        self.roll_btn.clicked.connect(self.NewRoll)
        

        '''Layout'''


        self.break_line_length = 42


        row=0
        self.grid_layout.addWidget(QLabel("-"*self.break_line_length), row, 0, 1, 2, alignment=Qt.AlignCenter)
    
        row+=1
        self.grid_layout.addWidget(self.upper_section_lab, row, 0, 1, 2, alignment=Qt.AlignCenter)

        row+=1
        self.grid_layout.addWidget(QLabel("-"*self.break_line_length), row, 0, 1, 2, alignment=Qt.AlignCenter)

        row+=1
        self.grid_layout.addWidget(self.aces_btn, row, 0, 1, 1)
        self.grid_layout.addWidget(self.aces_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        row+=1
        self.grid_layout.addWidget(self.twos_btn, row, 0, 1, 1)
        self.grid_layout.addWidget(self.twos_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        row+=1
        self.grid_layout.addWidget(self.threes_btn, row, 0, 1, 1)
        self.grid_layout.addWidget(self.threes_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        row+=1
        self.grid_layout.addWidget(self.fours_btn, row, 0, 1, 1)
        self.grid_layout.addWidget(self.fours_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        row+=1
        self.grid_layout.addWidget(self.fives_btn, row, 0, 1, 1)
        self.grid_layout.addWidget(self.fives_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        self.grid_layout.addWidget(QLabel("     "), row, 2, 1, 1)
        self.grid_layout.addWidget(self.dice1, row, 4, 2, 2, alignment=Qt.AlignCenter)

        row+=1
        self.grid_layout.addWidget(self.sixes_btn, row, 0, 1, 1)
        self.grid_layout.addWidget(self.sixes_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        row+=1
        self.grid_layout.addWidget(self.bonus_btn, row, 0, 1, 1)
        self.grid_layout.addWidget(self.bonus_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        self.grid_layout.addWidget(self.dice2, row, 4, 2, 2, alignment=Qt.AlignCenter)

        row+=1
        self.grid_layout.addWidget(QLabel("-"*self.break_line_length), row, 0, 1, 2, alignment=Qt.AlignCenter)

        row+=1
        self.grid_layout.addWidget(self.lower_section_lab, row, 0, 1, 2, alignment=Qt.AlignCenter)

        self.grid_layout.addWidget(self.dice3, row, 4, 2, 2, alignment=Qt.AlignCenter)

        row+=1
        self.grid_layout.addWidget(QLabel("-"*self.break_line_length), row, 0, 1, 2, alignment=Qt.AlignCenter)

        row+=1
        self.grid_layout.addWidget(self.threeofakind_btn, row, 0, 1, 1, alignment=Qt.AlignLeft)
        self.grid_layout.addWidget(self.threeofakind_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        self.grid_layout.addWidget(self.dice4, row, 4, 2, 2, alignment=Qt.AlignCenter)

        row+=1
        self.grid_layout.addWidget(self.fourofakind_btn, row, 0, 1, 1, alignment=Qt.AlignLeft)
        self.grid_layout.addWidget(self.fourofakind_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        row+=1
        self.grid_layout.addWidget(self.fullhouse_btn, row, 0, 1, 1, alignment=Qt.AlignLeft)
        self.grid_layout.addWidget(self.fullhouse_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        self.grid_layout.addWidget(self.dice5, row, 4, 2, 2, alignment=Qt.AlignCenter)

        row+=1
        self.grid_layout.addWidget(self.smstraight_btn, row, 0, 1, 1, alignment=Qt.AlignLeft)
        self.grid_layout.addWidget(self.smstraight_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        row+=1
        self.grid_layout.addWidget(self.lgstraight_btn, row, 0, 1, 1, alignment=Qt.AlignLeft)
        self.grid_layout.addWidget(self.lgstraight_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        row+=1
        self.grid_layout.addWidget(self.yahtzee_btn, row, 0, 1, 1, alignment=Qt.AlignLeft)
        self.grid_layout.addWidget(self.yahtzee_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        self.grid_layout.addWidget(self.roll_btn, row, 4, 2, 2, alignment=Qt.AlignCenter)

        row+=1
        self.grid_layout.addWidget(self.chance_btn, row, 0, 1, 1, alignment=Qt.AlignLeft)
        self.grid_layout.addWidget(self.chance_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        row+=1
        self.grid_layout.addWidget(self.yahtzee_b_btn, row, 0, 1, 1, alignment=Qt.AlignLeft)
        self.grid_layout.addWidget(self.yahtzee_b_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        row+=1
        self.grid_layout.addWidget(QLabel("-"*self.break_line_length), row, 0, 1, 2, alignment=Qt.AlignCenter)

        row+=1
        self.grid_layout.addWidget(self.upper_total_btn, row, 0, 1, 1, alignment=Qt.AlignLeft)
        self.grid_layout.addWidget(self.upper_total_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        row+=1
        self.grid_layout.addWidget(self.lower_total_btn, row, 0, 1, 1, alignment=Qt.AlignLeft)
        self.grid_layout.addWidget(self.lower_total_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        row+=1
        self.grid_layout.addWidget(self.grand_total_btn, row, 0, 1, 1, alignment=Qt.AlignLeft)
        self.grid_layout.addWidget(self.grand_total_val, row, 1, 1, 1, alignment=Qt.AlignLeft)

        self.grid_layout.addWidget(self.newgame_btn, row, 4, 2, 1)

        row+=1
        self.grid_layout.addWidget(QLabel("-"*self.break_line_length), row, 0, 1, 2, alignment=Qt.AlignCenter)

        



    def exit_program(selaf):
        '''Function used to exit the program and close all windows'''
        exit()

    def NewGame(self):
        self.dict = {'aces' : 0,
                     'twos' : 0,
                     'threes' : 0,
                     'fours' : 0,
                     'fives' : 0,
                     'sixes' : 0,
                     'threeofakind' : 0,
                     'fourofakind' : 0,
                     'fullhouse' : 0,
                     'smstraight' : 0,
                     'lgstraight' : 0,
                     'yahtzee' : 0,
                     'chance' : 0,
                     'bonus' : 0
                     }

        for btn in [self.aces_btn, self.twos_btn,
                    self.threes_btn, self.fours_btn,
                    self.fives_btn, self.sixes_btn,
                    self.bonus_btn]:
            btn.setEnabled(True)

        for val in [self.aces_val, self.twos_val,
                    self.threes_val, self.fours_val, 
                    self.fives_val, self.sixes_val, 
                    self.bonus_val]:
            val.setText('')

        for btn in [self.threeofakind_btn, self.fourofakind_btn,
                    self.fullhouse_btn, self.smstraight_btn,
                    self.lgstraight_btn, self.yahtzee_btn,
                    self.chance_btn, self.yahtzee_b_btn]:
            btn.setEnabled(True)


        for val in [self.threeofakind_val, self.fourofakind_val,
                    self.fullhouse_val, self.smstraight_val,
                    self.lgstraight_val, self.yahtzee_val,
                    self.chance_val, self.yahtzee_b_val]:
            val.setText('')

        for val in [self.upper_total_val, self.lower_total_val, self.grand_total_val]:
            val.setText('')

        for j, lab in enumerate([self.dice1, self.dice2, self.dice3, self.dice4, self.dice5]):
            lab.setChecked(False)
            self.dice_vals[j] = random.randrange(1, self.max_val, 1)
            lab.setIcon(QIcon(str(self.dice_vals[j]) + ".png"))
            lab.setIconSize(QSize(50, 50))

        self.number_of_rolls = 0
        self.roll_btn.setEnabled(True)  

        self.lower_tot = 0
        self.upper_tot = 0


    def NewRoll(self):
        for j, lab in enumerate([self.dice1, self.dice2, self.dice3, self.dice4, self.dice5]):
            if lab.isChecked() == False:
                self.dice_vals[j] = random.randrange(1, self.max_val, 1)
                lab.setIcon(QIcon(str(self.dice_vals[j]) + ".png"))
                lab.setIconSize(QSize(50, 50))

        self.number_of_rolls += 1

        if self.number_of_rolls == 3:
            self.roll_btn.setEnabled(False)

    def ResetRoll(self):

        for j, lab in enumerate([self.dice1, self.dice2, self.dice3, self.dice4, self.dice5]):
            self.dice_vals[j] = random.randrange(1, self.max_val, 1)
            lab.setIcon(QIcon(str(self.dice_vals[j]) + ".png"))
            lab.setIconSize(QSize(50, 50))
            lab.setChecked(False)

        self.roll_btn.setEnabled(True)

        self.number_of_rolls = 0

    def UpdateScore(self):

        if self.upper_tot >= 63:
            self.bonus_val.setText("35")
            self.upper_tot += 35
        self.upper_total_val.setText(str(self.upper_tot))
        self.lower_total_val.setText(str(self.lower_tot))
        self.grand_total_val.setText(str(self.upper_tot + self.lower_tot))

    def ChangeAces(self):
        if self.yahtzee_b_btn.isEnabled() == False:
            val = sum(self.dice_vals)
            self.yahtzee_b_btn.setEnabled(True)
        else:
            val = self.dice_vals.count(1) * 1

        self.aces_val.setText(str(val))

        self.upper_tot += val

        
        self.UpdateScore()
        self.ResetRoll()

        self.aces_btn.setEnabled(False)
        self.aces_btn.setStyleSheet("color : black")

    def ChangeTwos(self):
        if self.yahtzee_b_btn.isEnabled() == False:
            val = sum(self.dice_vals)
            self.yahtzee_b_btn.setEnabled(True)
        else:
            val = self.dice_vals.count(2) * 2

        self.twos_val.setText(str(val))

        self.upper_tot += val

        self.UpdateScore()
        self.ResetRoll()

        self.twos_btn.setEnabled(False)
        self.twos_btn.setStyleSheet("color : black")

    def ChangeThrees(self):
        if self.yahtzee_b_btn.isEnabled() == False:
            val = sum(self.dice_vals)
            self.yahtzee_b_btn.setEnabled(True)
        else:
            val = self.dice_vals.count(3) * 3

        self.threes_val.setText(str(val))

        self.upper_tot += val

        self.UpdateScore()
        self.ResetRoll()

        self.threes_btn.setEnabled(False)
        self.threes_btn.setStyleSheet("color : black")

    def ChangeFours(self):
        if self.yahtzee_b_btn.isEnabled() == False:
            val = sum(self.dice_vals)
            self.yahtzee_b_btn.setEnabled(True)
        else:
            val = self.dice_vals.count(4) * 4

        self.fours_val.setText(str(val))

        self.upper_tot += val

        self.UpdateScore()
        self.ResetRoll()

        self.fours_btn.setEnabled(False)
        self.fours_btn.setStyleSheet("color : black")

    def ChangeFives(self):
        if self.yahtzee_b_btn.isEnabled() == False:
            val = sum(self.dice_vals)
            self.yahtzee_b_btn.setEnabled(True)
        else:
            val = self.dice_vals.count(5) * 5

        self.fives_val.setText(str(val))

        self.upper_tot += val

        self.UpdateScore()
        self.ResetRoll()

        self.fives_btn.setEnabled(False)
        self.fives_btn.setStyleSheet("color : black")

    def ChangeSixes(self):
        if self.yahtzee_b_btn.isEnabled() == False:
            val = sum(self.dice_vals)
            self.yahtzee_b_btn.setEnabled(True)
        else:
            val = self.dice_vals.count(6) * 6

        self.sixes_val.setText(str(val))

        self.upper_tot += val

        self.UpdateScore()
        self.ResetRoll()

        self.sixes_btn.setEnabled(False)
        self.sixes_btn.setStyleSheet("color : black")

    def ChangeThreeOfAKind(self):
        if self.yahtzee_b_btn.isEnabled() == False:
            val = sum(self.dice_vals)
            self.yahtzee_b_btn.setEnabled(True)
        else:
            val = 0
            for j in range(1, 7):
                if self.dice_vals.count(j) >= 3:
                    val = sum(self.dice_vals)
                    break

        self.threeofakind_val.setText(str(val))

        self.lower_tot += val

        self.UpdateScore()
        self.ResetRoll()

        self.threeofakind_btn.setEnabled(False)
        self.threeofakind_btn.setStyleSheet("color : black")

    def ChangeFourOfAKind(self):
        if self.yahtzee_b_btn.isEnabled() == False:
            val = sum(self.dice_vals)
            self.yahtzee_b_btn.setEnabled(True)
        else:
            val = 0
            for j in range(1, 7):
                if self.dice_vals.count(j) >= 4:
                    val = sum(self.dice_vals)
                    break

        self.fourofakind_val.setText(str(val))

        self.lower_tot += val

        self.UpdateScore()
        self.ResetRoll()

        self.fourofakind_btn.setEnabled(False)
        self.fourofakind_btn.setStyleSheet("color : black")

    def ChangeFullHouse(self):
        if self.yahtzee_b_btn.isEnabled() == False:
            val = 25
            self.yahtzee_b_btn.setEnabled(True)
        else:
            dice_count = []

            for j in range(1, 7):
                dice_count.append(self.dice_vals.count(j))

            if 2 in dice_count and 3 in dice_count:
                val = 25
            else:
                val = 0

        self.fullhouse_val.setText(str(val))

        self.lower_tot += val

        self.UpdateScore()
        self.ResetRoll()

        self.fullhouse_btn.setEnabled(False)
        self.fullhouse_btn.setStyleSheet("color : black")

    def ChangeSmallStraight(self):
        if self.yahtzee_b_btn.isEnabled() == False:
            val = 30
            self.yahtzee_b_btn.setEnabled(True)
        else:
            dice_count = []

            for j in range(1, 7):
                dice_count.append(self.dice_vals.count(j))

            if 0 not in dice_count[:4] or 0 not in dice_count[1:5] or 0 not in dice_count[2:]:
                val = 30
            else:
                val = 0

        self.smstraight_val.setText(str(val))

        self.lower_tot += val

        self.UpdateScore()
        self.ResetRoll()

        self.smstraight_btn.setEnabled(False)
        self.smstraight_btn.setStyleSheet("color : black")

    def ChangeLargeStraight(self):
        if self.yahtzee_b_btn.isEnabled() == False:
            val = 40
            self.yahtzee_b_btn.setEnabled(True)
        else:
            dice_count = []

            for j in range(1, 7):
                dice_count.append(self.dice_vals.count(j))

            if 0 not in dice_count[:5] or 0 not in dice_count[1:]:
                val = 40
            else:
                val = 0

        self.lgstraight_val.setText(str(val))

        self.lower_tot += val

        self.UpdateScore()
        self.ResetRoll()

        self.lgstraight_btn.setEnabled(False)
        self.lgstraight_btn.setStyleSheet("color : black")

    def ChangeYahtzee(self):
        val = 0

        for j in range(1, 7):
            if self.dice_vals.count(j) >= 5:
                val = 50
                break

        self.yahtzee_val.setText(str(val))

        self.lower_tot += val

        self.UpdateScore()
        self.ResetRoll()

        self.yahtzee_btn.setEnabled(False)
        self.yahtzee_btn.setStyleSheet("color : black")

    def ChangeChance(self):
        if self.yahtzee_b_btn.isEnabled() == False:
            self.yahtzee_b_btn.setEnabled(True)

        val = sum(map(int, self.dice_vals))

        self.chance_val.setText(str(val))

        self.lower_tot += val

        self.UpdateScore()
        self.ResetRoll()

        self.chance_btn.setEnabled(False)
        self.chance_btn.setStyleSheet("color : black")

    def ChangeYahtzeeBonus(self):
        val = 0

        for j in range(1, 7):
            if self.dice_vals.count(j) >= 5:
                val = 50
                break

        if val == 50 and self.yahtzee_val.text() == '50':
            self.extra_yahtzee += 1

            self.lower_tot += 100

            self.yahtzee_b_val.setText(str(self.extra_yahtzee))
            self.yahtzee_b_btn.setEnabled(False)
            
            self.UpdateScore()




def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()
    win.destroy()

if __name__ == '__main__':
    sys.exit(main())

