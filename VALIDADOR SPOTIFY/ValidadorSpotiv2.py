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

# Leer el archivo Excel y crear el diccionario de datos
nombre_archivo_excel = 'cambio_contraseñas.xlsx'  
da = pd.read_excel(nombre_archivo_excel)
diccionario_password = da.set_index('correo')['contraseña'].to_dict()

nombre_archivo_excel = 'validador.xlsx'  
da = pd.read_excel(nombre_archivo_excel)
diccionario_validador = da.set_index('correo')['contraseña'].to_dict()

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

def guardar_contraseña(usuario, contrasena_generada):

    resultados.append([usuario, contrasena_generada])
    # Crear un DataFrame a partir de la lista de resultados
    df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Nueva Contraseña'])
        # Guardar el DataFrame en un archivo Excel
    df_resultados.to_excel('resultados-cambio-contraseña-spotify.xlsx', index=False)

    with pd.ExcelWriter('resultados-cambio-contraseña-spotify.xlsx', engine='openpyxl') as writer:
            # Escribir el DataFrame en el archivo Excel
            df_resultados.to_excel(writer, index=False, sheet_name='Sheet1')

            # Obtener la hoja activa
            sheet = writer.sheets['Sheet1']

            # Establecer el ancho de columna para la columna 'Usuario'
            sheet.column_dimensions['A'].width = 40  # Ajusta el ancho según tus necesidades

            # Establecer el ancho de columna para la columna 'Nueva Contraseña'
            sheet.column_dimensions['B'].width = 30  # Ajusta el ancho según tus necesidades
    return(print("guardado exitoso"))

def cerrar_banner_cookies(driver):
    try:
        botton_cookies = driver.find_element(By.XPATH, '//div[@id="onetrust-close-btn-container"]')
        botton_cookies.click()
    except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException):
        print("El botón 'cookies' no es interactuable")
        
def cerrar_pestanha_emergente(driver):
    try:
        botton_cookies = driver.find_element(By.XPATH, '//Button[@aria-label="Cerrar"]')
        botton_cookies.click()
        print("Clic en el botón 'pestaña emergente'")
    except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException):
        print("No se encontró el botón 'pestaña emergente'")

def contar_artistas_seguidos(driver):
    try:
        artistas = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li'))
        )
        cantidad_artistas = len(artistas)
        print(cantidad_artistas)
        return artistas, cantidad_artistas
    except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException):
        print("No se encontraron artistas")
        return None, 0
