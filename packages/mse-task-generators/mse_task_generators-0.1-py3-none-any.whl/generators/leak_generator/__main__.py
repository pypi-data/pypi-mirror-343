import argparse
from generators.leak_generator.leak_generator import LeaksGenerator

def main():
    parser = argparse.ArgumentParser(prog='Генератор задач')
    parser.add_argument('-m', '--mode',
                       help='Генерация задачи (1) или проверка (2)',
                       required=True,
                       choices=['1', '2'])
    parser.add_argument('-t', '--task',
                       help='Номер типа генерируемой задачи',
                       type=int,
                       default=3)  # Значение по умолчанию 3

    args = parser.parse_args()
    if args.task != 3:
        print('Пока единственный доступный тип задачи - 3')
        args.task = 3
    # Создаем генератор с указанным номером задачи
    generator = LeaksGenerator(args.task)

    if args.mode == "1":
        generator.create_task()
    elif args.mode == "2":
        generator.verify_task()



    