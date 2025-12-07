#1. Meme Generator – Docker aplikacija

Ta projekt predstavlja spletno aplikacijo Meme Generator, ki omogoča nalaganje slike ter dodajanje zgornjega in spodnjega besedila na sliko.  
Aplikacija je razvita v programskem jeziku Python z uporabo ogrodja Flask in knjižnice Pillow za obdelavo slik.  
Celoten projekt je uspešno zapakiran v Docker kontejner.

2. Funkcionalnosti aplikacije:
   
- Nalaganje poljubne slike
- Vnos zgornjega in spodnjega besedila
- Samodejno generiranje slike
- Prikaz generirane slike v brskalniku
- Delovanje znotraj Docker okolja

3. Zagon aplikacije z Dockerjem:

-Izgradnja Docker slike:
V ukazni vrstici v mapi projekta zaženemo:
"docker build -t meme-generator ."

-Zagon Docker kontejnerja:
"docker run -p 5000:5000 meme-generator"

- Dostop do aplikacije:
V spletni brskalnik vpišemo:
"http://localhost:5000"

Avtor: Rene Bračič Rajšp

