from flask import Flask, render_template, request, redirect                 # RETURN OPTIONS.
from flask_wtf import FlaskForm                                             # FORMS.
import pymysql.cursors                                                      # SQL CONECTION.
import os
from wtforms import StringField, PasswordField, BooleanField, SubmitField   # FORMS VARIABLES OPTIONS.
from wtforms.validators import DataRequired                                 # FORMS VARIABLE VALIDATORS.
from Bio import SeqIO                                                       # FASTA SEQUENCE MANIPULATION.
import pandas as pd                                                         # DATAFRAME CREATION.
from flask import flash, request, url_for, send_file                        # URL AND OPTIONS.
from flask import session                                                   # SESSION CREATION.


######################## FORMS CREATION
class CodeForm(FlaskForm):
    code = StringField('code', validators=[DataRequired()])                 # Getting code from search1 buttom.
    submit = SubmitField('Search1')
    
class CodeForm1(FlaskForm):
    code = StringField('code', validators=[DataRequired()])
    submit = SubmitField('Search2')

class CodeFormBlast(FlaskForm):
    code = StringField('Blastcode', validators=[DataRequired()])
    submit = SubmitField('BLAST')
    

######################## FLASK APP NAME AND SECRET KEY.
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


######################## CONNECTING TO THE DATABASE.
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='PRicm_2019',
                             db='mark',charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

######################## CREATING AN OPENED SESSION TO SAVE COOKIES.
@app.before_request
def session_management():
    session.permanent = True


####################### APPLICATION ROUTES!
@app.route("/")
def home():
     return render_template("home.html")                        # HOME ROUTE.


@app.route('/AccessionID' , methods=['GET', 'POST'])            # ACCESSION ID ROUTE.
def AccessionID():

    form = CodeForm(request.form)                               # Getting the INPUT ACC.ID from the form.
    data = form.code.data
    ################### QUERYING INTO SQL:
    cursor.execute("(SELECT GENE.GeneID, GENE.Domain, GENE.Sequencefasta, GENE.PUBMEDID PUBMED_SAMPLE, GENE_PUBMED.GEOGRAPHY, GENE_PUBMED.LATITUDE, GENE_PUBMED.LONGITUDE, GENE_PUBMED.TEMPERATURE, GENE_PUBMED.POSITION_105, GENE_PUBMED.DEPTH, ' ' O2, GENE_PUBMED.LOW_FILTER, GENE_PUBMED.UPPER_FILTER FROM GENE, GENE_PUBMED WHERE GENE.GeneID = GENE_PUBMED.GeneID AND GENE.GeneID = '"+data+"')UNION (SELECT GENE_SAMPLE.GeneID , GENE.Domain, GENE.Sequencefasta, SAMPLE.SAMPLEID, SAMPLE.Province Geography, SAMPLE.LATITUDE, SAMPLE.LONGITUDE, SAMPLE.TEMPERATURE, ' ' POSITION_105,SAMPLE.DEPTH, SAMPLE.O2, SAMPLE.LOW_FILTER, SAMPLE.UPPER_FILTER FROM GENE, GENE_SAMPLE, SAMPLE WHERE GENE.GeneID = GENE_SAMPLE.GeneID AND GENE_SAMPLE.SAMPLEID = SAMPLE.SAMPLEID AND GENE_SAMPLE.GeneID = '"+data+"')")
    datac = cursor.fetchall()                                   # Retrieving the result from the Database.
    print('ESTO ES SQL =', datac)
    if datac:                                                   # If its inside our DATABASE.
        datadict=datac[0]
        colnames = datadict.keys()                              # Get the keys from one of the dictionaries to extract COLUMNS NAMES.
        d=pd.DataFrame(columns = colnames, data = datac)        # Building the DataFrame.
        pd.set_option('display.width', 1000)
        pd.set_option('colheader_justify', 'center')            # Returning html page passing the Dataframe to visualize it.
        return render_template('AccessionID.html',  tables=[d.to_html(classes='mystyle')], titles=d.columns.values)

    return render_template('home.html')                         # If not data in Database, remain in home.html.


