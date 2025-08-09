class LanguageMeta(type):
    classes = []

    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        cls.classes.append(new_class)
        return new_class


class LanguageProcessor:
    LANGUAGES = [cls.LANGUAGE for cls in LanguageMeta.classes]
    CODES = [cls.CODE for cls in LanguageMeta.classes]

    @staticmethod
    def define_language(lang: str):
        for cls in [...]:
            if cls.CODE == lang:
                return cls


class BaseLanguage(...):
    pass
