import tkinter as tk
from tkinter import messagebox
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
resultados = []
webdrivers = []

# Leer el archivo Excel y crear el diccionario de datos
nombre_archivo_excel = 'cuentaspotify.xlsx'  
da = pd.read_excel(nombre_archivo_excel)
diccionario_datos = da.set_index('correo')['contraseña'].to_dict()
diccionario_password = da.set_index('correo')['nueva_contraseña'].to_dict()

def mi_codigo():
    try:
        for usuario, clave in diccionario_datos.items():
            for user, nueva_contraseña  in diccionario_password.items():  
                driver = webdriver.Chrome(service=chromeService(ChromeDriverManager().install()))

                driver.get('https://www.spotify.com/co-es/account/overview/?utm_source=spotify&utm_medium=menu&utm_campaign=your_account')
                driver.implicitly_wait(6)

                #iniciar sesion
                search_mail = driver.find_element(By.XPATH, '//*[@id="login-username"]')
                search_password = driver.find_element(By.XPATH, '//*[@id="login-password"]')
                search_ingresar = driver.find_element(By.XPATH, '//*[@id="login-button"]')

                search_mail.send_keys(usuario)
                search_password.send_keys(clave)
                search_ingresar.click()

                
                # time.sleep(5)
                # try:
                #     botton_cookies = driver.find_element(By.XPATH, '//div[@id="onetrust-close-btn-container"]')
                #     botton_cookies.click()
                # except ElementNotInteractableException:
                #     print("El botón 'cookies' no es interactuable")
                # except ElementClickInterceptedException:
                #     print("Intercepción al hacer clic en el botón 'cookies'")
                # except NoSuchElementException:
                #     print("No se encontró el botón 'cookies'")
                
                
                #boton cambio de contraseña
                botton_change_password = driver.find_element(By.XPATH, '//div[@aria-describedby="onClickHintchangePassword"]')
                botton_change_password.click()

                #clave antigua
                search_password1 = driver.find_element(By.XPATH, '//input[@id="old_password"]')
                search_password1.send_keys(clave)
                print(clave)

                #nueva clave
                search_newpaswword= driver.find_element(By.XPATH, '//input[@id="new_password"]')
                search_newpaswword.send_keys(nueva_contraseña)
                print(nueva_contraseña)

                #confirmar contraseña
                search_newpaswword2 = driver.find_element(By.XPATH, '//input[@id="new_password_confirmation"]')
                search_newpaswword2.send_keys(nueva_contraseña)
                print(nueva_contraseña)

                #guardar contraseñas
                Button_savepassword = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div/div[2]/div[2]/article/section/form/div[4]/button')
                Button_savepassword.click()


                #atras
                Button_return = driver.find_element(By.XPATH, '//button[@data-encore-id="buttonPrimary"]')
                Button_return.click()
        resultado = 1 / 0  # Simulando un error
    except Exception as e:
        # Mostrar una ventana emergente con el mensaje de error
        mostrar_ventana_error(str(e))

def mostrar_ventana_error(mensaje):
    # Crear una ventana emergente con el mensaje de error
    ventana_error = tk.Tk()
    ventana_error.title("No se encontro el boton")
    
    label = tk.Label(ventana_error, text=mensaje, padx=10, pady=10)
    label.pack()

    # Función para continuar después de hacer clic en el botón
    def continuar():
        ventana_error.destroy()

    def volver_a_intentar():
        mi_codigo()
    
    # Botón para continuar
    boton_continuar = tk.Button(ventana_error, text="Continuar", command=continuar)
    boton_continuar.pack()

    boton_intentar = tk.Button(ventana_error, text="volver_a_intentar", command=volver_a_intentar)
    boton_intentar.pack()

    # Mostrar la ventana y esperar interacción
    ventana_error.mainloop()

# Llamar a tu función principal
mi_codigo()