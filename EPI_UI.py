from distutils import command
from ipaddress import collapse_addresses
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import re
from typing import final

import EPI_Equipamento
import EPI_Funcionario
import EPI_Banco




def AtualizaçãoInicial():
    for item in tv_Funcionarios.get_children():
        tv_Funcionarios.delete(item)

    for item in tv_Funcionarios2.get_children():
        tv_Funcionarios2.delete(item)
    
    for item in tv_EPIS.get_children():
        tv_EPIS.delete(item)

    for item in tv_EPIS2.get_children():
        tv_EPIS2.delete(item)

   
    vsql="SELECT * FROM tb_Funcionarios"
    consulta=EPI_Banco.dql(vsql)
    
    for (n,f) in consulta:
        tv_Funcionarios.insert("","end",values=(n,f))
    
    
    vsql="SELECT * FROM tb_Funcionarios"
    consulta=EPI_Banco.dql(vsql)
    
    for (n,f) in consulta:
        tv_Funcionarios2.insert("","end",values=(n,f))

    
    vsql="SELECT * FROM tb_EPI"
    consulta=EPI_Banco.dql(vsql)
    
    for (n,f) in consulta:
        tv_EPIS.insert("","end",values=(n,f))
    
    
    vsql="SELECT * FROM tb_EPI"
    consulta=EPI_Banco.dql(vsql)
    
    for (n,f) in consulta:
        tv_EPIS2.insert("","end",values=(n,f))

def DeletarFuncionario():
    try:   
        FuncionarioDeletar=tv_Funcionarios.selection()[0]
        FuncionarioDeletar=tv_Funcionarios.item(FuncionarioDeletar,"values")
        FuncionarioDeletar=str(FuncionarioDeletar[0])    
        vsql="DELETE FROM tb_Funcionarios WHERE T_NOMEFUNCIONARIO='"+FuncionarioDeletar+"'"    
        EPI_Banco.dml(vsql)

        vsql="DROP TABLE '"+FuncionarioDeletar+"'"    
        EPI_Banco.dml(vsql)
        AtualizaçãoInicial()
        messagebox.showinfo(title="Operação bem sucedida",message="Funcionario removido do sistema")
    except:
        messagebox.showerror(title="Error",message="Favor selecionar um funcionario da lista para remover do sistema")

    

def DeletarEPI():
    try:   
        EPIDeletar=tv_EPIS.selection()[0]
        EPIDeletar=tv_EPIS.item(EPIDeletar,"values")
        EPIDeletar=str(EPIDeletar[0])
        print(EPIDeletar)
        vsql="DELETE FROM tb_EPI WHERE T_EQUIPAMENTO='"+EPIDeletar+"'"
        EPI_Banco.dml(vsql)
        AtualizaçãoInicial()
        messagebox.showinfo(title="Operação bem sucedida",message="EPI removido do sistema")
    except:
        messagebox.showerror(title="Error",message="Favor selecionar um EPI da lista para remover do sistema")

def GerarRelatorioFuturo():
    try:

        for item in tv_RelatorioFuturo.get_children():
            tv_RelatorioFuturo.delete(item)

        EPISVencidosFuturo=[]
        EPISValidosFuturo=[]
        dataatual=DataRelatorio.get()
        DataRE=re.split("/",str(dataatual))  
    
        res=datetime.datetime(int(DataRE[2]),int(DataRE[1]),int(DataRE[0]))
        res += datetime.timedelta(days=30)

        vsql="SELECT * FROM tb_Funcionarios"
        consulta1=EPI_Banco.dql(vsql)
        

        for x in consulta1:   
            try:     
                vsql="SELECT * FROM '"+str(x[0])+"'"
                consulta2=EPI_Banco.dql(vsql)

                for y in consulta2:
                    nomeepi=y[0]
                    datavencimento=y[2]
                    res2=datetime.datetime(int(datavencimento[0:4]),int(datavencimento[5:7]),int(datavencimento[8:10]))               
                

                    if res2>res:
                        EPISValidosFuturo.append(nomeepi)
                        
                        
                    if res2<res:
                        EPISVencidosFuturo.append(nomeepi)
                        
                        
                    
                
            except:
                print()
            finally:
                tv_RelatorioFuturo.insert("","end",values=(x[0],x[1],EPISValidosFuturo,EPISVencidosFuturo))
                EPISValidosFuturo.clear()
                EPISVencidosFuturo.clear()
                DataFuturaData.config(text=res)
    except:
        messagebox.showerror(title="Error",message="Favor informar uma data valida")

