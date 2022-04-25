from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from tkinter import messagebox
from tkinter.messagebox import WARNING
import time

def send_formation_info(formation_selected,formation_recherche,browser,time_limit=60):
    """Envoie des infos de formation au chrome"""
    if len(time_limit.get())==0:
        time_out=60
    else:
        time_out=time_limit.get()
    error=False
    try:
        formation_session_dropdown =  Select(WebDriverWait(browser,time_out).until(EC.presence_of_element_located((By.CLASS_NAME,"formation_session"))))
        formation_session_dropdown.select_by_visible_text(formation_selected)
        group_session_dropdown = Select(WebDriverWait(browser,time_out).until(EC.presence_of_element_located((By.CLASS_NAME,"group_session"))))
        all_options_gp_formation = group_session_dropdown.options
        options_gp_formations = [ option.text for option in all_options_gp_formation if formation_recherche in option.text ]
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
            return "error"
        else:
            return options_gp_formations