def main():
    for usuario, clave in diccionario_datos.items():
        try:
            driver = iniciar_sesion(usuario, clave)
            cuenta = 0
            cerrar_banner_cookies(driver)
            cerrar_pestanha_emergente(driver)

            artistas, cantidad_artistas = contar_artistas_seguidos(driver)
            cuenta = 1
            while cantidad_artistas > 0:
                playlist1 = "Playlist"
                artista = "Artista"
                album = "Álbum"
                episodios = "Episodios guardados"
                podcast = "Podcast"

                time.sleep(1)
                elemento_principal = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[1]')
                texto_span = elemento_principal.find_element(By.XPATH, './/span[@class="ListRowDetails__LineClamp-sc-sozu4l-1 hITFAK"]').text
                cantidad_artistas -= 1
                


                if playlist1 in texto_span :
                    try:
                        # print("playlist1")
                        LUGAR2 = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[1]')
                        action_chains = ActionChains(driver)
                        action_chains.context_click(LUGAR2).perform()
                        segir2 = driver.find_element(By.XPATH, '//span[@data-encore-id="type" and text()="Eliminar de Tu biblioteca"]')
                        segir2.click()
                        confirmar_segir = driver.find_element(By.XPATH, '//button[@class="Button-sc-qlcn5g-0 keyrGu" and @data-encore-id="buttonPrimary"]/span[text()="Eliminar"]')
                        confirmar_segir.click()
                        cantidad_artistas = len(artistas)
                        time.sleep(1)

                    except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException):
                        try:
                            eliminar_button = driver.find_element(By.XPATH, '//span[text()="Eliminar"]/ancestor::button')
                            eliminar_button.click()
                            confirmar_segir = driver.find_element(By.XPATH, '//button[@class="Button-sc-qlcn5g-0 keyrGu" and @data-encore-id="buttonPrimary"]/span[text()="Eliminar"]')
                            confirmar_segir.click()
                            cantidad_artistas = len(artistas)
                            time.sleep(1)

                        except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException):
                            megusta = "gusta"
                            seach_like = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[1]')
                            seach_like_text = seach_like.find_element(By.XPATH, '//*[@id="listrow-title-spotify:collection:tracks"]').text
                            seach_like.click()

                            if megusta in seach_like_text:
                                print("vamos aqui")
                                likes = WebDriverWait(driver, 10).until(
                                EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[4]/div/div[2]/div[2]/div')))
                                cantidad_likes = len(likes)
                                print(cantidad_likes)

                                while cantidad_likes > 0:
                                    
                                    try:
                                        botton_like = driver.find_element(By.XPATH, '//button[@aria-checked="true" and @data-testid="add-button" and @data-encore-id="buttonTertiary"]')
                                        botton_like.click()
                                        print("Clic en el botón 'like'")
                                        likes = WebDriverWait(driver, 10).until(
                                            EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[4]/div/div[2]/div[2]/div'))
                                        )
                                        cantidad_likes = len(likes)
                                        print(cantidad_likes)
                                        time.sleep(1)
                                    except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException,TimeoutException):
                                        print("No se encontró el botón 'like'")
                                        break  # Salir del bucle si no se encuentra el botón

                                        
                        except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, TimeoutException):
                                print("Elemento 'elementos' no encontrado. El flujo de código no continuará.")
                                continue

                elif artista in texto_span:
                    LUGAR2 = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[1]')
                    action_chains = ActionChains(driver)
                    action_chains.context_click(LUGAR2).perform()
                    segir = driver.find_element(By.XPATH, '//Button[@aria-disabled="false"]').click()
                    confirmar_segir = driver.find_element(By.XPATH, '//span[contains(@class, "ButtonInner-sc-14ud5tc-0") and contains(@class, "glYGDr") and contains(@class, "encore-bright-accent-set") and contains(@class, "MIsUJlamzLYuAlvPbmZz") and text()="Eliminar"]')
                    confirmar_segir.click()
                    cantidad_artistas = len(artistas)
                    time.sleep(1)

                elif album in texto_span :
                    LUGAR2 = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[1]')
                    action_chains = ActionChains(driver)
                    action_chains.context_click(LUGAR2).perform()
                    segir2 = driver.find_element(By.XPATH, '//span[@class="Type__TypeElement-sc-goli3j-0 ieTwfQ ellipsis-one-line htqz7Vb8mLJvGKTi1vrs"]')
                    segir2.click()
                    confirmar_segir = driver.find_element(By.XPATH, '//button[@class="Button-sc-qlcn5g-0 keyrGu" and @data-encore-id="buttonPrimary"]/span[text()="Eliminar"]')
                    confirmar_segir.click()
                    cantidad_artistas = len(artistas)
                    time.sleep(1)

                elif podcast in texto_span:
                    LUGAR2 = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[1]')
                    action_chains = ActionChains(driver)
                    action_chains.context_click(LUGAR2).perform()
                    segir = driver.find_element(By.XPATH, '//Button[@aria-disabled="false"]').click()
                    confirmar_segir = driver.find_element(By.XPATH, '//span[contains(@class, "ButtonInner-sc-14ud5tc-0") and contains(@class, "glYGDr") and contains(@class, "encore-bright-accent-set") and contains(@class, "MIsUJlamzLYuAlvPbmZz") and text()="Eliminar"]')
                    confirmar_segir.click()
                    cantidad_artistas = len(artistas)
                    time.sleep(1)
                
                elif episodios in texto_span :
                    columnartista = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[1]')
                    columnartista.click()

                    try:
                        elementos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_OxEpxzAgJiTENfolVUN"]//div[@class="T9iBYqbERZHdwDl0U2tC"]')))
                        contarpodcast = len(elementos)
                        
                        elementoscroll = driver.find_element(By.XPATH, '//div[@class="_OxEpxzAgJiTENfolVUN"]//div[@class="T9iBYqbERZHdwDl0U2tC"]')
                        driver.execute_script("arguments[0].scrollIntoView();", elementoscroll)

                        while contarpodcast > 0:
                            time.sleep(1)
                            
                            try:
                                boton = driver.find_element(By.XPATH, './/button[@data-testid="add-button"]')
                                boton.click()
                                print("Clic en el botón 'add'")
                                # Crear una instancia de ActionChains

                            except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, TimeoutException):
                                print("Eliminar fijos: Algo salió mal al hacer clic en el botón.")

                            elementos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_OxEpxzAgJiTENfolVUN"]//div[@class="T9iBYqbERZHdwDl0U2tC"]')))
                            contarpodcast = len(elementos)

                    except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, TimeoutException):
                        print("Elemento 'elementos' no encontrado. El flujo de código no continuará.")
                        cantidad_artistas = len(artistas)


                    time.sleep(1)     
                    artistas = WebDriverWait(driver, 10).until(
                    EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li')))
                    cantidad_artistas = len(artistas)
                    print(cantidad_artistas)

            cantidad_artistas = len(artistas)  
            resultados.append([usuario, clave, "RECICLAJE EXITOSO"])
            df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Contraseña', 'Resultado'])
            # Guardar el DataFrame en un archivo Excel
            df_resultados.to_excel('resultados-reciclaje-spoti.xlsx', index=False)

            
        except Exception as e:
        # En caso de error, verificar si es un error de contraseña incorrecta
            crea = "Crea"
            if cuenta == 0:
                try:
                    text = driver.find_element(By.XPATH, '//span[@class="Text__TextElement-sc-if376j-0 ksSRyh encore-text-body-medium-bold" and @data-encore-id="text"]').text
                    print (text)
                    if crea in text :
                        resultados.append([usuario, clave, "RECICLAJE EXITOSO"])
                        df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Contraseña', 'Resultado'])
                        # Guardar el DataFrame en un archivo Excel
                        df_resultados.to_excel('resultados-reciclaje-spoti.xlsx', index=False)
                        driver.quit()

                except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException,TimeoutException):
                    resultados.append([usuario, clave, "error de contraseña"])
                    df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Contraseña', 'Resultado'])
                    # Guardar el DataFrame en un archivo Excel
                    df_resultados.to_excel('resultados-reciclaje-spoti.xlsx', index=False)
                    driver.quit()
            else:      
                
                try:
                    text = driver.find_element(By.XPATH, '//span[@class="Text__TextElement-sc-if376j-0 ksSRyh encore-text-body-medium-bold" and @data-encore-id="text"]').text
                    print (text)
                    if crea in text :
                        resultados.append([usuario, clave, "RECICLAJE EXITOSO"])
                        df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Contraseña', 'Resultado'])
                        # Guardar el DataFrame en un archivo Excel
                        df_resultados.to_excel('resultados-reciclaje-spoti.xlsx', index=False)
                        driver.quit()

                except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException,TimeoutException):
                    resultados.append([usuario, clave, "ha ocurrido un error "])
                    df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Contraseña', 'Resultado'])
                    # Guardar el DataFrame en un archivo Excel
                    df_resultados.to_excel('resultados-reciclaje-spoti.xlsx', index=False)
                    driver.quit()
            

        finally:
            if 'driver' in locals() and driver is not None:
                driver.quit()

