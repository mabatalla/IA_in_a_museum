# IS THIS PICASSO?
AN AI GOES TO THE MUSEUM

---

### ABOUT

This is a project focused on images to get a deeper understanding of different ML algorithms. The starting point of
this project is an intuition on how to difference paintings present in a museum by the artists that painted them.

* WHY ART?
* APPROACH: OBJECTIVES & LIMITATIONS
* METHODOLOGY

---

### ART APPRECIATION INTUITION

* HOW WILL YOU GUIDE SOMEONE BLINDFOLDED THROUGH THE MUSEUM?

---

### COLOR THEORY

* FROM NATURAL PIGMENTS TO RGB COLOR MODE

---

### BEFORE CODING

1. Navigate to the project's folder via terminal.
  

2. Create a virtual environment using:  
  
    `python -m venv museum_env`
  

3. Activate the virtual environment with the following commands:
    * Win: `museum_env\Scripts\activate.bat`
    * Mac: `source museum_env\bin\activate`  
  

4. Now install all requirements with:  

    `pip install requirements.txt`
  

5. Don't forget to regenerate museum_requirements.txt if you pretend to do a pull request. This can be easily done 
   with:

    `pip freeze > requirements.txt`

---

### BUILDING THE MUSEUM

To start this project I needed a dataset, but I couldn't find an apropiate one.
Fortunately I found [wikiart's project by Lucas David][1] that gave me a great starting point.

Using his code I downloaded a big amount of pictures of some artis with a noticeable style difference:

* [Caravaggio](https://en.wikipedia.org/wiki/Caravaggio)
* [Edgar Degas](https://en.wikipedia.org/wiki/Degas)
* [Francisco de Goya](https://en.wikipedia.org/wiki/Goya)
* [Katsushika Hokusai](https://en.wikipedia.org/wiki/Hokusai)
* [Frida Kahlo](https://en.wikipedia.org/wiki/Frida_Kahlo)
* [Wassily Kandinsky](https://en.wikipedia.org/wiki/Wassily_Kandinsky)
* [Gustav Klimt](https://en.wikipedia.org/wiki/Gustav_Klimt)
* [Roy Lichtenstein](https://en.wikipedia.org/wiki/Roy_Lichtenstein)
* [Piet Mondrian](https://en.wikipedia.org/wiki/Piet_Mondrian)
* [Claude Monet](https://en.wikipedia.org/wiki/Claude_Monet)
* [Pablo Picasso](https://en.wikipedia.org/wiki/Pablo_Picasso)
* [Jackson Pollock](https://en.wikipedia.org/wiki/Jackson_Pollock)
* [Joaquín Sorolla](https://en.wikipedia.org/wiki/Joaqu%C3%ADn_Sorolla)
* [Diego Velázquez](https://en.wikipedia.org/wiki/Diego_Vel%C3%A1zquez)
* [Andy Warhol](https://en.wikipedia.org/wiki/Andy_Warhol)

To do so, you can use the wikiart script in ./utils/wikiart. I left a copy of the full list of artists
(artists_backup.json) in that folder in case you want to build your own museum.

With my setup (MacBook Pro, 2.3 GHz Quad-Core Intel Core i7 + 16 GB RAM and flash storage) it took me almost 3 
hours to get about 5500 pictures.

[1]: https://github.com/lucasdavid/wikiart
