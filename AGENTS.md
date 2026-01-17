# AGENTS.md

## Opis projektu
Stworzyć aplikację webową (serwer Flask) do wizualizacji danych EEG. Aplikacja powinna:
- Czytać zapisane dane EEG z plików (np. CSV). W repozytorium `Neurofeedback-Program` dane są symulowane, tutaj używamy gotowych plików.
- Wyświetlać sygnał wybranego kanału w czasie na wykresie.
- Umożliwiać wybór kanału, przedziału czasowego i trybu (surowy/odfiltrowany). Do filtracji używać logiki podobnej do metod w `signal_processor.py`.
- (Opcjonalnie) Pokazywać metryki relaksacji/koncentracji obliczane jak w `mental_state_analyzer.py`, ale kluczowy wymóg to sam sygnał.
- Zapewnić komponent HCI: interfejs zrozumiały dla badacza/studenta (opisy, etykiety, kolory) i krótka analiza, które elementy pomagają lub przeszkadzają w odbiorze.

## Instalacja i przygotowanie
- Python 3.7+
- Wirtualne środowisko (opcjonalnie) i instalacja zależności: `pip install flask pandas numpy brainflow`.
- `matplotlib` w razie potrzeby do testów filtracji poza interfejsem web.

## Struktura projektu
- `app.py` – główna aplikacja Flask.
- `templates/index.html` – szablon HTML ze skryptem Chart.js i kontrolkami (kanały, zakres, filtr).
- `static/` – katalog na zasoby statyczne (CSS/JS/obrazy, jeśli potrzebne).
- (Opcjonalnie) `data/` – katalog z plikami EEG (CSV lub inne).

## Kroki wdrożenia

1. **Aplikacja Flask**  
   - Import Flask, pandas itp.  
   - `app = Flask(__name__)`  
   - Trasa `/` (GET) z `render_template('index.html')`.  
   - Uruchamianie: `app.run(host="0.0.0.0", port=5000, debug=True)`.

2. **Dane EEG**  
   - Jeśli istnieje `eeg_data.csv`, wczytaj:  
     ```python
     import pandas as pd
     df = pd.read_csv('data/eeg_data.csv')
     ```
   - Kolumny = kanały (`Ch1`, `Ch2`, ...), wiersze = próbki w czasie.  
   - Lista kanałów: `channels = list(df.columns)`.

3. **HTML z kontrolkami**  
   - W `templates/index.html` podłączyć Chart.js (CDN).  
   - Selektor kanałów `<select id="channelSelect">` z `<option>` dla każdego kanału.  
   - Pola `start` i `end` (`<input type="number">` lub suwaki) dla przedziału.  
   - Przełącznik filtra `<input type="checkbox" id="filterCheckbox">`.  
   - Przycisk „Odśwież” lub nasłuchiwanie `onchange`.  
   - `<canvas id="eegChart"></canvas>` dla wykresu.

4. **JavaScript do aktualizacji wykresu**  
   - Przy ładowaniu: `/data?channel=X&start=Y&end=Z&filtered=false` (fetch).  
   - Przy zmianie parametrów wysyłać nowy request.  
   - Po otrzymaniu JSON:  
     ```js
     chart.data.labels = response.time;
     chart.data.datasets[0].data = response.voltage;
     chart.update();
     ```
   - Checkbox `filtered` włącza filtrowanie w zapytaniu.

5. **Trasa `/data`**  
   ```python
   @app.route('/data')
   def data():
       channel = request.args.get('channel')
       start = int(request.args.get('start', 0))
       end = int(request.args.get('end', 0))
       filtered = request.args.get('filtered') == 'true'
       signal = df[channel][start:end].to_numpy()
       if filtered:
           from brainflow.data_filter import DataFilter, FilterTypes
           sfreq = 250  # lub inna zgodnie z danymi
           DataFilter.perform_bandstop(signal, sfreq, 58.0, 62.0, 4, FilterTypes.BUTTERWORTH.value, 0)
           DataFilter.perform_bandpass(signal, sfreq, 8.0, 13.0, 4, FilterTypes.BUTTERWORTH.value, 0)
       time = list(range(start, start + len(signal)))
       return jsonify({"time": time, "voltage": signal.tolist()})
   ```
   - `start`, `end` to indeksy próbek; `sfreq` ustalić z danych. Blok filtracji wzorowany na `SignalProcessor.filter_signal`.

6. **Wykres Chart.js**  
   ```js
   const ctx = document.getElementById('eegChart').getContext('2d');
   let eegChart = new Chart(ctx, {
     type: 'line',
     data: { labels: [], datasets: [{ label: 'EEG', data: [], borderColor: 'blue', fill: false }]},
     options: { scales: { x: { display: true }, y: { display: true } } }
   });
   ```
   - Po otrzymaniu JSON aktualizować dane i wywołać `chart.update()`.

7. **Testy**  
   - `python app.py`, otworzyć `http://localhost:5000/`, sprawdzić zmianę kanału, zakresu i filtra.

8. **HCI – raport**  
   - Opisać użytkownika (np. badacz/student EEG), decyzje poznawcze (kanał, przedział, tryb surowy/filtr).  
   - Wskazać elementy, które pomagają (etykiety, kolory, prostota), przeszkadzają lub mogą wprowadzać błąd (niejasne nazwy kanałów, zbyt drobny krok zakresu itp.).

## Styl kodu i testy
- Czytelne nazwy, ewentualne funkcje pomocnicze (np. filtracja).
- Po istotnych zmianach testy ręczne.
- Krótkie komentarze przy kluczowej logice, by inni deweloperzy szybko zrozumieli kod.
