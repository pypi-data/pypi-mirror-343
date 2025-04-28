
# markdown2app [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:plain-mark/markdown2app/edit/main/docs/README.md)
markdown2app.plainmark.com

# Plainmark

Plainmark is a lightweight programming language embedded in Markdown that runs across multiple platforms including web browsers, terminal environments, desktop applications, and mobile devices.

## What is Plainmark?

Plainmark allows you to write both documentation and executable code in the same Markdown file. Code blocks tagged with ```plainmark are interpreted and executed by the Plainmark runtime.

## Key Features

- **Write Once, Run Anywhere**: The same Plainmark code works across all supported platforms
- **Embedded in Markdown**: Combine documentation and executable code in a single file
- **Platform-Specific APIs**: Access platform capabilities like file system, device sensors, etc.
- **Interactive Documents**: Create dynamic, interactive documentation
- **Easy to Learn**: Familiar JavaScript-like syntax

## Platform Implementation Guide

### Browser Implementation

The browser implementation uses JavaScript to interpret and execute Plainmark code. It consists of:

1. An HTML file that provides the editor interface
2. A JavaScript interpreter that extracts code blocks and executes them
3. DOM manipulation capabilities for UI rendering

**Running in Browser:**
1. Open `index.html` in any modern browser
2. Write your Plainmark code in the editor
3. Click "Run" to execute

 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:plain-mark/markdown2app/edit/main/docs/INSTALL.md)
### Terminal/Python Implementation

The Python implementation allows running Plainmark in any terminal environment. It consists of:

1. A Python script (`plainmark.py`) that processes Markdown files
2. A code extractor and interpreter for Plainmark code blocks
3. Python-based API for file system access and terminal commands

**Running in Terminal:**
```bash
# Execute a file
python plainmark.py example.md

# Start REPL mode
python plainmark.py --repl

# Create an example file
python plainmark.py --example
```

### Desktop Implementation (Electron)

The desktop implementation provides a native application experience using Electron. It consists of:

1. A main process (`main.js`) that handles application lifecycle
2. A renderer process (`index.html`) with the editor UI
3. IPC communication for file operations
4. Full system access through Node.js APIs

**Building for Desktop:**
```bash
# Install dependencies
npm install

# Run in development mode
npm start

# Build for distribution
npm run build
```

### Mobile Implementation (Android)

The Android implementation runs Plainmark on mobile devices. It consists of:

1. A Kotlin-based Android app
2. A WebView for executing Plainmark code
3. JavaScript interfaces for accessing device features (camera, sensors, etc.)
4. Integration with the Android filesystem

**Building for Android:**
1. Open the project in Android Studio
2. Connect an Android device or start an emulator
3. Build and run the app

## Plainmark Syntax Examples

### Basic Syntax

```markdown
# My Plainmark Program

This is a simple program.

```plainmark
// Variables
let name = "World";
let number = 42;

// Output
print("Hello, " + name + "!");
print("The answer is: " + number);
```



## Web

```bash      
cd web
```


1. **Użyj portu powyżej 1024** (najlepiej powyżej 8000):
   ```bash
   python -m http.server 8080
   ```

2. **Używaj poprawnej składni** - port podaje się bezpośrednio jako pierwszy argument:
   ```bash
   python -m http.server 8888
   ```

3. **Jeśli port jest zajęty**, możesz:
   - Użyć innego portu (np. 8001, 8080, 9000)
   - Zakończyć proces używający danego portu:
     ```bash
     # Znajdź proces używający portu 8000
     sudo lsof -i :8000
     # albo
     netstat -tuln | grep 8000
     
     # Zakończ proces (zastąp PID numerem procesu)
     kill PID
     ```

Spróbuj wykonać:
```bash
python -m http.server 8888
```

A następnie otwórz w przeglądarce adres:
```
http://localhost:8888
```

Jeśli nadal masz problemy z uruchomieniem serwera HTTP, możesz także wypróbować inne rozwiązania:

