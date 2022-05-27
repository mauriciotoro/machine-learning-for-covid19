import pandas as pd
from datetime import date

def load_dataset(filename, corte):
    df = pd.read_csv(filename,encoding = "ISO-8859-1")
    df["FECHA_SINTOMAS"] = pd.to_datetime(df["FECHA_SINTOMAS"], errors="coerce")
    df["FECHA_DEF"] = pd.to_datetime(df["FECHA_DEF"], errors="coerce")
    df["FECHA_INGRESO"] = pd.to_datetime(df["FECHA_INGRESO"], errors="coerce")
    today = date.today()

    df_positivos = df[df["RESULTADO"] == 1]
    df_positivos["anterior_corte"] = (pd.to_datetime(today) - df_positivos["FECHA_SINTOMAS"]).dt.days > corte
    df_creibles = df_positivos[(df_positivos["FECHA_DEF"].notnull()) | (df_positivos["anterior_corte"])]
    df_creibles.drop("anterior_corte", axis=1, inplace=True)
    df_creibles["fallecio"] = df_creibles["FECHA_DEF"].notna()
    df_creibles["fallecio"] = df_creibles["fallecio"].astype(int)

    df_creibles = df_creibles.drop(["FECHA_ACTUALIZACION", 
                "ID_REGISTRO", 
                'FECHA_INGRESO', 
                'FECHA_SINTOMAS',
                'FECHA_DEF',
                'ORIGEN',
                'SECTOR',
                'ENTIDAD_UM',
                'ENTIDAD_NAC',
                'ENTIDAD_RES',
                'MUNICIPIO_RES',
                'TIPO_PACIENTE',
                'NACIONALIDAD',
                'HABLA_LENGUA_INDIG',
                'RESULTADO',
                'MIGRANTE',
                'PAIS_NACIONALIDAD',
                'PAIS_ORIGEN',
                'INTUBADO',
                'UCI',
                'OTRO_CASO'], axis=1)

    categoricas = ['SEXO', 'NEUMONIA', 'EMBARAZO', 'DIABETES', 'EPOC',
        'ASMA', 'INMUSUPR', 'HIPERTENSION', 'OTRA_COM', 'CARDIOVASCULAR',
        'OBESIDAD', 'RENAL_CRONICA', 'TABAQUISMO', 'fallecio']

    for col in categoricas:
        df_creibles[col] = df_creibles[col].astype('category')

    return df_creibles

def plot_cm(y_test, y_pred, normalize=None):
    # values: dict of prediction {"0": "Not fraud", "1":"Fraud"}
    
    cm = np.round(confusion_matrix(y_test, y_pred, normalize=normalize),4)
    
    plt.figure()
    ax = sns.heatmap(cm,annot=True, xticklabels=["No falleció", "falleció"],yticklabels=["No falleció", "falleció"])

    
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Real")
    ax.set_title("Confussion matrix", fontsize = 15)

    plt.show()