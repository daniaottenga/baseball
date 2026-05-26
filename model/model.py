import copy
import itertools
import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._teams = []
        self._idMapTeams = {}
        self._bestPath = []
        self._bestObj = 0


    def getAllYears(self):
        return DAO.getAllYears()


    def getTeamsOfYear(self, year):
        self._teams = DAO.getTeamsOfYear(year)
        return self._teams


    def creaGrafo(self, year):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._teams)

        '''
        for u in self._grafo.nodes:
            for v in self._grafo.nodes:
                if u != v:
                    self._grafo.add_edge(u, v)
        '''

        myedges = list(itertools.combinations(self._teams, 2))
        self._grafo.add_edges_from(myedges)

        self._idMapTeams = {t.ID : t for t in self._grafo.nodes} # mappo l'id tra tutti i nodi del grafo

        mapSalary = DAO.getSalariesOfTeam(year, self._idMapTeams)
        for e in self._grafo.edges: # ciclo sugli archi (tupla nodo di partenza e di arrivo)
            self._grafo[e[0]][e[1]]['weight'] = mapSalary[e[0]] + mapSalary[e[1]]



    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)


    def getViciniGrafo(self, source):
        vicini = self._grafo.neighbors(source)
        viciniTuples = []

        for v in vicini:
            viciniTuples.append((v, self._grafo[source][v]['weight'])) # ogni riga della lista è una coppia
            # vicino-peso

        viciniTuples.sort(key = lambda x: x[1]) # li ordino per peso
        return viciniTuples


    def getPath(self, v0):
        self._bestPath = []
        self._bestObj = 0

        parziale = [v0] # so che da v0 ci devo partire
        for v in self._grafo.neighbors(v0):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

        return self._bestPath, self._bestObj


    def getPathV2(self, v0):
        self._bestPath = []
        self._bestObj = 0

        parziale = [v0]
        vicini = self.getViciniGrafo(v0)
        parziale.append(vicini[0][0])
        self._ricorsioneV2(parziale)

        return self._bestPath, self._bestObj


    def _ricorsione(self, parziale): # troppo lunga
        # condizione di ottimalità
        if self._score(parziale) > self._bestObj:
            self._bestObj = self._score(parziale)
            self._bestPath = copy.deepcopy(parziale)

        # condizine di terminazione (non c'è)
        # ricorsione
        for v in self._grafo.neighbors(parziale[-1]):
            if (self._grafo[parziale[-1]][v]['weight'] < self._grafo[parziale[-2]][parziale[-1]]['weight']
                    and v not in parziale):
                # lo posso aggiungere solo se il peso è minore del peso dell'arco prima e non ripeto i nodi
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()


    def _ricorsioneV2(self, parziale):
        # condizione di ottimalità
        if self._score(parziale) > self._bestObj:
            self._bestObj = self._score(parziale)
            self._bestPath = copy.deepcopy(parziale)

        # condizine di terminazione (non c'è)
        # ricorsione (prendo i vicini, li ordino per peso e li aggiungo)
        vicini = self.getViciniGrafo(parziale[-1])

        for v in vicini:
            if v[1] < self._grafo[parziale[-2]][parziale[-1]]['weight'] and v[0] not in parziale:
                # lo posso aggiungere solo se il peso è minore del peso dell'arco prima e non ripeto i nodi
                parziale.append(v[0])
                self._ricorsioneV2(parziale)
                parziale.pop()
                return # una volta trovato il migliore evito di esplorare tutte le altre strade con valore minore


    def _score(self, parziale):
        score = 0
        for i in range(0, len(parziale) - 1):
            score += self._grafo[parziale[i]][parziale[i + 1]]['weight'] # gli arriva una lista di nodi connessi
            # da archi e per ogni connessione aggiunge il valore del peso a score

        return score
