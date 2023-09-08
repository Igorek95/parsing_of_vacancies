from abc import ABC, abstractmethod


class Saver(ABC):
    """
    Абстрактный класс для сохранения и загрузки данных.
    """

    @abstractmethod
    def save_to_file(self):
        """
        Абстрактный метод для сохранения данных в файл.
        """
        pass

    @abstractmethod
    def load_from_file(self):
        """
        Абстрактный метод для загрузки данных из файла.
        """
        pass

    @abstractmethod
    def delete_vacancy(self):
        """
        Абстрактный метод для удаления данных.
        """
        pass
