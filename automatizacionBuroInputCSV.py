'''
Created on Jun 21, 2024

@author: ti
'''
import csv

data = {}
def readData():
    with open('prueba.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        #print(csv_reader)
        i = 0
        for row in csv_reader:
            data[i] = row
            i += 1

def matriz1():
    print("\nMatriz 1")
    ans = {}
    finalAns = "No se cuenta"
    locales = []
    cliente = ""
    for ind in data:
        if data[ind][0] == "RSF":
            locales.append(data[ind])
            cliente = "s"
    
    if cliente == "s":
        cliente = "n"
        sumc = 0
        i = 0
        for c in locales:
            periodo = c[2]
            periodo = int(periodo)
            meses = c[3]
            meses = int(meses)
            mop = c[1]
            mop = int(mop)
            sumc += meses
            if 0 < periodo <= 12:
                ans[i] = mop
                i += 1
                if sumc >= 3:
                    cliente = "s"
    
    if cliente == "s":
        for a in ans:
            if ans[a] <= 3:
                ans[a] = "A"
            else:
                ans[a] = "R"
    else:
        ans = {}
        numCuentas = len(data)
        if numCuentas == 1:
            solicitante = data[0][0]
            if not solicitante in ["V", "RSF"]:
                ans[0] = "-"
            else:
                periodo = data[0][2]
                periodo = int(periodo)
                mop = data[0][1]
                mop = int(mop)
                if 0 < periodo <= 12:
                    if mop <= 3:
                        ans[0] = "A"
                    else:
                        ans[0] = "R"
                else:
                    if mop in [96, 97, 99]:
                        ans[0] = "R"
                    else:
                        ans[0] = "-"
        elif numCuentas<1:
            finalAns = "Aprobado"
        else:
            for c in range(numCuentas):
                solicitante = data[c][0]
                if not solicitante in ["V", "RSF"]:
                    ans[c] = "-"
                    continue
                mop = data[c][1]
                print(mop)
                if mop in ["96", "97", "99"]:
                    ans[c] = "R"
                    continue
                mop = int(mop)
                periodo = data[c][2]
                periodo = int(periodo)
                if 0 < periodo <= 3:
                    if mop > 2:
                        ans[c] = "R"
                    else:
                        ans[c] = "A"
                elif 0 < periodo <= 6:
                    if mop > 3:
                        ans[c] = "R"
                    else:
                        ans[c] = "A"
                elif 0 < periodo <= 12:
                    if mop > 4:
                        ans[c] = "R"
                    else:
                        ans[c] = "A"
                else:
                    ans[c] = "-"
        print("\n\nel numero de cuentas es: " + str(numCuentas))
        
        
    for a in ans:
        if ans[a] == "-":
            print("cuenta " + str(a + 1) + " no cuenta")
        elif ans[a] == "R":
            finalAns = "Rechazado"
            print("cuenta " + str(a + 1) + " es un rechazo")
        else:
            if finalAns != "Rechazado":
                finalAns = "Aprobado"
            print("cuenta " + str(a + 1) + " es una aprobación")
            
    print("\nveredicto final de la matriz 1: " + finalAns)

readData()
matriz1()
print(data)
