import numpy as np
import pandas as pd
from urllib.request import urlopen
import json
from sodapy import Socrata
import plotly.express as px
import plotly.graph_objs as go


def load_colombia_df():
    client = Socrata("www.datos.gov.co", None)  # https://www.datos.gov.co/es/profile/edit/developer_settings   por si no funciona
    results = client.get("gt2j-8ykr", limit=100000)
    results_df = pd.DataFrame.from_records(results)
    return results_df

def preprocess_df(df):
    df = df.rename(columns={"fecha_diagnostico": "Fecha de diagnóstico",
                            "ciudad_de_ubicaci_n": "ciudad",
                            "fecha_de_notificaci_on": "Fecha de notificacion",
                            "atenci_n": "atencion"})
    
    df["sexo"] = df["sexo"].str.upper()
    df["estado"] = df["estado"].str.upper()
    df["atencion"] = df["atencion"].str.upper()
    df["tipo"] = df["tipo"].str.upper()
    df["edad"] = df["edad"].astype(int)
    
    df["Fecha de diagnóstico"] = pd.to_datetime(df["Fecha de diagnóstico"], errors="coerce")
    df["fecha_recuperado"] = pd.to_datetime(df["fecha_recuperado"], errors="coerce")
    df["fecha_de_muerte"] = pd.to_datetime(df["fecha_de_muerte"], errors="coerce")
    df["asintomatico"] = df["fis"] == "Asintomático"
    df["asintomatico"] = df["asintomatico"].astype(int)
    df["fis"] = pd.to_datetime(df["fis"], errors="coerce")
    df["tiempo recuperacion"] = df["fecha_recuperado"] - df["fis"]
    df["tiempo recuperacion"] = df["tiempo recuperacion"].dt.days
    
    df["tiempo muerte"] = df["fecha_de_muerte"] - df["fis"]
    df["tiempo muerte"] = df["tiempo muerte"].dt.days
    return df

def confirmed_by_day(df):
    cuenta = pd.DataFrame(df.groupby("Fecha de diagnóstico")["id_de_caso"].count()).reset_index()
    cuenta = cuenta.rename(columns={"id_de_caso":"cuenta"})
    fig = px.bar(data_frame=cuenta, x="Fecha de diagnóstico", y="cuenta")
    fig.update_layout(
        title_text = 'Confirmados por día en Colombia',
        font=dict(
            family="Courier New, monospace",
            size=10,
            color="#7f7f7f"
        ),
        titlefont= dict(size= 25)

    )
    return fig

df = load_colombia_df()
df.to_csv("ins_covid.csv", index=False)

df_col = preprocess_df(df)

fig_confirmed = confirmed_by_day(df_col)

print(fig_confirmed.to_json())