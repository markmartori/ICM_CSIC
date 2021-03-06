from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
import pymysql.cursors
import os
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


#Para crear dataframe:
import pandas as pd

#Para poder coger multiples opciones:
from flask import flash, request, url_for 


class CodeForm(FlaskForm):
    code = StringField('code', validators=[DataRequired()])
    submit = SubmitField('Search1')
    
class CodeForm1(FlaskForm):
    code = StringField('code', validators=[DataRequired()])
    submit = SubmitField('Search2')


app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='PRicm_2019',
                             db='mark',charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()



@app.route("/")
def home():
     return render_template("home.html")


@app.route("/AccessionID" , methods=['GET', 'POST'])
def AccessionID():

    form = CodeForm(request.form)
    '''## EL IF NO HACE FALTA
    if form.validate_on_submit():
        flash('AccessionID requested for code {}'.format(form.code.data))
        data=form.code.data
    ####
    '''
    data = form.code.data #Coge el input
    cursor.execute("(SELECT GENE.GeneID, GENE.Domain, GENE.Sequencefasta, GENE.PUBMEDID PUBMED_SAMPLE, GENE_PUBMED.GEOGRAPHY, GENE_PUBMED.LATITUDE, GENE_PUBMED.LONGITUDE, GENE_PUBMED.TEMPERATURE, GENE_PUBMED.POSITION_105, GENE_PUBMED.DEPTH, ' ' O2, GENE_PUBMED.LOW_FILTER, GENE_PUBMED.UPPER_FILTER FROM GENE, GENE_PUBMED WHERE GENE.GeneID = GENE_PUBMED.GeneID AND GENE.GeneID = '"+data+"')UNION (SELECT GENE_SAMPLE.GeneID , GENE.Domain, GENE.Sequencefasta, SAMPLE.SAMPLEID, SAMPLE.Province Geography, SAMPLE.LATITUDE, SAMPLE.LONGITUDE, SAMPLE.TEMPERATURE, ' ' POSITION_105,SAMPLE.DEPTH, SAMPLE.O2, SAMPLE.LOW_FILTER, SAMPLE.UPPER_FILTER FROM GENE, GENE_SAMPLE, SAMPLE WHERE GENE.GeneID = GENE_SAMPLE.GeneID AND GENE_SAMPLE.SAMPLEID = SAMPLE.SAMPLEID AND GENE_SAMPLE.GeneID = '"+data+"')")
    datac = cursor.fetchall() #Coger respuesta de la Base de Datos.
    print('ESTO ES SQL =', datac)
    if datac: # Si lo tenemos en la base de datos:
        datadict=datac[0]
        colnames = datadict.keys() #Coger las keys de uno de los diccionarios de la lista con Diccionarios que retorna el SQL, y usarlos como colnames.
        d=pd.DataFrame(columns = colnames, data = datac) #Pasar a Dataframe
        pd.set_option('display.width', 1000)
        pd.set_option('colheader_justify', 'center')
        return render_template('AccessionID.html',  tables=[d.to_html(classes='mystyle')], titles=d.columns.values)

    return render_template('home.html') # Si no lo tenemos no te muevas de página.

    #return render_template('AccessionID.html',value = d)
    #return render_template('home.html')


'''
    datap = datac[0] 
    if datac[0]:
        return render_template('AccessionID.html', value=datap)
    return render_template('AccessionID.html', value = 0)
'''   
    #return render_template("home.html",form = form)


@app.route("/PUBMEDID", methods=['GET', 'POST'])
def PUBMEDID():
    form = CodeForm1(request.form)
    '''## EL IF NO HACE FALTA
    if form.validate_on_submit():
        flash('AccessionID requested for code {}'.format(form.code.data))
        data=form.code.data
    ####
    '''
    dataa = form.code.data #Coge el input
    cursor.execute("(SELECT GENE.GeneID, GENE.Domain, GENE.Sequencefasta, GENE.PUBMEDID PUBMED_SAMPLE, GENE_PUBMED.GEOGRAPHY, GENE_PUBMED.LATITUDE, GENE_PUBMED.LONGITUDE, GENE_PUBMED.TEMPERATURE, GENE_PUBMED.POSITION_105, GENE_PUBMED.DEPTH,GENE_PUBMED.ABSORPTION, ' ' O2, GENE_PUBMED.LOW_FILTER, GENE_PUBMED.UPPER_FILTER FROM GENE, GENE_PUBMED WHERE GENE.GeneID = GENE_PUBMED.GeneID AND GENE_PUBMED.PUBMEDID = '"+dataa+"')")
    datac = cursor.fetchall() #Coger respuesta de la Base de Datos.
    if datac: # Si lo tenemos en la base de datos:
        datadict=datac[0]
        colnames = datadict.keys() #Coger las keys de uno de los diccionarios de la lista con Diccionarios que retorna el SQL, y usarlos como colnames. 
        df=pd.DataFrame(columns = colnames, data = datac) #Pasar a Dataframe
    
        pd.set_option('display.width', 1000)
        pd.set_option('colheader_justify', 'center')
        return render_template('PUBMEDID.html',  tables=[df.to_html(classes='mystyle')], titles=df.columns.values)

    return render_template('home.html') # Si no lo tenemos no te muevas de página.


