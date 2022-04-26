import os
import requests
from flask import Flask, session, render_template, request, redirect, jsonify, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
app = Flask(__name__)

# Check for environment variable
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# set secret key
app.secret_key = '_5#y2L"F4Q8z]/'

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/ quickstart
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db = SQLAlchemy(app)
Users=[]
Passwords=[]
Ills=['Taquicardia ventricular','Fibrilación ventricular','Flutter auricular','Taquicardia sinusal','Bradicardia sinusal','Taquicardia auricular','Aritmia sinusal','Taquicardia supra ventricular paroxistica','Fibrilacion auricular','Ritmo Idioventricular','Bloqueo de tercer grado','Ritmo cardiaco normal']
Pages=[1,2,3,4,5,6,7,8,9,10,11,12]
Texto=["La taquicardia ventricular es un trastorno del ritmo cardíaco (arritmia) causado por señales eléctricas anormales en las cavidades inferiores del corazón (ventrículos).  Las señales eléctricas anormales en los ventrículos provocan que el corazón lata más rápido de lo normal. La taquicardia ventricular puede ser breve, durar solo unos pocos segundos y no causar ningún síntoma. O bien, puede durar mucho más y causar síntomas como mareos, aturdimiento, palpitaciones o incluso la pérdida del conocimiento. /n Características:        Frecuencia cardiaca 100 o más latidos por minuto."
,"La fibrilación ventricular es un problema del ritmo cardíaco que ocurre cuando el corazón late con impulsos eléctricos rápidos y erráticos. Esto hace que las cavidades de bombeo del corazón (los ventrículos) se agiten con pulsaciones ineficaces, en lugar de bombear sangre. La fibrilación ventricular hace que la presión arterial caiga rápidamente, lo que interrumpe el suministro de sangre a los órganos vitales. La taquicardia ventricular no tratada usualmente lleva a la fibrilación ventricular./n Características: Frecuencia cardiaca 250 o más latidos por minuto. Ritmo muy irregular"
,"El aleteo auricular es un tipo de trastorno del ritmo cardiaco en el cual las cavidades superiores del corazón (aurículas) laten muy rápido. Esto conlleva a que los latidos del corazón adquieran un ritmo veloz y regular. Esta enfermedad suele no presentar síntomas, sin embargo, puedo conllevar problemas como: accidentes cerebrovasculares e insuficiencia cardíaca. Existen tratamientos eficaces para el aleteo auricular, entre ellos, la cicatrización de pequeñas regiones del tejido cardíaco (ablación) o los medicamentos. Características: Frecuencia cardiaca entre 250 y 350 latidos/min. Ritmo irregular o variable"
,"Se define como el aumento de la frecuencia cardiaca por encima de los 100 lpm. Se produce principalmente por estrés físico o mental, incremento de las demandas de oxígeno y enfermedades concomitantes. Se dice que para estos casos la taquicardia es en respuesta adaptativa del organismo y no requiere más tratamiento que el de la causa originaria. Rango de frecuencia.- 110 a 130 latidos por minuto."
,"Es un ritmo sinusal con una frecuencia inferior a 60 latidos por minuto (lpm). Principalmente está relacionada a alteraciones orgánicas en el nodo sinusal y se relaciona con estados vago tónicos o de entrenamiento físico y también a fármacos. Rango de frecuencia.- 40 a 50 latidos por minuto."
,"La taquicardia auricular es una frecuencia cardiaca acelerada que es provocada cuando se envían demasiados impulsos eléctricos desde las aurículas (parte superior) a los ventrículos (parte inferior) del corazón, donde las aurículas desde múltiples puntos dentro de la misma disparan señales al mismo tiempo. La frecuencia cardíaca rápida hace que el corazón se esfuerce demasiado y que no movilice la sangre de manera eficiente.Si los latidos cardíacos son muy rápidos, hay menos tiempo para que la cámara del corazón se llene con sangre entre dichos latidos; por lo tanto, no se bombea suficiente sangre al cerebro y al resto del cuerpo con cada contracción. /n Características: Frecuencia cardiaca entre 140 y 250 latidos/min. Ritmo regular."
,"La arritmia es una alteración del ritmo cardiaco normal en un corto espacio de tiempo influido por el ciclo respiratorio. Consiste en la ralentización de la frecuencia cardiaca durante la espiración y la aceleración de la misma durante la inspiración. Es frecuente encontrarla en niños y personas jóvenes pues estos suelen ser más activos, y se considera una variante del ritmo sinusal normal. /n Características: Frecuencia cardiaca entre 60 y 100 latidos/min. Ritmo irregular."
,"Ocurre principalmente en personas jóvenes y es más molesta que peligrosa, y puede aparecer durante un ejercicio intenso. Puede ser generada por una extrasístole que activa el corazón reiteradamente a una frecuencia rápida. Puede haber dos vías de conducción eléctrica en el nódulo auriculoventricular (una arritmia denominada taquicardia supra ventricular por reentrada en el nódulo auriculoventricular) o existir una vía de conducción eléctrica anómala entre las aurículas y los ventrículos. Rango de frecuencia.- 160 a 220 latidos por minuto"
,"La fibrilación auricular es una frecuencia cardiaca irregular, donde las dos cavidades superiores del corazón tienen señales caóticas provocando un ritmo acelerado que es irregular. Se tiene entre 100 y 175 latidos por minuto, aumenta el riesgo de problemas cardiacos, accidentes cerebrovasculares y insuficiencia cardiaca. No hay coordinación entre las cavidades superiores con las inferiores. Los síntomas de esta enfermedad son palpitaciones, dificultad para respirar y debilidad.  La onda P, el intervalo PR están ausentes pero el intervalo QRS esta normal con cierta ampliación en retrasos de conducción."
,"Es una arritmia con una velocidad de 20 a 40 lpm donde la onda P esta ausente, el intervalo PR es inmensurable, el complejo QRS tiene un aspecto extraño con un ancho menos a 0,10 segundos. Se produce cuando el principal marcapasos cardiaco no funciona o anda ralentizado. El control del ritmo se da por el miocardio dando unas señales que se mueven a través de los ventrículos sin el beneficio del sistema de conducción."
,"Se produce porque hay una interrupción total de la conducción AV desconectando eléctricamente a las aurículas y ventrículos. Esto causa que los ventrículos y las aurículas se despolaricen independientemente del otro.  Ya que las aurículas serán estimuladas por el nodo sinusal y los ventrículos por un marcapasos subsidiario. La onda P es de tamaño y forma normal, el intervalo PR esta ausente por la independencia, el complejo QRS normal y en ciertas ocasiones ancho."
,"La frecuencia cardiaca es el número de veces que se contrae el corazón durante un minuto (latidos por minuto). Para el correcto funcionamiento del organismo es necesario que el corazón actúe bombeando la sangre hacia todos los órganos, pero además lo debe hacer a una determinada presión (presión arterial) y a una determinada frecuencia. la frecuencia normal en reposo oscila entre 50 y 100 latidos por minuto. Sin embargo, hay que detallar un aspecto que altera su estado: Cuando nacemos tenemos una frecuencia cardíaca elevada porque la actividad del organismo es muy intensa. A partir del primer mes de vida, va disminuyendo hasta llegar a la edad adulta, manteniéndose estable después de los 20 años."]
# class Usuario(db.model):
#     username = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
#     contrasena = db.Column(db.String(120), unique=False, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username
# db.create_all()

