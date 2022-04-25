# LISEZ MOI

## Instructions

1. Installer chromedriver et le mettre dans son dossier Applications [Lien pour télécharger](https://chromedriver.chromium.org/)
2. Executer la commande : `pyinstaller App_telechargement_rapport.py --onefile` à la racine du dossier où se trouve le fichier App_telechargement_rapport.py 
3. Executer le fichier "App_telechargement_rapport" présent dans le dossier "dist"



## Explication démarche pour Build app et dmg sur MacOS
[Voir ressource blog](https://blog.aaronhktan.com/posts/2018/05/14/pyqt5-pyinstaller-executable)
1. Exécuter la commande suivant : `pyinstaller App_telechargement_rapport.py`"
2. Configurer le fichier `.spec`généré à la suite de la précédente commande (voir fichier pour la config pour Mac) [Chemin spécifique vers Doc Pyinstaller](https://pyinstaller.readthedocs.io/en/v4.2/spec-files.html)
3. Executer ensuite la commande suivante `pyinstaller App_telechargement_rapport.spec` ( avec les bonnes config de l'étape 2)
4. Pour ajouter des images a notre app il faut : 
   ```python
   import os, sys
    # Translate asset paths to useable format for PyInstaller
    def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)
   ```
5. Installer `create-dmg`: 
    ```sh
    sudo npm install -g create-dmg

    # If you get an error about "EACCES: permission denied,
    # mkdir '/usr/local/lib/node_modules/create-dmg/node_modules/fs-xattr/build'", 
    # run this command instead and see 
    # https://github.com/npm/npm/issues/17268#issuecomment-310167614 for more details
    sudo npm install -g create-dmg --unsafe-perm=true --allow-root

    ```
6.  Et ensuite éxécuter ce code pour créer le dmg:
    ```sh
    create-dmg '<your_app>.app'
    # If you gt an XCode error like "gyp: No Xcode or CLT version detected!"
    # try running the command below then retry the above command.
    # See https://stackoverflow.com/questions/27665426/trying-to-install-bcrypt-into-node-project-node-set-up-issues
    # for more information
    sudo xcode-select -switch /Applications/Xcode.app/Contents/Developer/
    ```
7. Enfin il faut créer une signature sur le fichier dmg pour pouvoir installer sans alerte de sécurité sur les ordinateurs : 
    ```sh
    codesign --sign "Andria Capai" --force --keychain ~/Library/Keychains/pathxxx /path/to/App_download_rapport_Chr.app       
    ```
