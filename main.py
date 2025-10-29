import os
import random
import hashlib
from typing import List, Dict, Tuple

def crear_directorio_trabajo():
    """Crea el directorio de trabajo si no existe"""
    directorio = "data_crypt"
    if not os.path.exists(directorio):
        os.makedirs(directorio)
        print(f"✓ Directorio '{directorio}' creado")
    return directorio

def generar_archivo_contraseñas_comunes():
    """Genera un archivo con las contraseñas más comunes"""
    contraseñas_comunes = [
        "123456",
        "password",
        "12345678",
        "qwerty",
        "123456789",
        "12345",
        "1234",
        "111111",
        "1234567",
        "dragon"
    ]
    
    directorio = crear_directorio_trabajo()
    archivo_path = os.path.join(directorio, "contraseñas_comunes.txt")
    
    with open(archivo_path, "w", encoding="utf-8") as f:
        for contraseña in contraseñas_comunes:
            f.write(contraseña + "\n")
    
    print(f"✓ Archivo '{archivo_path}' generado con {len(contraseñas_comunes)} contraseñas")
    return archivo_path

def leer_contraseñas_desde_archivo(archivo_path: str) -> List[str]:
    """Lee las contraseñas desde un archivo"""
    try:
        with open(archivo_path, "r", encoding="utf-8") as f:
            contraseñas = [linea.strip() for linea in f.readlines() if linea.strip()]
        print(f"✓ {len(contraseñas)} contraseñas leídas desde '{archivo_path}'")
        return contraseñas
    except FileNotFoundError:
        print(f"❌ Error: El archivo '{archivo_path}' no existe")
        return []

def mostrar_contraseñas(contraseñas: List[str]):
    """Muestra las contraseñas en formato numerado"""
    if not contraseñas:
        print("No hay contraseñas para mostrar")
        return
    
    print("\n--- CONTRASEÑAS ALMACENADAS ---")
    for i, contraseña in enumerate(contraseñas, 1):
        print(f"{i:2d}. {contraseña}")

def generar_contraseñas_aleatorias(cantidad: int = 15, longitud: int = 8):
    """Genera contraseñas aleatorias adicionales"""
    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%"
    contraseñas_aleatorias = []
    
    for i in range(cantidad):
        contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
        contraseñas_aleatorias.append(contraseña)
    
    directorio = crear_directorio_trabajo()
    archivo_path = os.path.join(directorio, "contraseñas_aleatorias.txt")
    
    with open(archivo_path, "w", encoding="utf-8") as f:
        for contraseña in contraseñas_aleatorias:
            f.write(contraseña + "\n")
    
    print(f"✓ {cantidad} contraseñas aleatorias generadas en '{archivo_path}'")
    return archivo_path

def calcular_hash_sha256(contraseña: str) -> str:
    """Calcula el hash SHA-256 de una contraseña"""
    return hashlib.sha256(contraseña.encode('utf-8')).hexdigest()

def generar_archivo_soluciones(archivo_contraseñas: str):
    """Genera un archivo con las contraseñas y sus hashes SHA256"""
    contraseñas = leer_contraseñas_desde_archivo(archivo_contraseñas)
    
    if not contraseñas:
        print("❌ No hay contraseñas para procesar")
        return None
    
    # Crear diccionario de contraseñas y hashes
    soluciones = {}
    for contraseña in contraseñas:
        soluciones[contraseña] = calcular_hash_sha256(contraseña)
    
    # Determinar el nombre del archivo de salida
    nombre_base = os.path.basename(archivo_contraseñas)
    nombre_solucion = f"soluciones_{nombre_base}"
    archivo_soluciones_path = os.path.join("data_crypt", nombre_solucion)
    
    # Escribir el archivo de soluciones
    with open(archivo_soluciones_path, "w", encoding="utf-8") as f:
        f.write("CONTRASEÑA | HASH SHA256\n")
        f.write("-" * 80 + "\n")
        for contraseña, hash_sha256 in soluciones.items():
            f.write(f"{contraseña} | {hash_sha256}\n")
    
    print(f"✓ Archivo de soluciones generado: '{archivo_soluciones_path}'")
    print(f"  - {len(soluciones)} contraseñas hasheadas")
    
    return archivo_soluciones_path, soluciones

