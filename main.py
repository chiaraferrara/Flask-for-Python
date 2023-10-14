#importando il nome della cartella importerà tutto ciò che sta all'interno.
from website import create_app 
app = create_app()

if __name__ == '__main__':  #solo se runniamo main.py eseguirà questo file.
    app.run(debug=True)