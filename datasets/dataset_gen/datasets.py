import numpy as np
import pandas as pd
from urllib.request import urlopen
import json
from sodapy import Socrata
import requests
import io
import os




def ins_api():
    client = Socrata("www.datos.gov.co", None) 
    results = client.get("gt2j-8ykr", limit=100000)
    df = pd.DataFrame.from_records(results)
    return df


def ins_filters(df):
    ages_upper = [4,9,14,19,24,29,34,39,44,49,54,59,64,69,74,79]
    ages_under = [a - 4 for a in ages_upper]

    extra_upper = [200, 10, 25, 60, 200]
    extra_under = [80, 0, 11, 25, 60]

    ages_upper.extend(extra_upper)
    ages_under.extend(extra_under)

    states_groups = ["infectados", "FALLECIDO", "RECUPERADO", "HOSPITAL UCI", "CASA"]
    for estado in states_groups:
        if not os.path.exists(f"INS/{estado}"):
            os.mkdir(f"INS/{estado}")


    for i, lb in enumerate(ages_under):
        for estado in states_groups:
            ub = ages_upper[i] # upper bound

            if estado == "infectados":
                df_group = df[((df["edad"] >= lb) &  (df["edad"] <= ub))]
            else:
                df_group = df[((df["edad"] >= lb) &  (df["edad"] <= ub) & (df["atencion"] == estado))]

            df_group.to_csv(f"INS/{estado}/{lb}_{ub}.csv", index=False)

def ins_aggs(df):
    pass

def load_ins():
    df = ins_api()
    names_dict = {
        "fecha_diagnostico": "Fecha de diagnóstico",
        "ciudad_de_ubicaci_n": "ciudad",
        "fecha_de_notificaci_on": "Fecha de notificacion",
        "atenci_n": "atencion",
        "fecha_de_notificaci_n": "fecha de notificacion",
        "pa_s_de_procedencia" : "pais de procedencia"
    }

    df = df.rename(columns=names_dict)
    
    df["sexo"] = df["sexo"].str.upper()
    df["estado"] = df["estado"].str.upper()
    df["atencion"] = df["atencion"].str.upper()
    df["tipo"] = df["tipo"].str.upper()
    df["edad"] = df["edad"].astype(int)
    

    df["fecha_recuperado"] = pd.to_datetime(df["fecha_recuperado"], errors="coerce")
    df["fecha_de_muerte"] = pd.to_datetime(df["fecha_de_muerte"], errors="coerce")
    df["asintomatico"] = df["fis"] == "Asintomático"
    df["asintomatico"] = df["asintomatico"].astype(int)
    df["fis"] = pd.to_datetime(df["fis"], errors="coerce")
    df["tiempo recuperacion"] = df["fecha_recuperado"] - df["fis"]
    df["tiempo recuperacion"] = df["tiempo recuperacion"].dt.days
    
    df["tiempo muerte"] = df["fecha_de_muerte"] - df["fis"]
    df["tiempo muerte"] = df["tiempo muerte"].dt.days

    df["fecha_recuperado"] = df["fecha_recuperado"].astype(str)
    df["fecha_de_muerte"] =  df["fecha_de_muerte"].astype(str)
    df = df.set_index("id_de_caso")
    if not os.path.exists("INS"):
        os.mkdir("INS")
    df.to_csv("INS/total.csv", index=False)
    ins_filters(df)
    return df



def jhon_hopkins(tipo):
    # Johns Hopkins
    if tipo == "Confirmed":
        file = "time_series_covid19_confirmed_global.csv"
    elif tipo == "Deaths":
        file = "time_series_covid19_deaths_global.csv"
    elif tipo == "Recovered":
        file = "time_series_covid19_recovered_global.csv"
    else:
        print("tipo no reconocido. Por favor escoger entre Confirmed, Deaths y Recovered")

    url_confirmed=f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/{file}"
    s=requests.get(url_confirmed).content
    df=pd.read_csv(io.StringIO(s.decode('utf-8')))
    df = df.drop(["Province/State", "Lat", "Long"], axis=1)
    df = pd.DataFrame(df.set_index("Country/Region").stack()).reset_index()
    df = df.rename(columns={"Country/Region":"Country","level_1":"Date", 0:tipo})
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.groupby(["Date", "Country"])[tipo].max().reset_index()
    return df

def load_jh():
    confirmed = jhon_hopkins("Confirmed")
    deaths = jhon_hopkins("Deaths")
    recovered = jhon_hopkins("Recovered")

    confirmed["Date"] = confirmed["Date"].astype(str)
    deaths["Date"] = deaths["Date"].astype(str)
    recovered["Date"] = recovered["Date"].astype(str)
    if not os.path.exists("Jhon Hopkins"):
        os.mkdir("Jhon Hopkins")
    confirmed.to_csv("Jhon Hopkins/confirmed.csv", index=False)
    deaths.to_csv("Jhon Hopkins/deaths.csv", index=False)
    recovered.to_csv("Jhon Hopkins/recovered.csv", index=False)
    return confirmed, deaths, recovered



load_ins()
load_jh()






