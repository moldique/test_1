import pytest

from src.decorators import log  # Явный импорт


def test_console_logging(capsys: pytest.CaptureFixture) -> None:
    """Тестирует вывод логов в консоль."""
    @log()
    def test_func(x: int) -> int:
        return x * 2

    result = test_func(5)
    assert result == 10
    captured = capsys.readouterr()
    assert "test_func ok" in captured.out


def test_error_logging(capsys: pytest.CaptureFixture) -> None:
    """Тестирует логирование ошибок."""
    @log()
    def test_func(x: int) -> None:
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        test_func(5)

    captured = capsys.readouterr()
    assert "test_func error" in captured.out
