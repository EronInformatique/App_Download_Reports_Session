from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from tkinter.messagebox import WARNING
import os, time
from tkinter import filedialog,messagebox
from pathlib import Path

def send_infos_to_chrome(formation_recherche,time_limit=60,id_param="andria.c@eronservice.fr",psswd_param="Andria-2021!"):
    """Envoie des infos et initialisation du driver"""
   
    if len(time_limit.get())==0:
        time_out=60
    else:
        time_out=time_limit.get()
    if len(id_param.get())==0:
        id="automate"
    else:
        id=id_param
    if len(psswd_param.get())==0:
        psswd="AutomateEron2!!"
    else:
        psswd=psswd_param

    error=False
    if os.path.exists("/Applications/Internet/Google Chrome.app/Contents/MacOS/Google Chrome"):
        path_google_chrome="/Applications/Internet/Google Chrome.app/Contents/MacOS/Google Chrome"
        path_firefox="/Applications/Internet/Firefox.app/Contents/MacOS/firefox-bin"
    else:
        path_google_chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        path_firefox="/Applications/Firefox.app/Contents/MacOS/firefox-bin"
    
    options = Options()
    # options.binary_location=path_firefox
    # options.binary=FirefoxBinary(firefox_path=path_firefox)
    options.binary_location = path_google_chrome
    
    options.add_experimental_option("detach", True)
    # options.preferences("detach", True)
    
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    # options.add_experimental_option('prefs', {'download.default_directory':'/Users/acapai/Downloads/'})
    # options.add_experimental_option('prefs',{"profile.default_content_setting_values.automatic_downloads": 1})

    # options = webdriver.ChromeOptions()
    # options.gpu = False
    # options.headless = True
    directory_download = filedialog.askdirectory(title = "Choisir un dossier pour le téléchargement des rapports")
    
    # profile = webdriver.FirefoxProfile()
    # profile.set_preference("browser.download.folderList", 2)
    # profile.set_preference("browser.download.manager.showWhenStarting", False)
    # profile.set_preference("browser.download.dir",directory_download )
    # profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
    
    directory_download_default = str(os.path.join(Path.home(), "Downloads"))
    print(directory_download_default)
    if directory_download =="": 
        directory_download = str(os.path.join(directory_download_default, "Rapports_Sessions_"+formation_recherche))
        is_exist = os.path.exists(directory_download)
        if not os.path.isdir(directory_download) or is_exist == False:
            os.makedirs(directory_download,exist_ok=False)
            
        
    
    options.add_experimental_option("prefs", {
        "download.default_directory" : directory_download,
        "profile.default_content_setting_values.automatic_downloads": 1,
        })


    rel_path="/Applications/chromedriver"
    # rel_path="/Applications/geckodriver"
    PATH = os.path.abspath(rel_path)
    print("PATH:",PATH)

    browser = webdriver.Chrome(options=options,executable_path=PATH)
    # browser = webdriver.Firefox(options=options,executable_path=PATH,firefox_profile=profile)
    browser.get("https://www.gafeo.fr/admin/tool/reportsessions/index.php")
    browser.find_element(By.ID,'username').send_keys(id)
    browser.find_element(By.ID,'password').send_keys(psswd)
    browser.find_element(By.CSS_SELECTOR,"button.btn-primary").click()

    try:
            formation_session_dropdown =  Select(WebDriverWait(browser,time_out).until(EC.presence_of_element_located((By.CLASS_NAME,"formation_session"))))
            all_options_formation = formation_session_dropdown.options
            options_formations = [ option.text for option in all_options_formation if formation_recherche in option.text ]
    except NoSuchElementException:
        print("There was an error, no such element")
        error=True
        time.sleep(5)
        browser.quit()
    except TimeoutException:
        messagebox.showerror(title="TimeOut", message="Le temps de réponse de GAFEO a excédé le temps limite configuré: "+" "+str(time_out),icon=WARNING)
        error=True
        browser.quit()
    else:
        print("There were no errors.")
    finally:
        print("Process completed.")
        if error:
            return "error",browser
        else:
            return options_formations,browser,directory_download