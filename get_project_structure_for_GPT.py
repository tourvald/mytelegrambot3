import os

def scan_directory(root_dir, exclude_dirs=None, indent_level=0):
    if exclude_dirs is None:
        exclude_dirs = ['venv', '__pycache__', '.git', '.idea']  # Папки для исключения

    try:
        for item in sorted(os.listdir(root_dir)):
            item_path = os.path.join(root_dir, item)

            # Проверяем, что элемент не находится в списке исключенных папок
            if os.path.isdir(item_path) and item not in exclude_dirs:
                print("  " * indent_level + f"[{item}]")
                scan_directory(item_path, exclude_dirs, indent_level + 1)
            elif os.path.isfile(item_path):
                print("  " * indent_level + item)
    except PermissionError as e:
        print(f"Permission denied: {e}")

if __name__ == "__main__":
    # Запускаем сканирование с текущей директории
    scan_directory(os.getcwd())