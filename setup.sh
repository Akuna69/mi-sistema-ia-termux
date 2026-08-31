#!/bin/bash

echo "=== 1. Actualizando paquetes del sistema ==="
pkg update && pkg upgrade -y

echo "=== 2. Instalando dependencias (Git, C++, Python, Wget) ==="
pkg install -y git cmake clang wget python libandroid-spawn

echo "=== 3. Instalando servidor web Flask ==="
pip install flask

echo "=== 4. Descargando y compilando el motor de IA (llama.cpp) ==="
if [ ! -d "llama.cpp" ]; then
  git clone https://github.com/ggml-org/llama.cpp
fi

cd llama.cpp
cmake -B build
cmake --build build --config Release
cd ..

echo "=== 5. Descargando el modelo ligero para Ankuna69 ==="
mkdir -p ~/models
if [ ! -f ~/models/llama-3.2-1b.gguf ]; then
  wget -O ~/models/llama-3.2-1b.gguf https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q4_K_M.gguf
fi

echo "=== Configuración completada con éxito ==="

