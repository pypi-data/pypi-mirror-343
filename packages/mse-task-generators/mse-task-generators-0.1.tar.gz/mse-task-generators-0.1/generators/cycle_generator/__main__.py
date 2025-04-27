import argparse
import os
import subprocess
import time
from generators.cycle_generator.cycle_generator_file import CCodeGenerator

def main():
    parser = argparse.ArgumentParser(prog='Генератор задач')
    parser.add_argument('-m', '--mode', help='Генерация задачи или проверка')
    parser.add_argument('-s', '--seed',
                            type=str, default=time.time(),
                            help="Целое число, которое используется в качестве начального значения для генерации случайных чисел")
    args = parser.parse_args()
    if args.mode == "1":
        try:
            # Запрашиваем у пользователя ввод максимальной глубины вложенности циклов
            max_depth = int(input("Введите количество циклов for: "))
            if max_depth < 1 or max_depth > 10:  # Проверяем, что введенное значение положительное
                raise ValueError("Количество должно быть положительным целым числом, меньше 10.")  # Если значение меньше 1, выбрасываем исключение
            # Запрашиваем у пользователя ввод максимальной глубины вложенности циклов
            max_num_of_array = int(input("Введите максимальное количество строк, с присваиванием значений элементам массива на один цикл for: "))
            if max_num_of_array < 1 or max_num_of_array > 10:  # Проверяем, что введенное значение положительное
                raise ValueError("Количество должно быть положительным целым числом, меньше 10.")  # Если значение меньше 1, выбрасываем исключение
        except ValueError as e:  # Обрабатываем исключения, возникающие при некорректном вводе
            print(f"Ошибка ввода: {e}")  # Выводим сообщение об ошибке
        else:  # Если исключений не возникло
            generator = CCodeGenerator(max_depth=max_depth, max_num_of_array=max_num_of_array)  # Создаем экземпляр класса CCodeGenerator с заданной глубиной
            pathe = os.path.dirname(__file__) + "/generators_files"
            output_file_path = os.path.join(pathe, "generated_code_with_cycle.c")
            generator.create_task(args.seed, output_file_path)  # Вызываем метод для записи сгенерированного кода в файл
            output_file_path_bin = os.path.join(pathe, "generated_code_with_cycle") # Путь к исполняемому файлу
            print(f"Исполняемый файл успешно сгенерирован и записан в файл: {output_file_path_bin}")  # Сообщаем пользователю об успешном завершении операции
            compile_command = ["gcc", "-g", "generators/cycle_generator/generators_files/generated_code_with_cycle.c", "-o", "generators/cycle_generator/generators_files/generated_code_with_cycle"]
            result = subprocess.run(compile_command, capture_output=True, text=True)

    elif args.mode == "2":
        pathe = os.path.dirname(__file__) + "/generators_files"
        filename = os.path.join(pathe, "generated_code_with_cycle.c")
        answer = CCodeGenerator.verify_task(filename)
        print(answer)




    