####################### This route is only used when the Client clicks on one AccessionID link, to send the client to the respective Acc.ID metadata.
@app.route('/AccessionID2/<path:code>',methods=['GET','POST'])
def AccessionID2(code):
    data = code                                                 # Getting the code passed in @app.route('/METADATA')
    if data:                                                    # If there is a code, QUERY it into our Database and get the results.
        cursor.execute("(SELECT GENE.GeneID, GENE.Domain, GENE.Sequencefasta, GENE.PUBMEDID PUBMED_SAMPLE, GENE_PUBMED.GEOGRAPHY, GENE_PUBMED.LATITUDE, GENE_PUBMED.LONGITUDE, GENE_PUBMED.TEMPERATURE, GENE_PUBMED.POSITION_105, GENE_PUBMED.DEPTH, ' ' O2, GENE_PUBMED.LOW_FILTER, GENE_PUBMED.UPPER_FILTER FROM GENE, GENE_PUBMED WHERE GENE.GeneID = GENE_PUBMED.GeneID AND GENE.GeneID = '"+data+"')UNION (SELECT GENE_SAMPLE.GeneID , GENE.Domain, GENE.Sequencefasta, SAMPLE.SAMPLEID, SAMPLE.Province Geography, SAMPLE.LATITUDE, SAMPLE.LONGITUDE, SAMPLE.TEMPERATURE, ' ' POSITION_105,SAMPLE.DEPTH, SAMPLE.O2, SAMPLE.LOW_FILTER, SAMPLE.UPPER_FILTER FROM GENE, GENE_SAMPLE, SAMPLE WHERE GENE.GeneID = GENE_SAMPLE.GeneID AND GENE_SAMPLE.SAMPLEID = SAMPLE.SAMPLEID AND GENE_SAMPLE.GeneID = '"+data+"')")
        datac = cursor.fetchall() 
        if datac: 
            datadict=datac[0]
            colnames = datadict.keys() 
            d=pd.DataFrame(columns = colnames, data = datac)    # Creating DataFrame and everything same as Acc.ID route.
            pd.set_option('display.width', 1000)
            pd.set_option('colheader_justify', 'center')
            return render_template('AccessionID.html',  tables=[d.to_html(classes='mystyle')], titles=d.columns.values)
        else:
            return render_template('RESULTS.html')
    return render_template('RESULTS.html')



@app.route("/PUBMEDID", methods=['GET', 'POST'])                # PUBMED ID route.
def PUBMEDID():
    form = CodeForm1(request.form)
    dataa = form.code.data                                      # Changing the querys as the information we want to provide now is different:
    cursor.execute("(SELECT GENE.GeneID, GENE.Domain, GENE.Sequencefasta, GENE.PUBMEDID PUBMED_SAMPLE, GENE_PUBMED.GEOGRAPHY, GENE_PUBMED.LATITUDE, GENE_PUBMED.LONGITUDE, GENE_PUBMED.TEMPERATURE, GENE_PUBMED.POSITION_105, GENE_PUBMED.DEPTH,GENE_PUBMED.ABSORPTION, ' ' O2, GENE_PUBMED.LOW_FILTER, GENE_PUBMED.UPPER_FILTER FROM GENE, GENE_PUBMED WHERE GENE.GeneID = GENE_PUBMED.GeneID AND GENE_PUBMED.PUBMEDID = '"+dataa+"')")
    datac = cursor.fetchall() 
    if datac: 
        datadict=datac[0]
        colnames = datadict.keys()
        df=pd.DataFrame(columns = colnames, data = datac)       # Creating DataFrame and everything same as Acc.ID route.
    
        pd.set_option('display.width', 1000)
        pd.set_option('colheader_justify', 'center')
        return render_template('PUBMEDID.html',  tables=[df.to_html(classes='mystyle')], titles=df.columns.values)

    return render_template('home.html')                         # If not PubmedID in our Database, remain in home.html.



@app.route("/METADATA", methods=['GET', 'POST'])                # METADATA route, where the FILTERING is done.
def METADATA():
    return render_template("METADATA.html")                     # All the filtering is shown in METADATA.html.


