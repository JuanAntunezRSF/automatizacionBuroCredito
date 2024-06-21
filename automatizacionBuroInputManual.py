'''
Created on Jun 21, 2024

@author: Juan Manuel Antunez
'''

def matriz1():
    print("\nMatriz 1")
    numCuentas = input("¿cuántas cuentas tiene?")
    numCuentas = int(numCuentas)
    ans = {}
    finalAns = "No se cuenta"
    if numCuentas == 1:
        solicitante = input("es un solicitante válido?")
        if solicitante != "v":
            ans[0] = "-"
        else:
            periodo = input("cuantos meses?")
            periodo = int(periodo)
            mop = input("cuál es el mop de la cuenta?")
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
            solicitante = input("es un solicitante válido?")
            if solicitante != "v":
                ans[c] = "-"
                continue
            mop = input("cuál es el mop de la cuenta?")
            if mop in ["96", "97", "99"]:
                ans[c] = "R"
                continue
            mop = int(mop)
            periodo = input("cuantos meses?")
            periodo = int(periodo)
            if 0 < periodo <= 3:
                if mop > 2:
                    ans[c] = "R"
                else:
                    ans[c] = "A"
            elif periodo <= 6:
                if mop > 3:
                    ans[c] = "R"
                else:
                    ans[c] = "A"
            elif periodo <= 12:
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

def matriz2():
    print("\nMatriz 2")
    finalAns = "?"
    ans = {}
    ingreso = input("cuánto gana?")
    ingreso = int(ingreso)
    if ingreso < 2000:
        ans["ingreso"] = "R"
    edad = input("cuál es su edad?")
    edad = int(edad)
    if edad < 18 or edad >= 70:
        ans["edad"] = "R"
    tipoVivienda = input("Tipo de vivienda (r - rentada / p - propia)?")
    if tipoVivienda == "r" or tipoVivienda == "rentada":
        finalAns = "?"
    elif tipoVivienda == "p" or tipoVivienda == "propia":
        actividadEconomica = input("Cuál es tu actividad económica (e - empleado / p - propio)?")
        if actividadEconomica == "p" or actividadEconomica == "propio":
            antiguedadEmpleo = input("Cuánto tiempo tienes trabajando en tu empleo (meses)?")
            antiguedadEmpleo = int(antiguedadEmpleo)
            if antiguedadEmpleo < 12:
                ans["antiguedadEmpleo"] = "R"
            elif antiguedadEmpleo >= 12:
                finalAns = "?"
        elif actividadEconomica == "e" or actividadEconomica == "empleado":
            trabajaPlataforma = input("Trabaja en alguna plataforma (s / n)?")
            if trabajaPlataforma == "s":
                finalAns = "?"
            else:
                antiguedadEmpleo = input("Cuánto tiempo tienes trabajando en tu empleo (meses)?")
                antiguedadEmpleo = int(antiguedadEmpleo)
                if antiguedadEmpleo < 6:
                    ans["antiguedadEmpleo"] = "R"
                elif antiguedadEmpleo >= 6:
                    comprobanteIngresos = input("Tiene comprobante de ingresos (s / n)?")
                    if comprobanteIngresos == "s":
                        altoRiesgo = input("Su actividad es de alto riesgo (s / n)?")
                        if altoRiesgo == "s":
                            ans["altoRiesgo"] = "R"
                        else:
                            finalAns = "?"
                    else:
                        finalAns = "?"
    
    print("\n")
    for a in ans:
        print("validación de " + a + " resultó en Rechazo")
    print("\nveredicto final de la matriz 2: " + finalAns)

matriz1()
#matriz2()

