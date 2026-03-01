from my_server import app
from flask import render_template, request, redirect, url_for, flash, session
from my_server.dbhandler import create_connection

@app.route('/')
@app.route('/index')
def start():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cookies')
def cookies():
    return render_template('cookies.html')

@app.route('/delete_account')
def delete_account():
    user_id = session['id']
    conn = create_connection()
    cur = conn.cursor()
    sql = f'DELETE FROM users WHERE id="{user_id}"'
    cur.execute(sql)
    conn.commit()
    conn.close()
    session['logged_in'] = False
    session.pop('id')
    return redirect(url_for('start'))

@app.route('/delete/<msg_id>')
def delete(msg_id = ''):
    conn = create_connection()
    cur = conn.cursor()
    sql = f'DELETE FROM messages WHERE id="{msg_id}"'
    print(msg_id)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return redirect(url_for('inbox'))

@app.route('/inbox', methods=['GET'])
def inbox():
    if session['logged_in'] == True: 

        id = session['id']

        conn = create_connection()
        cur = conn.cursor()
        sql = f'SELECT * FROM MESSAGES WHERE receiver="{id}"'
        messages = cur.execute(sql).fetchall()
        conn.commit()
        conn.close()

        return render_template('inbox.html', messages=messages)
    else:
        return redirect(url_for('login'))

@app.route('/list_users', methods=['GET'])
def list_users():
    if session['logged_in'] == True: 

        conn = create_connection()
        cur = conn.cursor()
        sql = 'SELECT * FROM users'
        users = cur.execute(sql).fetchall()
        conn.commit()
        conn.close()

        return render_template('list_users.html', users=users)
    else:
        return redirect(url_for('login'))

#om kommer till new_mail/<receiver> ska sidan renderas, där reciever_id ingår i formuläret via en input type="hidden"
#formuläret ska sedan skicka användaren vidare till new_mail (ingen receiver_id). När användaren kommer hit, ska all nödvändig
#information hämtas från formuläret och sedan sparas i databasen. användaren kan sedan skickas vidare till startsidan.

@app.route('/new_mail', methods=['POST'])
def new_mail_form():

    user_id = session['id']
    receiver_id = request.form['receiver_id']
    heading = request.form['heading']
    context = request.form['context']
    status = False

    conn = create_connection()
    cur = conn.cursor()
    sql = f'INSERT INTO messages(sender, receiver, heading, context, status) VALUES ("{user_id}", "{receiver_id}", "{heading}", "{context}", "Oläst")'
    cur.execute(sql)
    conn.commit()
    conn.close()

    flash('Meddelandet var skickat')
    return redirect(url_for('inbox'))

@app.route('/new_mail/<receiver_id>', methods=['GET'])
def new_mail(receiver_id = ''):
    return render_template('new_mail.html', receiver_id=receiver_id)

@app.route('/note', methods=['GET', 'POST'])
def note():
    return render_template('note.html')
    
@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = create_connection()
        cur = conn.cursor()
        sql = f'SELECT id, password FROM users WHERE username="{username}"'
        row = cur.execute(sql).fetchone()

        if password == row[1]:
            session['logged_in'] = True
            session['id'] = row[0]
            upd_nr = f'UPDATE users SET nr_login=nr_login + 1 WHERE username="{username}"'
            cur.execute(upd_nr)
            conn.commit()
            conn.close()
            return redirect(url_for('inbox'))
        else:
            flash('Kontrollera värderna')
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('id')
    return redirect(url_for('start'))

@app.route('/my_account')
def my_account():

    id = session['id']
    conn = create_connection()
    cur = conn.cursor()
    sql = f'SELECT * FROM users WHERE id="{id}"'
    users = cur.execute(sql).fetchone()
    conn.commit()
    conn.close()
    return render_template('my_account.html', users=users)

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/new_account', methods=['GET', 'POST'])
def new_account():
    if request.method == 'POST':

        name = request.form['name']
        surname = request.form['surname']
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']

        if password == password2:
            conn = create_connection()
            cur = conn.cursor()
            sql = f'INSERT INTO users(name, surname, username, password, nr_login) VALUES ("{name}", "{surname}", "{username}", "{password}", "0")'
            cur.execute(sql)
            conn.commit()
            conn.close()
            return redirect(url_for('login'))   
        else: 
            flash('Lösenorden stämmer inte överens. Försök igen', 'warning')
            return render_template('new_account.html')
    else:
        return render_template('new_account.html')

# skapa sidan read_email.html
# när användaren klickar på en länk (som ligger i inbox.html) ska användaren komma till sidan "/reademail/<id>", där id är id till 
# det mail som hen just klickade på
# Sidan ska med utgång i id hitta det aktuella mailet i databsen och presentera hela mailet (så det går att läsa)

@app.route('/reademail/<id>')
def read_email(id=''):
    
    conn = create_connection()
    cur = conn.cursor()

    change_status = f'UPDATE messages SET status="Läst" WHERE id={id}'
    cur.execute(change_status)

    sql = f'SELECT messages.id, users.username, messages.heading, messages.context FROM messages JOIN users ON messages.sender=users.id WHERE messages.id="{id}"' #id=på mail
    message = cur.execute(sql).fetchone()

    conn.commit()
    conn.close()
    
    return render_template('read_email.html', message=message)

@app.route('/secrecy')
def secrecy():
    #
    return render_template('secrecy.html')

@app.route('/support', methods=['GET', 'POST'])
def support():
        return render_template('support.html')

@app.route('/terms_of_use')
def terms_of_use():
    return render_template('terms_of_use.html')