@app.route("/RESULTS", methods=['GET', 'POST'])
def RESULTS():
    
    sdepth = request.form.get('depth')                          # Getting the value that the client selected regarding DEPTH.
    stemp = request.form.get('temperature')                     # Getting the value that the client selected regarding TEMPERATURE.
    sprovince = request.form.get('province')                    # Getting the value that the client selected regarding PROVINCE.
    slow_filter = request.form.get('low_filter')                # Getting the value that the client selected regarding LOW_FILTER.
    supper_filter = request.form.get('upper_filter')            # Getting the value that the client selected regarding UPPER_FILTER.
    socean = request.form.get('ocean')                          # Getting the value that the client selected regarding OCEAN.
    sseason = request.form.get('season')                        # Getting the value that the client selected regarding SEASON.

###################### CREATING THE MAIN PART OF THE QUERY, WHERE WE SELECT THE FIELDS WE WANT TO SHOW IN THE SCREEN
    sql1 = "SELECT DISTINCT GENE.GeneID, GENE.Domain, GENE.Phylum, GENE.Species, GENE.Sequencefasta, GENE_PUBMED.POSITION_105 FROM GENE, GENE_PUBMED WHERE GENE.GeneID = GENE_PUBMED.GeneID "
    sql2 = "SELECT DISTINCT GENE.GeneID , GENE.Domain, GENE.Phylum, GENE.Species,GENE.Sequencefasta, ' ' POSITION_105 FROM GENE, GENE_SAMPLE, SAMPLE WHERE GENE.GeneID = GENE_SAMPLE.GeneID AND GENE_SAMPLE.SAMPLEID = SAMPLE.SAMPLEID "

###################### EDDITING THE QUERY REGARDING CLIENTS SELECTION:
###################### DEPTH
    if sdepth != '0':
        if sdepth == '1':                                       # If the value selected by clients is 1...
            depthmin='0'
            depthmax='25'
        elif sdepth == '2':
            depthmin='26'
            depthmax='200'
        elif sdepth == '3':
            depthmin='201'
            depthmax='1000'
        elif sdepth == '4':
            depthmin='1001'
            depthmax='9999'

        sql1 += "AND GENE_PUBMED.DEPTH >= '"+depthmin+"' AND GENE_PUBMED.DEPTH <= '"+depthmax+"' "
        sql2 += "AND SAMPLE.DEPTH >= '"+depthmin+"' AND SAMPLE.DEPTH <= '"+depthmax+"' "


###################### TEMPERATURE
    if stemp != '0':
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

        sql1 += "AND GENE_PUBMED.TEMPERATURE >= '"+tempmin+"' AND GENE_PUBMED.TEMPERATURE <= '"+tempmax+"' "
        sql2 += "AND SAMPLE.TEMPERATURE >= '"+tempmin+"' AND SAMPLE.TEMPERATURE <= '"+tempmax+"' "


###################### PROVINCE                                 # The value obtained is already the province num, therefore, not sub 'IF' are needed.

    if sprovince !='0':
        sql1 += "AND GENE_PUBMED.Num_Province = "+sprovince+" " # As sprovince is an INT, no commas required, it is not a string.
        sql2 += "AND SAMPLE.ProvinceNum = "+sprovince+" "       # As sprovince is an INT, no commas required, it is not a string.

###################### LOWER FILTER

    if slow_filter != '0':
        if slow_filter =='1':
            low_filter = '0.22'
            low_filter2= '0.2'
            
        elif slow_filter=='2':
            low_filter= '0.4'
            low_filter2= '0.45'
            
        elif slow_filter =='3':
            low_filter = '0.6'
            low_filter2= '0.6'
            
        elif slow_filter =='4':
            low_filter = '0.8'
            low_filter2= '0.8'
        sql1 += "AND (GENE_PUBMED.LOW_FILTER = '"+low_filter+"' OR GENE_PUBMED.LOW_FILTER = '"+low_filter2+"') "
        sql2 += "AND (SAMPLE.LOW_FILTER = '"+low_filter+"' OR SAMPLE.LOW_FILTER = '"+low_filter2+"') "
            
        
