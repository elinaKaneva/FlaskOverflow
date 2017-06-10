import os, sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, '_stackoverflow.db'),
	SECRET_KEY='development key',
	DEBUG=True
	))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Database set up:
def connect_db():
    '''Connects to the specific database.'''
    rv = sqlite3.connect(app.config['DATABASE'])
    '''Opens a connection to the SQLite database file db. If successful, 
    returns a connection object.'''
    rv.row_factory = sqlite3.Row
    ''' Row instance is highly optimized row_factory for Connection objects.
    Mimics a tuple in most features. Supports mapping access by column name
    and index, iteration, representation, equality testing and len().
    More: https://docs.python.org/2/library/sqlite3.html#sqlite3.Row'''
    return rv

def get_db():
    '''Opens a new database connection if there is none yet for the
    current application context.'''
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
	'''Initialize the database content from a schema.'''
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read()) # executescript() executes multiple SQL statements with one call
	db.commit() # commit() saves changes to the database (done by insert or update statements)

@app.cli.command('initdb')
def initdb_command():
    '''Initializes the database.'''
    init_db()
    print('Initialized the database.')

@app.teardown_appcontext
def close_db(error):
    '''Closes the database again at the end of the request.'''
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        # Closes the database connection, does NOT automatically call commit()!

# Routing:
@app.route('/')
def list_questions():
    db = get_db()
    #id is also added for debugging purposes
    cur = db.execute('select title, text, id from questions order by id desc')
    questions = cur.fetchall()
    return render_template('list_questions.html', questions=questions)

@app.route('/add_question', methods=['POST'])
def add_question():
    # if not session.get('logged_in'):
    #     abort(401)
    db = get_db()
    db.execute('insert into questions (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New question was successfully added.')
    return redirect(url_for('list_questions'))

@app.route('/questions/')
def questions():
    return redirect(url_for('list_questions'))

@app.route('/questions/<int:qid>')
def get_question(qid):
    db = get_db()
    q = db.execute('select * from questions where id = %d' % qid)
    question = q.fetchone()
    a = db.execute('select text from answers where qid is %s' % qid)
    answers = a.fetchall()
    return render_template('show_question.html', question=question, answers=answers)

@app.route('/add_answer', methods=['POST'])
def add_answer():
    db = get_db()
    qid = request.form['qid']
    db.execute('insert into answers (text, qid) values (?, ?)', (request.form['text'], qid))
    db.commit()
    flash('New answer was successfully added.')
    return redirect(url_for('get_question', qid=qid))