import pytest
from main import BooksCollector

# Импортируем фикстуру из conftest.py

class TestBooksCollector:
    """
    Тесты для класса BooksCollector
    """
    
    # ===== ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ (согласно замечанию ревьюера) =====
    
    @pytest.mark.parametrize('invalid_name', [
        '',                          # пустая строка (0 символов)
        'A' * 41,                    # 41 символ (больше максимального)
        'Очень длинное название книги, которое явно превышает сорок символов и должно быть слишком длинным для добавления'  # явно длинное
    ])
    def test_add_new_book_with_invalid_name_length(self, collector, invalid_name):
        """
        Проверка, что книга НЕ добавляется при недопустимой длине имени:
        - пустая строка (0 символов)
        - больше 40 символов
        """
        collector.add_new_book(invalid_name)
        assert invalid_name not in collector.get_books_genre(), \
            f"Книга с именем '{invalid_name}' не должна добавляться"
    
    @pytest.mark.parametrize('valid_name', [
        'A',                          # 1 символ (минимум)
        'A' * 40,                      # 40 символов (максимум)
        'Нормальное название книги',   # средняя длина
        'Война и мир',                 # конкретное название
        '1984',                        # название с цифрами
        'Книга!@#'                      # название со спецсимволами
    ])
    def test_add_new_book_with_valid_name_length(self, collector, valid_name):
        """
        Проверка, что книга добавляется при допустимой длине имени:
        - от 1 до 40 символов включительно
        """
        collector.add_new_book(valid_name)
        assert valid_name in collector.get_books_genre(), \
            f"Книга с именем '{valid_name}' должна добавляться"
    
    # ===== ОСТАЛЬНЫЕ ТЕСТЫ =====
    
    def test_add_new_book_twice(self, collector):
        """Проверка, что нельзя добавить одну книгу дважды"""
        book_name = 'Уникальная книга'
        
        # Добавляем первый раз
        collector.add_new_book(book_name)
        initial_count = len(collector.get_books_genre())
        
        # Пытаемся добавить второй раз
        collector.add_new_book(book_name)
        final_count = len(collector.get_books_genre())
        
        assert final_count == initial_count == 1, \
            "Количество книг не должно увеличиться при повторном добавлении"
    
    def test_set_book_genre(self, collector):
        """Проверка установки жанра для существующей книги"""
        book_name = 'Фантастическая книга'
        genre = 'Фантастика'
        
        # Добавляем книгу и устанавливаем жанр
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        
        # Проверяем, что жанр установился
        assert collector.get_book_genre(book_name) == genre, \
            f"Жанр книги должен быть '{genre}'"
    
    def test_set_invalid_genre(self, collector):
        """Проверка, что нельзя установить несуществующий жанр"""
        book_name = 'Книга с неверным жанром'
        invalid_genre = 'Несуществующий жанр'
        
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, invalid_genre)
        
        # Жанр не должен установиться (остается пустым)
        assert collector.get_book_genre(book_name) == '', \
            "Нельзя установить несуществующий жанр"
    
    def test_get_books_with_specific_genre(self, collector):
        """Проверка получения списка книг по конкретному жанру"""
        # Добавляем несколько книг
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.add_new_book('Книга 3')
        
        # Устанавливаем разные жанры
        collector.set_book_genre('Книга 1', 'Фантастика')
        collector.set_book_genre('Книга 2', 'Детектив')
        collector.set_book_genre('Книга 3', 'Фантастика')
        
        # Получаем книги жанра "Фантастика"
        fantastic_books = collector.get_books_with_specific_genre('Фантастика')
        
        # Проверяем результат
        assert len(fantastic_books) == 2, \
            "Должно быть 2 книги жанра Фантастика"
        assert 'Книга 1' in fantastic_books, \
            "Книга 1 должна быть в списке"
        assert 'Книга 3' in fantastic_books, \
            "Книга 3 должна быть в списке"
        assert 'Книга 2' not in fantastic_books, \
            "Книга 2 не должна быть в списке"
    
    def test_get_books_genre_returns_dict(self, collector):
        """Проверка, что метод возвращает словарь"""
        result = collector.get_books_genre()
        assert isinstance(result, dict), \
            "Метод должен возвращать словарь"
    
    def test_get_books_for_children(self, collector):
        """Проверка фильтрации книг для детей"""
        # Добавляем книги
        collector.add_new_book('Детская книга')
        collector.add_new_book('Страшная книга')
        collector.add_new_book('Мультфильм')
        
        # Устанавливаем жанры
        collector.set_book_genre('Детская книга', 'Мультфильмы')
        collector.set_book_genre('Страшная книга', 'Ужасы')
        collector.set_book_genre('Мультфильм', 'Мультфильмы')
        
        # Получаем книги для детей
        children_books = collector.get_books_for_children()
        
        # Проверяем результат
        assert 'Детская книга' in children_books, \
            "Мультфильмы должны подходить детям"
        assert 'Мультфильм' in children_books, \
            "Мультфильмы должны подходить детям"
        assert 'Страшная книга' not in children_books, \
            "Ужасы не должны подходить детям"
    
    def test_add_book_in_favorites(self, collector):
        """Проверка добавления книги в избранное"""
        book_name = 'Любимая книга'
        
        # Добавляем книгу в коллекцию и в избранное
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        
        # Проверяем, что книга в избранном
        favorites = collector.get_list_of_favorites_books()
        assert book_name in favorites, \
            f"Книга '{book_name}' должна быть в избранном"
        assert len(favorites) == 1, \
            "В избранном должна быть 1 книга"
    
    def test_add_nonexistent_book_to_favorites(self, collector):
        """Проверка, что нельзя добавить в избранное книгу, которой нет в коллекции"""
        book_name = 'Несуществующая книга'
        
        # Пытаемся добавить в избранное книгу, которой нет в коллекции
        collector.add_book_in_favorites(book_name)
        
        # Проверяем, что книга не добавилась
        favorites = collector.get_list_of_favorites_books()
        assert book_name not in favorites, \
            "Нельзя добавить в избранное книгу, которой нет в коллекции"
    
    def test_add_same_book_to_favorites_twice(self, collector):
        """Проверка, что нельзя добавить одну книгу в избранное дважды"""
        book_name = 'Повторяющаяся книга'
        
        # Добавляем книгу в коллекцию
        collector.add_new_book(book_name)
        
        # Добавляем в избранное дважды
        collector.add_book_in_favorites(book_name)
        collector.add_book_in_favorites(book_name)  # повторная попытка
        
        # Проверяем, что книга только одна в избранном
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 1, \
            "Книга не должна добавляться в избранное повторно"
    
    def test_delete_book_from_favorites(self, collector):
        """
        Проверка удаления книги из избранного
        """
        book_name = 'Книга для удаления'
        
        # Добавляем книгу в коллекцию и в избранное
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        
        # Проверяем, что книга в избранном
        assert book_name in collector.get_list_of_favorites_books(), \
            "Книга должна быть в избранном перед удалением"
        
        # Удаляем из избранного
        collector.delete_book_from_favorites(book_name)
        
        # Проверяем, что книги нет в избранном
        assert book_name not in collector.get_list_of_favorites_books(), \
            "Книга должна быть удалена из избранного"
    
    def test_delete_nonexistent_book_from_favorites(self, collector):
        """Проверка удаления несуществующей книги из избранного"""
        initial_favorites = collector.get_list_of_favorites_books()
        
        # Пытаемся удалить несуществующую книгу
        collector.delete_book_from_favorites('Несуществующая книга')
        
        # Проверяем, что список избранного не изменился
        assert collector.get_list_of_favorites_books() == initial_favorites, \
            "Список избранного не должен измениться при удалении несуществующей книги"
        