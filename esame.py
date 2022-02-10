#Compito d'esame di Penzo Nicole frequentante il corso di AIDA per l'anno accademico 2021/2022.

#importo datetime dalla libreria datetime
from datetime import datetime


#creo una classe per gestire le eccezioni e gli errori futuri
class ExamException(Exception):
    pass

#creo la classe (madre) richiesta per effettuare l'esercizio, qui andrò a definire il file 
class CSVFile():

    #istanzio il nome del file tramite il costruttore (__init__)
    def __init__(self, name):
        
        #assegno il nome del file
        self.name = name

        #controllo che il file sia una stringa 
        if not isinstance(self.name, str):
            raise ExamException('Il nome del file non è una stringa')

        #creo una variabile di supporto
        lunghezza_file = 0

        #per operare sul file lo devo prima aprire
        file = open(self.name, 'r')

        #leggo il file riga per riga
        for riga in file:
            lunghezza_file = lunghezza_file + 1

        #se la lunghezza del file risulta avere meno di una riga in senso stretto vuol dire che il file è vuoto, alzo una exception
        if lunghezza_file < 1:
            raise ExamException('Il file è vuoto')

    #creo il metodo get_data()
    def get_data(self):

        #setto la lettura del file a True
        self.read=True 

        #provo ad aprire il file riga per riga
        try:
            lista=open(self.name, 'r')
            lista.readline()

        #se non è possibile aprire o leggere il file dato, setto la lettura del file a False e stampo un messaggio di errore
        except ExamException:
              self.read=False
              print('Errore in apertura del file')

        #controllo quindi che il file sia leggibile utilizzando un if, se non è possibile stampo un messaggio di errore altrimenti vado a vanti e continuo a lavorare sui dati del file
        if not self.read:
            raise ExamException ('Non è possibile leggere o aprire il file')
        
        else:
            #inizio a creare una lista per salvare i dati futuri
            lista_supporto = []
            #apro il file in maniera corretta e lo assegno ad una variabile chiamata file
            file = open(self.name, 'r')


            #voglio leggere il file riga per riga, utilizzo un ciclo for
            for riga in file:
                
                #separo gli elementi del file tramite il metodo .split() e li divido in base alle virgole
                elementi = riga.split(',')
                
                #per avere in seguito una lista di dati più pulita e ordinata rimuovo gli spazi e il carattere di new line tramite il metodo .strip()
                elementi[-1] = elementi[-1].strip()
    
                #dato che non voglio processare l'intestazione
                if elementi[0] != 'date':

                    #saltiamo le parti della lista con meno di due argomenti in senso stretto (ovvero se nelle liste della lista di liste mancano i dati dei passeggeri, l'anno-mese o entrambi)
                    if len(elementi)<2:
                        continue

                    #rimuovo gli spazi in eccesso dagli elementi con .strip()
                    elementi[0] = elementi[0].strip()
                    elementi[1] = elementi[1].strip()

                #mi assicuro che il primo elemento delle liste annidate (elements[0]) possa essere convertito in datetime
                try:
                    datetime.strptime(elementi[0], '%Y-%m')  
                #in caso contrario continuo
                except:
                    continue

                #provo a trasformare tutti gli elementi da stringhe a interi
                try:
                    elementi[1] = int(elementi[1])
                #se non è possibile assegno None all'elemento non convertibile
                except:
                    elementi[1] = None 
                
  
                #aggiungo gli elementi delle sottoliste precedentemente modificati in una lista, se ho più di due elementi, aggiungo solo il secondo tramite il metodo .append()
                lista_supporto.append(elementi[:2])
            
        #chiudo il file
        file.close()
        #ritorno la lista di dati ottenuta
        return lista_supporto


#creo la classe CSVTimeSeriesFile, figlia della classe CSVFile
class CSVTimeSeriesFile(CSVFile):

    #nuovo metodo get_data() che riscriverà il metodo omonimo della classe madre
    def get_data(self):
         
        #richiamo tramite il metodo super() il metodo get_data() della classe madre e l'assegno ad una variabile per utilizzarla in seguito
        lista_super_get_data = super().get_data()
    
        #assegno ad una variabile il primo elemento della prima lista presente nella lista_super_get_data
        primo_dato= lista_super_get_data[0][0]
        
        #controllo che l'ordine degli anni sia corretto

        #per ogni elemento presente nella lista di liste lista_super_get_data, considero i primi elementi delle sottoliste
        for elementi in lista_super_get_data [1:]:

            #se i primi elementi delle sottoliste sono maggiori o uguali al primo elemento della prima sottolista alzo una eccezione poichè vuol dire che i dati non sono in ordine temporale
            if primo_dato >= elementi[0]:
                raise ExamException('Il file non è ordinato  correttamente')

            #assegno il primo elemento alla variabile
            primo_dato = elementi[0]
        #ritorno la lista corretta 
        return lista_super_get_data


