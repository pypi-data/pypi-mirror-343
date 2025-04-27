from random import choice, seed
from cfile.core import Sequence, Function, Declaration, Statement, IncludeDirective, Blank, Block, Type, FunctionCall, \
    FunctionReturn
from generators.profiling1.function_generator import FunctionGenerator
from cfile import StyleOptions
from cfile.writer import Writer
import subprocess
from generators.base_module import BaseTaskManager
from wonderwords import RandomWord

int_type = Type("int")


class TaskFindingSlowFunctionGenerator(BaseTaskManager):
    """Генератор программы с вызовами функций, одна из которых выполняется
            дольше отстальных."""

    def __init__(self,
                 number_functions: int = 10,
                 # диапазон глубины вложенности циклов нормальной функции
                 norm_range_nesting_depth_for: tuple[int, int] = (2, 3),
                 # диапазон числа вложенных циклов нормальной функции
                 norm_range_n_nested_for: tuple[int, int] = (3, 4),
                 # диапазон глубины вложенности циклов отличающейся функции
                 deviant_range_nesting_depth_for: tuple[int, int] = (2, 3),
                 # диапазон числа вложенных циклов отличающейся функции
                 deviant_range_n_nested_for: tuple[int, int] = (3, 4),
                 # диапазон числа итераций цикла for
                 range_n_iterations_for: tuple[int, int] = (40, 50),
                 ):
        if number_functions <= 0:
            raise ValueError("Неверно указано число функций")
        ranges = [
            norm_range_nesting_depth_for,
            norm_range_n_nested_for,
            deviant_range_nesting_depth_for,
            deviant_range_n_nested_for
        ]
        for range in ranges:
            if range[0] > range[1]:
                raise ValueError("Неверный ввод диапазона")

        self.number_functions = number_functions
        self.norm_range_nesting_depth_for = norm_range_nesting_depth_for
        self.norm_range_n_nested_for = norm_range_n_nested_for
        self.deviant_range_nesting_depth_for = deviant_range_nesting_depth_for
        self.deviant_range_n_nested_for = deviant_range_n_nested_for
        self.range_n_iterations_for = range_n_iterations_for

    def create_task(self, random_seed, output: str):
        """Генерация программы"""

        seed(random_seed)

        words_generator = RandomWord()
        excluded_words = ['auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else',
                          'enum', 'extern', 'float', 'for', 'goto', 'if', 'long', 'register', 'return', 'short',
                          'signed', 'static', 'struct', 'switch', 'union', 'unsigned', 'void', 'volatile', 'while',
                          'main']
        regex = fr'^(?!{'|'.join(excluded_words)})[a-z]+$'
        function_names = words_generator.random_words(self.number_functions,
                                                      regex=regex)
        functions = [
            Function(name, int_type)
            for name in function_names
        ]
        deviant_function = choice(functions)

        code = Sequence()
        code.append(IncludeDirective("stdlib.h", True))
        code.append(Blank())

        generator = FunctionGenerator(self.range_n_iterations_for[0],
                                      self.range_n_iterations_for[1])
        for function in functions:
            code.append(Declaration(function))
            if function == deviant_function:  # генерация тела отличающейся функции
                function_body = generator.generate_function_body(
                    self.deviant_range_nesting_depth_for[0],
                    self.deviant_range_nesting_depth_for[1],
                    self.deviant_range_n_nested_for[0],
                    self.deviant_range_n_nested_for[1]
                )
            else:  # генерация тела нормальной функции
                function_body = generator.generate_function_body(
                    self.norm_range_nesting_depth_for[0],
                    self.norm_range_nesting_depth_for[1],
                    self.norm_range_n_nested_for[0],
                    self.norm_range_n_nested_for[1]
                )
            code.append(function_body)

        main_function = Function("main", "int")
        code.append(Declaration(main_function))
        function_body = Block()
        for function in functions:  # вызов всех функций в функции main
            function_body.append(Statement(FunctionCall(function.name)))
        function_body.append(Statement(FunctionReturn(0)))
        code.append(function_body)

        cfilename = self.get_cfilename(output)
        cfilepath = 'generators/profiling1/data/' + cfilename
        writer = Writer(StyleOptions())
        writer.write_file(code, cfilepath)

        subprocess.run(['gcc', '-pg', cfilepath, '-o', output])

    def get_cfilename(self, output: str):
        substrs = output.split('.')
        if len(substrs) > 1:
            return '.'.join(substrs[:len(substrs) - 1]) + '.c'
        else:
            return output + '.c'

    def verify_task(self, filename, answer):
        try:
            subprocess.run([f"./{filename}"])
        except FileNotFoundError:
            raise FileNotFoundError(f'Файл {filename} не найден')
        except OSError:
            raise OSError(f'Ошибка запуска {filename}')
        
        try:
            prof_process = subprocess.run(['gprof', '-bp', filename, 'gmon.out'],
                                            capture_output=True,
                                            text=True)
        except Exception:
            raise OSError('Ошибка запуска утилиты gprof')
        lines = prof_process.stdout.split('\n')
        table = lines[5:len(lines) - 1]
        if not table:
            raise OSError('Ошибка получения данных о профилировании с помощью gprof.')
        first_row = table[0].split()
        expected_answer = first_row[-1]
        return expected_answer == answer
