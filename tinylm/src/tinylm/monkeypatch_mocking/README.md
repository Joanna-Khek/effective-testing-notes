# Monkeypatch and Mocking

## Mocking
`Mocking`: replacing real components with fake ones so you can isolate the code under test from external side effects or nondeterministic behaviour

### When should we use mocking?
Every mock we add is another hting that could break when we refactor

- **Network services (e.g HTTP APIs)**:  to avoid slow, flaky calls to simualte responses
- **Database or file system:** to avoid requiring real databases or files in unit tests
- **Environment variables and configurations:** to test different settings without affecting the real environment
- **Costly or stateful services:** sending emails, billing, payment etc


Pure computations should be tested directly with real input/outputs.

Questions to think about: 
- "Can the implementation change without breaking this test?

## Test Stubs
They are test coes that stand in for real components. If the real `.predict` method has bugs or changes, this test will not catch it.

```python
class StubWordMarkov(tinylm.WordMarkov):
    def predict(self, txt: str) -> str:
        # Bypass randomness with a fixed response
        return "world
```

```python
def test_wordmarkov_with_test_double():
    model = StubWordMarkov("hello world hello there")
    # This test doesn't care how the model predicts — just that we can use it
    response = model.predict("hello")
    
    assert response == "world"
```

A useful way to use it:

```python
def generate_headline(model: WordMarkov, seed: str) -> str:
    """Generates a headline from a seed word using the model."""
    try:
        word = model.predict(seed)
        return f"{seed.title()} {word.title()}!"
    except KeyError:
        return "Breaking News!"
```

```python
class StubWordMarkov(WordMarkov):
    def predict(self, txt: str) -> str:
        return "recession"

def test_generate_headline_success():
    model = StubWordMarkov("")
    result = generate_headline(model, "economic")
    assert result == "Economic Recession!"
```

## Monkeypatch
`Monkeypatch`: Lets you use a fake to replace functions, attributes, environment variables and more for the duration of a test.

Sometimes we want to test behaviour that depends on a method. In the example below, the `setattr` replaces the `predict` method with the `fake_predict` method.

```python
def generate_sentence(model: WordMarkov, prompt: str) -> str:
    """Returns a title-cased sentence from a prompt word."""
    try:
        return f"{prompt.title()} {model.predict(prompt).title()}."
    except KeyError:
        return "Could Not Generate."
```

```python
def test_generate_sentence_monkeypatched(monkeypatch):
    model = WordMarkov("irrelevant training text")
    
    def fake_predict(_):
        return "resurgence"
        
    monkeypatch.setattr(
        model, "predict", fake_predict
    )

    result = generate_sentence(model, "economic")
    assert result == "Economic Resurgence."
```
It allows you to replace just the part of a dependency you care about like a method or attribute—without needing to build an entire test stub class. This is helpful when you want to isolate a speci7c behavior, such as making a random function deterministic.

We can also rewrite the environment variable example with `monkeypatch.setenv`.
```python
def is_utf8_enabled() -> bool:
    """Check if UTF-8 mode is enabled via environment variable."""
    return os.getenv("CHARSET", "ASCII").upper() == "UTF8"
```

```python
def test_charset_utf8(monkeypatch):
    monkeypatch.setenv("CHARSET", "UTF8")
    assert is_utf8_enabled() # True when CHARSET=UTF8

def test_charset_ascii(monkeypatch):
    monkeypatch.delenv("CHARSET", raising=False) # simulate unset or default
    assert not is_utf8_enabled() # Defaults to ASCII
```

