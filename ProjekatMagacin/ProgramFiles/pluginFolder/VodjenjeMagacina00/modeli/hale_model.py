from PySide2 import QtCore
import os
import sqlite3
from ..sqlite_init import konekcija_ka_bazi
####################################################
#def konekcija_ka_bazi():
#    return sqlite3.connect('magacin.db')
####################################################

class HaleListModel(QtCore.QAbstractTableModel):

    def __init__(self):
        super().__init__()
        # matrica, redovi su liste, a unutar tih listi se nalaze pojedinacni podaci o korisniku iz imenika
        self._conn = konekcija_ka_bazi()
        self._c = self._conn.cursor()
        self._data = []
        self.ucitaj_podatke_iz_baze()

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 5 #fiksan br vracamo

    def data(self, index, role):
        element = self.get_element(index)
        if element is None:
            return None

        if role == QtCore.Qt.DisplayRole:
            return element

    def headerData(self, section, orientation, role):
        if orientation != QtCore.Qt.Vertical:
            if (section == 0) and (role == QtCore.Qt.DisplayRole):
                return "id"
            elif (section == 1) and (role == QtCore.Qt.DisplayRole):
                return "ime hale"
            elif (section == 2) and (role == QtCore.Qt.DisplayRole):
                return "tip hale"
            elif (section == 3) and (role == QtCore.Qt.DisplayRole):
                return "ukupan broj mesta"
            elif (section == 4) and (role == QtCore.Qt.DisplayRole):
                return "broj zauzetih mesta"

    def setData(self, index, value, role):
        try:
            if value == "":
                return False
            self._data[index.row()][index.column()] = value
            self.dataChanged()
            return True
        except:
            return False

    def flags(self, index):
        # ne damo da menja datum rodjenja (primera radi)
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        # sve ostale podatke korisnik moze da menja

    def get_element(self, index : QtCore.QModelIndex):
        if index.isValid():
            element = self._data[index.row()][index.column()]
            if element:
                return element
        return None

    def remove(self, indices):
        # za na osnovu indeksa, dobijamo njihove redove, posto za jedan red je vezano pet indeksa (za kolone)
        # pravimo skup koji ce dati samo jedinstvene brojeve redova
        # uklanjanje vrsimo od nazad, jer ne zelimo da nam brojevi redova nakon uklanjanja odu van opsega.
        indices = sorted(set(map(lambda x: x.row(), indices)), reverse=True)
        for i in indices:
            #### remove from DB
            temp_id = self.get_id_kliknute_hale(i)
            result = self._conn.execute("""DELETE FROM rashladne_hale WHERE rashladne_hale_id = :ID""" , {'ID' : temp_id} )
            self._conn.commit()
            result = self._conn.execute("""DELETE FROM proizvodi_hale WHERE rashladne_hale_id = :ID""" , {'ID' : temp_id} )
            self._conn.commit()
            ##################
            self.beginRemoveRows(QtCore.QModelIndex(), i, i)
            del self._data[i]
            self.endRemoveRows()

    def add(self, data : dict):
        self.beginInsertRows(QtCore.QModelIndex(), len(self._data), len(self._data))
        ######
        result = self._conn.execute(""" SELECT naziv_hale FROM tip_hale where tip_hale_id=:idHere;""", {'idHere':data['tipHaleID'] })
        resultTipNaziv = list(result.fetchall())
        self._conn.commit()
        ######
        self._data.append([data['haleID'], data['nazivHale'], resultTipNaziv[0][0], data['brMesta'], data['brZazuzetihMesta']])
        self.endInsertRows()

    def ucitaj_podatke_iz_baze(self): #ucitavamo podatke iz baze
        result = self._conn.execute(""" SELECT rashladne_hale_id, ime_hale, naziv_hale, ukupan_br_mesta, br_zauzetih_mesta
FROM rashladne_hale INNER JOIN tip_hale ON rashladne_hale.tip_hale_id = tip_hale.tip_hale_id;
        """)
        self._data = list(result.fetchall())
        self._conn.commit()
#todo delete
    def get_id_kliknute_hale(self, index):
        return self._data[index][0]
