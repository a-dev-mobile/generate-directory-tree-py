#!/bin/bash
# SCRIPT_PATH="/home/dmitriy/Documents/DEV/MY_GITHUB/generate-directory-tree-py/build.sh" && chmod +x $SCRIPT_PATH && $SCRIPT_PATH

# Переменные для путей
SCRIPT_DIR=$(dirname "$0")
DIST_DIR="$SCRIPT_DIR/dist"
BUILD_DIR="$SCRIPT_DIR/build"
OUTPUT_DIR="/home/dmitriy/Documents/DEV/MY_GITHUB/generate-directory-tree-py/release"
OUTPUT_FILE="generate-directory-tree-latest.linux"

# Установка Python и зависимостей
echo "Setting up Python environment..."
python3 -m venv --copies venv
source venv/bin/activate
pip install --upgrade pip
pip install pyinstaller argparse==1.4.0 prettytable==3.10.0

# Создание директории для сборки, если ее нет
mkdir -p "$DIST_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

# Сборка бинарного файла с помощью PyInstaller
echo "Building executable..."
pyinstaller --onefile "$SCRIPT_DIR/scripts/main.py" --distpath "$DIST_DIR" --workpath "$BUILD_DIR"

# Проверка успешности сборки
if [ -f "$DIST_DIR/main" ]; then
    echo "Executable built successfully: $DIST_DIR/main"
    
    # Перемещение и переименование выходного файла
    mv "$DIST_DIR/main" "$OUTPUT_DIR/$OUTPUT_FILE"
    echo "Executable moved to: $OUTPUT_DIR/$OUTPUT_FILE"
else
    echo "Error: Build failed."
    exit 1
fi

# Опционально: очистка временных файлов сборки
rm -rf "$BUILD_DIR"

# Сообщение об окончании работы
echo "Build process completed."
