# Proyecto_Compiladores

Este proyecto se inspira en CoCoR para crear un generador de parsers y scanners en base a archivos CoCoL.

Librerías

Para correr el programa se recomienda utilizar Python 3.7 o superior, y se requiere tener las siguientes librerías instaladas:
•	  PySimpleGUI (Para utilizar la GUI de la aplicación)
•	  PySimpleAutomata (Para imprimir el DFA en un archivo)

Ejecución

Para correr el archivo para la producción del parser y scanner únicamente se necesita correr:
  python .\my_cocor.py
Esto desplegará un explorador de archivos que permita seleccionar el ATG a utilizar para la creación del compilador.
Para correr el parser y scanner luego de que se abran generado únicamente se necesita correr:
  python .\run_scanner.py
Esto desplegará un explorador de archivos que permita seleccionar el de pruebas que el parser estará leyendo.