def Change_passsword ():
    for usuario, clave in diccionario_password.items():
        driver = webdriver.Chrome(service=chromeService(ChromeDriverManager().install()))

        driver.get('https://www.spotify.com/co-es/account/overview/?utm_source=spotify&utm_medium=menu&utm_campaign=your_account')
        driver.implicitly_wait(6)
        try:
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
                botton_change_password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-describedby="onClickHintchangePassword"]'))).click()

            except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException):
                    print("Error al interactuar con el botón de cambio de contraseña")

            time.sleep(3)
            contrasena_generada = generar_contrasena(10)

            #clave antigua
            search_password1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="old_password"]')))
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


            #close
            Button_close = driver.find_element(By.XPATH, '//div[@aria-describedby="onClickHintsignOutEverywhere"]')
            Button_close.click()

            time.sleep(0.5)
            #close confirmation
            Button_close_confirmation = driver.find_element(By.XPATH, '//a[@data-encore-id="buttonSecondary"]')
            Button_close_confirmation.click()

            driver.quit()


        except Exception as e:
            resultados.append([usuario, "contraseña incorrecta"])
            # Crear un DataFrame a partir de la lista de resultados
            df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Nueva Contraseña'])
                # Guardar el DataFrame en un archivo Excel
            df_resultados.to_excel('resultados-cambio-contraseña-spotify.xlsx', index=False)