@app.route("/",methods=["GET","POST"])
def index():
    print("111111111111111")
    if session.get("name") is None:
        session["user"] = []
        session["contrasena"] = ""
        session["session"] = "si"
    # book = Book(sbnNumber=sbnNumber, title=title, author=author, pubYear=pubYear)
    # db.session.add(book)
    if request.method == "POST":
        session["session"]=request.form.get("session")
    # salir de la sesion
        if session["session"] == "no" :
            print("if2-1")
            session.clear()
            session["user"] = []
            clienteFijo=""
            session["psw1"] = ""
            session["psw2"] = ""
            session["session"] = "si"
            return  render_template("trueLogin.html")
    # submit login or register
        else:
            session["user"] = request.form.get("name")
            session["register"] = request.form.get("register")
            session["psw1"] = request.form.get("psw1")
    # check if user is in users
            if session["register"]=="0":
                if session["user"]in Users:
                    if Passwords[Users.index(session["user"])]==session["psw1"]:
                        print("user and pass correct")
                        return redirect(url_for('searchPage'))
                return render_template("error.html")
    # check if paswwords correct
            session["psw2"] = request.form.get("psw2")
            if not session["psw2"]==session["psw1"]:
                return render_template("error.html")
    # if no problem add user
            else:
                Users.append(session["user"])
                Passwords.append(session["psw1"])
                return redirect(url_for('searchPage'))

            # db.execute("""INSERT INTO "users" ("user","password") VALUES  (:name , :psw1) """, {"name":session["user"],"psw1":session["psw1"]})
            # db.commit()

        # return  render_template("trueLogin.html")
    return  render_template("trueLogin.html")


