from tkinter import *
import EPI_Banco
#from EPI_UI import tv_Funcionarios          #abrindo duas janelas
from EPI_Equipamento import EPI


class Funcionario:
    Nome=""
    Função=""

    def __init__(self, VNome,VFunção):
        self.Nome=VNome
        self.Função=VFunção

ListaFuncionarios=[]

def CriarFuncionario(nome,função):
    try:
        if(len(nome) != 0 and len(função) != 0):
            f=Funcionario(nome,função)
            vsql="INSERT INTO tb_Funcionarios (T_NOMEFUNCIONARIO, T_FUNÇÃO) VALUES ('"+f.Nome+"','"+f.Função+"')"
            EPI_Banco.dml(vsql)   

            ListaFuncionarios.append(f)
    except:
        print("Favor preencher todos os campos")
    finally:
        for x in ListaFuncionarios:
            print(x.Nome)