def GerarRelatorio():
    try:

        for item in tv_Relatorio.get_children():
            tv_Relatorio.delete(item)

        EPISVencidos=[]
        EPISValidos=[]
        dataatual=DataRelatorio.get()
        DataRE=re.split("/",str(dataatual))  
    
        res=datetime.datetime(int(DataRE[2]),int(DataRE[1]),int(DataRE[0]))


        vsql="SELECT * FROM tb_Funcionarios"
        consulta1=EPI_Banco.dql(vsql)
        

        for x in consulta1:   
            try:     
                vsql="SELECT * FROM '"+str(x[0])+"'"
                consulta2=EPI_Banco.dql(vsql)

                for y in consulta2:
                    nomeepi=y[0]
                    datavencimento=y[2]
                    res2=datetime.datetime(int(datavencimento[0:4]),int(datavencimento[5:7]),int(datavencimento[8:10]))               
                

                    if res2>res:
                        EPISValidos.append(nomeepi)
                        
                        
                    if res2<res:
                        EPISVencidos.append(nomeepi)
                        
                        
                    
                
            except:
                print()
            finally:
                tv_Relatorio.insert("","end",values=(x[0],x[1],EPISValidos,EPISVencidos))
                EPISValidos.clear()
                EPISVencidos.clear()
                GerarRelatorioFuturo()
    except:
        messagebox.showerror(title="Error",message="Favor informar uma data valida")

def EntregarEPI():
    try:
        FuncionarioSelecionado=tv_Funcionarios2.selection()[0]
        Valores=tv_Funcionarios2.item(FuncionarioSelecionado,"values")
        NomeEntregar=Valores[0]

        vsql="CREATE TABLE '"+NomeEntregar+"'(EPINOME VARCHAR PRIMARY KEY, DATAENTREGUE INTEGER(30), DATAVENCIMENTO INTEGER (30));"
        EPI_Banco.dml(vsql)

        EPISelecionados=tv_EPIS2.selection()
        for x in EPISelecionados:
            Valores=tv_EPIS2.item(x,"values")
            n=Valores[0]
            
            vsql="SELECT * FROM tb_EPI WHERE T_EQUIPAMENTO='"+n+"'"
            validadeEPI=EPI_Banco.dql(vsql)[0][1]        
            DataRE=re.split("/",str(DataEntrega.get()))    
    
            res=datetime.datetime(int(DataRE[2]),int(DataRE[1]),int(DataRE[0]))        
        
            DataValidade=res + datetime.timedelta(days=(validadeEPI))
            


            vsql="INSERT INTO '"+NomeEntregar+"' (EPINOME, DATAENTREGUE, DATAVENCIMENTO) VALUES ('"+n+"','"+DataEntrega.get()+"', '"+str(DataValidade)+"')"
            EPI_Banco.dml(vsql)
    except:
        messagebox.showerror(title="Error",message="Favor informar uma data valida")
    
        


def AtualizarFuncionarios():
    try:
        for item in tv_Funcionarios.get_children():
            tv_Funcionarios.delete(item)

        EPI_Funcionario.CriarFuncionario(NovoNome.get(),NovaFunção.get())
        vsql="SELECT * FROM tb_Funcionarios"
        consulta=EPI_Banco.dql(vsql)
        
        for (n,f) in consulta:
            tv_Funcionarios.insert("","end",values=(n,f))

        #------
        for item in tv_Funcionarios2.get_children():
            tv_Funcionarios2.delete(item)

        EPI_Funcionario.CriarFuncionario(NovoNome.get(),NovaFunção.get())
        vsql="SELECT * FROM tb_Funcionarios"
        consulta=EPI_Banco.dql(vsql)
        
        for (n,f) in consulta:
            tv_Funcionarios2.insert("","end",values=(n,f))
    except:
        messagebox.showerror(title="Error",message="Favor informar nome e função")
def AtualizarEPIS():
    try:
        for item in tv_EPIS.get_children():
            tv_EPIS.delete(item)

        EPI_Equipamento.CriarNovoEPI(VNome1.get(),VDias1.get())
        vsql="SELECT * FROM tb_EPI"
        consulta=EPI_Banco.dql(vsql)
        
        for (n,f) in consulta:
            tv_EPIS.insert("","end",values=(n,f))

        #-------
        for item in tv_EPIS2.get_children():
            tv_EPIS2.delete(item)

        """EPI_Equipamento.CriarNovoEPI(VNome1.get(),VDias1.get())
        vsql="SELECT * FROM tb_EPI"
        consulta=EPI_Banco.dql(vsql)"""
        
        for (n,f) in consulta:
            tv_EPIS2.insert("","end",values=(n,f))
    except:
        messagebox.showerror(title="Error",message="Favor informar nome e validade")
   


