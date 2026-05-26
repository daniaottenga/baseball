import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view

        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):
        if self._view._ddAnno.value is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Selezionare un anno dal menu",
                                                     color = "red"))
            self._view.update_page()
            return

        self._model.creaGrafo(self._view._ddAnno.value)
        n, m = self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(
            f"Grafo creato. Il grafo contiene {n} nodi e {m} archi",))
        self._view.update_page()


    def handleDettagli(self, e):
        if self._choiceTeams is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Selezionare un team dal menu",
                                                     color = "red"))
            self._view.update_page()
            return

        viciniTuple = self._model.getViciniGrafo(self._choiceTeams)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(
            f"Il nodo {self._choiceTeams} ha {len(viciniTuple)} vicini")) # deve essere sempre il numero di
        # nodi - 1 (29) perchè è completamente connesso
        self._view._txt_result.controls.append(ft.Text("Di seguito la lista dei vicini:"))

        for t in viciniTuple:
            self._view._txt_result.controls.append(ft.Text(f"{t[0]} - {t[1]}"))

        self._view.update_page()


    def handlePercorso(self, e):
        if self._choiceTeams is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Selezionare un team dal menu",
                                                     color = "red"))
            self._view.update_page()
            return

        percorso, valore = self._model.getPathV2(self._choiceTeams)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Di seguito la lista dei nodi percorsi (valore del percorso = {valore}: "))
        for p in percorso:
            self._view._txt_result.controls.append(ft.Text(f"{p}"))

        self._view.update_page()


    def fillDDYears(self):
        years = self._model.getAllYears()

        #yearsDD = []
        #for y in years:
        #    yearsDD.append(ft.dropdown.Option(y))

        yearsDD = list(map(lambda x: ft.dropdown.Option(x), years)) # applica la funzione all'iterable (lista)
        self._view._ddAnno.options = yearsDD
        self._view.update_page()


    def handleYearSelection(self, e):
        if self._view._ddAnno.value is None:
            self._view._txtOutSquadre.controls.clear()
            self._view._txtOutSquadre.controls.append(ft.Text("Selezionare un anno dal menu",
                                                     color = "red"))
            self._view.update_page()
            return

        teams = self._model.getTeamsOfYear(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(
            f"Per l'anno {self._view._ddAnno.value} sono iscritte al campionato "
            f"{len(teams)} squadre",
            color="green"))

        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(t))
            self._view._ddSquadra.options.append(
                ft.dropdown.Option(data = t,
                                    text = t.name,
                                    on_click = self.readDDTeams)
            )

        self._view.update_page()


    def readDDTeams(self, e):
        self._choiceTeams = e.control.data