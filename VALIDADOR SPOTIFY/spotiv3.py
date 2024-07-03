from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as chromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import *
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException,TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import secrets
import string
from tkinter import ttk



resultados = []
webdrivers = []
cantidad_artistas = 0

# Leer el archivo Excel y crear el diccionario de datos
nombre_archivo_excel = 'reciclaje-spoti.xlsx'  
da = pd.read_excel(nombre_archivo_excel)
diccionario_datos = da.set_index('correo')['contraseña'].to_dict()


def iniciar_sesion(usuario, clave):

    driver = webdriver.Chrome(service=chromeService(ChromeDriverManager().install()))
    driver.get('https://accounts.spotify.com/es/login?continue=https%3A%2F%2Fopen.spotify.com%2Fintl-es')
    driver.implicitly_wait(6)
    #iniciar sesion
    search_mail = driver.find_element(By.XPATH, '//*[@id="login-username"]')
    search_password = driver.find_element(By.XPATH, '//*[@id="login-password"]')
    search_ingresar = driver.find_element(By.XPATH, '//*[@id="login-button"]')
    search_mail.send_keys(usuario)
    search_password.send_keys(clave)
    search_ingresar.click()
    

    return driver

    
def main():
    for usuario, clave in diccionario_datos.items():
        driver = iniciar_sesion(usuario, clave)

        #buscar artistas
        artistas = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="Desktop_LeftSidebar_Id"]/nav/div[2]/div[1]/div[2]/div[2]/div/div/ul/div/div[2]/li'))
        )
        #contar artistas
        cantidad_artistas=len(artistas)

        print(cantidad_artistas)

        for i in range(cantidad_artistas):
            #seleccionar artista
            time.sleep(1)
            seleccion1 = driver.find_element(By.XPATH, '//*[@id="Desktop_LeftSidebar_Id"]/nav/div[2]/div[1]/div[2]/div[2]/div/div/ul/div/div[2]/li[' + str(i+1) + ']')
            seleccion1.click()
            time.sleep(1)
            texto_seleccion1 = seleccion1.text
            print(texto_seleccion1)


            

        driver.close()


main()