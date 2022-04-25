import os
from tkinter import messagebox
from tkinter.messagebox import WARNING
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from Packages.progressbar import MyProgressBar
import time


def download_reports(main_window,gp_formation_selected, browser,time_limit=60):
    """Fonction de téléchargement de rapport avec main_window = à la fenetre principal , browser le navigateur
    et gp_formation_selected = au dernier combobox de la fenêtre principal
    """

    directory_download = main_window.directory_download
    minus_DS_file =0
    if '.DS_Store' in os.listdir(directory_download):
            minus_DS_file=1
    if len(os.listdir(directory_download)) >minus_DS_file:
        messagebox.showerror(title="Erreur - Dossier de téléchargement", message="Le dossier de téléchargement doit être vide",icon=WARNING)
        return

    if len(time_limit.get())==0:
        time_out=60
    else:
        time_out=time_limit.get()
    
    error=False
    try:
        group_session_dropdown = Select(WebDriverWait(browser, time_out).until(
            EC.presence_of_element_located((By.CLASS_NAME, "group_session"))))
        group_session_dropdown.select_by_visible_text(gp_formation_selected)

        contenu = WebDriverWait(browser, time_out).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'contenu')))
        elems = WebDriverWait(contenu, time_out).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        print("Nombre d'apprenant:"+str(len(elems)))
        progressbar = MyProgressBar(main_window,len(elems))
        nb_elem=2
        for elem in elems:
            WebDriverWait(browser, time_out).until(EC.presence_of_element_located(
                (By.LINK_TEXT, elem.accessible_name))).click()
            find_href_pdf_elems = WebDriverWait(browser, time_out).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.contenu li div a')))
            while len(find_href_pdf_elems) != nb_elem:
                find_href_pdf_elems = WebDriverWait(browser, time_out).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.contenu li div a')))
            # nb_elem=nb_elem+1
        
        # nb_elem=1
        # for elem in elems:
            ## progress_step = float(100.0/len(elems))
            pdf_downloaded = 0
            while pdf_downloaded != 1:
                # find_href_pdf_elems = WebDriverWait(browser, time_out).until(
                #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.contenu li div a')))
                print("Nombre d'éléments téléchargeable trouvé:" +
                    str(len(find_href_pdf_elems)))
                # if len(find_href_pdf_elems) == 0:
                #     continue
                # else:
                i = 0
                el = find_href_pdf_elems[nb_elem-2]
                print("Nombre de fichier téléchargé avant if :" +
                    str(pdf_downloaded))
                # browser.execute_script("arguments[0].click();", el) fonctionne aussi
                if (i <= pdf_downloaded-1 and pdf_downloaded != 0):
                    i = i+1
                    print("comparison between i: " + str(i) +
                        " and nb pdf" + str(pdf_downloaded))
                    continue
                else:
                    print("Boucle dans la liste des éléments avec href:"+str(i))
                    # messagebox.showinfo(title="Autoriser le téléchargement de fichiers multiples",
                    # message="AVANT DE CLIQUER SUR OK , Veuillez autoriser le téléchargement de fichier multiple dans la barre de recherche à droite")
                    el.send_keys(Keys.RETURN)
                    # el.click()
                    pdf_downloaded = pdf_downloaded+1
                    print("Nombre de fichier téléchargé: " +
                        str(pdf_downloaded) + "/"+str(len(elems)))
                    progressbar.update_value()
                    # progress += progress_step
                    # progress_var.set(progress)
                i = i+1

            while not len(os.listdir(directory_download))-minus_DS_file==nb_elem/2:
                time.sleep(2)
            time.sleep(3)
            nb_elem=nb_elem+2

    except NoSuchElementException:
        print("There was an error, no such element")
        error=True
        progressbar.close_popup()
        browser.quit()
    except TimeoutException:
        messagebox.showerror(title="TimeOut", message="Le temps de réponse de GAFEO a excédé le temps limite configuré: "+" "+str(time_out)+"sec",icon=WARNING)
        error=True
        progressbar.close_popup()
    else:
        print("There were no errors.")
    finally:
        print("Process completed.")
        if error:
            progressbar.close_popup()
            return "error"
        else:
            pass
            # browser.quit()
