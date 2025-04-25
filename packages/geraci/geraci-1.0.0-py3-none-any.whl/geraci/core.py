import os
import logging
import shutil
import zipfile

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

s = "___________________________________________________"

def read_file(file):
    """
    Legge il contenuto di un file.
    
    Args:
        file (str): Nome del file o percorso completo.
        
    Returns:
        str: Contenuto del file se esiste, altrimenti un messaggio di errore.
    """
    logging.info(f"Lettura del file '{file}'...")
    if not validate_file_name(file):
        return f"⚠️ Nome file non valido: '{file}'"
    try:
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                return f.read()
        return f"⚠️ File '{file}' non esiste!"
    except FileNotFoundError:
        return f"⚠️ File '{file}' non trovato!"
    except PermissionError:
        return f"❌ Permesso negato per il file '{file}'!"
    except Exception as e:
        return f"❌ Errore generico: {e}"

def overwrite_file(file):
    """
    Sovrascrive il contenuto di un file.
    
    Args:
        file (str): Nome del file o percorso completo.
        
    Returns:
        str: Messaggio di successo o errore.
    """
    logging.info(f"Sovrascrittura del file '{file}'...")
    try:
        tipo = input("Scrivi - Carica\n: ").capitalize()
        while tipo not in ["Scrivi", "Carica"]:
            tipo = input("Scrivi - Carica\n: ").capitalize()
        match tipo:
            case "Scrivi":
                txt = input("Scrivi: ")
            case "Carica":
                f = input("---nome file o percorso---\n: ")
                txt = read_file(f)
        with open(file, "w", encoding="utf-8") as f:
            f.write(txt)
        return f"✅ File '{file}' scritto con successo!"
    except Exception as e:
        return f"❌ Errore: {e}"

def append_file(file):
    """
    Aggiunge contenuto a un file.
    
    Args:
        file (str): Nome del file o percorso completo.
        
    Returns:
        str: Messaggio di successo o errore.
    """
    logging.info(f"Aggiunta di contenuto al file '{file}'...")
    try:
        tipo = input("Scrivi - Carica\n: ").capitalize()
        while tipo not in ["Scrivi", "Carica"]:
            tipo = input("Scrivi - Carica\n: ").capitalize()
        if tipo == "Scrivi":
            txt = input("Scrivi: ")
        elif tipo == "Carica":
            f = input("---nome file o percorso---\n: ")
            txt = read_file(f)
        separatore = "\n" if os.path.exists(file) else ""
        with open(file, "a", encoding="utf-8") as f:
            f.write(separatore + txt)
        return f"✅ File '{file}' aggiornato con successo!"
    except Exception as e:
        return f"❌ Errore: {e}"

def create_file(file=None):
    """
    Crea un nuovo file.
    
    Args:
        file (str, optional): Nome del file o percorso completo. Se None, richiede input.
        
    Returns:
        str: Messaggio di successo o errore.
    """
    logging.info(f"Creazione del file '{file}'...")
    if not file:
        file = input("Nome file (es. rubrica.txt)\n: ")
    if not validate_file_name(file):
        return f"⚠️ Nome file non valido: '{file}'"
    try:
        with open(file, "x", encoding="utf-8"):
            return f"✅ File '{file}' creato!"
    except FileExistsError:
        return f"⚠️ Il file '{file}' esiste già!"
    except Exception as e:
        return f"❌ Errore: {e}"

def rename_file(old_name, new_name):
    """
    Rinomina un file.
    
    Args:
        old_name (str): Nome attuale del file.
        new_name (str): Nuovo nome del file.
        
    Returns:
        str: Messaggio di successo o errore.
    """
    logging.info(f"Rinominazione del file da '{old_name}' a '{new_name}'...")
    try:
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
            return f"✅ File rinominato da '{old_name}' a '{new_name}'!"
        return f"⚠️ Il file '{old_name}' non esiste!"
    except Exception as e:
        return f"❌ Errore: {e}"

def move_file(file, new_path):
    """
    Sposta un file in una nuova posizione.
    
    Args:
        file (str): Nome del file o percorso completo.
        new_path (str): Percorso di destinazione.
        
    Returns:
        str: Messaggio di successo o errore.
    """
    logging.info(f"Spostamento del file '{file}' in '{new_path}'...")
    try:
        if os.path.exists(file):
            shutil.move(file, os.path.join(new_path, os.path.basename(file)))
            return f"✅ File '{file}' spostato in '{new_path}'!"
        return f"⚠️ Il file '{file}' non esiste!"
    except Exception as e:
        return f"❌ Errore: {e}"