def validador():
    for usuario, clave in diccionario_validador.items():
        try:
            driver = iniciar_sesion(usuario, clave)
            elemento_inicio = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/nav/div[1]/ul/li[1]')
            span_inicio = elemento_inicio.find_element(By.XPATH, './/span[@data-encore-id="text"]').text           
            resultados.append([usuario, "contraseña correcta"])
            # Crear un DataFrame a partir de la lista de resultados
            df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Nueva Contraseña'])
                # Guardar el DataFrame en un archivo Excel
            df_resultados.to_excel('resultados-validador.xlsx', index=False)

            driver.quit()


        except Exception as e:
            resultados.append([usuario, "contraseña incorrecta"])
            # Crear un DataFrame a partir de la lista de resultados
            df_resultados = pd.DataFrame(resultados, columns=['Usuario', 'Nueva Contraseña'])
                # Guardar el DataFrame en un archivo Excel
            df_resultados.to_excel('resultados-validador.xlsx', index=False)

def cerrar_navegadores_y_salir():
    root.destroy()

root = Tk()
root.title("Validador SPOTIFY")
root.configure(bg="#191919")


# Configurar la imagen
imagen_path = "Reciclaje-Spotify.png"
imagen = PhotoImage(file=imagen_path)

# Obtener las dimensiones de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcular el tamaño deseado del Canvas
canvas_width = screen_width // 1.78
canvas_height = screen_height // 2.1

# Configurar el Canvas con dimensiones calculadas
canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="#191919", highlightthickness=0)
canvas.pack()

# Dibujar la imagen en el Canvas y ajustar el tamaño
canvas.create_image(0, 0, anchor=NW, image=imagen, tags="imagen")

# Crear un Frame para los tres primeros botones
frame_botones = Frame(root, bg="#191919")
frame_botones.pack()

# Configurar los botones en el primer Frame
boton_reciclar = ttk.Button(frame_botones, text="RECICLAR", command=main, style="TButton",width=27)
boton_reciclar.pack(side="left", padx=(50, 20), pady=10)

boton_password = ttk.Button(frame_botones, text="CAMBIO DE CONTRASEÑA", command=Change_passsword, style="TButton", width=27)
boton_password.pack(side="left", padx=(0, 0), pady=10)

boton_validar = ttk.Button(frame_botones, text="VALIDAR", command=validador, style="TButton", width=27)
boton_validar.pack(side="left", padx=(20, 50), pady=10)

# Crear un Frame para el botón "CERRAR"
frame_cerrar = Frame(root, bg="#191919")
frame_cerrar.pack()

# Configurar el botón "CERRAR" dentro del segundo Frame
boton_cerrar = ttk.Button(frame_cerrar, text="CERRAR ", command=cerrar_navegadores_y_salir, style="TButton", width=64)
boton_cerrar.grid(row=1, column=0, pady=(0, 10))
# Crear estilo para los botones
style = ttk.Style()
style.configure("TButton", font=("Arial", 10, "bold"), background="#037A24", foreground="black", borderwidth=0, padding=10)
style.map("TButton", background=[("active", "#037A24")])  # Cambiar el color al hacer clic

# Llamar a cerrar_navegadores() al cerrar la ventana de Tkinter
root.mainloop()