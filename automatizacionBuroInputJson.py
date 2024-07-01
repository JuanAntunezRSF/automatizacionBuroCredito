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
import json

data = {}
data2 = {}
monthsToNumber = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}
numbersToMonth = {1: "ene", 2: "feb", 3: "mar", 4: "abr", 5: "may", 6: "jun", 7: "jul", 8: "ago", 9: "sep", 10: "oct", 11: "nov", 12: "dic"}
today = date.today()
tm = today.month
ty = today.year
lym = 1 if tm + 1 == 13 else tm + 1
lyy = ty - 1
pathToFollow = 2#1 --> nuevo, 2 --> no hit, 3 --> renovado
pathInfo = {1: "Nuevo", 2: "No Hit/Sin cuentas", 3: "Renovado"}
estudiosToNumber = {"primaria": 1, "secundaria": 2, "preparatoria": 3, "universidad": 4, "maestria": 5, "doctorado": 6}

def validateOtorgante(otorgante):
    if otorgante in ["AA", "AF", "BA", "BB", "BC", "BE", "BH", "BM", "BY", "FF", "HG", "LS", "MI", "MS", "MN", "QM", "QU", "RR", "SI", "VV", "YY", "AL", "AU", "CC", "CF", "CL", "HI", "LR", "LS", "PL", "PN", "RE", "SC", "SE", "SM", "ST", "US"]:
        return "V"
    return "I"

def getPeriodoFormatFromDate(dateString):
    month = int(dateString[2:4])
    year = dateString[4:]
    return numbersToMonth[month] + year

def getMop():
    for d in data:
        if "9" in data[d][1]:
            data[d][1] = "9"
            continue
        tempMop = data[d][1][:data[d][2]]
        highestMop = 0
        for m in tempMop:
            if int(m) > highestMop:
                highestMop = int(m)
        
        data[d][1] = str(highestMop)

