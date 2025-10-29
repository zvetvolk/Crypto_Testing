# Crypto_Testing
# Sistema de Gestión y Búsqueda de Hashes

Un programa educativo en Python para gestionar contraseñas, generar hashes SHA-256 y realizar búsquedas inversas. Este programa genera automaticamente 2 diccionarios para poder probar una rainbow table y permite al usuario ingresar un hash para posteriormente buscarlo en los diccionarios precalculados de contraseñas con su respectivo hash. Un diccionario contiene las 10 contraseñas mas comunes utilizadas en Mexico y la segunda opcion permite generar un diccionario aleatorio desde la A-Z, a-z, 1-10, y caracteres especiales. Solo es necesario correr el programa y generara una carpeta llamada "data_crypt" y ahí mismo generara los dos diccionarios de palabras y con otra opcion calculara los hashes en SHA256 para posteriormente hacer una busqueda de contraseñas por hash.

## Características

- Generación de contraseñas comunes y aleatorias
- Cálculo de hashes SHA-256
- Búsqueda de contraseñas por hash (ataque de diccionario)
- Gestión automática de archivos
- Interfaz de menú interactivo

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/zvetvolk/crypto_hashing.git