1. **Użyj innego serwera HTTP**, np. Node.js:
   ```bash
   npx serve
   ```

2. **Użyj PHP (jeśli zainstalowane)**:
   ```bash
   php -S localhost:8888
   ```

3. **Sprawdź, czy masz uprawnienia do zapisu w katalogu**, w którym próbujesz uruchomić serwer.



### Aplikacja desktopowa

Instalacja aplikacji desktopowej (bazującej na Electron):

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/plain-mark/markdown2app.git
   cd markdown2app/desktop
   ```

2. Zainstaluj zależności:
   ```bash
   npm install
   ```

3. Uruchom aplikację:
   ```bash
   npm start
   ```

4. (Opcjonalnie) Zbuduj aplikację dla swojego systemu:
   ```bash
   npm run build
   ```

### Urządzenia mobilne (Android)

Aby zainstalować Plainmark na urządzeniu Android:

1. Pobierz plik APK z repozytorium lub sklepu Google Play
2. Uruchom plik APK na swoim urządzeniu
3. Zaakceptuj wymagane uprawnienia (dostęp do plików, kamera, itp.)
4. Aplikacja jest gotowa do użycia!

Alternatywnie, możesz zbudować aplikację z kodu źródłowego:

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/plain-mark/markdown2app.git
   ```

2. Otwórz folder `android` w Android Studio
3. Zbuduj i uruchom aplikację na emulatorze lub fizycznym urządzeniu

## Pierwsze kroki

Po zainstalowaniu Plainmark, czas na pierwszy program:

1. Utwórz nowy plik tekstowy o rozszerzeniu `.md` (np. `pierwszy.md`)
2. Wpisz następującą treść:

 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:plain-mark/markdown2app/edit/main/web/examples/basic.md)
# Podstawowy przykład Plainmark

W tym przykładzie pokazujemy podstawowe elementy języka Plainmark, takie jak zmienne, tablice, obiekty i pętle.

```js plainmark
// Zmienne
let name = "Świat";
let number = 42;

// Wypisanie
print("Witaj, " + name + "!");
print("Odpowiedź to: " + number);

// Tablica (array)
let fruits = ["Jabłko", "Banan", "Pomarańcza"];
print("Pierwszy owoc: " + fruits[0]);

// Obiekt
let person = {
  name: "Jan",
  age: 30,
  city: "Warszawa"
};
print("Osoba: " + JSON.stringify(person));

// Pętla
print("Liczenie do 5:");
for (let i = 1; i <= 5; i++) {
  print("Liczba: " + i);
}
```

## Wyjaśnienie kodu

1. **Zmienne** - definiowane za pomocą słowa kluczowego `let`
2. **Tablice** - kolekcje wartości w nawiasach kwadratowych
3. **Obiekty** - kolekcje par klucz-wartość w nawiasach klamrowych
4. **Pętle** - konstrukcja `for` do powtarzania operacji

Możesz modyfikować kod i eksperymentować z różnymi typami danych i operacjami.

# Mój program Plainmark [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:plain-mark/markdown2app/edit/main/web/examples/default-example.md)

To jest prosty program napisany w Plainmark. Możesz edytować ten kod i uruchomić go klikając przycisk "Uruchom".

```plainmark
// Definicja funkcji
function calculateSum(a, b) {
  return a + b;
}

// Definicja zmiennych
let x = 10;
let y = 20;

// Wywołanie funkcji i wypisanie wyniku
let result = calculateSum(x, y);
print("Suma " + x + " i " + y + " wynosi: " + result);

// Utworzenie prostego elementu UI
document.body.innerHTML += "<div style='margin-top: 20px; padding: 10px; background-color: #e0e0e0;'>Wygenerowane przez Plainmark!</div>";
```

## Jak działa Plainmark?

