import os
import argparse

# Пути к файлам
HTML_PATH = os.path.join("templates", "home.html")
CSS_PATH = os.path.join("static", "css", "home.css")
VIEWS_FILES = [
    os.path.join("chatty", "views.py"),
    os.path.join("ads", "views.py"),
    os.path.join("posts", "views.py"),
    os.path.join("users", "views.py"),
    os.path.join("subscriptions", "views.py")
]


def insert_ad_block_to_html(ad_number, top, right):
    if not os.path.exists(HTML_PATH):
        print("[❌] Файл templates/home.html не найден.")
        return

    with open(HTML_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    block_id = f"ad-sidebar-{ad_number}"
    if f'id="{block_id}"' in content:
        print("[⚠] HTML блок уже существует.")
        return

    ad_html = f'''
<!-- 🚀 Автогенерируемый рекламный блок #{ad_number} -->
<div id="{block_id}" class="ad-sidebar ad-sidebar-{ad_number}">
  {{% include 'ads/ad_slider.html' with ad_group=ads_{ad_number} %}}
</div>
'''

    insert_point = content.rfind('{% endblock %}')
    if insert_point == -1:
        print("[❌] Блок content не найден.")
        return

    new_content = content[:insert_point] + "\n" + ad_html + "\n" + content[insert_point:]
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[✔] HTML блок #{ad_number} добавлен.")


def insert_css_block(ad_number, top, right):
    if not os.path.exists(CSS_PATH):
        print("[❌] Файл static/css/home.css не найден.")
        return

    with open(CSS_PATH, "r", encoding="utf-8") as f:
        css_content = f.read()

    class_name = f".ad-sidebar-{ad_number}"
    if class_name in css_content:
        print("[⚠] CSS блок уже существует.")
        return

    css_block = f'''
/* 🚀 Стили для рекламного блока #{ad_number} */
.ad-sidebar-{ad_number} {{
  position: fixed;
  top: {top}px;
  right: {right};
  width: 300px;
  max-width: 20vw;
  z-index: 500;
}}
'''

    with open(CSS_PATH, "a", encoding="utf-8") as f:
        f.write(css_block)

    print(f"[✔] CSS блок #{ad_number} добавлен.")


def update_views_context(ad_number):
    variable = f"ads_{ad_number}"

    for path in VIEWS_FILES:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            if variable in content:
                continue

            # Добавим в первый def или class (псевдопример: вставим в context в render)
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if "def" in line and "home" in line:
                    indent = " " * (len(line) - len(line.lstrip()))
                    context_inserted = False
                    for j in range(i, len(lines)):
                        if "context =" in lines[j]:
                            # Добавляем ads_N внутрь словаря контекста
                            if "}" in lines[j]:
                                lines[j] = lines[j].replace("}", f", '{variable}': [], }}")
                                context_inserted = True
                                break
                    if context_inserted:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write("\n".join(lines))
                        print(f"[✔] Контекст {variable} добавлен в {path}")
                        return

    print("[❌] Файл views.py не найден или не содержит функцию 'home'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Добавление нового блока рекламы")
    parser.add_argument("block_number", type=int, help="Номер рекламного блока")
    parser.add_argument("--top", type=int, required=True, help="Отступ сверху (в px)")
    parser.add_argument("--right", type=str, required=True, help="Смещение справа (например: 'calc(...)')")

    args = parser.parse_args()
    insert_ad_block_to_html(args.block_number, args.top, args.right)
    insert_css_block(args.block_number, args.top, args.right)
    update_views_context(args.block_number)
