import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self,e):
        self._model.buildGraphPesato()
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("grafo correttamente creato"))
        #adesso posso abilutare il bottone per trovare raggiungibili, lo faccio perchè così son sicuro che il grafo è stato creato
        self._view.btnCalcola.disabled = False
        self._view.btnCercaPercorso.disabled = False


        self._view.lst_result.controls.append(ft.Text(f"grafo contiene: {self._model.getNumNodi()} nodi"))
        self._view.lst_result.controls.append(ft.Text(f"grafo contiene: {self._model.getNumArchi()} archi"))

        self._view.update_page()




    def handleCercaRaggiungibili(self,e):
        if self._fermataPartenza is None:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Partenza di Fermata non selezionata"))
            self._view.update_page()
            return
        #se tutto va bene
        nodes= self._model.getBFSNodesFromEdges(self._fermataPartenza)
        self._view.lst_result.controls.clear()
        #stampo risultato
        self._view.lst_result.controls.append(ft.Text(f" raggiungibili da {self._fermataPartenza}"))
        for node in nodes:
            self._view.lst_result.controls.append(ft.Text(node))
        self._view.update_page()

    def loadFermate(self, dd: ft.Dropdown()):
        fermate = self._model.fermate

        if dd.label == "Stazione di Partenza":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Partenza))
        elif dd.label == "Stazione di Arrivo":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Arrivo))

    def read_DD_Partenza(self,e):
        print("read_DD_Partenza called ")
        if e.control.data is None:
            self._fermataPartenza = None
        else:
            self._fermataPartenza = e.control.data

    def read_DD_Arrivo(self,e):
        print("read_DD_Arrivo called ")
        if e.control.data is None:
            self._fermataArrivo = None
        else:
            self._fermataArrivo = e.control.data

#per stampare il percorso minimo
    def handleCercaPercorso(self,e):
        if self._fermataArrivo.value is None or self._fermataPartenza.value is None:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Attenzione,selezionare una fermata di partenza e di arrivo"))
            self._view.update_page()
            return
        totTime,path= self._model.getShortestPath(self._fermataPartenza,self._fermataArrivo)

        if path== []:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("non ho trovato cammino minimo"))
            self._view.update_page()
            return
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"ho trovato un cammino tra{self._fermataPartenza} e {self._fermataArrivo} e impiega {totTime} minuti"))
        for n in path:
            self._view.lst_result.controls.append(ft.Text(n))

        self._view.update_page()
