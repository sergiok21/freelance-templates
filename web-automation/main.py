class Main(Processor):
    def run_process(self):
        params = self._check_config()

        data, proxy_file = self._check_proxy_file()
        self._check_threads(data=data, proxy_file=proxy_file, params=params)
        input('\nНатисніть ENTER для завершення роботи.')

    def _check_balances(self):
        """
        Перевірка введення на продовження виконання програми після отримання інформації про баланс.
        """
        answer = str(input('Почати виконання [Y/N]: '))
        if answer.lower() == 'n':
            sys.exit(0)
        elif answer.lower() != 'y' and answer.lower() != 'n':
            print('Невірна відповідь.')
            return self._check_balances()

    def _check_proxy_file(self):
        """
        Перевірка наявності проксі-файлу.
        """
        try:
            # proxy_file = str(input('\nНазва проксі-файлу: '))
            proxy_file = 'ip.txt'
            file_processor = FileProcessor()
            data = file_processor.get_data(file=proxy_file)
            return data, proxy_file
        except FileNotFoundError:
            print('Проксі-файл не знайдено (ip.txt).')
            return self._check_proxy_file()

    def _check_threads(self, data: list, proxy_file: str, params: dict):
        """
        Перевірка введення потоків.

        :param data: Повний список проксі отриманих із файлу (type: list).
        :param proxy_file: Шлях до проксі-файлу (type: str).
        :param params: Дані з конфігураційного файлу (type: dict)
        :type data: list
        :type proxy_file: str
        :type params: dict
        """
        try:
            thread_count = int(input('Кількість потоків: '))
            if thread_count > len(data):
                sys.exit(0)
            ThreadProcessor(count=thread_count, data=data, params=params).run_process()
        except ValueError:
            print('Помилка у визначенні потоків.')
            return self._check_threads(data=data, proxy_file=proxy_file, params=params)

    def _check_config(self):
        config = Config()
        if not os.path.exists('config.txt'):
            config.create_config()
            print('Створено конфігураційний файл. Після його редагування - запустіть програму.')
            input('\nНатисніть ENTER для завершення роботи.')
            sys.exit(0)
        return config.get_params()


if __name__ == '__main__':
    Main().run_process()
