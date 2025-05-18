import pytest

from src.decorators import log


def test_console_logging(capsys):
    @log()
    def test_func(x):
        return x * 2

    assert test_func(5) == 10
    captured = capsys.readouterr()
    assert "test_func ok" in captured.out


def test_error_logging(capsys):
    @log()
    def test_func(x):
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        test_func(5)

    captured = capsys.readouterr()
    assert "test_func error" in captured.out
