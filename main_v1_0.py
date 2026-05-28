
def main(settings):
    main_choice = show_main_menu()
    if main_choice == 1:
        translate_document_flow(settings)
    elif main_choice == 2:
        correction_document_flow()
    elif main_choice == 3:
        GPT_settings_flow()
    elif main_choice == 4:
        print("Выход")
        return False
    return True

def show_main_menu():
    while True:
        choice = input("\n=== Lingua Engine ===\n\n1. Перевести документ \n2. Проверить орфографию \n3. Настройки модели GPT \n4. Выход\n\nВаш выбор:").strip() # Вызов основного меню
        try:
            choice = int(choice)
        except:
            print("\n*** Это не число. Выберите число. ***")
            continue
        if not (1 <= choice <= 4):
            print("*** Введите число от 1 до 4 ***")
            continue
        return choice

def translate_document_flow(settings):
    while True:
        translation_menu_choice = show_translation_menu()
        if translation_menu_choice == 1:
            file_name = getting_file_name_input()
            text, error = open_file(file_name)
            if error:
                return True
            paragraphs = text_divider(text)
            blocks = addition_divider(paragraphs)
            blocks = semantic_block_builder(blocks)
            chunks = chunk_creation(blocks, settings["max_chars"])
            if settings["debug_mode"]:
                chunk_saver(chunks)
            translated_chunks = fake_translator(chunks)
            output_file_name = get_output_file_name()
            if output_file_name is None:
                return None
            translated_document_saver(translated_chunks, output_file_name)
            return None
        elif translation_menu_choice == 2:
            translation_menu_settings_workflow(settings)
        elif translation_menu_choice == 3:
            return
            
def show_translation_menu():
    while True:
        choice = input("\n=== Lingua Engine ===\n\n1. Загрузить документ\n2. Дополнительные настройки\n3. Назад\n\nВаш выбор:").strip() # чанк - это кусок текста 
        try:
            choice = int(choice)
        except:
            print("\n*** Это не число. Выберите число. ***")
            continue
        if not (1 <= choice <= 3):
            print("*** Введите число от 1 до 3 ***")
            continue
        return choice
    
def translation_menu_settings_workflow(settings):
    while True:
        choice = show_translation_menu_settings(settings)
        if choice == 4:
            return
        apply_translate_settings(settings, choice)

def show_translation_menu_settings(settings):
    while True:
        choice = input(f"\n=== Lingua Engine ===\n\nDebug Mode: {settings["debug_mode"]}\nТекущий размер чанков:{settings["max_chars"]}\nЯзык:{settings["language"]}\n\n1. Язык\n2. Дебаггинг Да/Нет.\n3. Объем чанка\n4. Назад\n\nВаш выбор:").strip() # чанк - это кусок текста 
        try:
            choice = int(choice)
        except:
            print("\n*** Это не число. Выберите число. ***")
            continue
        if not (1 <= choice <= 4):
            print("*** Введите число от 1 до 4 ***")
            continue
        return choice


settings = {
    "debug_mode": False,
    "max_chars": 3000,
    "language": "EN"
}

def apply_translate_settings(settings, choice):
    if choice == 1:
        language_choice = show_language_options(settings)
        if language_choice == 1: 
            settings["language"] = "EN"
        if language_choice == 2:
            settings["language"] = "CZ"
        if language_choice == 3:
            return settings
    if choice == 2:
        if settings["debug_mode"] == True:
            settings["debug_mode"] = False
        else:
            settings["debug_mode"] = True
    if choice == 3:   
        while True:    
            max_chars = input("Введите количество символов для одного чанка (от 1000 до 20000 символов):").strip() # чанк - это кусок текста 
            try:
                max_chars = int(max_chars)
            except:
                print("\n*** Это не число. Выберите число. ***")
                continue
            if not (1000 <= max_chars <= 20000):
                print("*** Введите число от 1000 до 20000 ***")
                continue
            settings["max_chars"] = max_chars
            break
    return settings