Plainmark to język programowania osadzony w Markdown. Kod jest umieszczany w blokach oznaczonych ```plainmark i wykonywany przez interpreter.

### Główne cechy:

1. **Składnia podobna do JavaScript** - łatwa do nauki i użycia
2. **Osadzenie w Markdown** - dokumentacja i kod w jednym pliku
3. **Dostęp do API przeglądarki** - manipulacja DOM, obsługa zdarzeń, itp.
4. **Symulowane API** - np. operacje na plikach

### Spróbuj to!

Edytuj kod powyżej i kliknij "Uruchom", aby zobaczyć rezultat. Możesz również wypróbować inne przykłady z menu rozwijanego "Przykłady".

# Przykład manipulacji DOM [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:plain-mark/markdown2app/edit/main/web/examples/dom.md)

Ten przykład pokazuje, jak Plainmark może manipulować zawartością strony poprzez tworzenie i modyfikowanie elementów DOM.

```js plainmark
// Tworzenie elementów DOM
let container = document.createElement("div");
container.style.padding = "15px";
container.style.backgroundColor = "#f0f0f0";
container.style.borderRadius = "5px";
container.style.marginTop = "20px";

let heading = document.createElement("h3");
heading.textContent = "Interaktywny element utworzony przez Plainmark";
heading.style.color = "#4285f4";

let button = document.createElement("button");
button.textContent = "Kliknij mnie!";
button.style.padding = "8px 16px";
button.style.backgroundColor = "#4CAF50";
button.style.color = "white";
button.style.border = "none";
button.style.borderRadius = "4px";
button.style.cursor = "pointer";
button.style.marginTop = "10px";

let counter = 0;
let counterDisplay = document.createElement("div");
counterDisplay.textContent = "Licznik kliknięć: " + counter;
counterDisplay.style.marginTop = "10px";

// Dodanie obsługi zdarzenia
button.addEventListener("click", function() {
  counter++;
  counterDisplay.textContent = "Licznik kliknięć: " + counter;
  print("Przycisk został kliknięty! Licznik: " + counter);
});

// Utworzenie struktury i dodanie do dokumentu
container.appendChild(heading);
container.appendChild(button);
container.appendChild(counterDisplay);
document.body.appendChild(container);

print("Element DOM został utworzony. Kliknij przycisk, aby zwiększyć licznik.");
```

## Wyjaśnienie kodu

1. **Tworzenie elementów** - używamy `document.createElement()` do tworzenia nowych elementów HTML
2. **Stylizacja** - ustawiamy style CSS dla każdego elementu
3. **Obsługa zdarzeń** - dodajemy listener zdarzenia do przycisku, aby reagować na kliknięcia
4. **Struktura DOM** - budujemy hierarchię elementów za pomocą `appendChild()`

Po uruchomieniu kodu zobaczysz interaktywny przycisk, który zlicza kliknięcia.

# Debugowanie funkcji silni [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:plain-mark/markdown2app/edit/main/web/examples/factorial-debug.md)

Ten przykład skupia się tylko na funkcji silni i lokalizacji błędu.

## Test 1: Podstawowa definicja funkcji

```python plainmark
# Podstawowy kod
def calculate_factorial(n):
    if n <= 1:
        return 1
    return n * calculate_factorial(n - 1)

# Tylko definicja funkcji, bez wywołania
print("Funkcja zdefiniowana")
```

## Test 2: Wywołanie funkcji i przypisanie do zmiennej

```python plainmark
# Definicja i wywołanie
def calculate_factorial(n):
    if n <= 1:
        return 1
    return n * calculate_factorial(n - 1)

# Wywołanie funkcji
result = calculate_factorial(5)
print("Wynik obliczony")
```

## Test 3: Wypisanie wyniku bez konkatenacji

```python plainmark
# Definicja i wywołanie z wypisaniem wyniku
def calculate_factorial(n):
    if n <= 1:
        return 1
    return n * calculate_factorial(n - 1)

