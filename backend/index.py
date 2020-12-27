from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

# PostgreSQL Database credentials loaded from the .env file
DATABASE = os.getenv('DATABASE')
DATABASE_USERNAME = os.getenv('')
DATABASE_PASSWORD = os.getenv('')

app = Flask(__name__)

# CORS implemented so that we don't get errors when trying to access the server from a different server location
CORS(app)


try:
    con = psycopg2.connect(
        database=DATABASE,
        user = DATABASE_USERNAME,
        password=DATABASE_PASSWORD)

    cur = con.cursor()

    # GET: Fetch all movies from the database
    @app.route('/')
    def fetch_all_movies():
        cur.execute('SELECT * FROM movies')
        rows = cur.fetchall()

        #rows = DATABASE
        print(rows)

        return jsonify(rows)

    # GET: Fetch movie by movieId from the database
    @app.route('/<int:movie_id>')
    def fetch_by_id(movie_id=None):
        cur.execute(f'SELECT * FROM movies WHERE movie_id = {movie_id}')
        rows = cur.fetchall()
        print(rows)

        return jsonify(rows)

    # POST: Create movies and add them to the database
    @app.route('/add-movie', methods=['GET', 'POST'])
    def add_movie():

        if request.method == 'POST':
            data = request.form.to_dict()
            print(data)
            cur.execute("INSERT INTO movies (movie_name, img_url, release_year, summary, director, genre, rating, movie_runtime, meta_score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (f"{data['movie_name']}", f"{data['img_url']}", data['release_year'], f"{data['summary']}",
                         f"{data['director']}", f"{data['genre']}", f"{data['rating']}", data['movie_runtime'], data['meta_score']))
            con.commit()
            print('Form Submitted')
            return redirect('http://localhost:3000', code="200")
            #return 'Form submitted'
        else:
            print('Form submission failed')
            return 'Form submission failed'

    # DELETE: Delete movie by movieId from the database
    @app.route('/delete-movie', methods=['GET', 'DELETE'])
    def delete_by_id():
        #print(request.args.get('movie_id'))
        movie_id = request.args.get('movie_id')
        #print(request.form)

        #print(movie_id['movie_id'])
        cur.execute(
            f"DELETE FROM movies WHERE movie_id = {movie_id} RETURNING movie_name")
        con.commit()

        return 'Movie Deleted'

    # PUT: Update movie by movieId from the database
    @app.route('/update-movie', methods=['GET', 'PUT'])
    def update_by_id():

        cur.execute(
            'UPDATE movies SET movie_name = \'Goldeneye\' WHERE movie_id = 11')
        con.commit()

        return 'Movie Updated'

except:
    print('Error')