App=Tk()
App.title("Gerenciador de EPI's")
#App.geometry("1728x972")
App.geometry("850x950")


Nb=ttk.Notebook(App)
Nb.place(x=0,y=0,width=1728,height=972)

Tb_Funcionarios=Frame(Nb)
Nb.add(Tb_Funcionarios,text="Funcionarios")

Tb_EPI=Frame(Nb)
Nb.add(Tb_EPI,text="EPIs")

Tb_Entregar=Frame(Nb)
Nb.add(Tb_Entregar,text="Entregar EPIS")

Tb_Relatorio=Frame(Nb)
Nb.add(Tb_Relatorio,text="Relatorio")

#-------------------------------------------------------
#EPI's

VNome1=StringVar()
VDias1=StringVar()


Titulo1=Label(Tb_EPI,text="Adionar novo EPI:")
Nome1=Label(Tb_EPI,text="Nome:")
Dias1=Label(Tb_EPI,text="Validade do EPI(dias):")
TodosEPIS=Label(Tb_EPI,text="Todos os EPIS:")


EntryNome1=Entry(Tb_EPI,textvariable=VNome1)
EntryDias1=Entry(Tb_EPI,textvariable=VDias1)

btnCriar=Button(Tb_EPI,text="Adicionar",command=AtualizarEPIS)
btnDeletarEPI=Button(Tb_EPI,text="Deletar EPI",command=DeletarEPI)

tv_EPIS=ttk.Treeview(Tb_EPI,columns=('nome','validade'),show='headings')
tv_EPIS.column('nome',minwidth=0,width=100)
tv_EPIS.column('validade',minwidth=0,width=100)
tv_EPIS.heading('nome',text="Nome:")
tv_EPIS.heading('validade',text="Validade(dias):")

Titulo1.grid(column=2,row=0,columnspan=2)
Nome1.grid(column=2,row=1)
Dias1.grid(column=3,row=1)

EntryNome1.grid(column=2,row=2)
EntryDias1.grid(column=3,row=2)

btnCriar.grid(column=2,row=3,columnspan=2)

TodosEPIS.grid(column=2,row=4,columnspan=2)
tv_EPIS.grid(column=2,row=5,columnspan=2)
btnDeletarEPI.grid(column=2,row=6,columnspan=2)
#-------------------------------------
#Funcionario

NovoNome=StringVar()
NovaFunção=StringVar()


TituloF1=Label(Tb_Funcionarios,text="Criar novo Funcionario:")
NomeFuncionario=Label(Tb_Funcionarios,text="Nome do Funcionario:")
FunçãoFuncionario=Label(Tb_Funcionarios,text="Função do Funcionario:")
TodosFuncionarios=Label(Tb_Funcionarios,text="Todos os Funcionarios:")

EntryNomeFuncionario=Entry(Tb_Funcionarios,textvariable=NovoNome)
EntryFunçãoFuncionario=Entry(Tb_Funcionarios,textvariable=NovaFunção)

btnCriarFuncionario=Button(Tb_Funcionarios,text="Adicionar",command=AtualizarFuncionarios)
btnDeletarFuncionario=Button(Tb_Funcionarios,text="Deletar",command=DeletarFuncionario)

tv_Funcionarios=ttk.Treeview(Tb_Funcionarios,columns=('nome','função'),show='headings')
tv_Funcionarios.column('nome',minwidth=0,width=100)
tv_Funcionarios.column('função',minwidth=0,width=100)
tv_Funcionarios.heading('nome',text="Nome:")
tv_Funcionarios.heading('função',text="Função:")



TituloF1.grid(column=2,row=0,columnspan=2)
NomeFuncionario.grid(column=2,row=1)
FunçãoFuncionario.grid(column=3,row=1)

EntryNomeFuncionario.grid(column=2,row=2)
EntryFunçãoFuncionario.grid(column=3,row=2)

btnCriarFuncionario.grid(column=2,row=3,columnspan=2)

TodosFuncionarios.grid(column=2,row=4,columnspan=2)
tv_Funcionarios.grid(column=2,row=5,columnspan=2)
btnDeletarFuncionario.grid(column=2,row=6,columnspan=2)

#----------------------------------------
#Entregar EPIS

DataEntrega=StringVar()