result = calculate_factorial(5)
print("Wynik:", result)
```

 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:plain-mark/markdown2app/edit/main/web/examples/files.md)
# Przykład obsługi plików (symulacja)

Ten przykład pokazuje, jak Plainmark może symulować operacje na plikach. W środowisku przeglądarki faktyczne operacje na plikach nie są możliwe, ale Plainmark oferuje symulowane API dla celów demonstracyjnych.

```js plainmark
// Symulacja operacji na plikach
// Uwaga: W przeglądarce to tylko symulacja - faktyczne pliki nie są tworzone

// Zapis do pliku
fs.writeFile("testfile.txt", "To jest zawartość testowego pliku.", function(err) {
  if (err) {
    print("Błąd podczas zapisu pliku: " + err.message);
  } else {
    print("Plik został zapisany pomyślnie!");
    
    // Odczyt z pliku
    fs.readFile("testfile.txt", function(err, data) {
      if (err) {
        print("Błąd podczas odczytu pliku: " + err.message);
      } else {
        print("Zawartość pliku: " + data);
      }
    });
    
    // Próba odczytu nieistniejącego pliku
    fs.readFile("nieistniejacy.txt", function(err, data) {
      if (err) {
        print("Oczekiwany błąd: " + err.message);
      } else {
        print("To nie powinno się wydarzyć!");
      }
    });
  }
});

print("Operacje na plikach zostały zainicjowane (asynchronicznie).");
```

## Wyjaśnienie kodu

1. **API plików** - Plainmark w przeglądarce symuluje operacje na plikach poprzez API `fs`
2. **Asynchroniczność** - operacje na plikach są asynchroniczne, używają callbacków
3. **Obsługa błędów** - sprawdzamy parametr `err` w callbackach, aby obsłużyć potencjalne błędy

Uwaga: W rzeczywistym środowisku terminalowym (Python), te operacje faktycznie utworzyłyby i czytały pliki na dysku.

# Minimalny przykład silni w Python + Plainmark [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:plain-mark/markdown2app/edit/main/web/examples/minimal-python-factorial.md)

## Przykład

```python plainmark
# Funkcja silni
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Wywołanie funkcji
result = factorial(5)

# Różne sposoby wyświetlania wyniku
# Sposób 1: Bez konkatenacji
print("Wynik silni:", result)

# Sposób 2: Z tekstem i przecinkiem
print("Silnia z 5 wynosi:", result)

# Sposób 3: Czysty wynik
print(result)
```

# Uproszczony przykład mieszanych języków [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:plain-mark/markdown2app/edit/main/web/examples/multi-lang.md)

Ten przykład demonstruje używanie Plainmark z różnymi językami programowania.

## JavaScript + Plainmark

```js plainmark
// Prosty kod JavaScript
let message = "Hello from JavaScript!";
print(message);

let jsElement = document.createElement("div");
jsElement.style.backgroundColor = "#f0db4f";
jsElement.style.padding = "10px";
jsElement.textContent = message;
document.body.appendChild(jsElement);
```

## Python + Plainmark

```python plainmark
# Prosty kod Python bez funkcji rekurencyjnych
message = "Hello from Python!"
print(message)

# Prosta zmienna bez operacji na stringach
python_element = document.createElement("div")
python_element.style.backgroundColor = "#306998"
python_element.style.padding = "10px"
python_element.style.color = "white"
python_element.textContent = message
document.body.appendChild(python_element)
```

# Test wyświetlania liczb [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:plain-mark/markdown2app/edit/main/web/examples/number-display-test.md)

Ten przykład testuje różne sposoby wyświetlania liczb w Plainmark.

## Test 1: Prosta liczba

```plainmark
// Przypisanie liczby
let num = 42;
print(num);
```

## Test 2: Konkatenacja z prefixem

```plainmark
// Prosty łańcuch + liczba
let num = 42;
print("Liczba: " + num);
```

## Test 3: Liczba jako wynik funkcji

```plainmark
// Funkcja zwracająca liczbę
function getNumber() {
  return 42;
}

