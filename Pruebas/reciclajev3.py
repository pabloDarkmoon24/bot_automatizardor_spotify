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



resultados = []
webdrivers = []
cantidad_artistas = 0
playlist1 = "Playlist"
artista = "Artista"
album = "Álbum"
episodios = "Episodios guardados"
podcast = "Podcast"
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

    except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException):
            print("El botón 'cookies' no es interactuable")

    try:
             botton_cookies = driver.find_element(By.XPATH, '//Button[@aria-label="Cerrar"]')
             botton_cookies.click()
             print("Clic en el botón 'pestaña emergente")

    except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException):
             print("No se encontró el botón 'pestaña emergente'")


    #contar los artistas seguidos
    try:
        artistas = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li'))
            )

        cantidad_artistas = len(artistas)
        print(cantidad_artistas)

    except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException):
        print("No se encontraron artistas")
       
    while cantidad_artistas > 1:
        elemento_principal = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[2]')
        texto_span = elemento_principal.find_element(By.XPATH, './/span[@class="ListRowDetails__LineClamp-sc-sozu4l-1 hITFAK"]').text
        cantidad_artistas = cantidad_artistas - 1

        
        if playlist1 in texto_span :

            try:
                # print("playlist1")
                LUGAR2 = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[2]')
                action_chains = ActionChains(driver)
                action_chains.context_click(LUGAR2).perform()
                segir2 = driver.find_element(By.XPATH, '//span[@class="Type__TypeElement-sc-goli3j-0 ieTwfQ ellipsis-one-line PDPsYDh4ntfQE3B4duUI" and @data-encore-id="type" and text()="Eliminar de Tu biblioteca"]')
                segir2.click()
                confirmar_segir = driver.find_element(By.XPATH, '//button[@class="Button-sc-qlcn5g-0 keyrGu" and @data-encore-id="buttonPrimary"]/span[text()="Eliminar"]')
                confirmar_segir.click()
                cantidad_artistas = len(artistas)
                time.sleep(1.5)

            except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException):
                   
                LUGAR2 = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[2]')
                action_chains = ActionChains(driver)
                action_chains.context_click(LUGAR2).perform() 
                eliminar_button = driver.find_element(By.XPATH, '//span[text()="Eliminar"]/ancestor::button')
                eliminar_button.click()
                confirmar_segir = driver.find_element(By.XPATH, '//button[@class="Button-sc-qlcn5g-0 keyrGu" and @data-encore-id="buttonPrimary"]/span[text()="Eliminar"]')
                confirmar_segir.click()
                cantidad_artistas = len(artistas)
                time.sleep(1.5)
                continue
                
                

        elif artista in texto_span :
            LUGAR2 = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[2]')
            action_chains = ActionChains(driver)
            action_chains.context_click(LUGAR2).perform()
            segir = driver.find_element(By.XPATH, '//Button[@aria-disabled="false"]').click()
            confirmar_segir = driver.find_element(By.XPATH, '//span[contains(@class, "ButtonInner-sc-14ud5tc-0") and contains(@class, "glYGDr") and contains(@class, "encore-bright-accent-set") and contains(@class, "MIsUJlamzLYuAlvPbmZz") and text()="Eliminar"]')
            confirmar_segir.click()
            cantidad_artistas = len(artistas)
            time.sleep(1.5) 

        elif album in texto_span :
            LUGAR2 = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[2]')
            action_chains = ActionChains(driver)
            action_chains.context_click(LUGAR2).perform()
            segir2 = driver.find_element(By.XPATH, '//span[@class="Type__TypeElement-sc-goli3j-0 ieTwfQ ellipsis-one-line PDPsYDh4ntfQE3B4duUI" and @data-encore-id="type" and text()="Eliminar de Tu biblioteca"]')
            segir2.click()
            confirmar_segir = driver.find_element(By.XPATH, '//button[@class="Button-sc-qlcn5g-0 keyrGu" and @data-encore-id="buttonPrimary"]/span[text()="Eliminar"]')
            confirmar_segir.click()
            cantidad_artistas = len(artistas)
            time.sleep(1.5)

        elif podcast in texto_span:
            LUGAR2 = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[2]')
            action_chains = ActionChains(driver)
            action_chains.context_click(LUGAR2).perform()
            segir = driver.find_element(By.XPATH, '//Button[@aria-disabled="false"]').click()
            confirmar_segir = driver.find_element(By.XPATH, '//span[contains(@class, "ButtonInner-sc-14ud5tc-0") and contains(@class, "glYGDr") and contains(@class, "encore-bright-accent-set") and contains(@class, "MIsUJlamzLYuAlvPbmZz") and text()="Eliminar"]')
            confirmar_segir.click()
            cantidad_artistas = len(artistas)
            time.sleep(1.5)
        
        elif episodios in texto_span :
            print("entro a eliminar guardados")
            columnartista = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[2]')
            columnartista.click()
            try:
                elementos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_OxEpxzAgJiTENfolVUN"]//div[@class="T9iBYqbERZHdwDl0U2tC"]')))
                contarpodcast = len(elementos)
                print(contarpodcast)
                cantidad_artistas = len(artistas)

                for elemento in elementos:
                    time.sleep(3)
                    try:
                        boton = elemento.find_element(By.XPATH, './/button[@data-testid="add-button"]')
                        columnartista = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[2]')
                        columnartista.click()
                                        
                            # Verificar si el botón es visible antes de hacer clic
                        if  boton.is_displayed():
                            boton.click()
                                            
                        else:
                                print("Botón no visible, no se hizo clic.")

                    except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException):
                                print("Eliminar fijos: Algo salió mal al hacer clic en el botón.")

            except NoSuchElementException:
                                print("Elemento 'elementos' no encontrado. El flujo de código no continuará.")
                                cantidad_artistas = len(artistas)                        
                                continue
        time.sleep(1)
            
        artistas = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li')))
        cantidad_artistas = len(artistas)
        print(cantidad_artistas)

    if cantidad_artistas == 1 :
            #seleccionar el primer artista para dejar de seguir o eliminar likes
            artista = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[1]')
            artista.click()
    
            try:
                botton_seguir = driver.find_element(By.XPATH, '//*[@data-encore-id="buttonSecondary"]')
                botton_seguir.click()
                print("Clic en el botón 'seguir'")
            except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException):
                print("No se encontró el botón 'seguir'") 

            # eliminar guardar
                try:
                    likes = WebDriverWait(driver, 10).until(
                    EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[4]/div/div[2]/div[2]/div'))
                    )
                    cantidad_likes = len(likes)
                    print (cantidad_likes)

                    while cantidad_likes > 0:

                        botton_like = driver.find_element(By.XPATH, '//button[@aria-checked="true" and @data-testid="add-button" and @data-encore-id="buttonTertiary"]')
                        botton_like.click()
                        print("Clic en el botón 'like'")

                        likes = WebDriverWait(driver, 10).until(
                        EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[4]/div/div[2]/div[2]/div'))
                        )
                        cantidad_likes = len(likes)
                        print(cantidad_likes)
                        time.sleep(1) 
                    
                except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException):
                    print("No se encontró el botón 'like'")
    else:
            print("sin datos")


        

