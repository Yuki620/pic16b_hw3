from flask import Flask, g, render_template, request
import sqlite3

app = Flask(__name__)

def get_message_db():
  # see if message_db exists already
  try:
      return g.message_db
  # if not then create it
  except:
      g.message_db = sqlite3.connect("messages_db.sqlite")
      cmd = '''
            CREATE TABLE IF NOT EXISTS messages (
                handle text,
                message text
            )
            ''' 
      cursor = g.message_db.cursor()
      cursor.execute(cmd)
      return g.message_db
  
def insert_message(request):
    # Extract message and handle from the form data
    msg = request.form["message"]
    hdl = request.form["handle"]

    # Get the database connection
    db = get_message_db()
    cursor = db.cursor()

    # insertion of handle and message values into `messages` table
    # `?` for value placeholders
    insert_sql = '''
                 INSERT INTO messages (handle, message)
                 VALUES (?, ?)
                 '''
    cursor.execute(insert_sql, (hdl, msg))

    # commit the changes
    db.commit()

    # close the connection
    cursor.close()
    return "Message submitted!"

def random_messages(n):
    # Connect to the database
    db = get_message_db()
    cursor = db.cursor()

    # SQL query to select n random messages
    cmd = '''
          SELECT * FROM messages
          ORDER BY RANDOM() LIMIT ?
          '''
    cursor.execute(cmd, (n,))
    messages = cursor.fetchall()
    # Close the connection
    db.close()

    return messages

@app.route('/', methods=['POST', 'GET'])
def submit():
    # GET is to request data from a specified resource
    if request.method=='GET':
        return render_template('submit.html')
    # POST is to send data to the server
    else:
        msg_status = insert_message(request)
        return render_template('submit.html', msg_status=msg_status)

@app.route('/view/')
def view():
    messages = random_messages(5)
    return render_template('view.html', messages=messages)