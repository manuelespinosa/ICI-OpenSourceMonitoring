import requests
import pandas as pd
import json
import paho.mqtt.client as mqtt
from time import sleep
from datetime import datetime
import random
from statistics import mean


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ICI/#")


def get_ree_demanda(start_date, end_date, time_trunc='hour'):
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'time_trunc': time_trunc,
        'geo_trunc': 'electric_system',
        'geo_limit': 'peninsular',
        'geo_ids': 8741
    }
    r = requests.get("https://apidatos.ree.es/es/datos/demanda/evolucion", params=params)

    data = json.loads(r.text)
    df = pd.DataFrame.from_dict(data['included'][0]['attributes']['values'])
    df.index = pd.DatetimeIndex(df['datetime'], yearfirst=True)
    df.drop(['percentage', 'datetime'], axis=1, inplace=True)
    df.rename({'value': 'demanda'}, axis=1, inplace=True)
    return df


def get_ree_generacion(start_date, end_date, time_trunc='day'):
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'time_trunc': time_trunc,
        'geo_trunc': 'electric_system',
        'geo_limit': 'peninsular',
        'geo_ids': 8741
    }
    r = requests.get("https://apidatos.ree.es/es/datos/generacion/estructura-generacion", params=params)

    data = json.loads(r.text)

    df = pd.DataFrame()

    for d in data['included']:
        titulo = d['type']
        dftemp = pd.DataFrame.from_dict(d['attributes']['values'])
        dftemp.rename({'value': titulo}, axis=1, inplace=True)
        dftemp.index = pd.DatetimeIndex(dftemp['datetime'], yearfirst=True)
        dftemp.drop(['datetime', 'percentage'], axis=1, inplace=True)
        df = pd.concat([df, dftemp], axis=1, ignore_index=False, sort=True)

    #df.index = df.index.tz_localize(None)
    #df.to_excel('Generacion.xlsx')
    return df


def send_df_to_mqtt(df, topic, delay):
    for idx, row in df.iterrows():
        datos = json.loads(row.to_json())
        datos['datetime'] = idx.__format__("%Y-%m-%dT%H:%M:%S%z")
        mqttc.publish(topic, json.dumps(datos))
        sleep(delay)


if __name__ == '__main__':
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    #mqttc.connect("test.mosquitto.org", 1883, 60)
    #mqttc.connect("imp3ddicei1.uca.es", 1883, 60)
    mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)

    mqttc.loop_start()

    while True:
        ed = datetime.now().strftime('%Y-%m-%dt%H:%M:%S')
        sd = datetime.now().replace(month=4, day=25, hour=0, minute=0, second=0).strftime('%Y-%m-%dt%H:%M:%S')

        df = get_ree_generacion(start_date=sd, end_date=ed, time_trunc='day')
        send_df_to_mqtt(df, topic='ICI/Energia/generacion', delay=0.2)

        df = get_ree_demanda(start_date=sd, end_date=ed, time_trunc='hour')
        send_df_to_mqtt(df, topic='ICI/Energia/demanda', delay=0.2)

        """
        phs = [random.uniform(3, 12) for _ in range(10)]
        temperaturas = [random.uniform(18, 30) for _ in range(10)]
        for i in range(300):
            del temperaturas[0]
            del phs[0]
            temperaturas.append(random.random()*2-1+temperaturas[-1
            ])
            phs.append(random.uniform(2, 13))

            temperatura = round(mean(temperaturas), 1)
            humedad = 50 - temperatura
            ph = round(mean(phs), 1)

            sensorDict = {"temperatura": temperatura,
                          "humedad": humedad,
                          "ph": ph}

            mqttc.publish("ICIEnergia/dummySensor", json.dumps(sensorDict))

            sleep(5)
        """

        sleep(300)


    mqttc.loop_stop()