'''
@app.route('/')
def index():
    return render_template(
        'index.html',
        data=[{'name':'red'}, {'name':'green'}, {'name':'blue'}])


@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.get('comp_select')
    return(str(select)) # just to see what select is
'''


@app.route("/METADATA", methods=['GET', 'POST'])
def METADATA():
    return render_template("METADATA.html")


@app.route("/RESULTS", methods=['GET', 'POST'])
def RESULTS():
    
    sdepth = request.form.get('depth') # El valor del select respecto a depth.
    stemp = request.form.get('temperature') # Respecto a temperature.
    sprovince = request.form.get('province') # Respecto a province.
    sgeo = request.form.get('geography')


    sql = "(SELECT GENE.GeneID, GENE.Domain, GENE.Sequencefasta, GENE.PUBMEDID PUBMED_SAMPLE, GENE_PUBMED.GEOGRAPHY, GENE_PUBMED.LATITUDE, GENE_PUBMED.LONGITUDE, GENE_PUBMED.TEMPERATURE, GENE_PUBMED.POSITION_105, GENE_PUBMED.DEPTH, ' ' O2, GENE_PUBMED.LOW_FILTER, GENE_PUBMED.UPPER_FILTER FROM GENE, GENE_PUBMED WHERE GENE.GeneID = GENE_PUBMED.GeneID
    
###################### DEPTH
    if sdepth != '0':
        if sdepth == '1':
            depthmin='0'
            depthmax='25'
        elif sdepth == '2':
            depthmin='25'
            depthmax='200'
        elif sdepth == '3':
            depthmin='200'
            depthmax='1000'
        elif sdepth=='4':
            depthmin:'1000'
            depthmax:'4000'
        sql1 += sql1 + "AND GENE_PUBMED.DEPTH >= '"+depthmin+"' AND GENE_PUBMED.DEPTH <= '"+depthmax+"'"
        sql2 += sql2 + "AND SAMPLE.DEPTH >= '"+depthmin+"' AND SAMPLE.DEPTH <= '"+depthmax+"'"


###################### TEMPERATURE	
    if stemp == '1':
        tempmin='0'
        tempmax='9'
    elif stemp == '2':
        tempmin='10'
        tempmax='20'
    elif stemp == '3':
        tempmin='21'
        tempmax='26'
    elif stemp == '4':
        tempmin='26'
        tempmax='30'
    elif stemp == '5':
        tempmin='30'
        tempmax='999'
    else:
        tempmin='0'
        tempmax='999'

###################### PROVINCE
### The value obtained is already the province num, therefore, not 'IF' is needed.

##################### GEOGRAPHY
        

    cursor.execute("(SELECT GENE.GeneID, GENE.Domain, GENE.Sequencefasta, GENE.PUBMEDID PUBMED_SAMPLE, GENE_PUBMED.GEOGRAPHY, GENE_PUBMED.LATITUDE, GENE_PUBMED.LONGITUDE, GENE_PUBMED.TEMPERATURE, GENE_PUBMED.POSITION_105, GENE_PUBMED.DEPTH, ' ' O2, GENE_PUBMED.LOW_FILTER, GENE_PUBMED.UPPER_FILTER FROM GENE, GENE_PUBMED WHERE GENE.GeneID = GENE_PUBMED.GeneID AND GENE_PUBMED.TEMPERATURE >= '"+tempmin+"' AND GENE_PUBMED.TEMPERATURE <= '"+tempmax+"' AND GENE_PUBMED.DEPTH >= '"+depthmin+"' AND GENE_PUBMED.DEPTH <= '"+depthmax+"' AND GENE_PUBMED.NUM_PROVINCE = '"+sprovince+"')UNION(SELECT DISTINCT(GENE_SAMPLE.GeneID) , GENE.Domain, GENE.Sequencefasta, SAMPLE.SAMPLEID, SAMPLE.Province Geography, SAMPLE.LATITUDE, SAMPLE.LONGITUDE, SAMPLE.TEMPERATURE, ' ' POSITION_105,SAMPLE.DEPTH, SAMPLE.O2, SAMPLE.LOW_FILTER, SAMPLE.UPPER_FILTER FROM GENE, GENE_SAMPLE, SAMPLE WHERE GENE.GeneID = GENE_SAMPLE.GeneID AND GENE_SAMPLE.SAMPLEID = SAMPLE.SAMPLEID AND SAMPLE.TEMPERATURE >= '"+tempmin+"' AND SAMPLE.TEMPERATURE <= '"+tempmax+"' AND SAMPLE.DEPTH >= '"+depthmin+"' AND SAMPLE.DEPTH <= '"+depthmax+"' AND SAMPLE.NUM_PROVINCE = '"+sprovince+"')")
    sql1=cursor.fetchall()
    datadict=sql1[0]
    colnames = datadict.keys()
    df=pd.DataFrame(columns = colnames, data = sql1)
    print('RESULTADO = ', df)

    return render_template('RESULTS.html', tables=[df.to_html(classes='mystyle')], titles=df.columns.values)
#    else:
 #       return(str(sdepth))
    
    









@app.route("/BLAST")
def BLAST():
    cursor.execute("SELECT TOP 30 * FROM GENE_SAMPLE")
    data = cursor.fetchall() #data from database
    return render_template("BLAST.html", value=data)









if __name__ == "__main__":
    app.run(debug=True)
  



#######
#######