let num = getNumber();
print(num);
```

## Test 4: Alternatywne sposoby wyświetlania liczby

```plainmark
// Różne sposoby wyświetlania
let num = 42;

// 1. Z przecinkiem
print("Z przecinkiem:", num);

// 2. Z szablonami literałów
print(`Z szablonem: ${num}`);

// 3. Z jawną konwersją na string
print("Jawna konwersja: " + num.toString());

// 4. Z konwersją przez funkcję
print("Przez funkcję: " + (num+""));
```

# Przykład Python + Plainmark z komentarzami JavaScript [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:plain-mark/markdown2app/edit/main/web/examples/python-example-with-js-comments.md)

## Przykład Python z komentarzami JS

```python plainmark
// To jest blok kodu Python z Plainmark, ale z komentarzami JS
message = "Hello from Python!"
print(message)

// W przeglądarce nadal wykonuje się jako JavaScript
// ale zachowujemy składnię Pythona dla czytelności
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
print("Wynik silni:", result)

// Tworzymy element DOM dla wyniku
python_element = document.createElement("div")
python_element.style.backgroundColor = "#306998"
python_element.style.padding = "10px"
python_element.style.color = "white"
python_element.textContent = "Python: " + message
document.body.appendChild(python_element)
```

 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:plain-mark/markdown2app/edit/main/web/examples/visualization.md)
# Przykład wizualizacji danych

Ten przykład pokazuje, jak Plainmark może być używany do tworzenia prostych wizualizacji danych bezpośrednio w przeglądarce. Utworzymy interaktywny wykres słupkowy z danymi miesięcznymi.

```js plainmark
// Dane do wizualizacji
let data = [
  { name: "Styczeń", value: 65 },
  { name: "Luty", value: 59 },
  { name: "Marzec", value: 80 },
  { name: "Kwiecień", value: 81 },
  { name: "Maj", value: 56 },
  { name: "Czerwiec", value: 55 }
];

// Utworzenie kontenera wykresu
let chartContainer = document.createElement("div");
chartContainer.style.width = "100%";
chartContainer.style.height = "300px";
chartContainer.style.marginTop = "20px";
chartContainer.style.position = "relative";

// Obliczenie maksymalnej wartości dla skalowania
let maxValue = Math.max(...data.map(item => item.value));
let barWidth = 100 / data.length;

// Utworzenie wykresu słupkowego
data.forEach((item, index) => {
  let barHeight = (item.value / maxValue) * 100;
  
  // Kontener słupka
  let bar = document.createElement("div");
  bar.style.position = "absolute";
  bar.style.bottom = "0";
  bar.style.left = (index * barWidth) + "%";
  bar.style.width = (barWidth - 2) + "%";
  bar.style.height = barHeight + "%";
  bar.style.backgroundColor = "rgba(66, 133, 244, 0.7)";
  bar.style.borderRadius = "4px 4px 0 0";
  bar.style.transition = "height 0.5s ease-in-out";
  
  // Etykieta z wartością
  let valueLabel = document.createElement("div");
  valueLabel.textContent = item.value;
  valueLabel.style.position = "absolute";
  valueLabel.style.top = "-25px";
  valueLabel.style.width = "100%";
  valueLabel.style.textAlign = "center";
  valueLabel.style.color = "#333";
  valueLabel.style.fontSize = "12px";
  
  // Etykieta z nazwą
  let nameLabel = document.createElement("div");
  nameLabel.textContent = item.name;
  nameLabel.style.position = "absolute";
  nameLabel.style.bottom = "-25px";
  nameLabel.style.width = "100%";
  nameLabel.style.textAlign = "center";
  nameLabel.style.color = "#333";
  nameLabel.style.fontSize = "12px";
  
  bar.appendChild(valueLabel);
  bar.appendChild(nameLabel);
  chartContainer.appendChild(bar);
  
  // Dodanie interakcji
  bar.addEventListener("mouseover", function() {
    this.style.backgroundColor = "rgba(66, 133, 244, 1)";
    valueLabel.style.fontWeight = "bold";
  });
  
  bar.addEventListener("mouseout", function() {
    this.style.backgroundColor = "rgba(66, 133, 244, 0.7)";
    valueLabel.style.fontWeight = "normal";
  });
});

