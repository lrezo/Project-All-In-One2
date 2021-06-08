from datetime import datetime

q = int(input("Which question you wanna see? "))

if q == 1:
    # Opgave 1
    woordlist = ["appel", "doerian", "banaan", "doerian", "appel", "kers",
                 "kers", "mango", "appel", "appel", "kers", "doerian", "banaan",
                 "appel", "appel", "appel", "appel", "banaan", "appel"]
    dict_woordlist = {}
    for i in woordlist:
        dict_woordlist[i] = woordlist.count(i)
    for i in dict_woordlist :
        print(f"{i}:{dict_woordlist[i]}")



if q == 2:
    # Opgave 2
    tekst = "appel,doerian ,banaan ,doerian ,appel,kers,kers,mango ," + \
            "appel,appel,kers,doerian ,banaan ,appel,appel,appel," + \
            "appel,banaan ,appel"
    tekst = tekst.split(",")
    dict_tekst = {}

    for i in tekst:
        dict_tekst[i] = tekst.count(i)
    for i in dict_tekst:
        print(f"{i}:{dict_tekst[i]}")

if q == 3:
    curses = {
        ' 880254 ': [' u123456 ', ' u383213 ', ' u234178 '],
        ' 822177 ': [' u123456 ', ' u223416 ', ' u234178 '],
        ' 822164 ': [' u123456 ', ' u223416 ', ' u383213 ', ' u234178 ']}

    for c in curses:
        print(c)
    for s in curses[c]:
        print(s, end=" ")
    print()

if q == 4:
    curses = {
        ' 880254 ':
            {"naam": " Onderzoeksvaardigheden   Data   Processing", "ects": 3,
             " studenten": {' u123456 ': 8, ' u383213 ': 7.5, ' u234178 ': 6}},
        ' 822177 ':
            {"naam": "Logica", "ects": 6,
             " studenten": {' u123456 ': 5, ' u223416 ': 7, ' u234178 ': 9}},
        ' 822164 ':
            {"naam": " Computer   Games", "ects": 6,
             " studenten": {' u123456 ': 7.5, ' u223416 ': 9}}}

    for c in curses:
        print("{}:   {}   ({})".format(c, curses[c]["naam"], curses[c]["ects"]))
    for s in curses[c][" studenten"]:
        print("{}:   {}".format(s, curses[c][" studenten"][s]))
    print()

if q == 5:

    numlist = []
    for i in range(10000):
        numlist.append(i)

    start = datetime.now()
    teller = 0
    for i in range(10000, 20000):
        if i in numlist: teller += 1
    eind = datetime.now()

    print("{}.{}   seconden   om   {}   nummers   te   vinden".format(
        (eind - start).seconds, (eind - start).microseconds, teller))

if q == 5:
    # Oefening 13.2
    tekst = """Kapper   Knap ,   de   knappe   kapper ,   knipt   en   kapt   heel knap ,   maar   de   knecht   van  
     kapper   Knap ,   de   knappe   kapper ,   knipt en   kapt   nog   knapper   dan   kapper   Knap ,   de   knappe 
       kapper. """


    dict_tekst = {}# Feee variable
    tekst = tekst.lower() # I set the text in lower
    tekst = tekst.split('  ') # split command to catch the words that has a space between them

    for i in tekst: # Loop catch the words in tekst
        dict_tekst[i] = tekst.count(i) #automaticly add the words with their respective numbers

    print(dict_tekst)#Print

if q == 6:
    # Oefening 13.2
    films = {"Monty   Python   and   the   Holy   Grail": [9, 10, 9.5, 8.5, 3, 7.5, 8] , "Monty   Python ' s   Life   of   Brian":[10, 10, 0, 9, 1, 8, 7.5, 8, 6, 9],
             "Monty   Python ' s   Meaning   of   Life":[7, 6, 5],
             "And   Now   For   Something   Completely   Different":[6, 5, 6, 6]}# I have setted all the votes in their respectives films

    name_films = list(films.keys())# Command that allows me to get all the movies names.
    dict_films = {} # A free dict variable to later use it to store the data.
    counter = 0 # Counter
    for i in name_films: #Loop that takes all the names from the new list
        dict_films[i] = f"{round(sum(films[i]) / len(films[i]),1)}" # here i sad with store each movie from i in the free dict variable and store also the sum of those votes
        print(f"{i} : {dict_films[i]}")# print the free variable that now has all the data that we need.


    #In oefening 3  we will use the dict commaand to store all the information van the books


if q == 7:
    engels_nederlands = {"last": "laatste", "week": "week", "the": "de",
                         "royal": " koninklijk", " festival": "feest", "hall":"hal",
                         "saw": "zaag", "first": "eerst", "performance": "optreden",
                         "of": "van", "a": "een", "new": "nieuw", "symphony": "symphonie",
                         "by": "bij", "one": "een", "world": "wereld", "leading":
                        "leidend", "modern": "modern", "composer": "componist", " composers": " componisten",
                         "two":"twee","shed": "schuur", "sheds": "schuren"}

    zin = "Last week The Royal Festival Hall saw the first performance of a new symphony by one of the world 's leading modern composers , Arthur Two-Sheds Jackson ."
    zin = zin.lower()
    zin = zin.split(" ")
    dict_zin = []
    print(zin)
    for zin in engels_nederlands.keys():
                dict_zin.append(zin)

    print(dict_zin)