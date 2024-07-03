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
import secrets
import string
import openpyxl
from selenium.webdriver.common.action_chains import ActionChains


resultados = []
webdrivers = []


# Leer el archivo Excel y crear el diccionario de datos
nombre_archivo_excel = 'cuentaspotify.xlsx'  
da = pd.read_excel(nombre_archivo_excel)
diccionario_datos = da.set_index('correo')['contraseña'].to_dict()



def generar_contrasena(longitud):
    
    numeros_permitidos = string.digits
    letras_permitidas = string.ascii_lowercase

    # Generar la mitad de la longitud con números y la otra mitad con letras
    mitad_longitud = longitud // 2
    numeros = ''.join(secrets.choice(numeros_permitidos) for _ in range(mitad_longitud))
    letras = ''.join(secrets.choice(letras_permitidas) for _ in range(mitad_longitud))

    # Concatenar números y letras
    contrasena = numeros + letras
    
    # Si la longitud es impar, añadir un carácter adicional de letras
    if longitud % 2 == 1:
        contrasena += secrets.choice(letras_permitidas)

    return contrasena

def guardar_contraseña_incorrecta(usuario):
    resultados.append([usuario, "Contraseña incorrecta"])
        # Crear un DataFrame a partir de la lista de resultados
    df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Nueva Contraseña'])
        # Guardar el DataFrame en un archivo Excel
    df_resultados.to_excel('resultadospotify.xlsx', index=False)

    with pd.ExcelWriter('resultadospotify.xlsx', engine='openpyxl') as writer:
            # Escribir el DataFrame en el archivo Excel
            df_resultados.to_excel(writer, index=False, sheet_name='Sheet1')

            # Obtener la hoja activa
            sheet = writer.sheets['Sheet1']

            # Establecer el ancho de columna para la columna 'Usuario'
            sheet.column_dimensions['A'].width = 40  # Ajusta el ancho según tus necesidades

            # Establecer el ancho de columna para la columna 'Nueva Contraseña'
            sheet.column_dimensions['B'].width = 30  # Ajusta el ancho según tus necesidades
    return(print("guardado exitoso"))

def guardar_contraseña(usuario, contrasena_generada):

    resultados.append([usuario, contrasena_generada])
    # Crear un DataFrame a partir de la lista de resultados
    df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Nueva Contraseña'])
        # Guardar el DataFrame en un archivo Excel
    df_resultados.to_excel('resultadospotify.xlsx', index=False)

    with pd.ExcelWriter('resultadospotify.xlsx', engine='openpyxl') as writer:
            # Escribir el DataFrame en el archivo Excel
            df_resultados.to_excel(writer, index=False, sheet_name='Sheet1')

            # Obtener la hoja activa
            sheet = writer.sheets['Sheet1']

            # Establecer el ancho de columna para la columna 'Usuario'
            sheet.column_dimensions['A'].width = 40  # Ajusta el ancho según tus necesidades

            # Establecer el ancho de columna para la columna 'Nueva Contraseña'
            sheet.column_dimensions['B'].width = 30  # Ajusta el ancho según tus necesidades
    return(print("guardado exitoso"))



for usuario, clave in diccionario_datos.items():
    driver = webdriver.Chrome(service=chromeService(ChromeDriverManager().install()))
    try:
        driver.get('https://www.spotify.com/co-es/account/overview/?utm_source=spotify&utm_medium=menu&utm_campaign=your_account')
        driver.implicitly_wait(6)

        #iniciar sesion
        search_mail = driver.find_element(By.XPATH, '//*[@id="login-username"]')
        search_password = driver.find_element(By.XPATH, '//*[@id="login-password"]')
        search_ingresar = driver.find_element(By.XPATH, '//*[@id="login-button"]')

        search_mail.send_keys(usuario)
        search_password.send_keys(clave)
        search_ingresar.click()

        
        time.sleep(6)
        botton_cookies = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="onetrust-close-btn-container"]'))).click()

        #boton cambio de contraseña
        try:
            botton_change_password = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@aria-describedby="onClickHintchangePassword"]'))).click()
        except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException):
            print("Error al interactuar con el botón de cambio de contraseña")

        time.sleep(3)
        contrasena_generada = generar_contrasena(8)

        #clave antigua
        search_password1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@id="old_password"]')))
        search_password1.send_keys(clave)
        print(clave)

        #nueva clave
        search_newpaswword= driver.find_element(By.XPATH, '//input[@id="new_password"]')
        search_newpaswword.send_keys(contrasena_generada)
        print(contrasena_generada)

        #confirmar contraseña
        search_newpaswword2 = driver.find_element(By.XPATH, '//input[@id="new_password_confirmation"]')
        search_newpaswword2.send_keys(contrasena_generada)
        print(contrasena_generada)

        #guardar contraseñas
        Button_savepassword = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div/div[2]/div[2]/article/section/form/div[4]/button')
        Button_savepassword.click()

        guardar_contraseña(usuario, contrasena_generada) 

        #atras
        Button_return = driver.find_element(By.XPATH, '//button[@data-encore-id="buttonPrimary"]')
        Button_return.click()

        
        try:
            dashboard = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div/div[1]/div/header/div/div[1]/a'))).click()
        except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException):
            print("Error al interactuar con el botón del dashboard principal")

        driver.refresh()
        time.sleep(3)
        #dashboard principal
        try:
            botton_pestana = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//Button[@aria-label="Cerrar"]'))).click()
            print("Clic en el botón 'pestaña emergente")
        except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException):
            print("No se encontro el boton de cookies ")

        #contar los artistas seguidos
        artistas = WebDriverWait(driver, 10).until(
             EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li')))
        cantidad_artistas = len(artistas)
        print(cantidad_artistas)
        input("reciclaje de usuarios")

        while cantidad_artistas > 1:
            time.sleep(1)   
            #seleccionar el primer artista para dejar de seguir
            artista = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[2]').click()

            try:
                botton_seguir = driver.find_element(By.XPATH, '//*[@data-encore-id="buttonSecondary"]')
                action_chains = ActionChains(driver)
                action_chains.context_click(botton_seguir).perform()
                
                print("Clic en el botón 'seguir'")
            except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException):
                print("No se encontró el botón 'seguir'")
                try:
                    botton_like = driver.find_element(By.XPATH, '//Button[@aria-checked="true"]')
                    botton_like.click()
                    print("Clic en el botón 'like'")
                except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException):
                    print("No se encontró el botón 'like'")


          # eliminar seguir

            time.sleep(1) 
            artistas = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li'))
             )

            cantidad_artistas = len(artistas)
            print(cantidad_artistas)
        input("reciclaje de likes")
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

                    botton_like = driver.find_element(By.XPATH, '//Button[@aria-checked="true"]')
                    botton_like.click()
                    print("Clic en el botón 'like'")

                    likes = WebDriverWait(driver, 10).until(
                    EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[4]/div/div[2]/div[2]/div'))
                    )
                    cantidad_likes = len(likes)
                    print(cantidad_likes)
                    time.sleep(0.2) 
                
            except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException):
                print("No se encontró el botón 'like'")
        else:
            print("sin datos")

    



input("Revision exitosa")          






