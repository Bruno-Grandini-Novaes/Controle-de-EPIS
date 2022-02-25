from tkinter import *
import EPI_Banco

class EPI:
    EPInome=""
    EPIvalidade=1

    def __init__(self,nome,validade):
        self.EPInome=nome
        self.EPIvalidade=validade

ListaEPIs = []

def CriarNovoEPI(Enome,Evalidade):

    try:
        if(len(Enome) != 0 and len(Evalidade) != 0):
            epi=EPI(Enome,Evalidade)
            vsql="INSERT INTO tb_EPI (T_EQUIPAMENTO, N_VALIDADE) VALUES ('"+epi.EPInome+"','"+epi.EPIvalidade+"')"
            EPI_Banco.dml(vsql)

            ListaEPIs.append(epi)

    except:
        print("digite nome e validade")
    finally:
        print(Enome,Evalidade)
        for x in ListaEPIs:
                print(x.EPInome)