@app.route("/searchPage",methods=["GET","POST"])
def searchPage():
    if session["user"]==None:
        return redirect(url_for('index'))
    # return  render_template("menuPage.html", name=session["user"])
    return  render_template("displayMenu.html", name=session["user"],options=Pages,ills=Ills,size=len(Ills))
@app.route("/selection", methods=["GET","POST"])
def selection():
    session["option"]=[]
    session["ills"]=[]
    session["value"] = int(request.form.get("value"))
    if session["value"] >=100 and session["value"]<250: #taquicardiaventricular
        session["option"].append(1)
        session["ills"].append(Ills[0])
    if session["value"] >=250 and session["value"]<300:#fibrilación ventricular
        session["option"].append(2)
        session["ills"].append(Ills[1])
    if session["value"] >=250 and session["value"]<350:#flutter auricular
        session["option"].append(3)
        session["ills"].append(Ills[2])
    if session["value"] >=110 and session["value"]<130:#taquicardiasinusal
        session["option"].append(4)
        session["ills"].append(Ills[3])
    if session["value"] >=40 and session["value"]<=50:#bradicardia sinusal
        session["option"].append(5)
        session["ills"].append(Ills[4])
    if session["value"] >=140 and session["value"]<250:#taquicardiaauricular
        session["option"].append(6)
        session["ills"].append(Ills[5])
    if session["value"] >=60 and session["value"]<100:#aritmia sinusal
        session["option"].append(7)
        session["ills"].append(Ills[6])
    if session["value"] >=160 and session["value"]<220:#taquicardia supra ventricular paroxistica
        session["option"].append(8)
        session["ills"].append(Ills[7])
    if session["value"] >=100 and session["value"]<175:#Fibrilacion auricular
        session["option"].append(9)
        session["ills"].append(Ills[8])
    if session["value"] >=20 and session["value"]<40:#Ritmo Idioventricular Bloqueo de tercer grado
        session["option"].append(10)
        session["ills"].append(Ills[9])
    if session["value"] >=35 and session["value"]<50:#Bloqueo de tercer grado
        session["option"].append(11)
        session["ills"].append(Ills[10])
    if session["value"] >=60 and session["value"]<100:#ritmo cardiaco normal
        session["option"].append(12)
        session["ills"].append(Ills[11])
    if session["value"] >350 or session["value"]<20:#ritmo cardiaco normal 
            return  render_template("error.html",mensaje="Error al ingresar los datos"),404
    return render_template("enfermedadSearch.html",option=session["option"],value=session["value"],ills=session["ills"],size=len(session["ills"]), name=session["user"])

#----------------------------///
@app.route("/searchPage/<Source>", methods=["GET","POST"])
def enfermedad(Source):
    if request.method == "POST":
        value=request.form.get("value")
    session["option"]=int(Source)
    if session["option"] in Pages:
        # return render_template("enfermedad12.html",text=Texto[session["option"]],title=Ills[session["option"]])
        return render_template("enfermedadisplay.html",text=Texto[session["option"]-1],title=Ills[session["option"]-1], name=session["user"])
    return  render_template("error.html",mensaje="Error al ingresar los datos"),404