def delete_file(file):
    """
    Elimina un file.
    
    Args:
        file (str): Nome del file o percorso completo.
        
    Returns:
        str: Messaggio di successo o errore.
    """
    logging.info(f"Eliminazione del file '{file}'...")
    try:
        if os.path.exists(file):
            os.remove(file)
            return f"✅ File '{file}' eliminato!"
        return f"⚠️ Il file '{file}' non esiste!"
    except Exception as e:
        return f"❌ Errore: {e}"

def create_directory(path):
    """
    Crea una nuova directory.
    
    Args:
        path (str): Percorso della directory.
        
    Returns:
        str: Messaggio di successo o errore.
    """
    logging.info(f"Creazione della directory '{path}'...")
    try:
        os.makedirs(path, exist_ok=True)
        return f"✅ Directory '{path}' creata!"
    except Exception as e:
        return f"❌ Errore: {e}"

def list_files_in_directory(path):
    """
    Elenca i file in una directory.
    
    Args:
        path (str): Percorso della directory.
        
    Returns:
        list/str: Lista dei file nella directory, oppure un messaggio di errore.
    """
    logging.info(f"Elenco dei file nella directory '{path}'...")
    try:
        if os.path.isdir(path):
            return os.listdir(path)
        return f"⚠️ '{path}' non è una directory!"
    except Exception as e:
        return f"❌ Errore: {e}"

def validate_file_name(file):
    """
    Verifica che il nome del file sia valido.
    
    Args:
        file (str): Nome del file o percorso completo.
        
    Returns:
        bool: True se il nome è valido, False altrimenti.
    """
    if not file or not isinstance(file, str):
        return False
    if "." not in file:
        return False
    return True

def compress_file(file, zip_name):
    """
    Comprime un file in un archivio ZIP.
    
    Args:
        file (str): Nome del file o percorso completo.
        zip_name (str): Nome dell'archivio ZIP.
        
    Returns:
        str: Messaggio di successo o errore.
    """
    logging.info(f"Compressione del file '{file}' in '{zip_name}'...")
    try:
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            zipf.write(file, os.path.basename(file))
        return f"✅ File '{file}' compresso in '{zip_name}'!"
    except Exception as e:
        return f"❌ Errore: {e}"

def decompress_file(zip_name, extract_path):
    """
    Decomprime un archivio ZIP.
    
    Args:
        zip_name (str): Nome dell'archivio ZIP.
        extract_path (str): Percorso di estrazione.
        
    Returns:
        str: Messaggio di successo o errore.
    """
    logging.info(f"Decompressione dell'archivio '{zip_name}' in '{extract_path}'...")
    try:
        with zipfile.ZipFile(zip_name, 'r') as zipf:
            zipf.extractall(extract_path)
        return f"✅ Archivio '{zip_name}' decompresso in '{extract_path}'!"
    except Exception as e:
        return f"❌ Errore: {e}"

def main_menu():
    """
    Menu principale per l'interazione con la libreria.
    """
    while True:
        print("\n--- MENU ---")
        print("1. Leggi file")
        print("2. Sovrascrivi file")
        print("3. Aggiungi a file")
        print("4. Crea file")
        print("5. Rinomina file")
        print("6. Sposta file")
        print("7. Elimina file")
        print("8. Crea directory")
        print("9. Elenco file in directory")
        print("10. Comprimi file")
        print("11. Decomprimi file")
        print("12. Esci")
        scelta = input("Scegli un'opzione: ")
        
        if scelta == "1":
            file = input("Nome del file: ")
            print(read_file(file))
        elif scelta == "2":
            file = input("Nome del file: ")
            print(overwrite_file(file))
        elif scelta == "3":
            file = input("Nome del file: ")
            print(append_file(file))
        elif scelta == "4":
            file = input("Nome del file (opzionale): ")
            print(create_file(file))
        elif scelta == "5":
            old_name = input("Nome attuale del file: ")
            new_name = input("Nuovo nome del file: ")
            print(rename_file(old_name, new_name))
        elif scelta == "6":
            file = input("Nome del file: ")
            new_path = input("Percorso di destinazione: ")
            print(move_file(file, new_path))
        elif scelta == "7":
            file = input("Nome del file: ")
            print(delete_file(file))
        elif scelta == "8":
            path = input("Percorso della directory: ")
            print(create_directory(path))
        elif scelta == "9":
            path = input("Percorso della directory: ")
            print(list_files_in_directory(path))
        elif scelta == "10":
            file = input("Nome del file: ")
            zip_name = input("Nome dell'archivio ZIP: ")
            print(compress_file(file, zip_name))
        elif scelta == "11":
            zip_name = input("Nome dell'archivio ZIP: ")
            extract_path = input("Percorso di estrazione: ")
            print(decompress_file(zip_name, extract_path))
        elif scelta == "12":
            print("Uscita...")
            break
        else:
            print("Opzione non valida!")

if __name__ == "__main__":
    main_menu()