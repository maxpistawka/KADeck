from flask import Flask, flash, render_template, request, redirect, session
from flask_mysqldb import MySQL
from datetime import date
from hgtk.exception import NotHangulException
from supermemo2 import SMTwo
import hgtk
import os
from flask import request



today = date.today()
app = Flask(__name__, template_folder='template')
secret = os.urandom(24) 
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "Max"
app.config['MYSQL_PASSWORD'] = "max123"
app.config['MYSQL_DB'] = "korean_decks"

mysql = MySQL(app)

currID = -1

app.config["SECRET_KEY"] = secret

def verify():
    global currID
    if currID > 0:
        return True
    if int(session.get('userid', -1)) > 0:
        currID = int(session.get('userid', -1))
        return True
    else: 
        return False
    
@app.route('/', methods=['GET', 'POST'])
def index():
    global currID
    if int(session.get('userid', -1)) > 0:
        currID = int(session.get('userid', -1))
        return redirect("/loggedin", code=301)
    
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'signup_identifier':
            try:
                username = request.form['username']
                email = request.form['email']
                password = request.form['password']
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users (username,pass, email, date_registered) VALUES (%s, %s, %s, %s)",
                            (username, password, email, today))
                mysql.connection.commit()
                cur.close()
                return "success"
            except:
                flash('Invalid Credentials')
                """# nothing"""
        elif request.form['btn_identifier'] == 'login_identifier':
            
                
                email = request.form['email']
                password = request.form['password']

                cur = mysql.connection.cursor()

                cur.execute("SELECT * FROM users WHERE email = '" + email + "' AND pass = '" + password + "'")

                result = cur.fetchone()
                if result:
                    currID = result[0]
                    cur.close()
                    session['userid'] = currID
                    return redirect("/loggedin", code=301)
            
        flash('Invalid Credentials')

    return render_template('index.html')
@app.route('/loggedin', methods = ['GET', 'POST'])
def loggedin():
    
    if not verify():
        return redirect("/", code=301)
    
    cur = mysql.connection.cursor()

    if request.method == 'POST':

        cur.execute("INSERT INTO decks (title, date_created, admin_user_id) VALUES (%s, %s, %s)",
                    (request.form['title'], today, currID))
        mysql.connection.commit()
        cur.execute("SELECT * FROM decks ORDER BY (deck_id) DESC LIMIT 1")
        deck_id = cur.fetchone()[0]
        cur.execute("INSERT INTO decks_user (deck_id, user_id) VALUES (%s, %s)", (deck_id, currID))
        mysql.connection.commit()
        return "successfully did it"

    cur.execute("SELECT * FROM decks_user WHERE user_id != " + str(currID))
    unfilteredDecks = cur.fetchall()
    ids = []
    for deck in unfilteredDecks:
        ids.append(deck[0])
    
    decks = []
    for id in ids:
        cur.execute("SELECT * FROM decks WHERE deck_id = " + str(id))
        deck = cur.fetchone()
        decks.append([str(deck[1]), deck[0]])

 
    cur.execute("SELECT * FROM decks_user WHERE user_id = " + str(currID))
    unfilteredDecks = cur.fetchall()
    ids = []
    for deck in unfilteredDecks:
        ids.append(deck[0])
    
    user_decks = []
    for id in ids:
        cur.execute("SELECT * FROM decks WHERE deck_id = " + str(id))
        deck = cur.fetchone()
        user_decks.append([str(deck[1]), deck[0]])


    return render_template('main.html', posts=user_decks, decks=decks)

@app.route('/subscribe_deck/<string:deck_id>')
def subscribe(deck_id):
    if not verify():
        return redirect("/", code=301)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO decks_user (deck_id, user_id) VALUES (%s, %s)", (deck_id, currID))
    mysql.connection.commit()
    cur.close()
    return "success"



@app.route('/deck/<string:deck_id>')
def deckView(deck_id):
    if not verify():
        return redirect("/", code=301)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM decks WHERE deck_id = " + str(deck_id))
    deck_name = cur.fetchone()[1]
    return render_template("view.html", deckid=deck_id, deckname=deck_name)



@app.route('/deck/<string:deck_id>/edit', methods = ['GET', 'POST'])
def deckEdit(deck_id):
    if not verify():
        return redirect("/", code=301)
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        if request.form['btn_identifier'] == 'add_identifier':
            english = request.form['english']
            korean = request.form['korean']
            ends = endsGenerator(korean)
            cur.execute("INSERT INTO vocabulary (deck_id, korean, english, endings) VALUES (%s, %s, %s, %s)",
                        (deck_id, korean, english, ends))

            mysql.connection.commit()

            return "added " + english + ": " + korean + ": " + ends
        elif request.form['btn_identifier'] == 'title_identifier':
            cur.execute("UPDATE decks SET title = '" + request.form['title'] + "' WHERE deck_id = " + str(deck_id))
            mysql.connection.commit()
            return "changed title"


    cur.execute("SELECT * FROM vocabulary WHERE deck_id = " + str(deck_id))
    vocab = cur.fetchall()

    return render_template("edit.html", deckid=deck_id, vocabs=vocab)

