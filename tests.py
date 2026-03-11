import pytest
from main import BooksCollector

class TestBooksCollector:
    """
    Тесты для класса BooksCollector
    """

    # Список допустимых жанров из условия
    @pytest.fixture
    def valid_genres(self):
        return ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']

    # ===== ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ =====
    @pytest.mark.parametrize('invalid_name', [
        '',                          # пустая строка (0 символов)
        'A' * 41,                    # 41 символ (больше максимального)
        'Очень длинное название книги, которое явно превышает сорок символов'
    ])
    def test_add_new_book_with_invalid_name_length(self, collector, invalid_name):
        """Проверка, что книга НЕ добавляется при недопустимой длине имени"""
        collector.add_new_book(invalid_name)
        assert invalid_name not in collector.get_books_genre()

    @pytest.mark.parametrize('valid_name', [
        'A',                          # 1 символ (минимум)
        'A' * 40,                     # 40 символов (максимум)
        'Нормальное название книги',  # средняя длина
        'Война и мир',                # конкретное название
        '1984',                        # название с цифрами
        'Книга!@#'                     # название со спецсимволами
    ])
    def test_add_new_book_with_valid_name_length(self, collector, valid_name):
        """Проверка, что книга добавляется при допустимой длине имени"""
        collector.add_new_book(valid_name)
        assert valid_name in collector.get_books_genre()

    def test_add_new_book_twice(self, collector):
        """Проверка, что нельзя добавить одну книгу дважды"""
        book_name = 'Уникальная книга'
        
        collector.add_new_book(book_name)
        initial_count = len(collector.get_books_genre())
        
        collector.add_new_book(book_name)
        final_count = len(collector.get_books_genre())
        
        assert final_count == initial_count == 1

    def test_set_book_genre(self, collector):
        """Проверка установки жанра для существующей книги"""
        book_name = 'Фантастическая книга'
        genre = 'Фантастика'
        
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        
        assert collector.get_book_genre(book_name) == genre

    def test_set_invalid_genre(self, collector, valid_genres):
        """Проверка, что нельзя установить несуществующий жанр"""
        book_name = 'Книга с неверным жанром'
        invalid_genre = 'Несуществующий жанр'
        
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, invalid_genre)
        
        # Проверяем, что жанр не изменился (остался пустым)
        assert collector.get_book_genre(book_name) == ''
        
        # Проверяем, что неверный жанр не в списке допустимых
        assert invalid_genre not in valid_genres

    def test_get_books_with_specific_genre(self, collector):
        """Проверка получения списка книг по конкретному жанру"""
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.add_new_book('Книга 3')
        
        collector.set_book_genre('Книга 1', 'Фантастика')
        collector.set_book_genre('Книга 2', 'Детектив')
        collector.set_book_genre('Книга 3', 'Фантастика')
        
        fantastic_books = collector.get_books_with_specific_genre('Фантастика')
        
        assert len(fantastic_books) == 2
        assert 'Книга 1' in fantastic_books
        assert 'Книга 3' in fantastic_books
        assert 'Книга 2' not in fantastic_books

    def test_get_books_genre_returns_dict(self, collector):
        """Проверка, что метод возвращает словарь"""
        result = collector.get_books_genre()
        assert isinstance(result, dict)

    def test_get_books_for_children(self, collector):
        """Проверка фильтрации книг для детей (без жанров Ужасы и Детективы)"""
        collector.add_new_book('Детская книга')
        collector.add_new_book('Страшная книга')
        collector.add_new_book('Мультфильм')
        
        collector.set_book_genre('Детская книга', 'Мультфильмы')
        collector.set_book_genre('Страшная книга', 'Ужасы')
        collector.set_book_genre('Мультфильм', 'Мультфильмы')
        
        children_books = collector.get_books_for_children()
        
        assert 'Детская книга' in children_books
        assert 'Мультфильм' in children_books
        assert 'Страшная книга' not in children_books

    def test_add_book_in_favorites(self, collector):
        """Проверка добавления книги в избранное"""
        book_name = 'Любимая книга'
        
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        
        favorites = collector.get_list_of_favorites_books()
        assert book_name in favorites
        assert len(favorites) == 1

    def test_add_nonexistent_book_to_favorites(self, collector):
        """Проверка, что нельзя добавить в избранное книгу, которой нет в коллекции"""
        book_name = 'Несуществующая книга'
        
        collector.add_book_in_favorites(book_name)
        
        favorites = collector.get_list_of_favorites_books()
        assert book_name not in favorites

    def test_add_same_book_to_favorites_twice(self, collector):
        """Проверка, что нельзя добавить одну книгу в избранное дважды"""
        book_name = 'Повторяющаяся книга'
        
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.add_book_in_favorites(book_name)
        
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 1

    def test_delete_book_from_favorites(self, collector):
        """Проверка удаления книги из избранного"""
        book_name = 'Книга для удаления'
        
        # Подготовка данных: добавляем книгу в коллекцию и в избранное
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        
        # Действие: удаляем из избранного
        collector.delete_book_from_favorites(book_name)
        
        # Проверка: книга должна отсутствовать в избранном
        assert book_name not in collector.get_list_of_favorites_books()

    def test_delete_nonexistent_book_from_favorites(self, collector):
        """Проверка удаления несуществующей книги из избранного"""
        initial_favorites = collector.get_list_of_favorites_books()
        
        collector.delete_book_from_favorites('Несуществующая книга')
        
        assert collector.get_list_of_favorites_books() == initial_favorites
        