def readData():
    values = '{"resp":true,"value":{"respuesta":{"persona":{"encabezado":{"version":"14","numeroReferenciaOperador":"                         ","clavePais":"MX","identificadorBuro":"0000","claveOtorgante":"FF25381001","claveRetornoConsumidorPrincipal":"1","claveRetornoConsumidorSecundario":"0","numeroControlConsulta":"3347303376"},"nombre":{"apellidoPaterno":"SANCHEZ","apellidoMaterno":"MARTINEZ","primerNombre":"HECTOR","segundoNombre":"JESUS","fechaNacimiento":"25101989","rfc":"SAMH891025360","nacionalidad":"MX","residencia":"1","estadoCivil":"M","sexo":"M","numeroRegistroElectoral":"1506112642","claveImpuestosOtroPais":"SAMH891025HNLNRC09","claveOtroPais":"MX","numeroDependientes":"01"},"domicilios":[{"direccion1":"TAMESIS 154","coloniaPoblacion":"CUMBRES ALLEGRO","delegacionMunicipio":"MONTERREY","ciudad":"MONTERREY","estado":"NL","cp":"64349","tipoDomicilio":"H","codPais":"MX","fechaReporteDireccion":"22042024"},{"direccion1":"AV AV BATALLON DE SN PATRICIO 109","direccion2":"PISO 11 NOM AF","coloniaPoblacion":"DEL VALLE ORIENTE","delegacionMunicipio":"SAN PEDRO GARZA GARCIA","ciudad":"SAN PEDRO GARZA GARCIA","estado":"NL","cp":"66260","tipoDomicilio":"H","indicadorEspecialDomicilio":"K","codPais":"MX","fechaReporteDireccion":"02082023"},{"direccion1":"PEDRO ARMENDARIZ 65 28","coloniaPoblacion":"MIRADOR DE LAS MITRAS","ciudad":"MONTERREY","estado":"NL","cp":"64348","numeroTelefono":"8183632815","tipoDomicilio":"H","codPais":"MX","fechaReporteDireccion":"31072023"},{"direccion1":"DOM CON SN","delegacionMunicipio":"MONTERREY","estado":"NL","cp":"64349","codPais":"MX","fechaReporteDireccion":"31012023"}],"empleos":[{"nombreEmpresa":"HECTOR JESUS SANCHEZ MARTINEZ","direccion1":"BATALLON DE SN PATR 109 11","coloniaPoblacion":"DEL VALLE ORIENTE","delegacionMunicipio":"SAN PEDRO GARZA GARCIA","estado":"NL","cp":"66260","numeroTelefono":"8182125964","codPais":"MX","fechaReportoEmpleo":"23052023"},{"nombreEmpresa":"INGENIERIA EN SISTEMAS","direccion1":"AV FRIDA CALO 195","coloniaPoblacion":"GALERIAS VALLE ORIENTE","delegacionMunicipio":"SN PEDRO GARZA GARCIA","ciudad":"SN PEDRO GARZA GARCIA","estado":"NL","cp":"66278","numeroTelefono":"8114135488","codPais":"MX","fechaReportoEmpleo":"17092014"}],"cuentas":[{"fechaActualizacion":"05062024","nombreOtorgante":"BANCO","indicadorTipoResponsabilidad":"I","tipoCuenta":"R","tipoContrato":"CC","claveUnidadMonetaria":"MX","frecuenciaPagos":"Z","montoPagar":"0","fechaAperturaCuenta":"28102014","fechaUltimoPago":"03062024","fechaUltimaCompra":"05112022","fechaReporte":"03062024","modoReportar":"A","creditoMaximo":"94347","saldoActual":"35217+","limiteCredito":"87100","saldoVencido":"0","formaPagoActual":"01","historicoPagos":"1111111","fechaMasRecienteHistoricoPagos":"31052024","fechaMasAntiguaHistoricoPagos":"30112023","montoUltimoPago":"2837"},{"fechaActualizacion":"05062024","nombreOtorgante":"BANCO","indicadorTipoResponsabilidad":"I","tipoCuenta":"R","tipoContrato":"CC","claveUnidadMonetaria":"MX","frecuenciaPagos":"Z","montoPagar":"0","fechaAperturaCuenta":"23022016","fechaUltimoPago":"03062024","fechaUltimaCompra":"02062024","fechaReporte":"03062024","modoReportar":"A","creditoMaximo":"22843","saldoActual":"18094+","limiteCredito":"18100","saldoVencido":"0","numeroPagosVencidos":"5","formaPagoActual":"01","historicoPagos":"111111111111111111111111","fechaMasRecienteHistoricoPagos":"31052024","fechaMasAntiguaHistoricoPagos":"31122017","fechaHistoricaMorosidadMasGrave":"31072018","montoUltimoPago":"14880"},{"fechaActualizacion":"20062024","nombreOtorgante":"FINANCIERA","indicadorTipoResponsabilidad":"I","tipoCuenta":"R","tipoContrato":"CC","claveUnidadMonetaria":"MX","frecuenciaPagos":"Z","montoPagar":"100","fechaAperturaCuenta":"07032023","fechaUltimoPago":"15052024","fechaUltimaCompra":"29052024","fechaReporte":"31052024","modoReportar":"A","creditoMaximo":"3315","saldoActual":"3289+","limiteCredito":"3500","saldoVencido":"0","formaPagoActual":"01","historicoPagos":"1","fechaMasRecienteHistoricoPagos":"30042024","fechaMasAntiguaHistoricoPagos":"30042024","montoUltimoPago":"3314"},{"fechaActualizacion":"18062024","nombreOtorgante":"FINANCIERA","indicadorTipoResponsabilidad":"I","tipoCuenta":"R","tipoContrato":"CC","claveUnidadMonetaria":"MX","frecuenciaPagos":"Z","montoPagar":"9258","fechaAperturaCuenta":"10082021","fechaUltimoPago":"21052024","fechaUltimaCompra":"26052024","fechaReporte":"31052024","modoReportar":"A","creditoMaximo":"26822","saldoActual":"24654+","limiteCredito":"25650","saldoVencido":"0","formaPagoActual":"01","historicoPagos":"11111111111111111","fechaMasRecienteHistoricoPagos":"30042024","fechaMasAntiguaHistoricoPagos":"31122022","montoUltimoPago":"9258"},{"fechaActualizacion":"13062024","nombreOtorgante":"FINANCIERA","indicadorTipoResponsabilidad":"I","tipoCuenta":"R","tipoContrato":"CC","claveUnidadMonetaria":"MX","frecuenciaPagos":"Z","montoPagar":"4463","fechaAperturaCuenta":"24112022","fechaUltimoPago":"22052024","fechaUltimaCompra":"25052024","fechaReporte":"31052024","modoReportar":"A","creditoMaximo":"32048","saldoActual":"32996+","limiteCredito":"33000","saldoVencido":"0","formaPagoActual":"01","historicoPagos":"111111111111111111","fechaMasRecienteHistoricoPagos":"30042024","fechaMasAntiguaHistoricoPagos":"30112022","montoUltimoPago":"10000","identificadorCredito":"Y"},{"fechaActualizacion":"11062024","nombreOtorgante":"TIENDA COMERCIAL","indicadorTipoResponsabilidad":"I","tipoCuenta":"R","tipoContrato":"CC","claveUnidadMonetaria":"MX","frecuenciaPagos":"Z","montoPagar":"1948","fechaAperturaCuenta":"15082012","fechaUltimoPago":"03052024","fechaUltimaCompra":"05052024","fechaReporte":"09052024","modoReportar":"A","creditoMaximo":"31984","saldoActual":"17506+","limiteCredito":"18000","saldoVencido":"0","formaPagoActual":"01","historicoPagos":"111111111111321121111111","fechaMasRecienteHistoricoPagos":"30042024","fechaMasAntiguaHistoricoPagos":"30112017","fechaHistoricaMorosidadMasGrave":"30042023","montoUltimoPago":"5000"},{"fechaActualizacion":"10042024","nombreOtorgante":"FINANCIERA","indicadorTipoResponsabilidad":"I","tipoCuenta":"R","tipoContrato":"CC","claveUnidadMonetaria":"MX","frecuenciaPagos":"Z","montoPagar":"100","fechaAperturaCuenta":"07032023","fechaUltimoPago":"14032024","fechaUltimaCompra":"18032024","fechaReporte":"31032024","modoReportar":"A","creditoMaximo":"3452","saldoActual":"3259+","limiteCredito":"3500","saldoVencido":"0","formaPagoActual":"01","historicoPagos":"111111111110","fechaMasRecienteHistoricoPagos":"29022024","fechaMasAntiguaHistoricoPagos":"31032023","montoUltimoPago":"3451"},{"fechaActualizacion":"07122023","nombreOtorgante":"BANCO","indicadorTipoResponsabilidad":"I","tipoCuenta":"R","tipoContrato":"CC","claveUnidadMonetaria":"MX","frecuenciaPagos":"Z","montoPagar":"0","fechaAperturaCuenta":"28102014","fechaUltimoPago":"01112023","fechaUltimaCompra":"05112022","fechaCierreCuenta":"30112023","fechaReporte":"30112023","modoReportar":"A","creditoMaximo":"94347","saldoActual":"0+","limiteCredito":"87100","saldoVencido":"0","numeroPagosVencidos":"8","formaPagoActual":"01","historicoPagos":"111133321111111111111111","fechaMasRecienteHistoricoPagos":"31102023","fechaMasAntiguaHistoricoPagos":"31032019","claveObservacion":"CA","importeSaldoMorosidadHistMasGrave":"6822","fechaHistoricaMorosidadMasGrave":"17042023","mopHistoricoMorosidadMasGrave":"03","montoUltimoPago":"1900"},{"fechaActualizacion":"04112023","claveOtorgante":"FF25380001","nombreOtorgante":"RSFINANCIEROS","numeroCuentaActual":"002098727","indicadorTipoResponsabilidad":"I","tipoCuenta":"I","tipoContrato":"PL","claveUnidadMonetaria":"MX","valorActivoValuacion":"55000","numeroPagos":"12","frecuenciaPagos":"M","montoPagar":"0","fechaAperturaCuenta":"18052023","fechaUltimoPago":"04102023","fechaUltimaCompra":"18052023","fechaCierreCuenta":"04102023","fechaReporte":"31102023","modoReportar":"A","creditoMaximo":"55000","saldoActual":"0+","limiteCredito":"0","saldoVencido":"0","formaPagoActual":"01","historicoPagos":"12111","fechaMasRecienteHistoricoPagos":"30092023","fechaMasAntiguaHistoricoPagos":"31052023","claveObservacion":"CC","importeSaldoMorosidadHistMasGrave":"944","fechaHistoricaMorosidadMasGrave":"31082023","mopHistoricoMorosidadMasGrave":"02","montoUltimoPago":"55870"},{"fechaActualizacion":"10052023","nombreOtorgante":"BANCO","indicadorTipoResponsabilidad":"I","tipoCuenta":"M","tipoContrato":"RE","claveUnidadMonetaria":"MX","numeroPagos":"240","frecuenciaPagos":"M","montoPagar":"0","fechaAperturaCuenta":"30042013","fechaUltimoPago":"14042023","fechaUltimaCompra":"30042013","fechaCierreCuenta":"14042023","fechaReporte":"30042023","modoReportar":"A","creditoMaximo":"1333650","saldoActual":"0+","limiteCredito":"0","saldoVencido":"0","formaPagoActual":"01","historicoPagos":"32131311111X111111111111","fechaMasRecienteHistoricoPagos":"30032023","fechaMasAntiguaHistoricoPagos":"30052020","claveObservacion":"CC","importeSaldoMorosidadHistMasGrave":"40306","fechaHistoricaMorosidadMasGrave":"01122022","mopHistoricoMorosidadMasGrave":"04","montoUltimoPago":"1075180"},{"fechaActualizacion":"10012023","nombreOtorgante":"FINANCIERA","indicadorTipoResponsabilidad":"I","tipoCuenta":"R","tipoContrato":"CC","claveUnidadMonetaria":"MX","frecuenciaPagos":"Z","montoPagar":"0","fechaAperturaCuenta":"10082021","fechaUltimoPago":"06122022","fechaUltimaCompra":"29092022","fechaCierreCuenta":"06122022","fechaReporte":"31122022","modoReportar":"A","creditoMaximo":"26822","saldoActual":"0+","limiteCredito":"25650","saldoVencido":"0","formaPagoActual":"01","historicoPagos":"1111111111111111","fechaMasRecienteHistoricoPagos":"30112022","fechaMasAntiguaHistoricoPagos":"30082021","claveObservacion":"CA","montoUltimoPago":"2539"},{"fechaActualizacion":"04012021","nombreOtorgante":"BANCO","indicadorTipoResponsabilidad":"I","tipoCuenta":"R","tipoContrato":"CC","claveUnidadMonetaria":"MX","frecuenciaPagos":"Z","montoPagar":"0","fechaAperturaCuenta":"22122010","fechaUltimoPago":"29122020","fechaUltimaCompra":"18092020","fechaCierreCuenta":"29122020","fechaReporte":"03012021","modoReportar":"M","creditoMaximo":"144521","saldoActual":"0+","limiteCredito":"114000","saldoVencido":"92434","numeroPagosVencidos":"1","formaPagoActual":"97","historicoPagos":"X2321111111111111111111X","fechaMasRecienteHistoricoPagos":"03122020","fechaMasAntiguaHistoricoPagos":"31072018","claveObservacion":"LC","fechaHistoricaMorosidadMasGrave":"31012021","montoUltimoPago":"30000"},{"fechaActualizacion":"18092023","nombreOtorgante":"BANCO","indicadorTipoResponsabilidad":"I","tipoCuenta":"M","tipoContrato":"RE","claveUnidadMonetaria":"MX","numeroPagos":"240","frecuenciaPagos":"M","montoPagar":"0","fechaAperturaCuenta":"30042013","fechaUltimoPago":"22122020","fechaUltimaCompra":"30042013","fechaCierreCuenta":"22122020","fechaReporte":"31122020","modoReportar":"M","creditoMaximo":"1333650","saldoActual":"0+","limiteCredito":"0","saldoVencido":"0","formaPagoActual":"01","historicoPagos":"111111111111111111111111","fechaMasRecienteHistoricoPagos":"14112020","fechaMasAntiguaHistoricoPagos":"31072018","claveObservacion":"RV","montoUltimoPago":"16121"},{"fechaActualizacion":"18092023","nombreOtorgante":"CIA Q  OTORGA","indicadorTipoResponsabilidad":"I","tipoCuenta":"O","tipoContrato":"CC","claveUnidadMonetaria":"MX","frecuenciaPagos":"M","montoPagar":"0","fechaAperturaCuenta":"09022017","fechaUltimoPago":"16062020","fechaUltimaCompra":"21122018","fechaCierreCuenta":"16062020","fechaReporte":"17062020","modoReportar":"M","creditoMaximo":"90495","saldoActual":"0+","saldoVencido":"0","formaPagoActual":"01","historicoPagos":"99999999999996554321111","fechaMasRecienteHistoricoPagos":"17052020","fechaMasAntiguaHistoricoPagos":"31072018","claveObservacion":"CL","fechaHistoricaMorosidadMasGrave":"31052020","montoUltimoPago":"5556"},{"fechaActualizacion":"18092023","nombreOtorgante":"BANCO","indicadorTipoResponsabilidad":"I","tipoCuenta":"R","tipoContrato":"CC","claveUnidadMonetaria":"MX","frecuenciaPagos":"Z","montoPagar":"0","fechaAperturaCuenta":"01042013","fechaUltimoPago":"14052020","fechaUltimaCompra":"01112018","fechaCierreCuenta":"10052020","fechaReporte":"31052020","modoReportar":"M","creditoMaximo":"75497","saldoActual":"0+","limiteCredito":"49000","saldoVencido":"31322","formaPagoActual":"97","historicoPagos":"1111111111111111111111","fechaMasRecienteHistoricoPagos":"15042020","fechaMasAntiguaHistoricoPagos":"31072018","claveObservacion":"LC","importeSaldoMorosidadHistMasGrave":"10360","fechaHistoricaMorosidadMasGrave":"31052020","montoUltimoPago":"8000"},{"fechaActualizacion":"26082023","nombreOtorgante":"TIENDA COMERCIAL","indicadorTipoResponsabilidad":"I","tipoCuenta":"R","tipoContrato":"CC","claveUnidadMonetaria":"MX","frecuenciaPagos":"Z","montoPagar":"0","fechaAperturaCuenta":"13042013","fechaUltimoPago":"30072019","fechaUltimaCompra":"29042018","fechaCierreCuenta":"30072019","fechaReporte":"30092019","modoReportar":"M","creditoMaximo":"27591","saldoActual":"0+","limiteCredito":"23000","saldoVencido":"0","formaPagoActual":"01","historicoPagos":"21","fechaMasRecienteHistoricoPagos":"30082019","fechaMasAntiguaHistoricoPagos":"31072019","claveObservacion":"CL","fechaHistoricaMorosidadMasGrave":"31082019","montoUltimoPago":"5836"},{"fechaActualizacion":"18092023","nombreOtorgante":"BANCO","indicadorTipoResponsabilidad":"I","tipoCuenta":"R","tipoContrato":"CC","claveUnidadMonetaria":"MX","frecuenciaPagos":"Z","montoPagar":"0","fechaAperturaCuenta":"22122010","fechaUltimoPago":"23112018","fechaUltimaCompra":"26112018","fechaCierreCuenta":"27112018","fechaReporte":"30112018","modoReportar":"M","creditoMaximo":"117306","saldoActual":"0+","limiteCredito":"114000","saldoVencido":"0","formaPagoActual":"01","historicoPagos":"1111","fechaMasRecienteHistoricoPagos":"25102018","fechaMasAntiguaHistoricoPagos":"31072018","claveObservacion":"RV","montoUltimoPago":"5710"}],"consultaEfectuadas":[{"fechaConsulta":"26062024","claveOtorgante":"FF25381001","nombreOtorgante":"RSFINANCIEROS","tipoContrato":"PL","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"22042024","nombreOtorgante":"CIA Q  OTORGA","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"03042024","nombreOtorgante":"SIC","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"18032024","nombreOtorgante":"FINANCIERA","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"11032024","nombreOtorgante":"SIC","tipoContrato":"UK","claveUnidadMonetaria":"MX","importeContrato":"4000","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"08032024","nombreOtorgante":"BANCO","tipoContrato":"UK","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"08032024","nombreOtorgante":"FINANCIERA","tipoContrato":"CS","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"01112023","nombreOtorgante":"BANCO","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"16102023","nombreOtorgante":"CIA Q  OTORGA","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"16092023","nombreOtorgante":"FINANCIERA","tipoContrato":"CS","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"15092023","nombreOtorgante":"BANCO","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"04092023","nombreOtorgante":"SIC","tipoContrato":"UK","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"14082023","nombreOtorgante":"BANCO","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"02082023","nombreOtorgante":"SIC","tipoContrato":"UK","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"02082023","nombreOtorgante":"CONSUMIDOR FINAL","tipoContrato":"UK","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"27072023","nombreOtorgante":"BANCO","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"17072023","nombreOtorgante":"SIC","tipoContrato":"UK","claveUnidadMonetaria":"MX","importeContrato":"4000","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"02072023","nombreOtorgante":"FINANCIERA","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"19062023","nombreOtorgante":"SIC","tipoContrato":"UK","claveUnidadMonetaria":"MX","importeContrato":"1000","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"08062023","nombreOtorgante":"MICROFINANCIERA","tipoContrato":"CL","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"29052023","nombreOtorgante":"FINANCIERA","tipoContrato":"AU","claveUnidadMonetaria":"MX","importeContrato":"376659","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"24052023","nombreOtorgante":"BANCO","tipoContrato":"UK","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"23052023","nombreOtorgante":"FINANCIERA","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"23052023","nombreOtorgante":"BANCO","tipoContrato":"AU","claveUnidadMonetaria":"MX","importeContrato":"332416","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"23052023","nombreOtorgante":"BANCO","tipoContrato":"UK","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"22052023","nombreOtorgante":"FINANCIERA","tipoContrato":"AU","claveUnidadMonetaria":"MX","importeContrato":"391391","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"19052023","nombreOtorgante":"FINANCIERA","tipoContrato":"CS","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"18052023","nombreOtorgante":"FINANCIERA","tipoContrato":"CS","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"13052023","claveOtorgante":"FF25381001","nombreOtorgante":"RSFINANCIEROS","tipoContrato":"PL","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"13052023","nombreOtorgante":"SERVS. GRALES.","tipoContrato":"PL","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"19042023","nombreOtorgante":"CONSUMIDOR FINAL","tipoContrato":"UK","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"15042023","nombreOtorgante":"SERVICIOS","tipoContrato":"CS","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"14042023","nombreOtorgante":"SIC","tipoContrato":"UK","claveUnidadMonetaria":"MX","importeContrato":"1000","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"12042023","nombreOtorgante":"SIC","tipoContrato":"UK","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"12032023","nombreOtorgante":"FINANCIERA","tipoContrato":"UK","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"12032023","nombreOtorgante":"FINANCIERA","tipoContrato":"CS","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"07032023","nombreOtorgante":"CONSUMIDOR FINAL","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"06032023","nombreOtorgante":"FINANCIERA","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"05032023","nombreOtorgante":"SIC","tipoContrato":"UK","claveUnidadMonetaria":"MX","importeContrato":"1000","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"03032023","nombreOtorgante":"FINANCIERA","tipoContrato":"PL","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"03032023","nombreOtorgante":"CONSUMIDOR FINAL","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"03032023","nombreOtorgante":"CONSUMIDOR FINAL","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"03032023","nombreOtorgante":"CONSUMIDOR FINAL","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"03032023","nombreOtorgante":"CONSUMIDOR FINAL","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"03032023","nombreOtorgante":"CONSUMIDOR FINAL","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"03032023","nombreOtorgante":"CONSUMIDOR FINAL","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"03032023","nombreOtorgante":"CONSUMIDOR FINAL","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"03032023","nombreOtorgante":"CONSUMIDOR FINAL","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"03032023","nombreOtorgante":"SERVICIOS","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"10022023","nombreOtorgante":"SIC","tipoContrato":"UK","claveUnidadMonetaria":"MX","importeContrato":"1000","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"19012023","nombreOtorgante":"SIC","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"16012023","nombreOtorgante":"FINANCIERA","tipoContrato":"CS","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"10012023","nombreOtorgante":"CONSUMIDOR FINAL","tipoContrato":"UK","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"21122022","nombreOtorgante":"SIC","tipoContrato":"UK","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"15122022","nombreOtorgante":"BANCO","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"15122022","nombreOtorgante":"FINANCIERA","tipoContrato":"UK","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"29112022","nombreOtorgante":"SIC","tipoContrato":"UK","claveUnidadMonetaria":"MX","importeContrato":"1000","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"24112022","nombreOtorgante":"FINANCIERA","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"30092022","nombreOtorgante":"SIC","tipoContrato":"UK","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"02092022","nombreOtorgante":"FINANCIERA","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"05082022","nombreOtorgante":"BANCO","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"20072022","nombreOtorgante":"FINANCIERA","tipoContrato":"CC","importeContrato":"0","indicadorTipoResponsabilidad":"I"},{"fechaConsulta":"29062022","nombreOtorgante":"SIC","tipoContrato":"UK","importeContrato":"0","indicadorTipoResponsabilidad":"I"}],"resumenReporte":[{"fechaIngresoBD":"12072009","numeroMOP7":"00","numeroMOP6":"00","numeroMOP5":"00","numeroMOP4":"00","numeroMOP3":"00","numeroMOP2":"00","numeroMOP1":"15","numeroMOP0":"00","numeroMOPUR":"00","numeroCuentas":"0017","cuentasPagosFijosHipotecas":"0003","cuentasRevolventesAbiertas":"0014","cuentasCerradas":"0010","cuentasNegativasActuales":"0002","cuentasClavesHistoriaNegativa":"0003","cuentasDisputa":"00","numeroSolicitudesUltimos6Meses":"06","nuevaDireccionReportadaUltimos60Dias":"N","mensajesAlerta":"NNNNNY","existenciaDeclaracionesConsumidor":"N","tipoMoneda":"MX","totalCreditosMaximosRevolventes":"214811","totalLimitesCreditoRevolventes":"188850","totalSaldosActualesRevolventes":"135015+","totalSaldosVencidosRevolventes":"123756","totalPagosRevolventes":"15869","pctLimiteCreditoUtilizadoRevolventes":"71","totalCreditosMaximosPagosFijos":"0","totalSaldosActualesPagosFijos":"0+","totalSaldosVencidosPagosFijos":"0","totalPagosPagosFijos":"0","numeroMOP96":"00","numeroMOP97":"02","numeroMOP99":"00","fechaAperturaCuentaMasAntigua":"22122010","fechaAperturaCuentaMasReciente":"18052023","totalSolicitudesReporte":"62","fechaSolicitudReporteMasReciente":"22042024","numeroTotalCuentasDespachoCobranza":"00","fechaAperturaCuentaMasRecienteDespachoCobranza":"00000000","numeroTotalSolicitudesDespachosCobranza":"00","fechaSolicitudMasRecienteDespachoCobranza":"00000000"}],"scoreBuroCredito":[{"nombreScore":"BC SCORE","codigoScore":"004","valorScore":"0006","codigoRazon":["166","46","205"]},{"nombreScore":"BC SCORE","codigoScore":"009","valorScore":"0692","codigoRazon":["21"]}]}}}}'
    json_values = json.loads(values)
    #print(json_values)
    json_cuentas = json_values["value"]["respuesta"]["persona"]["cuentas"]
    #print(json_cuentas)
    i = 0
    for c in json_cuentas:
        #otorgante
        nombreOtorgante = c["nombreOtorgante"]
        if nombreOtorgante == "RSFINANCIEROS":
            otorgante = "RSF"
        else:
            otorgante = c["tipoContrato"]
            otorgante = validateOtorgante(otorgante)
        data[i] = [otorgante]
        #mop
        historicoPagos = c["historicoPagos"]
        data[i].append(historicoPagos)
        #fecha_inicio
        fechaInicio = c["fechaMasAntiguaHistoricoPagos"]
        data[i].append("0")
        data[i].append(getPeriodoFormatFromDate(fechaInicio))
        #fecha_final
        fechaFin = c["fechaMasRecienteHistoricoPagos"]
        data[i].append(getPeriodoFormatFromDate(fechaFin))
        #saldo
        saldoActual = c["saldoActual"].replace("+", "")
        data[i].append(saldoActual)
        
        i += 1
    
    getPeriodo()
    getMop()
    """
    with open('campos_matriz1.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        i = 0
        for row in csv_reader:
            data[i] = row
            i += 1
    trimData()
    getPeriodo()
    """
            
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