def show_language_options(settings):
    while True:
        choice = input(f"\n=== Lingua Engine ===\n\nТекущий язык:{settings["language"]}\n\nВыберите язык:\n1. EN\n2. CZ\n3. Назад\n\nВаш выбор:").strip() # чанк - это кусок текста 
        try:
            choice = int(choice)
        except:
            print("\n*** Это не число. Выберите число. ***")
            continue
        if choice == 3:
            return choice
        if not (1 <= choice <= 3):
            print("*** Введите число от 1 до 3 ***")
            continue
        return choice

def correction_document_flow():
    pass

def correction_menu_flow():
    pass

def show_correction_menu():
    pass

def GPT_settings_flow():
    pass

def GPT_settings_menu():
    pass

def getting_file_name_input():
    file_name_input = input("Введите название файла, включительно формата (.txt): ").strip()
    return file_name_input

def open_file(file_name):
    if file_name == "":
        text = ""
        error = "Имя файла не задано"
        print(error)
        return text, error       
    try:
        with open(file_name,"r",encoding="utf-8") as file:
            text = file.read()
            error = ""
            return text, error
    except FileNotFoundError:
        error = "Файл не найден"
        text = ""
        print (error)
    return text, error 

def text_divider(text):
    paragraphs = text.split("\n\n")
    return paragraphs

def addition_divider(paragraphs):
    blocks = []
    for paragraph in paragraphs:
        if "\n" in paragraph:
            lines = paragraph.split("\n")
            for line in lines:
                if line.strip():
                    blocks.append(line)
        else: 
            if paragraph.strip():
                blocks.append(paragraph)
    return blocks

def semantic_block_builder(blocks):
    new_blocks = []
    temporary_text = ""
    for block in blocks:
        first_char = block.strip()[0]
        if first_char.islower():
            temporary_text += f"{block}\n" 
        else:    
            if temporary_text:
                temporary_text = f"\n{temporary_text}"
                new_blocks.append(temporary_text)
                temporary_text = ""
            new_blocks.append(block)
    if temporary_text:
        temporary_text = f"\n{temporary_text}"
        new_blocks.append(temporary_text)
    return new_blocks

def chunk_creation(blocks, settings):
    chunk = ""
    chunks = []
    for block in blocks:
        if len(chunk + block) <= settings["max_chars"] and chunk == "":
            chunk = block
        elif len(chunk + "\n" + block) <= settings["max_chars"] and chunk != "":
            chunk += "\n" + block
        else:
            chunks.append(chunk)
            chunk = block 
    if not chunk == "":
        chunks.append(chunk)     
    return chunks

def fake_translator(chunks):
    translated_chunks = []
    for chunk in chunks:
        if translated_chunks == []:
            chunk = f"[TRANSLATED]\n{chunk}"
            translated_chunks.append(chunk)
        else:
            chunk = f"\n{chunk}"
            translated_chunks.append(chunk)
    return translated_chunks

def get_output_file_name():
    while True:
        output_file_name = input("Введите название файла для сохранения результата, включительно формата (.txt) или ESC для выхода: ").strip()
        if not output_file_name:
            print("Вы не ввели название файла. ")
            continue
        if output_file_name.lower() == "esc":
            return None
        return output_file_name  

def translated_document_saver(translated_chunks, output_file_name):
    text = "".join(translated_chunks)
    with open(output_file_name, "w", encoding="utf-8") as result_file:
        result_file.write(text)
    return None

def chunk_saver(chunks):
    number_of_chunk = 1
    for chunk in chunks:
        name_of_chunk_file = (f"chunk_{number_of_chunk}.txt")
        with open(name_of_chunk_file, "w", encoding="utf-8") as result_file:
            result_file.write(chunk)
            number_of_chunk += 1
    return None


while True:
    should_continue = main(settings)
    if not should_continue:
        break
 