EntregarTitulo=Label(Tb_Entregar,text="Escolha um funcionario para atualizar os EPIs:")
EntregarData=Label(Tb_Entregar,text="Digite a data da entrega dos novos EPIs(ex:01/01/2022):")

EntryData=Entry(Tb_Entregar,textvariable=DataEntrega)

tv_Funcionarios2=ttk.Treeview(Tb_Entregar,columns=('nome','função'),show='headings')
tv_Funcionarios2.column('nome',minwidth=0,width=100)
tv_Funcionarios2.column('função',minwidth=0,width=100)
tv_Funcionarios2.heading('nome',text="Nome:")
tv_Funcionarios2.heading('função',text="Função:")

EscolherEPI=Label(Tb_Entregar,text="Escolha(selecione) quais EPIs o funcionario está recebendo:")

btn_entregar=Button(Tb_Entregar,text="Entregar",command=EntregarEPI)

tv_EPIS2=ttk.Treeview(Tb_Entregar,columns=('nome','validade'),show='headings')
tv_EPIS2.column('nome',minwidth=0,width=100)
tv_EPIS2.column('validade',minwidth=0,width=100)
tv_EPIS2.heading('nome',text="Nome:")
tv_EPIS2.heading('validade',text="Validade(dias):")


EntregarTitulo.grid(column=2,row=0,columnspan=2)
tv_Funcionarios2.grid(column=2,row=1,columnspan=2) 
EscolherEPI.grid(column=2,row=4)
tv_EPIS2.grid(column=2,row=5,columnspan=2)
btn_entregar.grid(column=2,row=6,columnspan=2)
EntregarData.grid(column=2,row=2)

EntryData.grid(column=2,row=3)

#----------------------------------------
#Relatorio
DataRelatorio=StringVar()

RelatorioTitulo=Label(Tb_Relatorio,text="Relatorio de Funcionarios na data de simulação atual:")
l_DataRelatorio=Label(Tb_Relatorio,text="Digite a data de simulação do relatorio(ex:10/01/2022):")

e_DataRelatorio=Entry(Tb_Relatorio,textvariable=DataRelatorio)

tv_Relatorio=ttk.Treeview(Tb_Relatorio,columns=('nome','função','epiaprovado','epireprovado'),show='headings')
tv_Relatorio.column('nome',minwidth=0,width=100)
tv_Relatorio.column('função',minwidth=0,width=100)
tv_Relatorio.column('epiaprovado',minwidth=0,width=300)
tv_Relatorio.column('epireprovado',minwidth=0,width=300)
tv_Relatorio.heading('nome',text="Nome:")
tv_Relatorio.heading('função',text="Função:")
tv_Relatorio.heading('epiaprovado',text="EPIs Validos:")
tv_Relatorio.heading('epireprovado',text="EPIs Vencidos:")

btn_relatorio=Button(Tb_Relatorio,text="Gerar Relatorio",command=GerarRelatorio)

RelatorioTitulo.grid(column=2,row=0)
tv_Relatorio.grid(column=2,row=1)
l_DataRelatorio.grid(column=2,row=2)
e_DataRelatorio.grid(column=2,row=3)
btn_relatorio.grid(column=2,row=4,columnspan=2)

#Relatorio Futuro
RelatorioFuturoTitulo=Label(Tb_Relatorio,text="Relatorio de Funcionarios futuro para planejamento de compras no proximo mês:")
DataFuturaTexto=Label(Tb_Relatorio,text="Data futura em simulação: ")
DataFuturaData=Label(Tb_Relatorio,text="")

tv_RelatorioFuturo=ttk.Treeview(Tb_Relatorio,columns=('nome','função','epiaprovado','epireprovado'),show='headings')
tv_RelatorioFuturo.column('nome',minwidth=0,width=100)
tv_RelatorioFuturo.column('função',minwidth=0,width=100)
tv_RelatorioFuturo.column('epiaprovado',minwidth=0,width=300)
tv_RelatorioFuturo.column('epireprovado',minwidth=0,width=300)
tv_RelatorioFuturo.heading('nome',text="Nome:")
tv_RelatorioFuturo.heading('função',text="Função:")
tv_RelatorioFuturo.heading('epiaprovado',text="EPIs Validos:")
tv_RelatorioFuturo.heading('epireprovado',text="EPIs Vencidos:")

RelatorioFuturoTitulo.grid(column=2,row=5)
DataFuturaTexto.grid(column=2,row=6)
DataFuturaData.grid(column=2,row=7)
tv_RelatorioFuturo.grid(column=2,row=8)


AtualizaçãoInicial()

App.mainloop()