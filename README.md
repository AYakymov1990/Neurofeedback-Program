# Projekt Neurofeedback w Pythonie

## Wprowadzenie

Ten projekt implementuje program neurofeedback w języku Python, oparty na artykule ["Creating a Neurofeedback Program With Python"](https://ahnaafk.medium.com/creating-a-neurofeedback-program-with-python-c6153022a4e7) autorstwa Ahnaaf Khan. Głównym celem jest stworzenie aplikacji, która w czasie rzeczywistym analizuje sygnał EEG (elektroencefalogram) i dostarcza użytkownikowi informacji zwrotnej (feedback) o jego stanie mentalnym, w szczególności poziomie relaksacji i koncentracji.

Kluczową modyfikacją w stosunku do oryginalnego projektu jest **wykorzystanie symulowanych danych EEG** zamiast rzeczywistego urządzenia BCI (Brain-Computer Interface). Dzięki temu projekt może być realizowany bez konieczności zakupu kosztownego sprzętu, co czyni go idealnym do celów edukacyjnych i prototypowania.

## Podstawy Naukowe

### Neurofeedback i Operant Conditioning

Neurofeedback to forma biofeedbacku, która wykorzystuje neuroplastyczność mózgu – jego zdolność do zmiany, wzrostu i uczenia się. Proces ten opiera się na **operant conditioning** (warunkowaniu instrumentalnym), technice polegającej na nagradzaniu pozytywnych zachowań i karaniu negatywnych.

W kontekście neurofeedbacku, proces wygląda następująco:

1. Użytkownik korzysta z urządzenia EEG do grania w grę kontrolowaną aktywnością mózgu (metoda nagradzania i karania).
2. Użytkownik próbuje się zrelaksować (akcja).
3. Gdy użytkownik się relaksuje, zaczyna wygrywać w grze (nagradzanie pozytywnych akcji).
4. Gdy użytkownik się denerwuje, zaczyna przegrywać w grze (karanie negatywnych akcji).
5. Proces jest powtarzany, aż użytkownik nauczy się samoregulacji aktywności mózgu.

### Fale Mózgowe

Aktywność elektryczna mózgu może być podzielona na różne pasma częstotliwości, zwane falami mózgowymi. Każde pasmo jest związane z określonym stanem świadomości:

| Pasmo Fal | Częstotliwość (Hz) | Stan Mentalny                                      |
| :-------- | :----------------- | :------------------------------------------------- |
| **Delta** | 0.5 - 4            | Głęboki sen, regeneracja organizmu                 |
| **Theta** | 4 - 7              | Głęboka medytacja, senność, kreatywność            |
| **Alfa**  | 8 - 12             | Relaksacja, odpoczynek, zamknięte oczy             |
| **Beta**  | 12 - 30            | Normalna aktywność, koncentracja, stres            |

W naszym projekcie skupiamy się głównie na falach **Alfa** (relaksacja) i **Beta** (koncentracja).

## Architektura Projektu

Projekt został zaprojektowany w sposób modułowy, co ułatwia rozbudowę i modyfikację. Składa się z następujących komponentów:

### Moduły

1.  **`data_generator.py`**: Odpowiedzialny za generowanie symulowanych danych EEG przy użyciu biblioteki Brainflow (`SYNTHETIC_BOARD`).
2.  **`signal_processor.py`**: Przetwarza surowy sygnał EEG – filtruje szumy i oblicza moc poszczególnych pasm częstotliwości fal mózgowych.
3.  **`mental_state_analyzer.py`**: Analizuje przetworzone dane i oblicza metryki relaksacji i koncentracji przy użyciu modeli uczenia maszynowego z Brainflow.
4.  **`visualizer.py`**: Tworzy interfejs użytkownika z wykresami na żywo, pokazującymi sygnał EEG oraz poziomy relaksacji i koncentracji.
5.  **`main.py`**: Główny plik aplikacji, który koordynuje działanie wszystkich modułów.

### Struktura Plików

```
neurofeedback_project/
├── .cursor-rules.json      # Zasady dla środowiska Cursor IDE
├── main.py                 # Główny skrypt aplikacji
├── data_generator.py       # Moduł generowania danych EEG
├── signal_processor.py     # Moduł przetwarzania sygnału
├── mental_state_analyzer.py# Moduł analizy stanu mentalnego
├── visualizer.py           # Moduł wizualizacji
├── requirements.txt        # Lista zależności
└── README.md               # Dokumentacja projektu
```

## Wykorzystane Technologie

Projekt wykorzystuje wyłącznie **darmowe biblioteki open-source**:

*   **Brainflow** (`~4.0.2`): Główna biblioteka do generowania danych EEG, filtrowania sygnału i analizy stanu mentalnego.
*   **NumPy** (`~1.19.4`): Efektywne operacje na wielowymiarowych tablicach danych.
*   **Pandas** (`~1.2.1`): Organizacja i manipulacja danymi EEG w formie DataFrame.
*   **Matplotlib** (`~3.3.4`): Tworzenie dynamicznych wykresów na żywo.

## Instalacja i Uruchomienie

### Wymagania Wstępne

*   Python 3.7 lub nowszy
*   `pip` (menedżer pakietów Pythona)

### Kroki Instalacji

1.  **Sklonuj repozytorium projektu:**
    ```bash
    git clone https://github.com/AYakymov1990/Neurofeedback-Program.git
    cd Neurofeedback-Program
    ```

2.  **Stwórz wirtualne środowisko:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Na Windows: venv\Scripts\activate
    ```

3.  **Zainstaluj zależności:**
    ```bash
    pip install -r requirements.txt
    ```

### Uruchomienie Aplikacji

```bash
python main.py
```

Po uruchomieniu otworzy się okno z wykresami na żywo. W terminalu będą wyświetlane poziomy relaksacji i koncentracji.

## Cursor Rules

Plik `.cursor-rules.json` zawiera zasady i wytyczne dla środowiska Cursor IDE, które pomogą Ci w utrzymaniu spójności kodu i przestrzeganiu najlepszych praktyk podczas pracy nad projektem. Obejmują one:

*   **Strukturę projektu i moduły**: Gdzie umieszczać kod związany z poszczególnymi funkcjonalnościami.
*   **Standardy kodowania**: Przestrzeganie PEP 8, używanie docstringów, type hints.
*   **Użycie biblioteki Brainflow**: Specyficzne wytyczne dotyczące inicjalizacji, filtrowania i analizy danych.

## Szczegółowy Plan Realizacji (Checklist)

Plik `project_checklist.md` zawiera bardzo szczegółowy, krokowy plan implementacji projektu. Jest on podzielony na fazy:

1.  **Przygotowanie środowiska i struktury projektu**
2.  **Implementacja modułu generatora danych**
3.  **Implementacja modułu przetwarzania sygnału**
4.  **Implementacja modułu analizy stanu mentalnego**
5.  **Implementacja wizualizacji i feedbacku**
6.  **Integracja modułów w `main.py`**
7.  **Uruchomienie i testowanie**

Każdy krok jest opisany szczegółowo z przykładami kodu, co pozwala na stopniową implementację projektu.

## Możliwości Rozbudowy

Po zrealizowaniu podstawowej wersji projektu, możesz rozważyć następujące rozszerzenia:

*   **Różne tryby treningu**: Dodaj tryby dla medytacji, poprawy koncentracji, redukcji stresu.
*   **Zapisywanie sesji**: Implementuj funkcjonalność zapisywania danych z sesji do pliku, aby móc analizować postępy w czasie.
*   **Bardziej zaawansowana wizualizacja**: Użyj bibliotek takich jak `Plotly` lub `Dash` do stworzenia interaktywnego dashboardu.
*   **Machine Learning**: Trenuj własne modele klasyfikacji stanów mentalnych na publicznych zbiorach danych EEG.
*   **Integracja z rzeczywistym urządzeniem**: Po opanowaniu projektu na danych symulowanych, możesz spróbować podłączyć rzeczywiste urządzenie EEG (np. OpenBCI, Muse).

## Źródła i Referencje

*   [Repozytorium Projektu na GitHub](https://github.com/AYakymov1990/Neurofeedback-Program)
*   [Artykuł oryginalny: "Creating a Neurofeedback Program With Python"](https://ahnaafk.medium.com/creating-a-neurofeedback-program-with-python-c6153022a4e7) - Ahnaaf Khan
*   [Repozytorium GitHub autora artykułu](https://github.com/ahnaafk/neurofeedback)
*   [Dokumentacja Brainflow](https://brainflow.readthedocs.io/)
*   [Dokumentacja Matplotlib](https://matplotlib.org/stable/contents.html)

## Autorzy Projektu

*   **VALENTYN KOVALCHUK**
    *   Nr albumu: 158996
    *   Grupa D2

*   **YAKYMOV OLEKSANDR**
    *   Nr albumu: 159004
    *   Grupa D2