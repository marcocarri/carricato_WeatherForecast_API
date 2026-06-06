# carricato_WeatherForecast_API 


***Studente:*** **Marco Carricato**, ***Matricola:*** **7135631** \
***Tipo di progetto:*** **REST API**  
***Framework usati:*** **Django, Django REST Framework (DRF)**


## Descrizione del progetto
Applicazione back-end che espone una REST API per la consultazione delle previsioni meteo. Il sistema include un 
tracciamento giornaliero delle richieste per limitare gli abusi da parte degli utenti pubblici e un sistema di profili 
Premium che permette il salvataggio e la consultazione illimitata della propria cronologia di ricerche. I dati meteo sono 
simulati in modo coerente in base a città e data.


## Funzionalità implementate
**Anonimo / User standard:**
- Richiesta dati meteo simulati per città e data
- Rate limiting: massimo 5 richieste al giorno tracciate per Indirizzo IP o Sessione
- Validazione rigorosa degli input (nome città, formato data)

**User premium:**
- Richieste meteo illimitate (nessun rate limit)
- Salvataggio automatico delle query meteo in un database dedicato (storico)
- Lettura della propria lista di ricerche salvate
- Autenticazione sicura tramite Token HTTP

**User Admin:**
- Gestione utenti e assegnazione ruoli (is_premium) tramite pannello Django Admin
- Generazione e revoca dei Token di accesso


## Istruzioni per l'installazione locale
1. **Clonazione della repository sul computer:**
   ```bash
   git clone https://github.com/marcocarri/carricato_WeatherForecast_API
   cd carricato_WeatherForecast_API
   ```
2. **Creazione dell'ambiente virtuale e attivazione:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate
   ```
3. **Installazione delle dipendenze funzionali:**
   ```bash
   pip install -r requirements.txt
   ```   
4. ***Opzionale (il database è già incluso)*** **- Applicazione delle migrazioni:**
   ```bash
   python manage.py migrate
   ```
5. **Avvio del server locale:**
   ```bash
   python manage.py runserver
   ```


## Database incluso e Account Demo
Il file del database SQLite incluso (*db.sqlite3*) è pre-popolato e contiene già i dati di base e gli account per 
testare immediatamente il progetto

**Accounts Demo disponibili:**
- **Admin** --> username: *admin_demo*, password: *admin12345*
- **Utente Premium** --> username: *premium_demo*, password: *premium12345*, token: *d8d64e8de083241b0bef5b2ce9b70e1bc71c1fef*, 
(Utente Premium, *is_premium=True*)
- **Utente Standard** --> username: *user_demo*, password: *user12345*, token: *b5dfddcabd8df020124f609a4a940d86bcd8aed9*, 
(Utente Standard, *is_premium=False*)


## Link di pubblicazione online
**URL Base dell'API pubblicata:** *marcocarri.eu.pythonanywhere.com*


## Endpoint dell'API REST
| **Metodo** | **URL**                | **Autenticazione** | **Ruoli permessi** | **Descrizione**                                                     | **Corpo della richiesta (esempio)**               | **Corpo della risposta (esempio)**                                                                                                 
|:-----------|:-----------------------|:-------------------|:-------------------|:--------------------------------------------------------------------|:--------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------|
| POST       | /api/weather/forecast/ | None               | Anonimo/Standard   | Genera previsione. Limitato a 5 chiamate/giorno per i non Premium.  | *{"city": "Roma", "target_date": "2026-07-12"}*   | *{"city": "Roma", "target_date": "2026-07-12", "temperature": 25.4, "weather_condition": "Soleggiato", "humidity": 60}*            
| POST       | /api/weather/saved/    | Token              | Premium            | Genera previsione e la salva nello storico dell'utente. Illimitato. | *{"city": "Milano", "target_date": "2026-08-15"}* | *{"id": 1, "city": "Milano", "target_date": "2026-08-15", "temperature": 28.1, "weather_condition": "Pioggia", "saved_at": "..."}* 
| GET        | /api/weather/saved/    | Token              | Premium            | Restituisce lo storico delle query salvate dall'utente              | *Nessuno*                                         | *[{"id": 1, "city": "Milano", ...}]*                                                                                               

## Istruzioni per il Test (con HTTPie)
Per testare le API da terminale, è richiesto il pacchetto HTTPie installato:
```bash 
pip install HTTPie
``` 
È necessario che il server sia in esecuzione (sostituire 127.0.0.1:8000 con il link di deploy per testare la versione online)
1. **Test Anonimo/Utente Standard (con Rate Limit)** \
   Ripetendo questo comando le prime 5 volte otteremo i dati meteo richiesti, mentre dalla sesta in poi si verifica il 
   blocco della richiesta e la risposta conterrà il messaggio di errore adeguato (*Errore 429 Too Many Requests*):
   ```bash
   # Anonimo
   http POST http://127.0.0.1:8000/api/weather/forecast/ city="Firenze" target_date="2026-06-10"
   # Utente Standard (con Token)
   http POST http://127.0.0.1:8000/api/weather/forecast/ city="Firenze" target_date="2026-06-10" Authorization:"Token b5dfddcabd8df020124f609a4a940d86bcd8aed9"
   ```
2. **Test Permessi (Utente Standard bloccato)** \
   Effettuando una richiesta concessa solo agli utenti premium, con il token di un account standard, l'accesso ci verrà 
   negato e otterremo come risposta il messaggio di errore adeguato (*403 Forbidden*):
   ```bash
   http GET http://127.0.0.1:8000/api/weather/saved/ Authorization:"Token b5dfddcabd8df020124f609a4a940d86bcd8aed9"
   ```
3. **Test Premium (Salvataggio e Lettura History)** \
   Tramite un utente premium, effettuiamo una (o più) richieste di salvataggio di dati meteo, che poi possiamo visualizzare 
   nella lista delle richieste salvate:
   ```bash
   # Salvataggio richiesta
   http POST http://127.0.0.1:8000/api/weather/saved/ city="Firenze" target_date="2026-06-10" Authorization:"Token d8d64e8de083241b0bef5b2ce9b70e1bc71c1fef"
   # Lettura Lista delle richieste salvate
   http GET http://127.0.0.1:8000/api/weather/saved/ Authorization:"Token d8d64e8de083241b0bef5b2ce9b70e1bc71c1fef"
   ```