def mostrar_soluciones(archivo_soluciones: str):
    """Muestra las contraseñas y sus hashes desde el archivo de soluciones"""
    try:
        with open(archivo_soluciones, "r", encoding="utf-8") as f:
            contenido = f.read()
        print(f"\n--- CONTENIDO DE {os.path.basename(archivo_soluciones)} ---")
        print(contenido)
    except FileNotFoundError:
        print(f"❌ Error: El archivo '{archivo_soluciones}' no existe")

def buscar_hash_en_soluciones(hash_buscado: str) -> Tuple[str, str]:
    """Busca un hash en todos los archivos de soluciones y devuelve la contraseña"""
    directorio = "data_crypt"
    hash_buscado = hash_buscado.lower().strip()
    
    if not os.path.exists(directorio):
        print("❌ El directorio 'data_crypt' no existe")
        return None, None
    
    # Buscar en todos los archivos que empiecen con "soluciones_"
    archivos_soluciones = [f for f in os.listdir(directorio) if f.startswith("soluciones_")]
    
    if not archivos_soluciones:
        print("❌ No hay archivos de soluciones disponibles")
        return None, None
    
    print(f"🔍 Buscando hash en {len(archivos_soluciones)} archivos de soluciones...")
    
    for archivo in archivos_soluciones:
        archivo_path = os.path.join(directorio, archivo)
        print(f"  Buscando en: {archivo}")
        
        try:
            with open(archivo_path, "r", encoding="utf-8") as f:
                lineas = f.readlines()
            
            # Saltar las primeras 2 líneas (encabezados)
            for linea in lineas[2:]:
                if "|" in linea:
                    partes = linea.split("|")
                    if len(partes) == 2:
                        contraseña = partes[0].strip()
                        hash_guardado = partes[1].strip()
                        
                        if hash_guardado.lower() == hash_buscado:
                            print(f"✅ ¡HASH ENCONTRADO!")
                            return contraseña, archivo
        
        except Exception as e:
            print(f"  ❌ Error leyendo {archivo}: {e}")
    
    print("❌ Hash no encontrado en ningún archivo de soluciones")
    return None, None

def buscar_hash_interactivo():
    """Función interactiva para buscar un hash en las soluciones"""
    print("\n--- BUSCADOR DE HASHES ---")
    print("Ingresa un hash SHA-256 para buscar su contraseña correspondiente")
    print("Ejemplo: 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92")
    print("-" * 50)
    
    hash_buscado = input("Hash a buscar: ").strip()
    
    if not hash_buscado:
        print("❌ No se ingresó ningún hash")
        return
    
    # Validar formato básico de hash SHA-256 (64 caracteres hexadecimales)
    if len(hash_buscado) != 64 or not all(c in '0123456789abcdef' for c in hash_buscado.lower()):
        print("❌ El formato del hash no es válido")
        print("   Un hash SHA-256 debe tener 64 caracteres hexadecimales")
        return
    
    contraseña_encontrada, archivo_encontrado = buscar_hash_en_soluciones(hash_buscado)
    
    if contraseña_encontrada:
        print(f"\n🎉 ¡HASH DESCIFRADO!")
        print(f"📁 Encontrado en: {archivo_encontrado}")
        print(f"🔑 Contraseña: {contraseña_encontrada}")
        print(f"🔐 Hash: {hash_buscado}")
        
        # Verificación adicional
        hash_calculado = calcular_hash_sha256(contraseña_encontrada)
        if hash_calculado == hash_buscado:
            print("✅ Verificación: Hash calculado coincide con el buscado")
        else:
            print("❌ Verificación: Los hashes NO coinciden (esto no debería pasar)")
    else:
        print(f"\n😞 El hash no fue encontrado en la base de datos")
        print("   Posibles razones:")
        print("   - La contraseña no está en los archivos de soluciones")
        print("   - No se han generado archivos de soluciones")
        print("   - El hash puede corresponder a una contraseña con salt")

