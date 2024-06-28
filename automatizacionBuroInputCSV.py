'''
Created on Jun 21, 2024

@author: ti
copiar los json de base de datos para la tabla 
select 

 buro_credito_consulta.id_consulta 
,buro_credito_consulta.id_usuario 
,buro_credito_consulta.id_solicitud 
,buro_credito_consulta.id_sucursal 
#,administracion_sucursales.sucursal 
,core_catalogo_origen.origen 
#,prospecto_web_solicitud.id_origen 
#,buro_credito_consulta.estatus 
#,buro_credito_consulta.curp
,buro_credito_consulta.exito 
,buro_credito_consulta_sc.microfinanciera 
,date(buro_credito_consulta_sc.fecha_registro) as fecha_registro 
,buro_credito_consulta_sc.fecha_registro
,buro_credito_consulta.cadena_respuesta 
,buro_credito_consulta.folio_consulta 

from buro_credito_consulta 

left join buro_credito_consulta_sc
on buro_credito_consulta.id_consulta = buro_credito_consulta_sc.id_consulta 

left join administracion_sucursales 
on administracion_sucursales.id_sucursal = buro_credito_consulta.id_sucursal

left join prospecto_web_solicitud 
on prospecto_web_solicitud.id_solicitud = buro_credito_consulta.id_solicitud

left join credito_solicitud_origen 
on credito_solicitud_origen.id_solicitud = prospecto_web_solicitud.id_solicitud 

left join core_catalogo_origen 
on core_catalogo_origen.id_origen = prospecto_web_solicitud.id_origen 

where true 
and administracion_sucursales.id_sucursal = 179
and date(buro_credito_consulta_sc.fecha_registro) between '2024-05-31'  and '2024-05-31'  ;
'''

from datetime import date
import csv

data = {}
data2 = {}
dataTemp = {}
monthsToNumber = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}
numbersToMonth = {1: "ene", 2: "feb", 3: "mar", 4: "abr", 5: "may", 6: "jun", 7: "jul", 8: "ago", 9: "sep", 10: "oct", 11: "nov", 12: "dic"}
today = date.today()
tm = today.month
ty = today.year
lym = 1 if tm + 1 == 13 else tm + 1
lyy = ty - 1
def readData():
    with open('campos_matriz1.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        i = 0
        for row in csv_reader:
            data[i] = row
            i += 1
    trimData()
    getPeriodo()
            
    with open('campos_matriz2.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data2[row[0]] = row[1]
        if "referencias" in data2:
            data2["referencias"] = data2["referencias"].split("-")

def trimData():
    flag = False
    for row in dict(data):
        if data[row][0] == "#" or flag:
            flag = True
            del data[row]

def getPeriodo():
    for ind in data:
        if data[ind][0] in ["RSF", "V"]:
            per1 = data[ind][3]
            per2 = data[ind][4]
            m1 = monthsToNumber[per1[:3]]
            a1 = int(per1[3:])
            m2 = monthsToNumber[per2[:3]]
            a2 = int(per2[3:])

            if m2 >= m1:
                ad = a2 - a1
                md = m2 - m1
                md += ad * 12
            else:
                ad = a2 - a1
                if ad >= 1:
                    ad -= 1
                    md = 12 + m2 - m1
                md += ad * 12
            data[ind][3] = md + 1
            
            if a2 > lyy or (a2 == lyy and m2 >= lym):
                if a1 > lyy or (a1 == lyy and m1 >= lym):
                    data[ind][2] = md + 1
                else:
                    if m2 >= lym:
                        ad = a2 - lyy
                        md = m2 - lym
                        md += ad * 12
                    else:
                        ad = a2 - lyy
                        if ad >= 1:
                            ad -= 1
                            md = 12 + m2 - lym
                    data[ind][2] = md + 1
            else:
                data[ind][2] = 0
            
def comparePeriods(per1, per2):
    m1 = monthsToNumber[per1[:3]]
    a1 = int(per1[3:])
    m2 = monthsToNumber[per2[:3]]
    a2 = int(per2[3:])
    if a2 > a1:
        return per2
    elif a1 > a2:
        return per1
    else:
        if m2 > m1:
            return per2
    return per1

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
                ans[i] = [mop, c[4], c[5]]
                i += 1
                if sumc >= 3:
                    cliente = "s"
            else:
                ans[i] = ["-"]
                i += 1
    
    if cliente == "s":
        ansPeriodo = {}
        for a in ans:
            if ans[a][0] != "-":
                ansPeriodo[a] = ans[a]
            else:
                ans[a] = "-"
        ansSaldos = {}
        for a in ansPeriodo:
            if int(ans[a][2]) > 0:
                ansSaldos[a] = ans[a]
        if len(ansSaldos) == 0:
            mostRecentDate = numbersToMonth[lym] + str(lyy)
            for a in ansPeriodo:
                mostRecentDate = comparePeriods(mostRecentDate, ans[a][1])
            for a in ansPeriodo:
                if ans[a][1] != mostRecentDate:
                    ans[a] = "-"
                else:
                    if ans[a][0] <= 3:
                        ans[a] = "A"
                    else:
                        ans[a] = "R"
        else:
            for a in ans:
                ans[a] = "-"
            for a in ansSaldos:
                if ansSaldos[a][0] <= 3:
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

def matriz2():
    print("\nMatriz 2")
    finalAns = "Aprobado"
    ans = {}
    if 18 < int(data2["edad"]) < 70:
        ans["edad"] = "A"
    else:
        ans["edad"] = "R"
        finalAns = "Rechazado"
    
    if int(data2["antiguedad_empleo"]) < 6:
        ans["arraigo laboral"] = "R"
        finalAns = "Rechazado"
    else:
        if data2["actividad_economica"] == "propio" and int(data2["antiguedad_empleo"]) < 12:
            ans["arraigo laboral"] = "R"
            finalAns = "Rechazado"
        else:
            ans["arraigo laboral"] = "A"
    
    if data2["comprobante_ingresos"] == "si":
        ans["comprobante ingresos"] = "A"
    else:
        ans["comprobante ingresos"] = "R"
        finalAns = "Rechazado"
    
    if data2["porta_armas"] == "si":
        ans["porta armas"] = "R"
        finalAns = "Rechazado"
    else:
        ans["porta armas"] = "A"
    
    """
    if len(data2["referencias"]) < 6:
        ans["referencias"] = "R"
        finalAns = "Rechazado"
    else:
        ans["referencias"] = "A"
    """
    
    if int(data2["ingreso"]) < 2000:
        ans["ingreso"] = "R"
        finalAns = "Rechazado"
    else:
        ans["ingreso"] = "A"
    
    if data2["tipo_empleo"] in ["informal", "formal"]:
        ans["tipo_empleo"] = "A"
    else:
        ans["tipo_empleo"] = "R"
        finalAns = "Rechazado"
    
    ans["antiguedad domicilio"] = "A"
        
    for a in ans:
        if ans[a] == "R":
            print(a + ":   No cumple")
        else:
            print(a + ":   Cumple")
    
    #print("\nveredicto final de la matriz 2: " + finalAns)
    print("\nveredicto final de la matriz 2: Pendiente por recibir información")

readData()
matriz1()
#matriz2()
print(data)
#print(data2)
