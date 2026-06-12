# carricato_WeatherForecast_API 


***Studente:*** **Marco Carricato**, ***Matricola:*** **7135631** \
***Tipo di progetto:*** **REST API**  
***Framework e Librerie:*** **Django, Django REST Framework (DRF), SimpleJWT, SQLite**


## Descrizione del progetto
Applicazione back-end per la consultazione delle previsioni meteo e la gestione degli utenti. Il sistema include: un 
tracciamento giornaliero delle richieste per limitare gli abusi da parte degli utenti pubblici; un sistema di abbonamento 
Premium che permette il salvataggio delle richieste, la consultazione dello storico e l'accesso alle statistiche dell'
account; un'autenticazione sicura tramite JWT e un pannello di amministrazione REST per i moderatori. I dati meteo sono 
simulati in modo coerente in base a città e data.


## Funzionalità implementate
### Anonimo / Utente Standard:
- Auto-registrazione al servizio e login (tramite JWT)
- Richiesta dati meteo simulati per città e data
- *Rate limiting*: massimo 5 richieste al giorno tracciate per Indirizzo IP o Sessione
- Possibilità di fare upgrade dell'account (passare ad account Premium)
- Validazione rigorosa degli input e gestione degli errori

### Utente Premium:
- Richiesta dati meteo senza limiti (nessun rate limit)
- Salvataggio automatico delle query meteo in un database dedicato (storico)
- Consultazione della propria lista di ricerche salvate
- Visualizzazione delle statistiche del proprio storico
- Possibilità di fare downgrade dell'account (passare ad account Standard)

### Moderatore (Staff):
- Gestione degli utenti tramite API (CRUD completo)
- Possibilità di modificare i dati degli utenti, assegnare il ruolo Premium, bannare o eliminare gli account
- *Sicurezza:* Un moderatore non può nominare altri moderatori

### Admin Supremo (Superuser):
- Accesso completo al database tramite interfaccia grafica Django Admin
- Nominazione dei Moderatori


## Istruzioni per l'installazione locale
1. ### Clonazione della repository sul computer:
   ```bash
   git clone https://github.com/marcocarri/carricato_WeatherForecast_API
   cd carricato_WeatherForecast_API
   ```
2. ### Creazione dell'ambiente virtuale e attivazione:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate
   ```
3. ### Installazione delle dipendenze funzionali:
   ```bash
   pip install -r requirements.txt
   ```   
4. ### *Opzionale (il database è già incluso)* - Applicazione delle migrazioni:
   ```bash
   python manage.py migrate
   ```
5. ### Avvio del server locale:
   ```bash
   python manage.py runserver
   ```


## Database incluso e Account Demo
Il file del database SQLite incluso (*db.sqlite3*) è pre-popolato e contiene già i dati di base e gli account per 
testare immediatamente il progetto. Dato che il sistema utilizza i JWT, è necessario effettuare il Login via API con 
uno di questi account per generare un token valido.

**Admin**( is_superuser=*True*, is_staff=*True*, is_active=*True*, is_premium=*True*)**:**
- username: *admin_demo*, email: *admin@demo.com*, password: *admin_12345*

**Moderatori**(is_superuser=*False*, is_staff=*True*, is_active=*True*, is_premium=*True*)**:**
- username: *moderatore1_demo*, email: *moderatore1@demo.com*, password: *mod1_12345*
- username: *moderatore2_demo*, email: *moderatore2@demo.com*, password: *mod2_12345*

**Utenti Premium**(is_superuser=*False*, is_staff=*False*, is_active=*True*, is_premium=*True*)**:**
- username: *utente1_demo*, email: *utente1@demo.com*, password: *ut1_12345*
- username: *utente2_demo*, email: *utente2@demo.com*, password: *ut2_12345*

**Utenti Standard**(is_superuser=*False*, is_staff=*False*, is_active=*True*, is_premium=*False*)**:**
- username: *utente3_demo*, email: *utente3@demo.com*, password: *ut3_12345*
- username: *utente4_demo*, email: *utente4@demo.com*, password: *ut4_12345*

**Utenti Bannati**(is_superuser=*False*, is_staff=*False*, is_active=*False*, is_premium=*False*)**:**
- username: *utente5_demo*, email: *utente5@demo.com*, password: *ut5_12345*


## Link di pubblicazione online
**URL Base dell'API pubblicata:** *marcocarri.eu.pythonanywhere.com*


## Endpoint dell'API REST
| **Metodo**          | **URL**                   | **Autenticazione** | **Ruoli permessi** | **Descrizione**                                                                                                                                                                                                                                                     |                                                                                         
|:--------------------|:--------------------------|:-------------------|:-------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POST                | /api/users/register/      | Nessuna            | Anonimo            | Registra un nuovo utente Standard                                                                                                                                                                                                                                   |            
| POST                | /api/users/login/         | Nessuna            | Tutti              | Genera Access e Refresh Token (JWT)                                                                                                                                                                                                                                 | 
| GET                 | /api/users/login/refresh/ | Nessuna            | Tutti              | Genera un nuovo Access Token usando il Refresh                                                                                                                                                                                                                      |   
| POST                | /api/users/upgrade/       | JWT (Bearer)       | Standard           | Promuove l'account a Premium                                                                                                                                                                                                                                        |
| POST                | /api/users/downgrade/     | JWT (Bearer)       | Premium            | Retrocede l'account a Standard                                                                                                                                                                                                                                      |
| GET/POST/PUT/DELETE | /api/users/manage/        | JWT (Bearer)       | Moderatore         | Gestione completa degli utenti (CRUD)                                                                                                                                                                                                                               |
| POST                | /api/weather/forecast/    | Nessuna/JWT        | Anonimo/Standard   | Genera previsione. Limitato a 5 chiamate/giorno per i non Premium                                                                                                                                                                                                   |            
| POST                | /api/weather/saved/       | JWT (Bearer)       | Premium            | Genera previsione e la salva nello storico dell'utente. Illimitato                                                                                                                                                                                                  | 
| GET                 | /api/weather/saved/       | JWT (Bearer)       | Premium            | Restituisce lo storico delle query salvate dall'utente                                                                                                                                                                                                              |   
| GET                 | /api/weather/stats/       | JWT (Bearer)       | Premium            | Restituisce statistiche aggregate sullo storico meteo                                                                                                                                                                                                               |

## Istruzioni per il Test (con HTTPie)
Per testare le API da terminale, è richiesto il pacchetto HTTPie installato:
```bash 
pip install HTTPie
``` 
È necessario sostituire `<TOKEN_...>` con i token di accesso reali generati sul momento e, per testare la versione online, 
`http://127.0.0.1:8000` con l'URL di deploy

