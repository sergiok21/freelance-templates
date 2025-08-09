class Generator:
    """Генератор даних"""
    total_length = random.randint(8, 12)

    def generate_nickname(self):
        """Генерує нікнейм заданої довжини."""
        with open('fake_names.txt', 'r') as f:
            nicknames = f.read().split('\n')[:-1]
            return random.choice(nicknames)

    def generate_password(self):
        lower, upper = string.ascii_lowercase, string.ascii_uppercase
        digits, symbols = string.digits, string.punctuation

        password = [
            random.choice(lower), random.choice(upper), random.choice(digits), random.choice(symbols)
        ]

        remaining_length = self.total_length - len(password)
        password += random.choices(lower + upper + digits + symbols, k=remaining_length)

        random.shuffle(password)

        return ''.join(password)