def matriz1(pathToFollow):
    print("\nMatriz 1")
    ans = {}
    finalAns = "Aprobado"
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
        pathToFollow = 3
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
                pathToFollow = 1
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
    print("Camino a seguir en la siguientes validaciones: " + pathInfo[pathToFollow])#str(pathToFollow) + 
    return pathToFollow

def matriz2():
    print("\nMatriz 2")
    finalAns = "Aprobado"
    ans = {}
    if pathToFollow == 2:
        if 26 < int(data2["edad"]) < 70:
            ans["edad"] = "A"
        else:
            ans["edad"] = "R"
            finalAns = "Rechazado"
        
        if estudiosToNumber[data2["estudios"]] >= 3:
            ans["estudios"] = "A"
        else:
            ans["estudios"] = "R"
            finalAns = "Rechazado"
        
        if data2["tipo_vivienda"] in ["propia", "familiar"]:
            ans["tipo vivienda"] = "A"
        else:
            ans["tipo vivienda"] = "R"
            finalAns = "Rechazado"
    elif pathToFollow == 3:
        if 18 < int(data2["edad"]) < 76:
            ans["edad"] = "A"
        else:
            ans["edad"] = "R"
            finalAns = "Rechazado"
    else:
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
    
    if data2["comprobante_ingresos"] in ["nomina", "SAT"]:
        ans["comprobante ingresos"] = "A"
    else:
        ans["comprobante ingresos"] = "R"
        finalAns = "Rechazado"
    
    if data2["porta_armas"] == "si":
        ans["porta armas"] = "R"
        finalAns = "Rechazado"
    else:
        ans["porta armas"] = "A"
    
    if int(data2["ingreso"]) < 2000:
        ans["ingreso"] = "R"
        finalAns = "Rechazado"
    else:
        ans["ingreso"] = "A"
    
    ans["tipo_empleo"] = "A"
    
    ans["antiguedad domicilio"] = "A"
        
    for a in ans:
        if ans[a] == "R":
            fancyPrinting(a, "No cumple", 25)
        else:
            fancyPrinting(a, "Cumple", 25)
    
    print("\nveredicto final de la matriz 2: " + finalAns)
    #print("\nveredicto final de la matriz 2: Pendiente por recibir información")

def fancyPrinting(var1, var2, spaces):
    emptySpaces = " " * (spaces - len(var1))
    print(var1 + ":" + emptySpaces + var2)

readData()
pathToFollow = matriz1(pathToFollow)
#matriz2()
print(data)
print(data2)