#################### UPPER FILTER
    if supper_filter != '0':
        if supper_filter =='1':
            upper_filter = '0.6'       
        elif supper_filter=='2':
            upper_filter= '0.8'
        elif supper_filter =='3':
            upper_filter = '1.6'
        elif supper_filter =='4':
            upper_filter = '2'
        elif supper_filter =='5':
            upper_filter = '3'
        elif supper_filter =='6':
            upper_filter ='5'

        sql1 += "AND GENE_PUBMED.UPPER_FILTER = '"+upper_filter+"' "
        sql2 += "AND SAMPLE.UPPER_FILTER = '"+upper_filter+"' "


##################### OCEAN
    if socean !='0':
        if socean == '1':
            ocean='Atlantic'
        elif socean =='2':
            ocean='Pacific'
        elif socean=='3':
            ocean='Indian'
        elif socean=='4':
            ocean='Antarctic'
        elif socean=='5':
            ocean='Arctic'
        sql1 += "AND GENE_PUBMED.Ocean = '"+ocean+"' "
        sql2 += "AND SAMPLE.Ocean = '"+ocean+"' "

####################### SEASON
    if sseason !='0':
        if sseason == '1':
            season='Winter'
        elif sseason == '2':
            season='Spring'
        elif sseason =='3':
            season='Summer'
        elif sseason =='4':
            season='Autumn'
        sql1 += "AND GENE_PUBMED.SEASON = '"+season+"' "
        sql2 += "AND SAMPLE.SEASON = '"+season+"' "

####################### END OF FILTERING
        
####################### QUERYING THE FULL SQL THAT THE CLIENT CHOOSE
        
    cursor.execute("("+sql1+") UNION ("+sql2+")")               # The UNION is needed as we are querying into PUBMED and SAMPLE entities from our DATABASE.
    sqltot=cursor.fetchall()                                    # Get the results.
    
    if sqltot:
        datadict=sqltot[0]
        colnames = datadict.keys()
        df=pd.DataFrame(columns = colnames, data = sqltot)
        var=df['GeneID']
        #link= "{{ url_for('AccessionID',code="+var+") }}"      # Another way of creating a LINK.
        #df['GeneID']= '<a href="{}">'+var+'</a>'.format(link)  # Another way of creating a LINK.
        df['GeneID']="<a href='/AccessionID2/"+var+"'>"+var+"</a>" # Our way of creating a LINK to AccessionID2.

        pd.set_option('display.max_colwidth', 130)              # Expanding column width to allow full GeneIDLink visualization.
        PRdf = df.to_html(classes=['mystyle'],escape=False)     # Swapping DataFrame display to facilitate passing it to html.

        ############################## MODIFYING SQL-QUERY TO ALLOW SAVING IT INTO THE SESSION.
        from1 = sql1.index('FROM')                              # Getting the query from 'FROM' until END.
        from2 = sql2.index('FROM')                              # Same for sql2.
        sqlsession='(SELECT GENE.GeneID '+sql1[from1::]+')UNION(SELECT DISTINCT GENE.GeneID '+sql2[from2::]+')' #Creating the NEW QUERY to be passes through SESSION.
        
        ############################## SAVING THE QUERY INTO SESSION.
        session['datadownload']=sqlsession

        return render_template('RESULTS.html', tables=[PRdf], titles=df.columns.values)
    else:
        return render_template('METADATA.html')
    
    

