from website import create_app

app = create_app()


if __name__ == '__main__': # tylko kiedy uruchomimy ten program import main.py z innego pliku to by sie wykonalo
    app.run(debug=True) # za kazdym razem gdy dokonamy zmiane, automatyczny rerun serwera

    