// Dodanie osi Y
let yAxis = document.createElement("div");
yAxis.style.position = "absolute";
yAxis.style.left = "-30px";
yAxis.style.top = "0";
yAxis.style.bottom = "0";
yAxis.style.width = "30px";
yAxis.style.borderRight = "1px solid #ccc";

// Dodanie podziałek na osi Y
for (let i = 0; i <= 5; i++) {
  let tick = document.createElement("div");
  tick.textContent = Math.round(maxValue * (1 - i / 5));
  tick.style.position = "absolute";
  tick.style.right = "5px";
  tick.style.top = ((i / 5) * 100) + "%";
  tick.style.fontSize = "10px";
  tick.style.color = "#666";
  tick.style.transform = "translateY(-50%)";
  
  yAxis.appendChild(tick);
}

// Dodanie osi X
let xAxis = document.createElement("div");
xAxis.style.position = "absolute";
xAxis.style.left = "0";
xAxis.style.right = "0";
xAxis.style.bottom = "-30px";
xAxis.style.height = "30px";
xAxis.style.borderTop = "1px solid #ccc";

// Dodanie tytułu wykresu
let chartTitle = document.createElement("div");
chartTitle.textContent = "Miesięczne dane";
chartTitle.style.textAlign = "center";
chartTitle.style.fontSize = "16px";
chartTitle.style.fontWeight = "bold";
chartTitle.style.marginBottom = "20px";

// Dodanie legendy
let legend = document.createElement("div");
legend.style.display = "flex";
legend.style.justifyContent = "center";
legend.style.alignItems = "center";
legend.style.marginTop = "40px";

let legendItem = document.createElement("div");
legendItem.style.display = "flex";
legendItem.style.alignItems = "center";
legendItem.style.marginRight = "20px";

let legendColor = document.createElement("div");
legendColor.style.width = "20px";
legendColor.style.height = "20px";
legendColor.style.backgroundColor = "rgba(66, 133, 244, 0.7)";
legendColor.style.marginRight = "5px";

let legendText = document.createElement("div");
legendText.textContent = "Wartość miesięczna";

legendItem.appendChild(legendColor);
legendItem.appendChild(legendText);
legend.appendChild(legendItem);

// Utworzenie kontenera głównego
let mainContainer = document.createElement("div");
mainContainer.style.position = "relative";
mainContainer.style.padding = "40px 40px 60px 40px";
mainContainer.style.border = "1px solid #ccc";
mainContainer.style.borderRadius = "4px";
mainContainer.style.backgroundColor = "white";

mainContainer.appendChild(chartTitle);
mainContainer.appendChild(chartContainer);
mainContainer.appendChild(legend);
chartContainer.appendChild(yAxis);
chartContainer.appendChild(xAxis);

document.body.appendChild(mainContainer);

print("Utworzono interaktywny wykres słupkowy z danymi miesięcznymi.");
```

## Wyjaśnienie kodu

1. **Dane** - definiujemy tablicę obiektów z danymi miesięcznymi
2. **Tworzenie wykresu** - budujemy wykres słupkowy za pomocą elementów DOM i CSS
3. **Interaktywność** - dodajemy zdarzenia `mouseover` i `mouseout` dla lepszego doświadczenia użytkownika
4. **Osie i etykiety** - dodajemy osie X i Y oraz etykiety dla lepszej czytelności

Ten przykład pokazuje, jak można tworzyć proste, ale efektywne wizualizacje danych bez użycia zewnętrznych bibliotek.

---
+ Modular Documentation made possible by the [FlatEdit](http://www.flatedit.com) project.