@app.route("/FASTA", methods=['GET', 'POST'])
def FASTA():

    ################################# Getting Client's choise.
    stype = request.form.get('fasta')                          # Getting the value that the client selected regarding FASTA.
    ################################# COLLECT SESSION INFORMATION
    if 'datadownload' in session:                               # If session is ocupied.
        sqlsession=session['datadownload']                      # Extract the information passed.
        cursor.execute(sqlsession)                              # Query against DB.
        sqltot2=cursor.fetchall()                               # Recieve the result of the query.

        ############################# CREATING THE FILE THAT WILL BE GIVEN TO THE CLIENT AND OUTPUTING IT.
         #From our DATABASE.
        with open('OUTPUT_FASTA.fa','w') as out_file:           # CREATE THE EMPTY FILE, CALLED OUTPUT_FASTA.fa
            geneids=[]                                          # Put all values of the dictionaries in a list, as SQL returns a list of dictionaries.
            for dictionary in sqltot2:
                geneids+=list(dictionary.values())		# Add the values one by one.

            if stype=='0':                                          # If client selects NUC.
                fasta_sequences = SeqIO.parse(open('/home/mark/Escritorio/PRACTICAS_ICM_CSIC/BASESDEDATOS/NUCDATABASE.fa'),'fasta')
                for fasta in fasta_sequences:                       # For each entry of the DATABASE.
                    name, sequence = fasta.id, str(fasta.seq)
                    for geneid in geneids:                          # Compare the database IDs with the GeneID from the list.
                        if geneid == fasta.id:
                            out_file.write('>'+name+'\n')           # Write in the output file.
                            out_file.write('\n'.join([sequence[i:i+60] for i in range(0,len(sequence),60)])+'\n') #Each 60 AA break the line.
            
            elif stype=='1':                                        # If client selects AA.
                fasta_sequences = SeqIO.parse(open('/home/mark/Escritorio/PRACTICAS_ICM_CSIC/BASESDEDATOS/PRODATABASE.faa'),'fasta')
                for fasta in fasta_sequences:
                    name, sequence = fasta.id, str(fasta.seq)
                    for geneid in geneids:       
                        if geneid == fasta.id:
                            out_file.write('>'+name+'\n')           
                            out_file.write('\n'.join([sequence[i:i+60] for i in range(0,len(sequence),60)])+'\n')
            out_file.close()

        session.clear()                                         # Clean the session.


        return send_file('/home/mark/Escritorio/GIT/ICM_CSIC/WEBPAGE/OUTPUT_FASTA.fa', attachment_filename='OUTPUT_FASTA.fa')                  # Return the file.
        #return render_template('RESULTS.html')
    
    return render_template('METADATA.html')




@app.route("/BLAST",methods=['GET', 'POST'])
def BLAST():
        
    return redirect('http://localhost:4567')



@app.route("/BLASTOUTPUT", methods=['GET','POST'])
def BLASTOUTPUT():
    
    form = CodeFormBlast(request.form)
    query=form.code.data





if __name__ == "__main__":
    app.run(debug=True)
  




####### SQLTOTAL = "(SELECT GENE.GeneID, GENE.Domain, GENE.Sequencefasta, GENE.PUBMEDID PUBMED_SAMPLE, GENE_PUBMED.GEOGRAPHY, GENE_PUBMED.LATITUDE, GENE_PUBMED.LONGITUDE, GENE_PUBMED.TEMPERATURE, GENE_PUBMED.POSITION_105, GENE_PUBMED.DEPTH, ' ' O2, GENE_PUBMED.LOW_FILTER, GENE_PUBMED.UPPER_FILTER FROM GENE, GENE_PUBMED WHERE GENE.GeneID = GENE_PUBMED.GeneID AND GENE_PUBMED.TEMPERATURE >= '"+tempmin+"' AND GENE_PUBMED.TEMPERATURE <= '"+tempmax+"' AND GENE_PUBMED.DEPTH >= '"+depthmin+"' AND GENE_PUBMED.DEPTH <= '"+depthmax+"' AND GENE_PUBMED.NUM_PROVINCE = '"+sprovince+"')UNION(SELECT DISTINCT(GENE_SAMPLE.GeneID) , GENE.Domain, GENE.Sequencefasta, SAMPLE.SAMPLEID, SAMPLE.Province Geography, SAMPLE.LATITUDE, SAMPLE.LONGITUDE, SAMPLE.TEMPERATURE, ' ' POSITION_105,SAMPLE.DEPTH, SAMPLE.O2, SAMPLE.LOW_FILTER, SAMPLE.UPPER_FILTER FROM GENE, GENE_SAMPLE, SAMPLE WHERE GENE.GeneID = GENE_SAMPLE.GeneID AND GENE_SAMPLE.SAMPLEID = SAMPLE.SAMPLEID AND SAMPLE.TEMPERATURE >= '"+tempmin+"' AND SAMPLE.TEMPERATURE <= '"+tempmax+"' AND SAMPLE.DEPTH >= '"+depthmin+"' AND SAMPLE.DEPTH <= '"+depthmax+"' AND SAMPLE.NUM_PROVINCE = '"+sprovince+"')"


#######
#######



