# Scriptor

Scriptor to niewielka biblioteka Pythona do definiowania i uruchamiania prostych skryptów opartych na regułach. Skrypt to ciąg reguł warunkowych, które po spełnieniu warunku wykonują jedną lub kilka akcji. Lekka i przydatna do szybkiego prototypowania.

> Bezpieczeństwo: Scriptor używa eval() i exec(). Nie uruchamiaj nieznanych/skontrolowanych skryptów.

## Funkcje
- Kompaktowy format reguł (warunek -> akcje).
- Wstrzykiwanie zmiennych do środowiska wykonawczego skryptu.
- Opcjonalny import modułów przez prefiks w skrypcie.
- Minimalne środowisko IDE (scriptorIDE.py) do edycji i uruchamiania skryptów.

## Instalacja
Sklonuj repozytorium i (opcjonalnie) zainstaluj w trybie editable:

```bash
git clone https://github.com/libmaster169/py-scriptor.git
cd py-scriptor
pip install -e .
```

Lub dodaj folder z repozytorium do PYTHONPATH.

## Format skryptu
Skrypt to pojedynczy łańcuch reguł rozdzielonych średnikami (`;`). Każda reguła używa `>>>` do oddzielenia warunku od akcji. Kilka akcji rozdziela się przecinkami.

Opcjonalne importy: poprzedź skrypt nazwami modułów rozdzielonymi `::`, a następnie samą treścią skryptu.

Format:
module1::module2::...::warunek >>> akcja1, akcja2; warunek2 >>> akcja3

- warunek: wyrażenie Pythona oceniane z użyciem dostarczonych zmiennych (eval).
- akcja: instrukcja Pythona wykonywana z użyciem dostarczonych zmiennych (exec).

Przykłady:
- `x > 0 >>> x -= 1`
- `math::x > 0 >>> print(math.sqrt(x)), x -= 1`

## API

Klasa: RuleScript (w pliku py_scriptor/__init__.py)

- RuleScript(script: str, vars: dict)
  - script: łańcuch skryptu. Aby zaimportować moduły, użyj prefiksu "module::...::script_body".
  - vars: słownik zmiennych dostępnych dla warunków i akcji. Zaimportowane moduły są dodawane do tego słownika pod nazwą modułu.

- setVar(var: str, value)
  - Ustawia zmienną w słowniku runtime.

- getVar(var: str) -> Any
  - Pobiera zmienną ze słownika runtime.

- run(max_steps: int = 1000, cps: int = 0) -> bool
  - Wykonuje reguły przez maksymalnie max_steps iteracji. Zwraca True przy poprawnym zakończeniu, False przy błędach importu lub wykonania.
  - Uwaga: parametr cps nie jest obecnie używany.

- getImports() -> str
  - Zwraca tekst linii importujących zaimportowane moduły (np. `import math`).

## Przykłady użycia

Podstawowy przykład:

```python
from scriptor import RuleScript

script = "x > 0 >>> print(x), x -= 1; x == 0 >>> print('gotowe')"
vars = {"x": 3}

rs = RuleScript(script, vars)
rs.run(max_steps=10)
```

Z importem modułu:

```python
script = "math::x > 0 >>> print(math.sqrt(x)), x -= 1"
vars = {"x": 4}
rs = RuleScript(script, vars)
rs.run(max_steps=10)
```

Uruchamianie IDE (scriptorIDE.py):

```bash
python scriptorIDE.py
```

## Bezpieczeństwo
Scriptor wykonuje kod Pythona przy pomocy eval/exec. Nie uruchamiaj skryptów z nieznanych źródeł. Dla bezpieczniejszego uruchamiania rozważ:
- Uruchamianie w odizolowanym procesie/kontejnerze.
- Parsowanie AST i ograniczanie dozwolonych operacji.
- Ograniczenie dostępnych globali.

## Wkład (Contributing)
Wkład mile widziany. Sugestie:
- Ulepszyć parser (wielolinijkowe skrypty, komentarze).
- Dodać bezpieczny tryb wykonania (ograniczone globalne/AST).
- Dodać testy jednostkowe i CI.

Przed większymi zmianami otwórz issue, potem zgłoś pull request z testami.

## Licencja
Plik LICENSE zawiera licencję MIT.

## Issues / Kontakt
Zgłaszaj błędy lub prośby o funkcje na: https://github.com/libmaster169/py-scriptor/issues