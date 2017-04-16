# Project Makalu 
Im Zuge des neuen Online Shops der **anna group** wird auch ein neues Session Handling benötigt. Der hier vorliegende 
Code steht kurz vor dem produktiven Livegang. Trotz der rapiden Entwicklung machen sich erhebliche Zweifel breit, ob
 nicht etwas wichtiges vergessen wurde?

### Motivation
Moderne WebApps verfügen teilweise über eine enorme Komplexität. Um den Kunden vor mögliche Angriffe zu schützen, benötigen unter anderem Requestsdie an eine WebApp gestellt werden eine Login-Session. Ein Request benötigt üblicherweise die Daten aus einer 
vorherigen Response (bspw. CSRF tokens). Die empfangenen Daten in einem Teilrequest, können auch einige Requests später noch 
benötigt werden (bspw. während des Checkout Prozesses in einem Webshop). Dies macht den Einsatz von "unique" Namen/IDs 
notwendig, während der Erstellung eines Requests. 

**Randbemerkung**: Das Fuzzing bspw. im Kontext eines CSRF tokens, erzeugt eine Vielzahl von Daten sowie Aufrufe innerhalb der WebApplikation. Dadurch kann im Falle eines Angriffs, die Performance der gesamten Applikation beeinträchtigen. Die Performance selbst,
steht in diesem Penetration Tests NICHT im Fokus, kann aber je nach gewählter Fuzzing-Methode zu einem "Problem" für den Angriff werden. 

## Problemstellung:
 Helfe der **anna group** durch einen Penetration Test die Sicherheit des Session Handlings zu prüfen. Um diesen Wunsch
 nachzukommen muss zunächst die Applikation installiert und betriebsbereit gemacht werden. Hierbei hilft 
 sicherlich folgende Anleitung weiter:
 
##### Installation der WebApp
```
1. Install Python 3.4 + virtualenv
2. (optional) virtualenv -p python3 pyenv
3. (optional) . pyenv/bin/activate
4. pip3 install flask
```

##### Starten der WebApp
```
1. (optional, wenn in virtualenv) . pyenv/bin/activate
2. python3 ProjectMaklulaApp.py
3. Öffne die URL: http://localhost:8001 m Browser 
```

#####  [Credentials](https://www.heise.de/security/meldung/hallo-ist-meistgenutztes-deutsches-Passwort-auf-Platz-zehn-steht-ficken-3579567.html): user/hallo 

## Durchführung des Penetration Tests
Für den Test existiert folgende Use Cases. Zur Durchführung des Penetration Tests kann das File 
"/doc/Burp.burp-projectopts.json" mittels [Burp](https://portswigger.net/burp/freedownload/) als Projekt 
geladen werden. In der JSON-Datei sind alle "session handling rules" enthalten, um die nachfolgenden Challenges
zu lösen. Die Challenges können natürlich auch mit anderen Tools wie bspw. OWASP ZAP gelöst werden.

#### Use Case: Bau dir einen eigenen CSRF Token
```
Challenge: Der Übertragene CSRF Token muss übereinstimmen und mit jedem POST Request übertragen werden

Lösung:
* Capture des Requests von einem bestehenden CSRF Token
* Erstelle eine "Run a Macro" session handling Regel
    * Der Scope liegt auf den Parameter des CSRF Tokens
    * Update den CSRF Token NUR im aktuell gestellten Request
```


#### Use Case: Behalte die Login-Session offen
```
Challenge: Mit einer Wahrscheinlichkeit von 5% beenden WebApplikationen die Login-Session

Lösung:
* Capture des Login-Requests in einem Makro
* Erstelle eine "Check Session is Valid" Regel
    * Erstelle einen Request
    * Prüfe den Response-Body nach einem Benutzernamen für die gültige Session
    * Alternativ: Prüfe die Umleitung der Login-URL (die Session muss für diesen Fall invalide sein)
    * Spiele das aufgezeichnete Makro ab bei der Invalidierung der Session
```
    
#### Use Case: Begehe Bestellbetrug 
```
Challenge: Führe multiple Requests durch bis die finale Bestellbestätigung erscheint

Lösung:
* Führe alle Requests durch bis einer mit Hilfe eines Makros gefuzzed werden kann.
* Finalisiere den Bestellbetrug mit einem "Run a Post-Request Macro", dass den aktuellen Request zurück gibt
* Definiere einen engen Definitionsbereich (URL, Parameter)
```

#### Use Case: Löschen von Eingefügten Daten
```
Challenge: Aktuell sind nur drei Einträge erlaubt. Um dies etwas gerechter zu machen, soll die "add" 
Funktionalität gefuzzed werden

Lösung:
* Lösche nachträglich gerade hinzugefügte Notizen 
    * Erstelle ein POST-request Makro, dass die Object ID extrahiert und anschließend den Löschvorgang anstößt.
```
