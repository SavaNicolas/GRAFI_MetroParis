from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate() #lista con le fermate
        #creo grafo
        self._grafo= nx.DiGraph()
        # mappa di fermate
        self.idMapFermate={}
        for f in self._fermate:
            self.idMapFermate[f.id_fermata] = f

    def buildGraphPesato(self):
        #aggiungiamo i nodi(li ho nelle fermate)
        self._grafo.add_nodes_from(self._fermate)
        #aggiungo archi
        self.addEdgesPesati()


    def addEdgesPesati(self):
        self._grafo.clear_edges()
        allEdges= DAO.allEdges()
        for edge in allEdges:
            u = self.idMapFermate[edge.id_stazP]
            v= self.idMapFermate[edge.id_stazA]
            #se l'arco già c'era aumento il peso dell'arco di 1
            if self._grafo.has_edge(u, v):
                self._grafo[u][v]['weight'] += 1
                #per contare quante partenze e arrivi uguali ci sono, usando linee diverse:
                # con la query avrei fatto il count con order by id_partenza, id_arrivo(devono stare anche nel group by)
            else:
                self._grafo.add_edge(u, v, weight=1)

    def addEdges_Pesati_lineeDiverse(self):
        """il grafo è pesato e il suo peso rappresenta il numero di linee diverse che connettono le due fermate"""
        allEdges = DAO.allEdgesPesati(self.idMapNodes) #lista di archi che hanno anche il peso come attributo
        for edge in allEdges:
            nodo_1 = edge.nodo1
            nodo_2 = edge.nodo2
            peso= edge.peso
            if self._grafo.has_edge(nodo_1, nodo_2):  # controllo se esiste già l'arco
                continue
            else:
                self._grafo.add_edge(nodo_1, nodo_2, weight=peso)

    def getArchiPesoMaggiore(self):
        #filtra archi con pesi maggiori di 1
        edges= self._grafo.edges(data=True)
        res=[]
        for e in edges:
            if self._grafo.has_edge(e[0], e[1])["weight"]>1:
                res.append(e)
        return res



    def buildGraph(self):
        #aggiungiamo i nodi(li ho nelle fermate)
        self._grafo.add_nodes_from(self._fermate)
        #aggiungo archi
        self.addEdges3()

    def addEdges1(self):
        """
        aggiungo gli archi con doppio ciclo sui nodi e testando se per
        ogni coppia esiste una connessione(troppo lento
        """
        # aggiungiamo gli archi, confrontando uno ad uno
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasConnessione(u, v):
                    self._grafo.add_edge(u, v)

    def addEdges2(self):
        """
        ciclo una sola volta e faccio una query per trovare tutti i vicini!!!(più veloce)
        """
        for u in self._fermate:
            for connessione in DAO.getVicini(u):
                v= self.idMapFermate[connessione.id_stazA]
                self._grafo.add_edge(u, v)

    def addEdges3(self):
        """
        query che mi da tutte le connessioni e ciclo in pyton(ancora + veloce)
        """
        allEdges= DAO.allEdges()
        for edge in allEdges:
            u = self.idMapFermate[edge.id_stazP]
            v= self.idMapFermate[edge.id_stazA]
            if self._grafo.has_edge(u,v):  # controllo se esiste già l'arco
                continue
            else:
                self._grafo.add_edge(u, v)

    #visito grafo
    def getBFSNodesFromTree(self,source):
       #nodi raggiungibili da source
        tree=nx.bfs_tree(self._grafo,source) #ritorna un albero orientato
        archi=list(tree.edges())
        nodi=list(tree.nodes())
        return nodi[1:] #perchè non ci serve il nodo source
        #man mano mi allontano dal nodo source

    def getBFSNodesFromEdges(self,source):
        #trovo i nodi dagli archi
        archi=nx.bfs_edges(self._grafo,source) #lista di tuple(partenza,arrivo)
        res=[]
        for u,v in archi:
            res.append(v) #solo i nodi di arrivo
        return res

    def getDFSNodesFromTree(self,source):
        tree=nx.dfs_tree(self._grafo,source)
        archi=list(tree.edges())
        nodi=list(tree.nodes())
        return nodi[1:]
        #ordine diverso da bfs perchè va sempre con l'adiacente


    def getNumNodi(self):
        return len(self._grafo.nodes())

    def getNumArchi(self):
        return len(self._grafo.edges())


    @property
    def fermate(self):
        return self._fermate
