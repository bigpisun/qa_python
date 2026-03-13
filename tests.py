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

    # ===== ТЕСТЫ МЕТОДА add_new_book =====
    @pytest.mark.parametrize('invalid_name', [
        '',                          # пустая строка (0 символов)
        'A' * 41,                    # 41 символ (больше максимального)
        'Очень длинное название книги, которое явно превышает сорок символов'
    ])
    def test_add_new_book_with_invalid_name_length(self, collector, invalid_name):
        """Проверка, что книга НЕ добавляется при недопустимой длине имени"""
        collector.add_new_book(invalid_name)
        
        # Прямой доступ к словарю books_genre
        assert invalid_name not in collector.books_genre

    @pytest.mark.parametrize('valid_name', [
        'A',                          # 1 символ (минимум)
        'A' * 40,                     # 40 символов (максимум)
        'Нормальное название книги',
        'Война и мир',
        '1984',
        'Книга!@#'
    ])
    def test_add_new_book_with_valid_name_length(self, collector, valid_name):
        """Проверка, что книга добавляется при допустимой длине имени"""
        collector.add_new_book(valid_name)
        
        # Прямой доступ к словарю
        assert valid_name in collector.books_genre
        assert collector.books_genre[valid_name] == ''

    def test_add_new_book_twice(self, collector):
        """Проверка, что нельзя добавить одну книгу дважды"""
        book_name = 'Уникальная книга'
        
        collector.add_new_book(book_name)
        collector.add_new_book(book_name)
        
        # Проверяем через прямой доступ
        assert len(collector.books_genre) == 1
        assert book_name in collector.books_genre

    # ===== ТЕСТЫ МЕТОДА set_book_genre =====
    def test_set_book_genre(self, collector):
        """Проверка установки жанра для существующей книги"""
        book_name = 'Фантастическая книга'
        genre = 'Фантастика'
        
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        
        # Проверяем через прямой доступ к словарю, а не через get_book_genre
        assert collector.books_genre[book_name] == genre

    def test_set_book_genre_for_nonexistent_book(self, collector):
        """Проверка, что нельзя установить жанр для несуществующей книги"""
        book_name = 'Несуществующая книга'
        genre = 'Фантастика'
        
        # Сохраняем состояние до вызова
        initial_state = collector.books_genre.copy()
        
        collector.set_book_genre(book_name, genre)
        
        # Проверяем, что состояние не изменилось
        assert collector.books_genre == initial_state

    def test_set_invalid_genre(self, collector):
        """Проверка, что нельзя установить несуществующий жанр"""
        book_name = 'Книга с неверным жанром'
        invalid_genre = 'Несуществующий жанр'
        
        collector.add_new_book(book_name)
        
        # Запоминаем текущий жанр (пустой)
        current_genre = collector.books_genre[book_name]
        
        collector.set_book_genre(book_name, invalid_genre)
        
        # Проверяем, что жанр не изменился
        assert collector.books_genre[book_name] == current_genre

    # ===== ТЕСТЫ МЕТОДА get_book_genre =====
    def test_get_book_genre(self, collector):
        """Проверка получения жанра существующей книги"""
        book_name = 'Тестовая книга'
        genre = 'Детективы'
        
        # Прямое заполнение словаря
        collector.books_genre[book_name] = genre
        
        # Проверяем именно метод get_book_genre
        assert collector.get_book_genre(book_name) == genre

    def test_get_book_genre_for_nonexistent_book(self, collector):
        """Проверка получения жанра для несуществующей книги"""
        book_name = 'Несуществующая книга'
        
        result = collector.get_book_genre(book_name)
        
        # Метод должен вернуть None (по логике класса)
        assert result is None

    # ===== ТЕСТЫ МЕТОДА get_books_with_specific_genre =====
    def test_get_books_with_specific_genre(self, collector):
        """Проверка получения списка книг по конкретному жанру"""
        # Прямое заполнение словаря
        collector.books_genre = {
            'Книга 1': 'Фантастика',
            'Книга 2': 'Детективы',
            'Книга 3': 'Фантастика',
            'Книга 4': 'Ужасы'
        }
        
        fantastic_books = collector.get_books_with_specific_genre('Фантастика')
        
        # Проверяем результат одним ассертом (улучшение)
        assert fantastic_books == ['Книга 1', 'Книга 3']

    def test_get_books_with_specific_genre_empty_result(self, collector):
        """Проверка получения списка книг по жанру, которого нет"""
        collector.books_genre = {
            'Книга 1': 'Фантастика',
            'Книга 2': 'Детективы'
        }
        
        horror_books = collector.get_books_with_specific_genre('Ужасы')
        
        assert horror_books == []

    # ===== ТЕСТЫ МЕТОДА get_books_genre =====
    def test_get_books_genre_returns_correct_dict(self, collector):
        """Проверка, что метод возвращает правильный словарь книг с жанрами"""
        # Задаём тестовые данные
        test_data = {
            'Книга 1': 'Фантастика',
            'Книга 2': 'Детективы',
            'Книга 3': ''
        }
        collector.books_genre = test_data.copy()
        
        result = collector.get_books_genre()
        
        # Проверяем, что возвращается именно тот словарь, который мы задали
        assert result == test_data

    # ===== ТЕСТЫ МЕТОДА get_books_for_children =====
    def test_get_books_for_children(self, collector):
        """Проверка фильтрации книг для детей"""
        collector.books_genre = {
            'Детская книга': 'Мультфильмы',
            'Страшная книга': 'Ужасы',
            'Детектив': 'Детективы',
            'Фантастика': 'Фантастика',
            'Комедия': 'Комедии'
        }
        
        children_books = collector.get_books_for_children()
        
        # Проверяем одним ассертом
        expected_books = ['Детская книга', 'Фантастика', 'Комедия']
        assert sorted(children_books) == sorted(expected_books)

    # ===== ТЕСТЫ МЕТОДОВ ДЛЯ ИЗБРАННОГО =====
    def test_add_book_in_favorites(self, collector):
        """Проверка добавления книги в избранное"""
        book_name = 'Любимая книга'
        collector.add_new_book(book_name)
        
        collector.add_book_in_favorites(book_name)
        
        # Прямой доступ к списку favorites
        assert collector.favorites == [book_name]

    def test_add_nonexistent_book_to_favorites(self, collector):
        """Проверка, что нельзя добавить в избранное книгу, которой нет в коллекции"""
        book_name = 'Несуществующая книга'
        initial_favorites = collector.favorites.copy()
        
        collector.add_book_in_favorites(book_name)
        
        assert collector.favorites == initial_favorites

    def test_add_same_book_to_favorites_twice(self, collector):
        """Проверка, что нельзя добавить одну книгу в избранное дважды"""
        book_name = 'Повторяющаяся книга'
        collector.add_new_book(book_name)
        
        collector.add_book_in_favorites(book_name)
        collector.add_book_in_favorites(book_name)
        
        assert collector.favorites == [book_name]

    def test_delete_book_from_favorites(self, collector):
        """Проверка удаления книги из избранного"""
        book_name = 'Книга для удаления'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        
        # Проверяем, что книга в избранном
        assert book_name in collector.favorites
        
        collector.delete_book_from_favorites(book_name)
        
        assert book_name not in collector.favorites

    def test_delete_nonexistent_book_from_favorites(self, collector):
        """Проверка удаления несуществующей книги из избранного"""
        initial_favorites = collector.favorites.copy()
        
        collector.delete_book_from_favorites('Несуществующая книга')
        
        assert collector.favorites == initial_favorites

    # ===== ТЕСТЫ МЕТОДА get_list_of_favorites_books =====
    def test_get_list_of_favorites_books(self, collector):
        """Проверка получения списка избранных книг"""
        # Прямое заполнение списка избранного
        test_favorites = ['Книга 1', 'Книга 2']
        collector.favorites = test_favorites.copy()
        
        result = collector.get_list_of_favorites_books()
        
        # Проверяем, что метод возвращает правильный список
        assert result == test_favorites
        
