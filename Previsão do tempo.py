import requests
import json
from datetime import date
## import pprint 
                                                       ## Para o funcionamento do programa é necessario uso key do accuWeather.
accuweatherAPIKey = "if9DEmC5q77FuNmpIBqfIJknlDEL7urc" ##SITE KEY: https://developer.accuweather.com 
dias_semana = ["Domingo","Segunda-feira","terça-feira","quarta-feira","quinta-feira","sexta-feira","sábado"]

def pegarCoord():

    r = requests.get('http://www.geoplugin.net/json.gp')

    if (r.status_code != 200): ## 200 OK, SE NÃO = ERRO
        print ("Não foi possível obter a localização.")
        return None
    else:
        try:
            localizacao = json.loads(r.text)
            coordenadas = {}
            coordenadas ["lat"] = localizacao['geoplugin_latitude']
            coordenadas ["long"] = localizacao['geoplugin_longitude']
            return coordenadas
        except:
            return None

def pegarCodLocal(lat,long):     
            locationAPIurl = "http://dataservice.accuweather.com/locations/v1/cities/geoposition"\
            + "/search?apikey=" + accuweatherAPIKey + "&q=" + lat + "%2C" + long +"&language=pt-br" 
            ## "\" para quebrar linha e continuar a str
            
            r = requests.get(locationAPIurl)
            if (r.status_code != 200):
                print ("Não foi possível obter o código do seu local.")
                return None
            else:
                try:
                    locationResponse = json.loads(r.text)
                    infoLocal = {}
                    infoLocal["nomeLocal"] = locationResponse ["LocalizedName"] + ", " + locationResponse ["AdministrativeArea"]["LocalizedName"] + ". " + locationResponse ["Country"]["LocalizedName"]
                    infoLocal["codigoLocal"] = locationResponse ["Key"] ## para obter o clima
                    return infoLocal
                except:
                    return None

def pegarTempo(codigoLocal,nomeLocal):

        CurrentConditionsAPIurl = "http://dataservice.accuweather.com/currentconditions/v1/"+ \
        codigoLocal + "?apikey="+ accuweatherAPIKey +"&language=pt-br"

        r = requests.get(CurrentConditionsAPIurl)
        if (r.status_code != 200):
            print ("Não foi possível obter o clima do seu local.")
            return None
        else:
            try:
                CurrentConditionsAPIurl = json.loads(r.text)
                infoClima = {}
                infoClima["textoClima"] = CurrentConditionsAPIurl [0]["WeatherText"]
                infoClima["temperatura"] = CurrentConditionsAPIurl[0]["Temperature"]["Metric"]["Value"]
                infoClima["nomeLocal"] = nomeLocal
                return infoClima
            except:
                return None
            
def pegarTemp5dias(codigoLocal):

        DailyAPIurl = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/" + codigoLocal + \
        "?apikey=" + accuweatherAPIKey + "&language=pt-br&metric=true"

        r = requests.get(DailyAPIurl)
        if (r.status_code != 200):
                print ("Não foi possível obter o clima do seu local.")
                return None
        else:
            try:
                DailyResponse = json.loads(r.text)
                infoClima5 = []
                for dia in DailyResponse["DailyForecasts"]:
                    climaDia = {}
                    climaDia["max"] = dia ["Temperature"]["Maximum"]["Value"]
                    climaDia["min"] = dia ["Temperature"]["Minimum"]["Value"]
                    climaDia["clima"] = dia ["Day"]["IconPhrase"]
                    diaSemana = int (date.fromtimestamp(dia["EpochDate"]).strftime("%w"))
                    climaDia["dia"] = dias_semana[diaSemana]
                    infoClima5.append(climaDia)
                return infoClima5
                       
            except:
                    return None

def mostrarPrevisao(lat, long):
    try:
        local = pegarCodLocal(lat,long)
        climaAtual = pegarTempo(local["codigoLocal"],local["nomeLocal"])
        print("Clima atual em: " + climaAtual["nomeLocal"])
        print(climaAtual["textoClima"])
        print("Temperatura: " + str (climaAtual["temperatura"]) + "\xb0" + "C")
    except:
        print("Erro ao obter o clima atual.")

            
    opcao = input ("Deseja ver a previsão para os próximos dias? (s ou n): ").lower()

    if opcao == "s":
        print("\n Clima para hoje e para os próximos dias: \n")

        try:
            previsao5dias = pegarTemp5dias(local["codigoLocal"])
            for dia in previsao5dias:
                print(dia ["dia"])
                print("Mínima: " + str(dia["min"])+ "\xb0" + "C")
                print("Maxima: " + str(dia["max"])+ "\xb0" + "C")
                print("Clima: " + dia["clima"])
                print("=========================================================")
        except:
            print ("Erro ao obter a previsão para os próximos dias")

try:
    coordenadas = pegarCoord()
    mostrarPrevisao(coordenadas["lat"], coordenadas["long"])
    
except:
    print("Erro não foi possível obter o clima")



        
    
