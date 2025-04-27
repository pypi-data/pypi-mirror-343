from random import choice, seed, randint
from cfile.core import Sequence, Function, Declaration, Statement, IncludeDirective, Blank, Block, Type, FunctionCall, \
    FunctionReturn
from generators.profiling1.function_generator import FunctionGenerator
from cfile import StyleOptions
from cfile.writer import Writer
import subprocess
from generators.base_module import BaseTaskManager
from wonderwords import RandomWord

int_type = Type("int")


class TaskFindingSlowFuncInFuncGenerator(BaseTaskManager):
    """Генератор программы с вызовами функций, в числе которых есть функция find_me,
    в которой одна из вызываемых функций выполняется дольше остальных"""

    def __init__(self,
                 # диапазон глубины вложенности циклов нормальной функции
                 norm_range_nesting_depth_for: tuple[int, int] = (2, 3),
                 # диапазон числа вложенных циклов нормальной функции
                 norm_range_n_nested_for: tuple[int, int] = (3, 4),
                 # диапазон глубины вложенности циклов отличающейся функции
                 deviant_range_nesting_depth_for: tuple[int, int] = (2, 3),
                 # диапазон числа вложенных циклов отличающейся функции
                 deviant_range_n_nested_for: tuple[int, int] = (3, 4),
                 # диапазон числа вложенных вызовов функций
                 range_nested_fcalls: tuple[int, int] = (2, 3),
                 # диапазон глубины вызовов функций
                 range_depth_fcalls: tuple[int, int] = (3, 4),
                 # диапазон глубины вызовов, на которой находится функция, в которой нужно найти медленную
                 range_depth_f_find_me: tuple[int, int] = (1, 2),
                 # диапазон числа итераций цикла for
                 range_n_iterations_for: tuple[int, int] = (40, 50),
                 ):
        ranges = [
            norm_range_nesting_depth_for,
            norm_range_n_nested_for,
            deviant_range_nesting_depth_for,
            deviant_range_n_nested_for,
            range_nested_fcalls,
            range_depth_fcalls,
            range_depth_f_find_me
        ]
        for range in ranges:
            if range[0] > range[1]:
                raise ValueError("Неверный ввод диапазона")

        self.norm_range_nesting_depth_for = norm_range_nesting_depth_for
        self.norm_range_n_nested_for = norm_range_n_nested_for
        self.deviant_range_nesting_depth_for = deviant_range_nesting_depth_for
        self.deviant_range_n_nested_for = deviant_range_n_nested_for
        self.range_nested_fcalls = range_nested_fcalls
        self.range_depth_fcalls = range_depth_fcalls
        self.range_depth_f_find_me = range_depth_f_find_me
        self.range_n_iterations_for = range_n_iterations_for

    def create_task(self, random_seed, output: str):
        """Генерация программы"""

        seed(random_seed)

        seq_num = 0  # последовательность чисел для имён функций
        words_generator = RandomWord()
        max_num_functions = sum([
            self.range_nested_fcalls[1] ** depth
            for depth in range(1, self.range_depth_fcalls[1] + 1)
        ])
        excluded_words = ['auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else',
                          'enum', 'extern', 'float', 'for', 'goto', 'if', 'long', 'register', 'return', 'short',
                          'signed', 'static', 'struct', 'switch', 'union', 'unsigned', 'void', 'volatile', 'while',
                          'main']
        regex = fr'^(?!{'|'.join(excluded_words)})[a-z]+$'
        function_names = words_generator.random_words(max_num_functions,
                                                      regex=regex)
        function_calls = {}  # словарь для графа вызовов

        depth_fcalls = randint(
            self.range_depth_fcalls[0], self.range_depth_fcalls[1])
        depth_f_find_me = randint(
            self.range_depth_f_find_me[0], self.range_depth_f_find_me[1])  # глубина find_me
        functions_on_cur_depth = [Function("main", int_type)]
        for cur_depth in range(1, depth_fcalls + 1):  # построение графа вызовов
            functions_on_prev_depth = functions_on_cur_depth
            functions_on_cur_depth = []
            for f in functions_on_prev_depth:
                nested_fcalls = randint(
                    self.range_nested_fcalls[0], self.range_nested_fcalls[1])
                function_calls[f] = [
                    Function(function_names[seq_num + i], int_type) for i in range(nested_fcalls)
                ]
                seq_num += len(function_calls[f])
                functions_on_cur_depth += function_calls[f]
            if cur_depth == depth_f_find_me:  # найдена глубина find_me
                # выбор функции find_me
                f_find_me = choice(functions_on_cur_depth)
                f_find_me.name = 'find_me'

        for f in functions_on_cur_depth:  # функции, не вызывающие функции
            function_calls[f] = []

        # выбор медленных функции
        slow_functions = [choice(calls)
                          for _, calls in function_calls.items() if calls]
        code = Sequence()
        code.append(IncludeDirective("stdlib.h", True))
        code.append(Blank())

        generator = FunctionGenerator(self.range_n_iterations_for[0],
                                      self.range_n_iterations_for[1])
        for function, calls in reversed(function_calls.items()):
            code.append(Declaration(function))
            if function in slow_functions:  # генерация тела медленной функции
                function_body = generator.generate_function_body(
                    self.deviant_range_nesting_depth_for[0],
                    self.deviant_range_nesting_depth_for[1],
                    self.deviant_range_n_nested_for[0],
                    self.deviant_range_n_nested_for[1]
                )
            else:  # генерация тела быстрой функции
                function_body = generator.generate_function_body(
                    self.norm_range_nesting_depth_for[0],
                    self.norm_range_nesting_depth_for[1],
                    self.norm_range_n_nested_for[0],
                    self.norm_range_n_nested_for[1]
                )
            for call in calls:  # вызов всех функций в функции main
                function_body.append(Statement(FunctionCall(call.name)))
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
            prof_process = subprocess.run(['gprof', '-b', filename, 'gmon.out', '--graph=find_me'],
                                          capture_output=True,
                                          text=True)
        except Exception:
            raise OSError('Ошибка запуска утилиты gprof')
        table = prof_process.stdout.split('\n' + '-' * 47 + '\n')[:-1]
        if not table:
            raise OSError(
                'Ошибка получения данных о профилировании с помощью gprof.')
        # разделение строк таблицы по переносам строки
        table = [row.split('\n') for row in table]
        table[0] = table[0][6:]  # удаление заголовка и шапки таблицы
        row_with_called_functions = None
        for row in table:  # поиск строки таблицы с вызванными функциями из find_me
            # в строке таблицы приведены функции вызванные из find_me
            if 'find_me' in row[1]:
                row_with_called_functions = row
                break

        # разделение по столбцам таблицы
        row_with_called_functions = [line.split()
                                     for line in row_with_called_functions]
        # функции вызванные из find_me
        called_functions = row_with_called_functions[2:]
        # сортировка времени
        called_functions = sorted(
            called_functions, key=lambda function: float(function[0]), reverse=True)
        # имя функции выполняющейся дольше остальных
        expected_answer = called_functions[0][3]
        return expected_answer == answer
