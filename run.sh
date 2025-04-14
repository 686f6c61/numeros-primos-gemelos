#!/bin/bash

# ============================================================================
# Script de ejecución para Visualizador de Números Primos Gemelos
# 
# Este script realiza las siguientes operaciones:
# 1. Detecta la versión de Python disponible (python o python3)
# 2. Crea un entorno virtual si no existe
# 3. Instala las dependencias necesarias
# 4. Ejecuta la aplicación
#
# Autor: @https://github.com/686f6c61
# Fecha: $(date +%Y-%m-%d)
# ============================================================================

# Definimos colores para la salida
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
ROJO='\033[0;31m'
AZUL='\033[0;34m'
NC='\033[0m' # Sin Color

# Nombre del entorno virtual
VENV_DIR=".venv"

# Imprimir mensaje con formato
imprimir() {
    echo -e "${AZUL}[INFO]${NC} $1"
}

imprimir_exito() {
    echo -e "${VERDE}[OK]${NC} $1"
}

imprimir_advertencia() {
    echo -e "${AMARILLO}[ADVERTENCIA]${NC} $1"
}

imprimir_error() {
    echo -e "${ROJO}[ERROR]${NC} $1"
}

# Función para verificar si un comando existe
comando_existe() {
    command -v "$1" >/dev/null 2>&1
}

# ============================================================================
# 1. Detectar versión de Python
# ============================================================================
imprimir "Detectando versión de Python..."

# Intentamos primero con python3, luego con python
if comando_existe python3; then
    PYTHON="python3"
    imprimir_exito "Python 3 encontrado"
elif comando_existe python; then
    # Verificamos que sea Python 3.x y no Python 2.x
    VERSION=$(python -c 'import sys; print(sys.version_info[0])')
    if [ "$VERSION" -eq 3 ]; then
        PYTHON="python"
        imprimir_exito "Python 3 encontrado (como 'python')"
    else
        imprimir_error "Se encontró Python $VERSION, pero se requiere Python 3"
        exit 1
    fi
else
    imprimir_error "No se encontró Python en el sistema"
    imprimir_error "Por favor, instala Python 3 e intenta de nuevo"
    exit 1
fi

# ============================================================================
# 2. Verificar/crear entorno virtual
# ============================================================================
if [ ! -d "$VENV_DIR" ]; then
    imprimir "Creando entorno virtual en $VENV_DIR..."
    if $PYTHON -m venv "$VENV_DIR"; then
        imprimir_exito "Entorno virtual creado correctamente"
    else
        imprimir_error "No se pudo crear el entorno virtual"
        
        # Intentamos con virtualenv como alternativa
        if comando_existe virtualenv; then
            imprimir "Intentando con virtualenv..."
            if virtualenv -p $PYTHON "$VENV_DIR"; then
                imprimir_exito "Entorno virtual creado con virtualenv"
            else
                imprimir_error "Falló la creación del entorno virtual"
                exit 1
            fi
        else
            imprimir_error "No se pudo crear el entorno virtual. Verifica que el módulo 'venv' está instalado"
            exit 1
        fi
    fi
else
    imprimir "Usando entorno virtual existente"
fi

# ============================================================================
# 3. Activar entorno virtual e instalar dependencias
# ============================================================================
imprimir "Activando entorno virtual..."

# Determinar el script de activación según el sistema operativo
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows (Git Bash o similar)
    ACTIVATE="$VENV_DIR/Scripts/activate"
else
    # Unix/Linux/MacOS
    ACTIVATE="$VENV_DIR/bin/activate"
fi

if [ -f "$ACTIVATE" ]; then
    source "$ACTIVATE"
    imprimir_exito "Entorno virtual activado"
else
    imprimir_error "No se pudo encontrar el script de activación en $ACTIVATE"
    exit 1
fi

# Instalar dependencias si no están ya instaladas
if [ -f "requirements.txt" ]; then
    imprimir "Verificando e instalando dependencias..."
    pip install -r requirements.txt
    imprimir_exito "Dependencias instaladas/verificadas correctamente"
else
    imprimir_advertencia "No se encontró requirements.txt"
fi

# ============================================================================
# 4. Ejecutar la aplicación
# ============================================================================
imprimir "Iniciando el Visualizador de Números Primos Gemelos..."

# Primero intentamos con la interfaz gráfica, si falla usamos el modo consola
if [ -f "interfaz.py" ]; then
    imprimir "Ejecutando interfaz gráfica..."
    $PYTHON interfaz.py
    RESULTADO=$?
    
    if [ $RESULTADO -ne 0 ]; then
        imprimir_advertencia "La interfaz gráfica falló al ejecutarse. Probando el modo consola..."
        if [ -f "gemelos.py" ]; then
            imprimir "Ejecutando modo consola..."
            $PYTHON gemelos.py
        else
            imprimir_error "No se encuentra el archivo principal gemelos.py"
            exit 1
        fi
    fi
elif [ -f "gemelos.py" ]; then
    imprimir "Ejecutando modo consola..."
    $PYTHON gemelos.py
else
    imprimir_error "No se encuentran los archivos de la aplicación (interfaz.py o gemelos.py)"
    exit 1
fi

# Desactivar el entorno virtual
deactivate
imprimir_exito "Aplicación cerrada. Entorno virtual desactivado."
exit 0 