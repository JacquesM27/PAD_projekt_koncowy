### Wybrane pole i temat  
Zamierzam skupić się na analizie danych dotyczących opon zimowych dostępnych w sklepach internetowych, takich jak Oponeo i SklepOpon. Projekt będzie obejmował zbieranie danych o różnych modelach opon, ich parametrach technicznych i dostępności, co pozwoli na przeprowadzenie analizy oraz stworzenie modelu wspierającego wybór opon najbardziej dopasowanych do wymagań użytkownika.

---

### Metoda pozyskiwania danych  
Dane zostaną zebrane za pomocą technik web scrapingowych, wykorzystując bibliotekę Selenium. Skrypt odwiedzi strony Oponeo i SklepOpon, zbierając szczegóły o oponach zimowych, takie jak:  
- Nazwa, marka i model  
- Rozmiar (np. 205/55 R16)  
- Indeksy nośności i prędkości  
- Wskaźniki efektywności paliwowej, przyczepności na mokrej nawierzchni i poziomu hałasu  
- Cena, klasa opony, oceny użytkowników i dostępność.  

---

### Cel badania  
Celem projektu jest stworzenie modelu, który:  
1. Klasyfikuje opony pod względem ich stosunku jakości do ceny, dostępności i innych parametrów technicznych.  
2. Pozwala użytkownikowi na wprowadzenie kryteriów wyszukiwania (np. cena, marka, klasa, wskaźnik przyczepności na mokrej nawierzchni) i zwraca 2-3 najlepiej dopasowane modele opon.  
3. Przedstawia wyniki w intuicyjnym dashboardzie, który wizualizuje kluczowe wskaźniki (np. zależność ceny od klasy, popularność konkretnych rozmiarów opon).

---

### Złożoność zbioru danych  
Zbiór danych jest bogaty i wielowymiarowy, zawiera zarówno dane kategoryczne (marka, model, klasa), jak i ciągłe (cena, oceny użytkowników, poziom hałasu). Parametry takie jak dostępność czy indeksy prędkości i nośności wprowadzają dodatkową warstwę do analizy. Dzięki różnorodności danych możliwe będzie odkrycie interesujących zależności i stworzenie złożonego modelu wspierającego wybór opon.

---

### Dostosowanie metod analizy  
Dla zebranego zbioru danych zastosuję:  
- **Analizę eksploracyjną (EDA)**: Wizualizacje rozkładu cen i popularności modeli w różnych segmentach rynku.  
- **Analizę korelacji**: Zbadam zależności między parametrami technicznymi a ceną i ocenami użytkowników.  
- **Modele rekomendacyjne**: Model na podstawie parametrów wprowadzonych przez użytkownika (np. romiar, cena, marka, klasa, wskaźnik głośności czy przyczepności na mokrej nawierzchni) zwróci 2-3 najlepiej dopasowane opony spełniające jego kryteria.  

---

### Tworzenie dashboardu  
Dashboard zostanie zbudowany w Streamlit, prezentując dane w formie:  
- Wykresów (np. zależności ceny od klasy i rozmiaru).  
- Mapy cieplnej popularności rozmiarów opon w różnych segmentach rynku.

Dashboard ułatwi interpretację wyników i wspomoże proces podejmowania decyzji przez użytkowników.