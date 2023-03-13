from website import create_app
import psycopg2
app = create_app()


if __name__ == '__main__': # run by main.py
    app.run(debug=True) # applies changes whenever you rerun the server