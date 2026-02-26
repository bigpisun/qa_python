import pytest
from main import BooksCollector

class TestBooksCollector:
    
    def test_add_new_book_add_two_books(self):
        # Создаем экземпляр класса BooksCollector
        collector = BooksCollector()
        
        # Добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        
        # Проверяем, что добавилось именно две книги
        assert len(collector.get_books_genre()) == 2
    
    def test_add_new_book_with_valid_name(self):
        collector = BooksCollector()
        book_name = 'Нормальная книга'
        collector.add_new_book(book_name)
        assert book_name in collector.get_books_genre()
    
    def test_add_new_book_with_long_name(self):
        collector = BooksCollector()
        long_name = 'О' * 41  # 41 символ
        collector.add_new_book(long_name)
        assert long_name not in collector.get_books_genre()
    
    def test_set_book_genre(self):
        collector = BooksCollector()
        book_name = 'Война и мир'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, 'Детективы')
        assert collector.get_book_genre(book_name) == 'Детективы'
    
    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.set_book_genre('Книга 1', 'Ужасы')
        collector.set_book_genre('Книга 2', 'Комедии')
        books = collector.get_books_with_specific_genre('Ужасы')
        assert books == ['Книга 1']
    
    def test_get_books_for_children(self):
        collector = BooksCollector()
        collector.add_new_book('Детская книга')
        collector.add_new_book('Страшная книга')
        collector.set_book_genre('Детская книга', 'Мультфильмы')
        collector.set_book_genre('Страшная книга', 'Ужасы')
        children_books = collector.get_books_for_children()
        assert 'Страшная книга' not in children_books
        assert 'Детская книга' in children_books
    
    def test_add_book_in_favorites(self):
        collector = BooksCollector()
        book_name = 'Любимая книга'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.get_list_of_favorites_books()
    
    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        book_name = 'Любимая книга'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        assert book_name not in collector.get_list_of_favorites_books()