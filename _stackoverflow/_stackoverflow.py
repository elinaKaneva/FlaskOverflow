import os, sqlite3, sys, unicodedata
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
def feed():
    return redirect(url_for('questions'))

@app.route('/questions/')
def questions():
    db = get_db()
    q = db.execute('SELECT * FROM Question ORDER BY id DESC').fetchall()
    questions = []

    for eachQ in q:
        questions.append({
        'id': eachQ['id'],
        'title': eachQ['title'],
        'tags': db.execute('SELECT name FROM Tag WHERE id IN (SELECT tag_id FROM QuestionTag WHERE question_id = %d)' % eachQ['id']).fetchall()
        })

    return render_template('question_feed.html', questions=questions)

#TBD: ask_question and add_question can be combined - by checking for query method - GET, POST
@app.route('/questions/ask')
def ask_question():
    return render_template('ask_question.html')

@app.route('/add_question', methods=['POST'])
def add_question():
    # if not session.get('logged_in'):
    #     abort(401)
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('INSERT INTO Question (title, text) VALUES (?, ?)',
                 [request.form['title'], request.form['text']])
    question_id = cursor.lastrowid

    tags_input = unicodedata.normalize('NFKD', request.form['tags']).encode('ascii','ignore')
    tags = tags_input.split(" ")
    for eachTag in tags:
        # import pdb; pdb.set_trace()
        try:
            cursor.execute('INSERT INTO Tag (name) VALUES ("%s")' % (eachTag))
            tag_id = cursor.lastrowid
        except sqlite3.IntegrityError as e:
            tag_id = cursor.execute('SELECT * FROM Tag WHERE name = "%s"' % eachTag).fetchone()['id']
            print('SQLite Error: ', e.args, sys.exc_info())
        cursor.execute('INSERT INTO QuestionTag (question_id, tag_id) VALUES ("%s", "%s")' % (question_id, tag_id))

    db.commit()
    flash('New question was successfully added.')
    return redirect(url_for('questions'))

@app.route('/questions/<int:question_id>')
def get_question(question_id):
    db = get_db()
    question = db.execute('SELECT * FROM Question WHERE id = %d' % question_id).fetchone()
    answers = db.execute('SELECT * FROM Answer WHERE question_id = %d' % question_id).fetchall()
    tags = db.execute('SELECT name FROM Tag WHERE id IN (SELECT tag_id FROM QuestionTag WHERE question_id = %d)' % question['id']).fetchall()
    return render_template('show_question.html', question=question, answers=answers, tags=tags)

@app.route('/add_answer', methods=['POST'])
def add_answer():
    db = get_db()
    question_id = request.form['question_id']
    db.execute('INSERT INTO Answer (text, question_id) VALUES (?, ?)', (request.form['text'], question_id))
    db.commit()
    flash('New answer was successfully added.')
    return redirect(url_for('get_question', question_id=question_id))