1. ### Autenticazione e Account
   **Test Registrazione**
   ```bash
   http POST http://127.0.0.1:8000/api/users/register/ username="utente_test" email="utente@test.com" password="test_12345"
   
   # risposta attesa: 201 Created
   ```
   
   **Test Login (generazione token)**
   ```bash
   http POST http://127.0.0.1:8000/api/users/login/ username="utente_test" password="test_12345"
   
   # risposta attesa: 200 OK
   # restituisce: <TOKEN>, <TOKEN_REFRESH>
   ```
   **Test Refresh (ri-generazione token)**
   ```bash
   http POST http://127.0.0.1:8000/api/users/login/refresh/ refresh="<TOKEN_REFRESH>"
   
   # risposta attesa: 200 OK
   # restituisce: <TOKEN_NUOVO>
   ``` 
   **Test Upgrade (attivazione Premium)**
   ```bash
   #richiesta di upgrade con account Standard
   http POST http://127.0.0.1:8000/api/users/upgrade/ Authorization:"Bearer <TOKEN_STANDARD>"
   
   # risposta attesa: 200 OK
   # messaggio: "Congratulazioni! Ora sei un utente Premium. Hai accesso alle ricerche meteo illimitate e al salvataggio dello storico."
   # account promosso a Premium (is_premium=True)
   ```
   ```bash
   # richiesta di upgrade con account Premium
   http POST http://127.0.0.1:8000/api/users/upgrade/ Authorization:"Bearer <TOKEN_PREMIUM>"
   
   # risposta attesa: 400 Bad Request
   # messaggio: "Sei già un utente Premium!" 
   ```
   **Test Downgrade (annullamento Premium)**
   ```bash
   #richiesta di downgrade con account Premium
   http POST http://127.0.0.1:8000/api/users/downgrade/ Authorization:"Bearer <TOKEN_PREMIUM>"
   
   # risposta attesa: 200 OK
   # messaggio: "Hai disdetto l'abbonamento. Ora sei un utente Standard."
   # account retrocesso a Standard (is_premium=False)
   ```
   ```bash
   # richiesta di downgrade con account Standard
   http POST http://127.0.0.1:8000/api/users/downgrade/ Authorization:"Bearer <TOKEN_STANDARD>"
   
   # risposta attesa: 400 Bad Request
   # messaggio: "Il tuo account è già Standard."
   ```
