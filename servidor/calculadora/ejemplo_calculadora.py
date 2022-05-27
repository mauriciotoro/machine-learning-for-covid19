from calculadora import calculadora

dict_comor = {
    'SEXO': 2, #1 mujer
    'NEUMONIA': 1, # 1 es si
    'EDAD': 25, 
    'EMBARAZO': 2, 
    'DIABETES': 2, 
    'EPOC': 2, 
    'ASMA': 2,
    'INMUSUPR': 2, 
    'HIPERTENSION': 2, 
    'CARDIOVASCULAR': 1, 
    'OTRA_COM': 2, 
    'OBESIDAD': 2,
    'RENAL_CRONICA': 2, 
    'TABAQUISMO': 2
}

print(calculadora(dict_comor))