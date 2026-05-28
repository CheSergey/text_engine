def getting_file_name_input():
    file_name_input = input("Введите название файла, включительно формата (.txt): ").strip()
    return file_name_input

def top_clarification():
    while True:
        top = input("Введите какое колличество ТОП слов записать в файл (максимум 50): ").strip()
        try:
            top = int(top)
        except:
            print("Это не число")
            continue
        if top > 50:
            print("Максимальный топ до 50")
            continue 
        if top <= 0:
            print("Число должно быть больше 0")
            continue
        return top  
    
def get_text_from_file(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            text = file.read()
            error = ""
            return text, error
    except FileNotFoundError:
        error = "Файл не найден"
        text = ""
        print (error)
    return text, error  

def is_valid(text, error):
    if error == "Файл не найден":
        return False
    elif text == "" and error == "":
        print("Файл пуст")
        return False
    else:
        return True

        
# except Exception as e:
#     print(e)

def text_cleaning(text):
    for symbol in "!,.?!@#$%^*)_;'":
        text = text.replace(symbol, "")
    return text

def prepare_words(words):
    words = words.lower().split()
    number_of_words = len(words)
    return words, number_of_words

def word_decomposition(words):
    result = {}
    for word in words:
        if len(word) >=3:
            if word in result:
                result[word] += 1
            else:
                result[word] = 1
    return result

def get_count(pair):
    return pair[1]

def pairs_in_order(result):
    pairs=list(result.items())
    new_pairs = sorted(pairs, key=get_count, reverse = True) 
    return new_pairs

def uniq_words_number(new_pairs):
    return len(new_pairs)

def getting_file_name_output():
    file_name_output = input("Введите название файла для сохранения файла, включительно формата: ").strip()
    if file_name_output:
        return file_name_output
    while not file_name_output:
        file_name_output = input("Введите название файла для сохранения файла, включительно формата. Для приостановки обработки файла напишите - отмена: ").strip()
        if file_name_output.lower() == "отмена":
            return False
        if file_name_output:
            return file_name_output
        print("Имя файла не может быть пустым")
     

def write_result_to_file(text, file_name_output, number_of_words, uniq_words, top_n):
    if len(text) < top_n:
        top_n = len(text)
        new_text = (f"Всего слов: {number_of_words}\nУникальных слов: {uniq_words}\n\n\nTOP-{top_n} (максимальный доступный ТОП):\n")
    else: 
        new_text = (f"Всего слов: {number_of_words}\nУникальных слов: {uniq_words}\n\n\nTOP-{top_n}:\n")
    for word, count in text[:top_n]:
        new_text += (f"{word}: {count}\n")
    with open(file_name_output, "w", encoding="utf-8") as result_file:
        result_file.write(new_text)



continue_program = "да"
while continue_program == "да":
    file_name_input = getting_file_name_input()
    text, error = get_text_from_file(file_name_input)
    is_ok = is_valid(text, error)

    if is_ok:

        top_n = top_clarification()
        text = text_cleaning(text)
        words, number_of_words = prepare_words(text)
        result = word_decomposition(words)
        result_pairs = pairs_in_order(result)
        uniq_words = uniq_words_number(result_pairs)
        file_name_output = getting_file_name_output()
        if file_name_output:
            write_result_to_file(result_pairs, file_name_output, number_of_words, uniq_words, top_n)

    continue_program = input("Хотите проанализировать другой файл? (да/нет): ").lower()
    while continue_program not in ["да", "нет"]:
        continue_program = input("Ответьте только (да/нет): ").lower()



# lines = []
# for word, count in text[:3]:
#     lines.append(f"{word}: {count}")

# new_text = "\n".join(lines)