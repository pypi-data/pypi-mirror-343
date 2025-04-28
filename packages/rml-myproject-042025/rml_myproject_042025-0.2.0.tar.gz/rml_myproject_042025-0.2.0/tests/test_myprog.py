from myproject.myprog import hello

def test_simple_input():
    assert hello('Reuven') == 'Hello, Reuven!'

def test_empty_input():
    assert hello('') == 'Hello, !'

def test_int_input():
    assert hello(5) == 'Hello, 5!'
