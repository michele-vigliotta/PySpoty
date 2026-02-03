import os
import subprocess
import shutil
import json
import sys

def get_nome_playlist(url_playlist):
    result = subprocess.run(
        ["spotdl", "meta", url_playlist],
        capture_output=True,
        text=True,
        check=True
    )
    data = json.loads(result.stdout)
    return data["name"]

def playlist_esiste(nome_playlist):
    return os.path.isdir(nome_playlist)

def verifica_ffmpeg():
    
    # Verifica se ffmpeg è installato
    return shutil.which("ffmpeg") is not None

def scarica_playlist(url_playlist):
    """
    Scarica canzoni usando spotdl e nomina la cartella come la playlist.
    """
    print(f"--- Analisi della playlist: {url_playlist} ---")
    nome_playlist = get_nome_playlist(url_playlist)

    print("Sto recuperando il nome della playlist e iniziando il download...")

    # Costruiamo il comando con il template per l'output.
    # {list-name} -> Viene sostituito automaticamente col nome della playlist
    # {artists} - {title} -> Nome del file
    # Il simbolo '/' indica a spotdl di creare una sottocartella
    
    comando = [
        "spotdl", 
        url_playlist, 
        "--output", 
        "{list-name}/{artists} - {title}.{output-ext}"
    ]

    try:
        # Eseguiamo il comando
        subprocess.run(comando, check=True)
        print("\n✅ Download completato! Trovi la cartella nella stessa posizione di questo script.")
        
    except subprocess.CalledProcessError as e:
        print(f"\nErrore durante il download. Codice errore: {e.returncode}")
        print("Assicurati che l'URL sia corretto.")
    except KeyboardInterrupt:
        print("\nDownload interrotto dall'utente.")

def main():
    print(" _____________________________")
    print("| Spotify Playlist Downloader |")
    print("| 𓆏   ~~♫~~   𓆏    ~~♫~~   𓆏  |")
    print("|_____________________________|")
    
    
    if not verifica_ffmpeg():
        print("ERRORE: FFmpeg non è installato o non è nel PATH.")
        return

    url = input("Inserisci l'URL della playlist Spotify: \n").strip()
    
    # Controllo base dell'URL
    while "spotify.com" not in url:
        print("Sembra che l'URL inserito non sia di Spotify.")
        url = input("Per favore, inserisci un URL valido della playlist Spotify: \n").strip()
        

    scarica_playlist(url)

if __name__ == "__main__":
    main()