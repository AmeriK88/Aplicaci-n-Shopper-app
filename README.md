# Shopper-App

Shopper es una aplicación de lista de compras desarrollada en Python con KivyMD para la interfaz de usuario. Permite a los usuarios gestionar su lista de compras de forma fácil y eficiente, con funcionalidades como agregar artículos, eliminar artículos, exportar la lista y modo oscuro.

## Requisitos

Asegúrate de tener instalado Python y pip. Puedes instalar las dependencias del proyecto utilizando el archivo `requirements.txt` proporcionado.


`"pip install -r requirements.txt"´


## Ejecución
Para ejecutar la aplicación, simplemente ejecuta el script principal main.py:


`"python main.py"´

## Visualización de la aplicación:

![Captura de pantalla 2024-04-25 160645](https://github.com/AmeriK88/Aplicaci-n-Shopper-app/assets/165429251/2cd89443-ccc9-46e1-bb11-dfb53dfe1157)
![Captura de pantalla 2024-04-25 160652](https://github.com/AmeriK88/Aplicaci-n-Shopper-app/assets/165429251/87dbc51a-76ba-4410-a6f0-d84d6699d66d)
![Captura de pantalla 2024-04-25 160838](https://github.com/AmeriK88/Aplicaci-n-Shopper-app/assets/165429251/b09d9932-d35c-4243-b674-e05c8766b7d7)
![Captura de pantalla 2024-04-25 160856](https://github.com/AmeriK88/Aplicaci-n-Shopper-app/assets/165429251/9307216a-6012-48f2-b839-7a2929f6e221)


## Contribuir
Las contribuciones son bienvenidas. Si encuentras algún problema o tienes alguna sugerencia de mejora, no dudes en abrir un issue o enviar un pull request.

## Crear ejecutable 
Generar un archivo **.exe** para la aplicación de escritorio

1. Necesitas tener PyInstaller instalado. Puedes instalarlo ejecutando pip install pyinstaller.
2. Abre una terminal y navega hasta la carpeta raíz del proyecto.
3. Ejecuta el siguiente comando para generar el archivo ejecutable:
   
    `"pyinstaller --onefile main.py´"
   
**Esto generará un archivo ejecutable llamado main.exe en la carpeta dist.**
  -Si quieres añadir el icono de la ventana asegúrate de añadir `"pyinstaller --onefile --add-data "icono.ico;." main.py"´

Una vez generado el archivo **.exe**, puedes ejecutarlo directamente en tu sistema Windows haciendo doble clic en él.

## Adaptar la aplicación para dispositivos móviles

**Requisitos previos**

1. KivyMD instalado en tu sistema.
2. Buildozer instalado para compilar la aplicación para Android. Puedes seguir las instrucciones de instalación de Buildozer en su repositorio oficial.

Pasos para compilar la aplicación para Android:

1. Abre una terminal y navega hasta la carpeta raíz del proyecto.
2. Ejecuta el siguiente comando para compilar la aplicación para Android:

  `"buildozer android debug"´
  
Esto generará un archivo **.apk** en la carpeta bin que puedes instalar en dispositivos Android.
Transfiere el archivo .apk a tu dispositivo móvil y sigue las instrucciones para instalar la aplicación.

## Autor
Desarrollado por José Félix Gordo.




