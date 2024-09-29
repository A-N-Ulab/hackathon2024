# To repozytorium
To repozytorium jest jednocześnie sposoben na udostępnienie kodu Chloe, ale także służyło jako nasze repo przy jej tworzeniu. Dlatego w poniższej instrukcji będzie wymieniany tylko folder `Chloe` z jego podfolderami.

# Chloe
Chloe, czyli twoja personalna personalna nauczycielka matematyki. Czasami bywa lekko niesforna, może nawet i wulgarna, ale wszyscy wiemy, że im coś jest głupszse tym lepiej wchodzi do głowy. A poza tym, zapisaliśmy Chloe na terapie...

# Instalacja
Obecnie, instalacja ma tylko sens w celach developmentu, jeśli jednak chcesz przetestowac Chloe, postępuj za poniższymi krokami:    
* Sprawdź czy masz zainstalowanego pythona, póki co Chlose została sprawdzona na pythonie 3.7, 3.8 i 3.10
* Zainstaluj Flaska'a. Aby to zrobić  użyj komendy `pip install flask`
* Pobierz to repository, albo pobierając zipa, albo klonując biblioteke z terminala
* Otwórz pobrany folder i otwórz plik `main.py` z foldeu `Chloe`
* uruchom ten program, jeżeli wszystko zostało zrobione poprawnie, powinna Ci się ukazać wiadomość o uruchomieniu Flaska na adresie http://127.0.0.1:5000

# Skalowanie/dodawanie własnych zadań i poblemy z tym związane
## Dodawanie własnych zadań
Stworzenie nowych zdań jest bardzo proste, wystarczy że w folderze `Chloe/static/Lessons` utorzymy nowy plik .txt. Struktura tego pliku też jest bardzo prosta
```
Info: Długość odcinka[...]:;img1
Task: Bok AB ma długość[...]. Ile wynosi A?_5
 ```
Powyrzszy przygład stworzy nową lekcję z jednym przykładem i jednym zadaniem. Przykłady są oznaczane prefixem `Info:`, później podajemy faktyczny przykład, a po średniku `;` możeny dodać nazwę zdjęcia jakie zostanie dodane poniżej przykładu. Prefixem `Task` oznaczamy zadania do wykonania, po prefixie należy podać pytanie, a po podłodze `_` podajemy wynik jaki powinniśmy otrzymać po wykonaniu zadania. **Najżażniejsze różnice:** `Taski` nie mogą mieć zdjęć. Pozostałe rzeczy są obliczne automatycznie przez samą Chloe.
## Dodawanie lekcji do strony
Ten krok niestety nie jest tak prosty jak poprzedni, aby dodać kolejną lekcję należy. Obecnie Chloe nie obsługuje nowych działów można tylko dodawać nowe lekcje. \
Dodawanie nowych lekcji: 
* w pliku `Chloe/templates/main.html` pod linią 73 trzeba dodać nową linię wyglądającą tak: `<button class="{{NIEPOWTARZALNE_ID_LEKCJI}}" id="NIEPOWTARZALNE_ID_LEKCJI" name="button" value="NIEPOWTARZALNA_WARTOŚĆ_LEKCJI">TEMAT</button>` np. `<button class="{{classLesson4}}" id="less4" name="button" value="lesson4">lekcja 4 - równanie okręgu</button>`. Ważne jest żeby wszystko oznaczone jako `NIEPOWTARZALNE`, jak sama nazwa wskazuje, nie powtarzało się nidzie indziej w całej Chloe.
* w pliku `Chloe/main.py` w lini 30 do self.classList należy dodać jeszcze jednego stringa "lock", oznacza to że nowo dodana lekcja będzie zablokowana
Ostatnim problemem związanym z dodawaniem własnych zadań/lekcji są znaki specjalne, obecnie tylko jeden przycisk jest skonfigurowany na *"stałe"* jako pierwiastek

# Poprawki w przyszłości
Jeżeli Chloe będzie dalej rozwijana, to albo będzie musiała być przepisana na ze zmianami uwzględniającymi powyższe problemy (z braku czasu nie udało nam się tego rozwiązać na hackathonie) w pythonie albo w innym języku/framweorku bardziej odpowiedznim do tego zadania.

# Przyszłe funkcje/plany
Jednym z większych naszych planów jest gamifikacja edukacji, zwłaszcza, że można w naprawde ciekawy sposób uczyć, tak jak w tym przypadku, matematyki. Chcielibyśmy aby dzięki temu przekonać uczniów, że matematyka może być naprawde ciekawa.

