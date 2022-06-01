from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QStackedWidget
from board import Board
from csp import CSP, backtracking_search, forward_checking, mac
from generate import generate, format2Gui, format2Solver
from kenken import KenKen

algorithm = {
    1: "BT",
    2: "FC",
    3: "MAC"
}

class configuration(QDialog):
    def __init__(self, widget: QStackedWidget):
        super(configuration, self).__init__()
        loadUi("dialog.ui", self)
        self.widget = widget
        self.user.clicked.connect(self.userClicked)
        self.solve.clicked.connect(self.autoClicked)
        self.reset.clicked.connect(self.resetClicked)
        self.same.clicked.connect(self.runSameBoard)
        self.run.clicked.connect(self.runCode)
        self.values = {
            'solver': 'auto',
            'algorithm': '',
            'board_size': ''
        }
        self.board = False
    
    def userClicked(self):
        self.algorithm.setCurrentIndex(0)
        self.values['solver'] = 'user'
        
    def autoClicked(self):
        self.algorithm.setCurrentIndex(0)
        self.values['solver'] = 'auto'

    def resetClicked(self):
        self.algorithm.setCurrentIndex(0)
        self.algorithm.setEnabled(True)
        self.board_size.setCurrentIndex(0)
        self.solve.setChecked(True)
        self.values = {
            'solver': 'auto',
            'algorithm': '',
            'board_size': '',
            'num_boards': ''
        }
        self.board = False
        Board().close()
        
    def check(self):
        if self.values['solver'] == 'auto':
            return (self.algorithm.currentIndex() != 0) and (self.board_size.currentIndex() != 0)
        elif self.values['solver'] == 'user':
            return self.board_size.currentIndex() != 0    

    def runSameBoard(self):
        if self.values['board_size'] == self.board_size.currentIndex() + 2: 
            if self.board:
                soln = []
                if self.values['algorithm'] == 'BT':
                    soln = backtracking_search(self.game_kenken)
                if self.values['algorithm'] == 'FC':
                    soln = backtracking_search(self.game_kenken, inference=forward_checking)
                if self.values['algorithm'] == 'MAC':
                    soln = backtracking_search(self.game_kenken, inference=mac)
                try:
                    board = Board(
                        solver=self.values['solver'], 
                        n=self.values['board_size'], 
                        algorithm=self.values['algorithm']
                    )
                    board.get_inputs(self.grid)
                    board.run(soln = self.kenken.format_soln(soln, self.values['board_size']))
                    self.board = True
                except:
                    pass
            else:
                self.runCode()
        else:
            self.runCode()
    
    def runCode(self):
        if self.check():
            self.values['board_size'] = self.board_size.currentIndex() + 2
            if self.values['solver'] == 'auto':      
                self.values['algorithm'] = algorithm[self.algorithm.currentIndex()]
                n, grids = generate(self.values['board_size'])
                _, self.grid = format2Gui(n, grids)
                n, lines = format2Solver(self.values['board_size'], grids)
                self.kenken = KenKen(n, lines)
                self.game_kenken = CSP(self.kenken.variables, self.kenken.domains, self.kenken.neighbors, self.kenken.kenken_constraint)
                self.kenken.add_CSP(self.game_kenken)
                soln = []
                if self.values['algorithm'] == 'BT':
                    soln = backtracking_search(self.game_kenken)
                if self.values['algorithm'] == 'FC':
                    soln = backtracking_search(self.game_kenken, inference=forward_checking)
                if self.values['algorithm'] == 'MAC':
                    soln = backtracking_search(self.game_kenken, inference=mac)
                # self.kenken.display(backtracking_search(self.game_kenken), n)
                try:
                    board = Board(
                        solver=self.values['solver'], 
                        n=self.values['board_size'], 
                        algorithm=self.values['algorithm']
                    )
                    board.get_inputs(self.grid)
                    self.board = True
                    board.run(soln = self.kenken.format_soln(soln, n))
                except:
                    pass
            elif self.values['solver'] == 'user':
                # try:
                    board = Board(n=self.values['board_size'])
                    n, grids = generate(self.values['board_size'])
                    _, self.grid = format2Gui(n, grids)
                    n, lines = format2Solver(self.values['board_size'], grids)
                    self.kenken = KenKen(n, lines)
                    self.game_kenken = CSP(self.kenken.variables, self.kenken.domains, self.kenken.neighbors, self.kenken.kenken_constraint)
                    self.kenken.add_CSP(self.game_kenken)
                    soln = backtracking_search(self.game_kenken, inference=forward_checking)
                    solver = []
                    for i in range(n):
                        sub = []
                        for j in range(n):
                            print(soln[f'K{i}{j}'], end=' ')
                            sub.append(soln[f'K{i}{j}'])
                        print()
                        solver.append(sub)
                    board.get_inputs(self.grid)
                    board.set_output(solver)
                    board.run()
                    self.board = False
                # except Exception as e:
                #     print(e)
        else:
            print('Complete all inputs')
    