#ora definisco il metodo che conterrà l'algoritmo principale di calcolo della differenza media
def compute_avg_monthly_difference(time_series, first_year, last_year):

    #controllo che gli anni forniti in input siano stringhe
    if not isinstance(first_year, str) and not(last_year , str):
        raise ExamException('I dati inseriti non sono stringhe')

    #controllo che quando mi vengono forniti gli anni in input non mi vengano date stringhe vuote 
    if first_year == '' :
        raise ExamException('Il primo intervallo è una stringa vuota')
    if last_year == '' :
        raise ExamException('Il secondo intervallo è una stringa vuota')

    #controllo con il metodo .isdigit() che le stringhe siano composte soltanto da numeri
    if not first_year.isdigit() and not last_year.isdigit():
        raise ExamException('I dati forniti non contengono numeri')
    
    #utilizzo una variabile temporanea temp per scambiare l'anno iniziale e l'anno finale nel caso questo ultimo sia maggiore del primo in input
    if int(last_year) < int(first_year):
        temp=first_year
        first_year=last_year
        last_year=temp
    
    #controllo che il contenuto della time_series siano liste
    if not isinstance(time_series, list):
        raise ExamException('time_series non è una lista')

    #controllo che la lista non sia vuota
    if time_series == [] :
        raise ExamException('La lista time_series non ha elementi')


    #converto first_year e last_year in interi
    first_year = int(first_year)
    last_year = int(last_year)
    
    #numero di anni su cui dovrò fare la media (intervallo di anni da considerare)
    intervallo_anni = last_year-first_year

    #creo una lista di liste che conterrà i dati dei passeggeri, la quale conterrà a sua volta tante liste quanti sono gli anni che decido di prendere in considerazione 
    lista_passeggeri = []

    for years in range(intervallo_anni+1):

        #lista_di_null è una lista che contiene tante liste quanti sono gli anni che ho preso in considerazione
        lista_di_null = [None, None, None, None, None, None, None, None, None, None, None, None]

        #aggiungo gli anni alla fine della lista in modo che ogni lista abbia l'anno corrispondente
        lista_di_null.append(first_year + years)
        #aggiungo con .append() i dati dei passeggeri alla lista_passeggeri
        lista_passeggeri.append(lista_di_null)

    #controllo tutti gli elementi della lista_passeggeri
    for componenti in lista_passeggeri:

        #controllo gli elementi presenti nella time_series ritornata dalla get_data()
        for elementi in time_series:

            #divido il primo argomento anno-mese usando il metodo .split() e basandomi sul "-"
            dati = elementi[0].split('-')

            #dato che ho diviso il mese dall'anno, posso confrontare i dati degli anni con i dati presenti nella lista_passeggeri ( in particolare se il valore convertito a intero degli anni, passati come stringa tramite time_series della get_data(), coincidono con il primo elemento della lista_passeggeri)
            if int(dati[0]) == componenti[-1]:
 
                #ora nel caso in cui gli anni dei dati divisi tramite .split() sono gli stessi presenti nella lista_passeggeri assegnerò il valore dei passeggeri al loro indice corrispondente. #l'indice "elementi[1]"" corrisponde al mese di ogni dato
                componenti[int(dati[1])-1] = elementi[1]

    #ora inizio a sommare le varie differenze tra i dati di ogni anno, nel caso mi capiti un None, farò continuare il programma con continue

    #preparo una lista vuota per contenere i valori della differenza media finale
    lista_finale = []
    #variabili di supporto che userò come contatori durante il processo di calcolo
    mesi = 0  
    somme = 0 
    #uso un while che si fermerà quando il contatore "mesi" supererà il numero di mesi dell'anno in senso stretto
    while mesi < 12:

        #ciclo for per ogni anno nel range dell'intervallo di anni prima calcolato
        for anni in range(intervallo_anni):

            #accedo alle liste annidate come fossero matrici, il primo indice "anni" mi fa accedere ad una specifica sottolista mentre il secondo indice "mesi" mi fa accedere al numero di passeggeri in uno specifico mese
            #nel caso uno dei due elementi o entrambi corrispondano a None, assegnerò alla differenza zero
            if lista_passeggeri[anni+1][mesi] == None or lista_passeggeri[anni][mesi] == None:
                differenze = 0

            #in caso contrario assegnerò la differenza alla variabile differenza  
            else:
                differenze = lista_passeggeri[anni+1][mesi] - lista_passeggeri[anni][mesi]
            
            #sommo al contatore della somma i valori delle differenze 
            somme= somme + differenze

        #aggiungo questi valori alla lista di valori finali 
        lista_finale.append(somme)

        #per l'iterazione, devo ri-assegnare zero alla somma e incrementare di uno il mese che sto considerando
        somme= 0
        mesi = mesi + 1

    #concludo il calcolo facendo la media della somma delle differenze. divido quindi la lista finale per il numero di anni calcolato in precedenza
    lista_finale = [s /intervallo_anni for s in lista_finale]
    
    #ritorno la lista finale
    return lista_finale

