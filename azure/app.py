from flask import Flask, render_template
from databace_conector import DataBase
import base64
from io import BytesIO
from matplotlib.figure import Figure
from get_luftkvalitet_data import get_dht_sgp_data

database = DataBase('database/main_db.db')

app = Flask(__name__)

#setup fungtioner
def get_rum(skole=''):
    rum_list =[]
    rum_db = database.get_databace_data(f'SELECT * FROM rum{skole}',35)
    for rum in rum_db:
        rum_full ={}
        rum_full['id'] = rum[0]
        rum_full['skoleid'] = rum[1]
        rum_full['navn'] = rum[2]
        rum_list.append(rum_full)
    return rum_list

def get_skole():
    skole_liste = [None]
    skoler = database.get_databace_data('SELECT * FROM skole')
    for skole in skoler:
        skole_liste.append(skole[1])
    return skole_liste

def luftværdi_graf(rumid,vælg_graf_værdi):
    datetimes, temp, hum, co2, voc = get_dht_sgp_data(10,rumid)
    graf_værdi = (temp, hum, co2, voc)
    graf_navn = (('Temperatur i Celsius','°C'),('Fugtighedsmålinger i Procent','Fugtighed i %'),('Kuldioxid målinger i PPM ','Co2 i PPM'),('VOC målinger i PPB','VOC i PPB'))
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.set_title(graf_navn[vælg_graf_værdi][0], color="white")
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor ("#5A5560")
    ax.plot(datetimes, graf_værdi[vælg_graf_værdi], c = "#faec26", marker ="o")
    ax.set_xlabel("Tidspunkt")
    ax.set_ylabel(graf_navn[vælg_graf_værdi][1])
    fig.patch.set_facecolor("#5A5560")
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.spines['left'].set_color("#5A5560")
    ax.spines['bottom'].set_color("#5A5560")
    ax.spines['top'].set_color("#5A5560")
    ax.spines['right'].set_color("#5A5560")
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

#webpages

@app.context_processor
def inject_user():
    bace_skoler = get_skole()
    return dict(bace_skoler = bace_skoler, bace_skoler_lenth = len(bace_skoler)-1)

@app.route('/')
def home():
    rum = get_rum()
    skole = get_skole()
    return render_template('index.html',lenth = len(rum),rum = rum, skole = skole)

@app.route('/skole/<int:skole_nr>/')
def skole(skole_nr):
    skole = get_skole()
    rum_liste = get_rum(f' WHERE skoleid IS {skole_nr}')
    name = skole[skole_nr]
    return render_template('skole.html',skole=name, lenth = len(rum_liste), rum = rum_liste)

@app.route('/rum/<int:rum>/')
def rum(rum):
    rum_temperatur = luftværdi_graf(rum,0)
    rum_humidity = luftværdi_graf(rum,1)
    rum_CO2 = luftværdi_graf(rum,2)
    rum_VOC = luftværdi_graf(rum,3)
    rum_list = get_rum()
    skole_list = get_skole()
    name = rum_list[rum-1]['navn']
    skole_navn = skole_list[rum_list[rum-1]['skoleid']]
    return render_template('rum.html',rum=name,skole_navn=skole_navn, rum_temperatur = rum_temperatur, rum_humidity = rum_humidity, rum_CO2 = rum_CO2, rum_VOC = rum_VOC)

@app.route('/kontrolpanel/')
def kontrolpanel():
    return render_template('kontrolpanel.html')

@app.route('/login/')
def login():
    return render_template('login.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0')