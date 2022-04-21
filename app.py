
from flask import *
from flask_mysqldb import MySQL
import shortuuid

app=Flask(__name__)
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']= "*******"
app.config['MYSQL_DB']="url"

mysql=MySQL(app)

@app.route('/',methods=['GET','POST'])
def shorten():
    
    if request.method == 'POST':
        url = request.form['url']
        
        if not url:
            flash('The URL is required!')
            return redirect(url_for('shorten'))

        cur = mysql.connection.cursor()
        short_url = shortuuid.ShortUUID().random(length=7)
        query = "INSERT INTO urlstable (link, shortenlink) VALUES (%s, %s)"
        cur.execute(query,(url, short_url))
        mysql.connection.commit()
        cur.close()
        
        
        return render_template('index.html',short_url=short_url)
    return render_template('index.html')


@app.route('/<short_url>')
def getlink(short_url):

    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM urlstable WHERE shortenlink = (%s)",(short_url,))
    data = cur.fetchone()

    if data:
        return redirect(data[0])

    cur.close()
    flash('Invalid URL')
    return redirect(url_for('shorten'))

if __name__=='__main__' :
    app.secret_key='******'
    app.run(debug=True)
