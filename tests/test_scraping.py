import pytest
import fileinput
from script import scraping

def test_scraping_with_default_params(monkeypatch):
    monkeypatch.setattr('sys.argv', ['scraping.py'])

    result = scraping.main()
    assert result

    total_lines = sum(1 for _ in fileinput.input('/app/posts.csv'))
    assert total_lines > 1 and total_lines <= 11

def test_scraping_with_all_pages(monkeypatch):
    monkeypatch.setattr('sys.argv', ['scraping.py', '--all-pages'])
    
    result = scraping.main()
    assert result

    total_lines = sum(1 for _ in fileinput.input('/app/posts.csv'))
    assert total_lines > 91

def test_scraping_with_specific_page(monkeypatch):
    monkeypatch.setattr('sys.argv', ['scraping.py', '--initial-page=2', '--last-page=3'])
    
    result = scraping.main()
    assert result

    total_lines = sum(1 for _ in fileinput.input('/app/posts.csv'))
    assert total_lines > 10 and total_lines <= 21

def test_scraping_with_all_params(monkeypatch):
    monkeypatch.setattr('sys.argv', ['scraping.py', '--initial-page=1', '--last-page=3', '--all-pages'])
    
    result = scraping.main()
    assert result

    total_lines = sum(1 for _ in fileinput.input('/app/posts.csv'))
    assert total_lines > 91
