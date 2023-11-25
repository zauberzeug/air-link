
from textfile import TextFile


def test_add_missing(tmp_path):
    test_file = TextFile(tmp_path / 'test.txt')
    test_file.path.write_text('line 1\nline 2\nline 3\n')
    test_file.add_missing(['line 2', 'line 4', 'line 5'])
    assert test_file.path.read_text() == 'line 1\nline 2\nline 3\nline 4\nline 5\n'

def test_touch(tmp_path):
    test_file = TextFile(tmp_path / 'subdir' / 'test.txt')
    test_file.touch()
    assert test_file.path.exists()
    assert test_file.path.parent.exists()
    assert test_file.path.is_file()
    assert not test_file.path.is_dir()

def test_update_lines(tmp_path):
    test_file = TextFile(tmp_path / 'test.txt')
    test_file.path.write_text('line 1 = one\nline 2 = two\n')
    test_file.update_lines({'line 1': 'line 1 = ONE', 'line 3': 'line 3 = THREE', 'two': 'line 2 = TWO'})
    assert test_file.path.read_text() == 'line 1 = ONE\nline 2 = TWO\nline 3 = THREE\n', 'should update existing lines and add missing lines at the end'
