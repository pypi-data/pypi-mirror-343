import argparse
from generators.profiling1.finding_slow_function import TaskFindingSlowFunctionGenerator
from generators.profiling1.finding_slow_function_in_function import TaskFindingSlowFuncInFuncGenerator
import time


def get_args():
    parser = argparse.ArgumentParser(
        description="""
        Генерация исходного кода программы для задачи на профилирование
        """)

    task_subparsers = parser.add_subparsers(dest='task', required=True)

    task1_parser = task_subparsers.add_parser('finding_in_main')
    task1_mode_subparsers = task1_parser.add_subparsers(dest='mode', required=True)
    task1_init_parser = task1_mode_subparsers.add_parser('init')
    task1_check_parser = task1_mode_subparsers.add_parser('check')

    task2_parser = task_subparsers.add_parser('finding_in_find_me')
    task2_mode_subparsers = task2_parser.add_subparsers(dest='mode', required=True)
    task2_init_parser = task2_mode_subparsers.add_parser('init')
    task2_check_parser = task2_mode_subparsers.add_parser('check')

    for check_parser in [task1_check_parser, task2_check_parser]:
        check_parser.add_argument("--filename", "-b",
                                        type=str, default="a.out",
                                        help="имя бинарного файла")
        check_parser.add_argument("--answer", "-a",
                                        type=str, default="",
                                        help="ответ")

    for init_parser in [task1_init_parser, task2_init_parser]:
        init_parser.add_argument("--random_seed", "-s",
                            type=str, default=time.time(),
                            help="целое число, которое используется в качестве начального значения для генерации случайных чисел")
        init_parser.add_argument("--norm_depth_for",  "-d",
                            type=str, default='2,3',
                            help='диапазон глубины вложенности циклов нормальной функции - "<min>,<max>"')
        init_parser.add_argument("--deviant_depth_for",  "-D",
                            type=str, default='3,4',
                            help='диапазон глубины вложенности циклов отличающейся функции - "<min>,<max>"')
        init_parser.add_argument("--norm_n_nested_for",  "-n",
                            type=str, default='2,3',
                            help='диапазон числа вложенных циклов нормальной функции - "<min>,<max>"')
        init_parser.add_argument("--deviant_n_nested_for",  "-N",
                            type=str, default='3,4',
                            help='диапазон числа вложенных циклов отличающейся функции - "<min>,<max>"')
        init_parser.add_argument("--range_n_iterations_for", "-I",
                                 type=str, default='40,50',
                                 help='диапазон числа итераций цикла for - "<min>,<max>"')
        init_parser.add_argument("--output", "-o",
                            type=str, default="a.out",
                            help="имя выходного файла")

    task1_init_parser.add_argument("--number_funcrions", "-f",
                             type=int, default=10,
                             help="число генерируемых функций")

    task2_init_parser.add_argument("--range_nested_fcalls", "-c",
                             type=str, default='2,3',
                             help='диапазон числа вложенных вызовов функций - "<min>,<max>"')
    task2_init_parser.add_argument("--range_depth_fcalls", "-C",
                             type=str, default='3,4',
                             help='диапазон глубины вызовов функций - "<min>,<max>"')
    task2_init_parser.add_argument("--range_depth_f_find_me", "-m",
                             type=str, default='1,2',
                             help='диапазон глубины вызовов, на которой находится функция, в которой нужно найти медленную - "<min>,<max>"')

    return parser.parse_args()


def main():
    args = get_args()
    try:
        match args.task:
            case "finding_in_main":
                match args.mode:
                    case "init":
                        generator = TaskFindingSlowFunctionGenerator(
                            args.number_funcrions,
                            tuple(map(int, args.norm_depth_for.split(","))),
                            tuple(map(int, args.norm_n_nested_for.split(","))),
                            tuple(map(int, args.deviant_depth_for.split(","))),
                            tuple(map(int, args.deviant_n_nested_for.split(","))),
                            tuple(map(int, args.range_n_iterations_for.split(","))),
                        )
                        generator.create_task(args.random_seed, args.output)
                        print(f'Бинарик успешно сгенерирован, он доступен по пути {args.output}')
                    case "check":
                        generator = TaskFindingSlowFunctionGenerator()
                        print(generator.verify_task(args.filename, args.answer))

            case "finding_in_find_me":
                match args.mode:
                    case "init":
                        generator = TaskFindingSlowFuncInFuncGenerator(
                            tuple(map(int, args.norm_depth_for.split(","))),
                            tuple(map(int, args.norm_n_nested_for.split(","))),
                            tuple(map(int, args.deviant_depth_for.split(","))),
                            tuple(map(int, args.deviant_n_nested_for.split(","))),
                            tuple(map(int, args.range_nested_fcalls.split(","))),
                            tuple(map(int, args.range_depth_fcalls.split(","))),
                            tuple(map(int, args.range_depth_f_find_me.split(","))),
                            tuple(map(int, args.range_n_iterations_for.split(","))),
                        )
                        generator.create_task(args.random_seed, args.output)
                        print(f'Бинарик успешно сгенерирован, он доступен по пути {args.output}')
                    case "check":
                        generator = TaskFindingSlowFuncInFuncGenerator()
                        print(generator.verify_task(args.filename, args.answer))

    except Exception as e:
        print(e)
        exit(-1)