def menu_principal():
    """Menú principal del programa"""
    while True:
        print("\n" + "="*50)
        print("           GENERADOR Y BUSCADOR DE HASHES")
        print("="*50)
        print("1. Generar archivo con contraseñas comunes")
        print("2. Leer y mostrar contraseñas comunes")
        print("3. Generar contraseñas aleatorias")
        print("4. Leer y mostrar contraseñas aleatorias")
        print("5. Generar hashes SHA256 (archivo soluciones)")
        print("6. Buscar contraseña por hash")
        print("7. Mostrar archivos disponibles")
        print("8. Salir")
        print("-"*50)
        
        opcion = input("Selecciona una opción (1-8): ").strip()
        
        if opcion == "1":
            archivo = generar_archivo_contraseñas_comunes()
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "2":
            archivo_path = os.path.join("data_crypt", "contraseñas_comunes.txt")
            contraseñas = leer_contraseñas_desde_archivo(archivo_path)
            mostrar_contraseñas(contraseñas)
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "3":
            try:
                cantidad = int(input("Cantidad de contraseñas a generar (default 15): ") or "15")
                longitud = int(input("Longitud de cada contraseña (default 8): ") or "8")
                archivo = generar_contraseñas_aleatorias(cantidad, longitud)
            except ValueError:
                print("❌ Error: Ingresa números válidos")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "4":
            archivo_path = os.path.join("data_crypt", "contraseñas_aleatorias.txt")
            contraseñas = leer_contraseñas_desde_archivo(archivo_path)
            mostrar_contraseñas(contraseñas)
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "5":
            print("\n¿De qué archivo quieres generar los hashes?")
            print("1. contraseñas_comunes.txt")
            print("2. contraseñas_aleatorias.txt")
            print("3. Otro archivo")
            
            sub_opcion = input("Selecciona (1-3): ").strip()
            
            if sub_opcion == "1":
                archivo_path = os.path.join("data_crypt", "contraseñas_comunes.txt")
            elif sub_opcion == "2":
                archivo_path = os.path.join("data_crypt", "contraseñas_aleatorias.txt")
            elif sub_opcion == "3":
                archivo_path = input("Ingresa la ruta del archivo: ").strip()
            else:
                print("❌ Opción no válida")
                input("\nPresiona Enter para continuar...")
                continue
            
            if os.path.exists(archivo_path):
                resultado = generar_archivo_soluciones(archivo_path)
                if resultado:
                    archivo_soluciones, soluciones = resultado
                    # Mostrar preview de las primeras soluciones
                    print(f"\n--- PREVIEW (primeras 3 entradas) ---")
                    for i, (contraseña, hash_sha256) in enumerate(list(soluciones.items())[:3]):
                        print(f"{contraseña} -> {hash_sha256[:32]}...")
            else:
                print(f"❌ El archivo '{archivo_path}' no existe")
            
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "6":
            buscar_hash_interactivo()
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "7":
            mostrar_archivos_disponibles()
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "8":
            print("¡Hasta luego! 👋")
            break
            
        else:
            print("❌ Opción no válida. Por favor, selecciona 1-8")

def mostrar_archivos_disponibles():
    """Muestra los archivos disponibles en el directorio de trabajo"""
    directorio = "data_crypt"
    if not os.path.exists(directorio):
        print("El directorio 'data_crypt' no existe aún")
        return
    
    archivos = os.listdir(directorio)
    if not archivos:
        print("No hay archivos en el directorio 'data_crypt'")
        return
    
    print("\n--- ARCHIVOS DISPONIBLES ---")
    for archivo in archivos:
        ruta_completa = os.path.join(directorio, archivo)
        tamaño = os.path.getsize(ruta_completa)
        tipo = "🔐 " if archivo.startswith("soluciones_") else "📄 "
        print(f"{tipo}{archivo} ({tamaño} bytes)")

if __name__ == "__main__":
    print("🔐 INICIANDO SISTEMA DE GESTIÓN Y BÚSQUEDA DE HASHES")
    print("   Directorio de trabajo: 'data_crypt/'")
    menu_principal()