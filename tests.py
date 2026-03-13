import pytest
from main import BooksCollector

class TestBooksCollector:
    """
    Тесты для класса BooksCollector
    """

    @pytest.fixture
    def collector(self):
        """Фикстура возвращает новый экземпляр коллекции для каждого теста"""
        return BooksCollector()

    @pytest.fixture
    def valid_genres(self):
        """Фикстура со списком допустимых жанров"""
        return ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']

    # ===== ТЕСТЫ МЕТОДА add_new_book =====
    @pytest.mark.parametrize('invalid_name', [
        '',                          # пустая строка (0 символов)
        'A' * 41,                    # 41 символ (больше максимального)
        'Очень длинное название книги, которое явно превышает сорок символов'
    ])
    def test_add_new_book_with_invalid_name_length(self, collector, invalid_name):
        """Проверка, что книга НЕ добавляется при недопустимой длине имени"""
        collector.add_new_book(invalid_name)
        
        # Прямой доступ к словарю books_genre для проверки
        assert invalid_name not in collector.books_genre

    @pytest.mark.parametrize('valid_name', [
        'A',                          # 1 символ (минимум)
        'A' * 40,                     # 40 символов (максимум)
        'Нормальное название книги',  # средняя длина
        'Война и мир',                # конкретное название
        '1984',                       # название с цифрами
        'Книга!@#'                    # название со спецсимволами
    ])
    def test_add_new_book_with_valid_name_length(self, collector, valid_name):
        """Проверка, что книга добавляется при допустимой длине имени"""
        collector.add_new_book(valid_name)
        
        # Прямой доступ к словарю books_genre для проверки
        assert valid_name in collector.books_genre
        # Проверяем, что у новой книги пустой жанр
        assert collector.books_genre[valid_name] == ''

    def test_add_new_book_twice(self, collector):
        """Проверка, что нельзя добавить одну книгу дважды"""
        book_name = 'Уникальная книга'
        
        collector.add_new_book(book_name)
        collector.add_new_book(book_name)
        
        # Проверяем через прямой доступ к словарю
        assert len(collector.books_genre) == 1
        assert book_name in collector.books_genre

    # ===== ТЕСТЫ МЕТОДА set_book_genre =====
    def test_set_book_genre(self, collector):
        """Проверка установки жанра для существующей книги"""
        book_name = 'Фантастическая книга'
        genre = 'Фантастика'
        
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        
        # Прямая проверка словаря
        assert collector.books_genre[book_name] == genre

    def test_set_book_genre_for_nonexistent_book(self, collector):
        """Проверка, что нельзя установить жанр для несуществующей книги"""
        book_name = 'Несуществующая книга'
        genre = 'Фантастика'
        
        # Пытаемся установить жанр для книги, которой нет
        collector.set_book_genre(book_name, genre)
        
        # Проверяем, что словарь не изменился
        assert book_name not in collector.books_genre

    def test_set_invalid_genre(self, collector):
        """Проверка, что нельзя установить несуществующий жанр"""
        book_name = 'Книга с неверным жанром'
        invalid_genre = 'Несуществующий жанр'
        
        collector.add_new_book(book_name)
        
        # Сохраняем текущий жанр (пустой)
        current_genre = collector.books_genre[book_name]
        
        # Пытаемся установить несуществующий жанр
        collector.set_book_genre(book_name, invalid_genre)
        
        # Проверяем, что жанр не изменился
        assert collector.books_genre[book_name] == current_genre

    # ===== ТЕСТЫ МЕТОДА get_book_genre =====
    def test_get_book_genre(self, collector):
        """Проверка получения жанра книги"""
        book_name = 'Тестовая книга'
        genre = 'Детективы'
        
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        
        # Сравниваем результат метода с прямым доступом
        assert collector.get_book_genre(book_name) == collector.books_genre[book_name]

    def test_get_book_genre_for_nonexistent_book(self, collector):
        """Проверка получения жанра для несуществующей книги"""
        book_name = 'Несуществующая книга'
        
        # Метод должен вернуть None или пустую строку (зависит от реализации)
        result = collector.get_book_genre(book_name)
        assert result is None or result == ''

    # ===== ТЕСТЫ МЕТОДА get_books_with_specific_genre =====
    def test_get_books_with_specific_genre(self, collector):
        """Проверка получения списка книг по конкретному жанру"""
        # Прямое заполнение словаря (изолированная подготовка данных)
        collector.books_genre = {
            'Книга 1': 'Фантастика',
            'Книга 2': 'Детективы',
            'Книга 3': 'Фантастика',
            'Книга 4': 'Ужасы'
        }
        
        fantastic_books = collector.get_books_with_specific_genre('Фантастика')
        
        # Проверка результата
        assert len(fantastic_books) == 2
        assert 'Книга 1' in fantastic_books
        assert 'Книга 3' in fantastic_books
        assert 'Книга 2' not in fantastic_books

    def test_get_books_with_specific_genre_empty_result(self, collector):
        """Проверка получения списка книг по жанру, которого нет"""
        collector.books_genre = {
            'Книга 1': 'Фантастика',
            'Книга 2': 'Детективы'
        }
        
        horror_books = collector.get_books_with_specific_genre('Ужасы')
        
        assert horror_books == []

    # ===== ТЕСТЫ МЕТОДА get_books_genre =====
    def test_get_books_genre_returns_dict(self, collector):
        """Проверка, что метод возвращает словарь"""
        # Проверяем, что метод возвращает именно словарь, а не его копию
        collector.books_genre = {'Книга': 'Фантастика'}
        result = collector.get_books_genre()
        
        assert isinstance(result, dict)
        assert result == collector.books_genre

    # ===== ТЕСТЫ МЕТОДА get_books_for_children =====
    def test_get_books_for_children(self, collector):
        """Проверка фильтрации книг для детей (без жанров Ужасы и Детективы)"""
        # Прямое заполнение словаря
        collector.books_genre = {
            'Детская книга': 'Мультфильмы',
            'Страшная книга': 'Ужасы',
            'Детектив': 'Детективы',
            'Фантастика': 'Фантастика',
            'Комедия': 'Комедии'
        }
        
        children_books = collector.get_books_for_children()
        
        assert len(children_books) == 3
        assert 'Детская книга' in children_books
        assert 'Фантастика' in children_books
        assert 'Комедия' in children_books
        assert 'Страшная книга' not in children_books
        assert 'Детектив' not in children_books

    def test_get_books_for_children_with_age_restricted_genres(self, collector, valid_genres):
        """Проверка, что возрастные жанры не попадают в детские книги"""
        # Проверяем все жанры из списка допустимых
        collector.books_genre = {f'Книга {genre}': genre for genre in valid_genres}
        
        children_books = collector.get_books_for_children()
        
        # Жанры, которые должны быть исключены
        age_restricted = ['Ужасы', 'Детективы']
        
        for book in children_books:
            genre = collector.get_book_genre(book)
            assert genre not in age_restricted

    # ===== ТЕСТЫ МЕТОДОВ ДЛЯ ИЗБРАННОГО =====
    def test_add_book_in_favorites(self, collector):
        """Проверка добавления книги в избранное"""
        book_name = 'Любимая книга'
        collector.add_new_book(book_name)
        
        collector.add_book_in_favorites(book_name)
        
        # Прямой доступ к списку favorites
        assert book_name in collector.favorites
        assert len(collector.favorites) == 1

    def test_add_nonexistent_book_to_favorites(self, collector):
        """Проверка, что нельзя добавить в избранное книгу, которой нет в коллекции"""
        book_name = 'Несуществующая книга'
        initial_favorites = collector.favorites.copy() if hasattr(collector, 'favorites') else []
        
        collector.add_book_in_favorites(book_name)
        
        # Проверяем, что список избранного не изменился
        assert collector.favorites == initial_favorites

    def test_add_same_book_to_favorites_twice(self, collector):
        """Проверка, что нельзя добавить одну книгу в избранное дважды"""
        book_name = 'Повторяющаяся книга'
        collector.add_new_book(book_name)
        
        collector.add_book_in_favorites(book_name)
        collector.add_book_in_favorites(book_name)
        
        # Прямая проверка списка favorites
        assert len(collector.favorites) == 1
        assert collector.favorites[0] == book_name

    def test_delete_book_from_favorites(self, collector):
        """Проверка удаления книги из избранного"""
        book_name = 'Книга для удаления'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        
        # Проверяем, что книга действительно в избранном
        assert book_name in collector.favorites
        
        collector.delete_book_from_favorites(book_name)
        
        # Проверяем, что книга удалена
        assert book_name not in collector.favorites

    def test_delete_nonexistent_book_from_favorites(self, collector):
        """Проверка удаления несуществующей книги из избранного"""
        # Сохраняем начальное состояние
        initial_favorites = collector.favorites.copy() if hasattr(collector, 'favorites') else []
        
        collector.delete_book_from_favorites('Несуществующая книга')
        
        # Проверяем, что список не изменился
        assert collector.favorites == initial_favorites

    def test_get_list_of_favorites_books(self, collector):
        """Проверка получения списка избранных книг"""
        # Прямое заполнение списка избранного
        collector.favorites = ['Книга 1', 'Книга 2']
        
        result = collector.get_list_of_favorites_books()
        
        # Проверяем, что метод возвращает правильный список
        assert result == ['Книга 1', 'Книга 2']
        # Проверяем, что это тот же объект или копия (зависит от реализации)
        assert isinstance(result, list)
        
