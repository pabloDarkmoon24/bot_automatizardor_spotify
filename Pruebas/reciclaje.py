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
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


resultados = []
webdrivers = []

# Leer el archivo Excel y crear el diccionario de datos
nombre_archivo_excel = 'cuentaspotify.xlsx'  
da = pd.read_excel(nombre_archivo_excel)
diccionario_datos = da.set_index('correo')['contraseña'].to_dict()

for usuario, clave in diccionario_datos.items():
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


    try:
            botton_cookies = driver.find_element(By.XPATH, '//div[@id="onetrust-close-btn-container"]')
            botton_cookies.click()
    except ElementNotInteractableException:
            print("El botón 'cookies' no es interactuable")
    except ElementClickInterceptedException:
            print("Intercepción al hacer clic en el botón 'cookies'")
    except NoSuchElementException:
            print("No se encontró el botón 'cookies'")
    try:
             botton_cookies = driver.find_element(By.XPATH, '//Button[@aria-label="Cerrar"]')
             botton_cookies.click()
             print("Clic en el botón 'pestaña emergente")
    except NoSuchElementException:
             print("No se encontró el botón 'pestaña emergente'")
    except ElementNotInteractableException:
            print("El botón 'cookies' no es interactuable")
    except ElementClickInterceptedException:
            print("Intercepción al hacer clic en el botón 'cookies'")


    #contar los artistas seguidos
    try:
        artistas = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li'))
            )

        cantidad_artistas = len(artistas)
        print(cantidad_artistas)

    except NoSuchElementException:
        print("No se encontraron artistas")

        #proceso de cambio de clave        
        driver = webdriver.Chrome(service=chromeService(ChromeDriverManager().install()))
        driver.get('https://www.spotify.com/co-es/account/overview/?utm_source=spotify&utm_medium=menu&utm_campaign=your_account')
        input("cambio de clave")
    
    except ElementNotInteractableException:
        print("No se encontraron artistas")
        #proceso de cambio de clave 
        driver = webdriver.Chrome(service=chromeService(ChromeDriverManager().install()))
        driver.get('https://www.spotify.com/co-es/account/overview/?utm_source=spotify&utm_medium=menu&utm_campaign=your_account')
        input("cambio de clave")

    except ElementClickInterceptedException:
        print("No se encontraron artistas")
        #proceso de cambio de clave 
        driver = webdriver.Chrome(service=chromeService(ChromeDriverManager().install()))
        driver.get('https://www.spotify.com/co-es/account/overview/?utm_source=spotify&utm_medium=menu&utm_campaign=your_account')
        input("cambio de clave")

    while cantidad_artistas > 1:
        
        #seleccionar el primer artista para dejar de seguir
        artista = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[2]')
        artista.click()

        # eliminar seguir
        try:
            botton_seguir = driver.find_element(By.XPATH, '//*[@data-encore-id="buttonSecondary"]')
            action_chains = ActionChains(driver)
            action_chains.context_click(botton_seguir)
            print("Clic en el botón 'seguir'")
        except NoSuchElementException:
            print("No se encontró el botón 'seguir'")
        except ElementNotInteractableException:
            print("El botón 'seguir' no es interactuable")
        except ElementClickInterceptedException:
            print("Intercepción al hacer clic en el botón 'seguir'")

        
        # eliminar guardar
        try:
            botton_like = driver.find_element(By.XPATH, '//Button[@aria-checked="true"]')
            botton_like.click()
            print("Clic en el botón 'like'")
        except NoSuchElementException:
            print("No se encontró el botón 'like'")
        except ElementNotInteractableException:
            print("El botón 'like' no es interactuable")
        except ElementClickInterceptedException:
            print("Intercepción al hacer clic en el botón 'like'")

        time.sleep(1) 
        artistas = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li'))
         )

        cantidad_artistas = len(artistas)
        print(cantidad_artistas)
        time.sleep(1) 

    if cantidad_artistas == 1 :
        #seleccionar el primer artista para dejar de seguir o eliminar likes
        artista = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[1]')
        artista.click()
  
        try:
            botton_seguir = driver.find_element(By.XPATH, '//*[@data-encore-id="buttonSecondary"]')
            botton_seguir.click()
            print("Clic en el botón 'seguir'")
        except NoSuchElementException:
            print("No se encontró el botón 'seguir'")
        except ElementNotInteractableException:
            print("El botón 'seguir' no es interactuable")
        except ElementClickInterceptedException:
            print("Intercepción al hacer clic en el botón 'seguir'")

        # eliminar guardar
        try:
            likes = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[4]/div/div[2]/div[2]/div'))
            )
            cantidad_likes = len(likes)
            print (cantidad_likes)

            while cantidad_likes > 0:

                botton_like = driver.find_element(By.XPATH, '//Button[@aria-checked="true"]')
                botton_like.click()
                print("Clic en el botón 'like'")
                cantidad_likes = cantidad_likes-1
                time.sleep(1) 
                print("cantidad de likes")

        except NoSuchElementException:
            print("No se encontró el botón 'like'")
        except ElementNotInteractableException:
            print("El botón 'like' no es interactuable")
        except ElementClickInterceptedException:
            print("Intercepción al hacer clic en el botón 'like'")

    if cantidad_artistas == 0 :
        #proceso de cambio de clave        
        driver = webdriver.Chrome(service=chromeService(ChromeDriverManager().install()))

        driver.get('https://www.spotify.com/co-es/account/overview/?utm_source=spotify&utm_medium=menu&utm_campaign=your_account')
        
        input("cambio de clave")

    
input("Revision exitosa")          






# Crear un DataFrame a partir de la lista de resultados
df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Contraseña', 'Resultado'])

# Guardar el DataFrame en un archivo Excel
df_resultados.to_excel('resultadospotify.xlsx', index=False)