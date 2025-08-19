# Si importano le librerie necessarie per lo svolgimento
import numpy as np
import os
from pathlib import Path
import shutil
import csv
import argparse



# Di seguito si va a selezionare la cartella su cui si adrà a lavorare
directory = os.fsencode('files')
# Si crea un lista per poter visualizzare da terminale quali sono i file esistenti
lista_file = []
# Si crea una variabile booleana per aiutarsi a verificare l'esistenza del file recap.csv
recap_exists = False

# Si inizializza un primo ciclo for sui file che sono contenuti nella directory
for file_enc in sorted(os.listdir(directory)):
    
    # Si trasformano i file da variabile byte(file_enc) a stringa 
    file = os.fsdecode(file_enc)
    # Si salva il percorso completo in una variabile
    full_path = os.path.join('files',file)
    # Si controlla che vengano considerati solamente i file e non le sottocartelle che saranno create
    if not os.path.isfile(full_path):
        continue
    # Si controlla l' esistenza del file recap.csv
    if 'recap.csv' == file:
        recap_exists = True
        continue
    # Si trasformano i file da variabile byte(file_enc) a stringa 
    file = os.fsdecode(file_enc)
    # Si salvano i file contenuti nella cartella files in una lista che sarà usata in parser(choices)
    lista_file.append(file)

# Si crea l'oggetto parser 
parser = argparse.ArgumentParser(description="Programma per sposatare file nelle sottocartelle desiderate")
# Si aggiunge l'argomento del parser in questo caso il file che si vuole spostare
parser.add_argument('file',type=str,help='Inserire il nome del file da spostare',choices=lista_file)
file_arg = parser.parse_args()

# Si inizializza un ciclo for sui file che sono contenuti nella directory
for file_enc in sorted(os.listdir(directory)):
    
    # Si trasformano i file da variabile byte(file_enc) a stringa 
    file = os.fsdecode(file_enc)

    # Si cerca il file immesso da riga di comando tra quelli presenti nella cartella files
    if file_arg.file == file:

        # Salviamo il percorso completo in una variabile
        full_path = os.path.join('files',file)
        
        # Variabile che contiene solo il nome del file senza estensione
        file_name = Path(file).stem
        # Variabile che contiene la dimensione del file in Byte
        file_size = os.path.getsize(full_path)
        # Si convertono tutte le lettere del file in minuscolo per un controllo migliore
        file_lower = file.lower()

        # Di seguito andiamo a dividere i file in base alla loro estensione
        
        if file_lower.endswith(('.txt', '.odt')):      
            # Variabile tipo e cartella di destinazione per i file di tipo documento
            file_type = 'doc'
            dest_folder = 'Docs'
            
        elif file_lower.endswith(('.jpg', '.jpeg', '.png')):
            # Variabile tipo e cartella di destinazione per i file di tipo immagine
            file_type = 'image'
            dest_folder = 'Images'

        elif file_lower.endswith('.mp3'):
            # Variabile tipo e cartella di destinazione per i file di tipo audio
            file_type = 'audio'
            dest_folder = 'Audio'

        else:
            # Variabile di controllo per i file di tipo sconosciuto
            file_type = 'unknown'
            # Non viene assegnato nessun valore alla cartella di destinazione dei file sconosciuti
            dest_folder = None

        # Se è stato assegnato un nome alla sottocartella di destinazione allora andremo a spostarci il file
        if dest_folder:
            # Variabile con il percorso della sottocartella
            dest_path = os.path.join('files', dest_folder)
            # Creiamo la sottocartella se non esiste
            os.makedirs(dest_path, exist_ok=True)
            # Muoviamo il file nella sottocartella con il percorso dest_path
            shutil.move(full_path, os.path.join(dest_path, file))

# Si salvano in un dizionario i dati del file per recap.csv
dict_recap = {
    'name' : file_name,
    'type' : file_type,
    'size(B)' : file_size
}
# Variabile con il percorso dove salvare il file di recap.csv 
file_path = 'files/recap.csv'

# Si crea o si aggiorna, nel caso esista già, il file recap.csv
with open(file_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=dict_recap.keys())
    
    if not recap_exists:
        writer.writeheader()
    
    writer.writerow(dict_recap)