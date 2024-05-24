### Tema 1 - Le Stats Sportif ###

### Implementare ###
Pentru implementare am ales sa folosesc direct ThreadPoolExecutor, fara a-mi crea eu de la 0 un threadpool,
deoarce din punctul meu de vedere a fost o abordare mai simpla si mai eficienta.
Prima data am initializat ThreadPoolExeutor-ul calculand numarul de thread-uri sa fie egal ori cu numarul de
cores al procesorului, ori cu variabila setata, daca aceasta exista. Dupa aceasta, am creat un dictionar
in care am salvat toate task-urile, pentru a le putea astepta pe toate la final.
Functiile implementate in ThreadPool sunt pentru a face handle job-ului, adica a il adauga in dictionarul
de task-uri, a il executa daca exista thread-uri disponibile, a astepta la finalizarea task-urilor si a
returna rezultatele.
Pentru a citi datele din fisier, am folosit biblioteca pandas, care imi permite sa citesc datele din fisier
intr-un DataFrame, fiind o structura cu care se pot manipula datele foarte usor. Cu pandas am manipulat datele
si in interiorul rutelor, pentru a le putea returna in formatul dorit. Functiile pentru rute sunt detaliate in fisierul
routes.py, in care se explica functionalitatea fiecareia.

### Unitesting ###
Pentru unit testing am folosit biblioteca unittest, care imi permite sa fac teste unitare pentru fiecare functie
in parte. Am testat si api-ul pentru shutdown si in rest am testat fiecare functie in parte pentru fiecare ruta
pentru a vedea daca functioneaza asa cum trebuie. Pentru a rula testele, am folosit comanda `python -m unittest test_the_app.py`.

#### Decizii de implementare + documentatie ###
Pentru a citi datele din fisier, am folosit biblioteca pandas, care imi permite sa citesc datele din fisier
intr-un DataFrame, fiind o structura cu care se pot manipula datele foarte usor.
Ca si documentatie, am folosit documentatia oficiala a bibliotecii pandas, care se gaseste la adresa:
https://pandas.pydata.org/pandas-docs/stable/reference/index.html - pentru sectiune de functii, iar
pentru intelegerea efectiva a lucrurlui cu biblioteca, am folosit https://www.youtube.com/watch?v=ClNP-lTzKgI&t=329s

Pentru implemantarea rutelor am folosit biblioteca Flask, care imi permite sa creez un server web, care sa
asculte pe un anumit port si sa raspunda la anumite requesturi. Pentru a intelege cum functioneaza Flask,
am folosit https://www.youtube.com/watch?v=f085KDOy43k si https://www.youtube.com/watch?v=XrG_TlwPtsU&t=13s.