2. ### Flusso meteo
   **Test richiesta dati meteo (anonimo)**
   ```bash
   http POST http://127.0.0.1:8000/api/weather/forecast/ city="Firenze" target_date="2026-06-10"
   
   # risposta attesa: 200 OK
   # restituisce: dati generati della previsione meteo
   ```
   **Test richiesta dati meteo (utente autenticato)**
   ```bash
   http POST http://127.0.0.1:8000/api/weather/forecast/ city="Firenze" target_date="2026-06-10" Authorization:"Bearer <TOKEN>"
   
   # risposta attesa: 200 OK
   # restituisce: dati generati della previsione meteo
   ```
   **Test blocco Rate Limit (dopo 5 richieste):**
   ```bash
   # ripetere uno dei due comandi precedenti per >5 volte consecutive
   # dalla richiesta >5:
   
   # risposta attesa: 429 Too Many Requests 
   # messaggio: "Limite giornaliero di 5 richieste raggiunto. Passa a Premium per richieste illimitate!"
   ```
   ```bash
   # esempio: per testare il funzionamento, 6 richieste fatte da anonimo
   http POST http://127.0.0.1:8000/api/weather/forecast/ city="Firenze" target_date="2026-06-10"
   http POST http://127.0.0.1:8000/api/weather/forecast/ city="Firenze" target_date="2026-06-10"
   http POST http://127.0.0.1:8000/api/weather/forecast/ city="Firenze" target_date="2026-06-10"
   http POST http://127.0.0.1:8000/api/weather/forecast/ city="Firenze" target_date="2026-06-10"
   http POST http://127.0.0.1:8000/api/weather/forecast/ city="Firenze" target_date="2026-06-10"
   http POST http://127.0.0.1:8000/api/weather/forecast/ city="Firenze" target_date="2026-06-10"
   ```
3. ### Flusso meteo (premium)
   **Test salvataggio richiesta dati meteo:**
   ```bash
   http POST http://127.0.0.1:8000/api/weather/saved/ city="Firenze" target_date="2026-06-10" Authorization:"Bearer <TOKEN_PREMIUM>"
   
   # risposta attesa: 201 Created
   # restituisce: dati generati della previsione meteo
   # dati salvati nello storico
   ```
   **Test visualizzazione storico:**
   ```bash
   http GET http://127.0.0.1:8000/api/weather/saved/ Authorization:"Bearer <TOKEN_PREMIUM>"
   
   # risposta attesa: 200 OK 
   # restituisce: lista delle richieste salvate (JSON)
   ```
   **Test visualizzazione statistiche:**
   ```bash
   http GET http://127.0.0.1:8000/api/weather/stats/ Authorization:"Bearer <TOKEN_PREMIUM>"
   
   # risposta attesa: 200 OK
   # restituisce: statistiche (dati aggregati) dell'account
   ```
   **Test permessi (account Standard NON può effettuare operazioni Premium):**
   ```bash
   http GET http://127.0.0.1:8000/api/weather/saved/ Authorization:"Bearer <TOKEN_STANDARD>"
   
   # risposta attesa: 403 Forbidden
   # messaggio: "Accesso negato. Questa funzionalità è riservata agli utenti Premium."
   ```
4. ### Moderazioni utenti
   **Test lettura completa del database utenti:**
   ```bash
   http GET http://127.0.0.1:8000/api/users/manage/ Authorization:"Bearer <TOKEN_MODERATORE>"
   
   # risposta attesa: 200 OK 
   # restituisce: lista degli account (ogni account ha un ID identificativo)
   ````
   **Test modifica dati utente:**
   ```bash
   # esempio: uso l'ID=12 di utente_test (creato prima) e modifico username, email e is_premium
   http PATCH http://127.0.0.1:8000/api/users/manage/12/ username="modificato_test" email="modificato@test.com" is_premium=true Authorization:"Bearer <TOKEN_MODERATORE>"
   
   # risposta attesa: 200 OK
   # restituisce: dati dell'account aggiornati
   ```
   **Test ban utente (disattivazione account):**
   ```bash
   # esempio: uso l'ID=12 di modificato_test (ex utente_test, modificato sopra) (creato prima) e lo banno
   http PATCH http://127.0.0.1:8000/api/users/manage/12/ is_active=false Authorization:"Bearer <TOKEN_MODERATORE>"
   
   # risposta attesa: 200 OK
   # restituisce: dati dell'account aggiornati 
   
   # per sbannare un account si esegue la stessa operazione ma con is_active=true
   ```
   **Test account bannato non può operare:**
   ```bash
   # esempio: provo a fare il login con modificato_test (account bannato) (ex utente_test, modificato sopra) (creato prima)
   http POST http://127.0.0.1:8000/api/users/login/ username="modificato_test" password="test_12345"
   
   # risposta attesa: 401 Unauthorized 
   # messaggio: "No active account found with the given credentials"
   # QUALSIASI altra operazione fatta con un account bannato ottiene la stessa risposta, non è possibile effettuare NESSUNA operazione
   ```
   **Test eliminazione account:**
   ```bash
   # esempio: uso l'ID=12 di modificato_test (ex utente_test, modificato sopra) (creato prima)
   http DELETE http://127.0.0.1:8000/api/users/manage/12/ Authorization:"Bearer <TOKEN_MODERATORE>"
   
   # risposta attesa: 204 No Content
   # account eliminato dal DB definitivamente
   ```
   **Test RBAC (utente non-staff NON può accedere alla moderazione):**
   ```bash
   http GET http://127.0.0.1:8000/api/users/manage/ Authorization:"Bearer <TOKEN_NON_MODERATORE>"
   
   # risposta attesa: 403 Forbidden
   # QUALSIASI altra operazione riservata allo staff fatta con un account non-staff ottiene la stessa risposta, non è possibile effettuare NESSUNA operazione riservata allo staff con un account non-staff
   ```