def endsGenerator(kor):
    ends = ""
    for s in range(len(kor) - 1):
        try:
            decomposed = hgtk.letter.decompose(kor[s])
            if decomposed[-1]:
                try:
                    nextDecomposed = hgtk.letter.decompose(kor[s + 1])
                    ends += decomposed[-1] + nextDecomposed[0]
                except NotHangulException:
                    """ nothing """
        except NotHangulException:
            """ not Hangul """
    return ends
@app.route('/unsubscribe/<string:deck_id>')
def unsubscribe(deck_id):
    if not verify():
        return redirect("/", code=301)
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM decks_user WHERE deck_id = " + str(deck_id) + " AND user_id = " + str(currID))
    mysql.connection.commit()
    return "unsubscribe from" + str(deck_id)


@app.route('/deletevocab/<string:vocab_id>')
def deleteVocab(vocab_id):
    if not verify():
        return redirect("/", code=301)
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM vocabulary WHERE vocab_id = " + str(vocab_id))
    cur.execute("DELETE FROM logs WHERE vocab_id = " + str(vocab_id))
    mysql.connection.commit()
    return "delete vocab" + str(vocab_id)



@app.route('/deck/<string:deck_id>/review/<string:vocab_id>', methods = ['GET', 'POST'])
def deckReview(deck_id, vocab_id):
    if not verify():
        return redirect("/", code=301)
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        return redirect('/deck/' + str(deck_id) + '/review-back/' + vocab_id)

    if int(vocab_id) < 0:
        currVocab = getNextVocab(deck_id)
        return redirect('/deck/' + str(deck_id) + '/review/' + str(currVocab[0]))
    cur.execute("SELECT * FROM vocabulary WHERE vocab_id = " + str(vocab_id))
    currVocab = cur.fetchone()

    return render_template("reviewfront.html", vocab=currVocab)


@app.route('/deck/<string:deck_id>/review-back/<string:vocab_id>', methods=['GET', 'POST'])
def deckReviewBack(deck_id, vocab_id):
    if not verify():
        return redirect("/", code=301)
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        if request.form['btn_identifier'] == "flip":
            return redirect('/deck/' + str(deck_id) + '/review/' + vocab_id)
        score = int(request.form['btn_identifier'])
        urgencyCalc(score, deck_id, vocab_id)
        mysql.connection.commit()
        return redirect('/deck/' + str(deck_id) + '/review/-1')

    cur.execute("SELECT * FROM vocabulary WHERE vocab_id = " + str(vocab_id))
    currVocab = cur.fetchone()
    return render_template("reviewback.html", vocab=currVocab)

def urgencyCalc(score, deck_id, vocab_id):
    if not verify():
        return redirect("/", code=301)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM logs WHERE vocab_id = " + str(vocab_id) + " AND user_id = " + str(currID))
    log = cur.fetchone()
    if log is None:
        review = SMTwo.first_review(score)
        cur.execute("INSERT INTO logs (deck_id, vocab_id, user_id, next_date, easiness, review_interval, repetitions) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (int(deck_id), int(vocab_id), int(currID) ,review.review_date, review.easiness, review.interval, review.repetitions))
    else:
        review = SMTwo(log[5], log[6], log[7]).review(score)
        cur.execute("UPDATE logs SET next_date = %s, easiness = %s, review_interval = %s, repetitions = %s WHERE log_id = "
                    + str(log[0]), (review.review_date, review.easiness, review.interval, review.repetitions))
    mysql.connection.commit()


def getNextVocab(deck_id):
    if not verify():
        return redirect("/", code=301)
    ''' first look for days before today in logs, then look forvocab in the deck that arent in logs, then look for one in logs with the soonest time after, then just pick a random one.'''
    cur = mysql.connection.cursor()

    # Any to-dos?
    cur.execute("SELECT * FROM logs WHERE deck_id = %s AND user_id = %s AND next_date < %s ORDER BY next_date ASC LIMIT 1",
                (deck_id, currID, today))
    log = cur.fetchone()

    if log is not None:
        cur.execute("SELECT * FROM vocabulary WHERE vocab_id = " + str(log[2]))
        return cur.fetchone()

    # Any no-log vocab? (a vocab that belongs to the deck that a user has no logs for)

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM vocabulary WHERE vocab_id NOT IN (SELECT vocab_id FROM logs WHERE user_id = " + str(currID) + ")")

    vocab = cur.fetchone()
    if vocab:
        return vocab


    # Any to-do in the future vocab?
    cur.execute("SELECT * FROM logs WHERE deck_id = %s AND user_id = %s AND next_date >= NOW() ORDER BY next_date ASC LIMIT 1",
                (deck_id, currID))
    log = cur.fetchone()

    if log:
        cur.execute("SELECT * FROM vocabulary WHERE vocab_id = " + str(log[2]))
        return cur.fetchone()
    # Random One

    cur.execute("SELECT * FROM vocabulary WHERE deck_id = " + str(deck_id) + " ORDER BY RAND() LIMIT 1")
    return cur.fetchone()

if __name__ == "__main__":
    app.run(debug=True)

