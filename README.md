# **Broker MQTT v5**

## Introducere

MQTT reprezintă un protocol de transport pentru mesaje, fundamentat pe arhitectura TCP/IP și conceptul eficient de publish/subscribe. Conceput inițial în 1999 de către Andy Stanford-Clark (IBM) și Arlen Nipper (Arcom, acum Cirrus Link), protocolul a fost dezvoltat pentru a satisface cerințele de conectivitate în medii cu resurse limitate, cum ar fi conductele de petrol, unde era esențială minimizarea consumului de energie și a lățimii de bandă disponibile.
Un aspect semnificativ al acestui protocol constă în decuplarea completă între entitățile care publică mesaje (publishers) și cele care le recepționează (subscribers), realizată prin intermediul unui broker. Broker-ul constituie nucleul oricărui sistem publish/subscribe, gestionând recepționarea mesajelor, filtrarea acestora, asignarea abonaților la diferite topic-uri și distribuirea mesajelor către acești abonați.
Rolul central al broker-ului se extinde și în domeniul autentificării și autorizării clienților. Prin urmare, este crucial ca broker-ul să fie extrem de scalabil, integrabil în sistemele backend, ușor de monitorizat și rezistent la eșec.
Procedura de inițiere a unei conexiuni implică trimiterea unui mesaj CONNECT din partea clientului către broker, urmat de un mesaj CONNACK emis de către broker împreună cu un cod de stare corespunzător. Această interacțiune constituie punctul de pornire al comunicării în cadrul sistemului bazat pe protocolul MQTT.



![image](https://github.com/TUIASI-AC-IoT/proiectrcp2023-echipa-4-2023/assets/99644342/152134b3-1ea3-4e99-9393-b67c8725a270)

## Keep Alive 

Mecanismul Keep Alive asigură menținerea deschisă a conexiunii între broker și client, asigurându-se că ambii sunt conștienți de starea conexiunii. Acest proces se realizează prin utilizarea pachetelor PINGREQ și PINGRESP.
PACHETELE PINGREQ sunt trimise la intervale predefinite de timp atunci când nu se detectează nicio transmitere de pachete între client și broker. Aceste pachete, fără un conținut util (payload), au rolul de a menține conexiunea clientului.
PACHETELE PINGRESP sunt răspunsuri corespunzătoare la PINGREQ și, asemenea acestora, nu conțin payload. Ele confirmă clientului că brokerul este încă conectat și activează un schimb periodic pentru a menține starea conexiunii.
În absența unui schimb regulat de pachete, dacă perioada predefinită pentru transmiterea PINGREQ expiră fără a se detecta activitate, brokerul deconectează automat clientul. Similar, dacă clientul nu primește în timp util un răspuns la PINGREQ, este recomandabil să încheie conexiunea.

## Last Will

Mecanismul "Last Will" reprezintă o caracteristică esențială a protocolului MQTT, permitând clienților tip publisher să trimită un mesaj predefinit abonaților în situația în care aceștia sunt deconectați în mod forțat, fără a emite un pachet de tip DISCONNECT. Acest mesaj, fără proprietăți specifice, este similar unui mesaj obișnuit, conținând un topic, un nivel de calitate al serviciului (QoS), payload și poate fi definit de către orice client la stabilirea conexiunii cu brokerul.
Scenariile potrivite pentru utilizarea mesajului "Last Will" includ:
-	Deconectarea clientului ca rezultat al mecanismului "Keep Alive".
-	Situația în care clientul nu trimite pachetul DISCONNECT la închiderea conexiunii.
-	Situația în care brokerul închide conexiunea din cauza unei erori de protocol.
Această facilitate asigură o notificare coerentă a stării deconectării către abonații relevanți, fără necesitatea intervenției manuale în astfel de situații, contribuind la o gestionare mai eficientă a stării conexiunii între clienți și brokerul MQTT.

## Quality of Service

### QoS 0

Nivelul minim al calității serviciului este QoS 0, denumit și "cel mult o dată." La acest nivel, asigurăm că mesajul publicat de către publisher este transmis, în cel mult o singură încercare, către toți subscriberii interesați. Practic, acest nivel de serviciu implică trimiterea a un singur pachet de informații fără a aștepta o confirmare formală a recepției din partea subscriberilor.

### QoS 1

La nivelul 1 al calității serviciului QoS, se asigură că mesajul transmis ajunge la toți subscriberii, cel puțin o dată. Spre deosebire de QoS 0, la acest nivel se așteaptă o confirmare formală a recepției. În cazul protocolului MQTT 3.1.1, în situația în care nu se primește o confirmare într-un interval rezonabil, mesajul este retransmis, cu dezavantajul potențialei duplicări a mesajelor.
Cu apariția protocolului MQTT versiunea 5, s-a recunoscut că retransmiterea mesajelor poate duce la aglomerări de pachete și nu este întotdeauna cea mai eficientă soluție. Conceptul de "cel puțin o dată" este încă respectat, dar, în locul retransmiterii directe a mesajului, brokerii și clienții gestionează situația prin retrimiterea unor pachete speciale. Această abordare oferă o alternativă mai eficientă la retransmiterea integrală a mesajelor, păstrând totodată asigurarea că fiecare subscriber primește informația cel puțin o dată.

### QoS 2

QoS 2 reprezintă cel mai înalt nivel de serviciu în cadrul protocolului MQTT, garantând că fiecare mesaj este primit exact o singură dată de către destinatari. Chiar dacă oferă cea mai mare siguranță, nivelul QoS 2 este și cel mai lent.
Procesul la nivel QoS 2 începe atunci când un receptor primește un pachet PUBLISH de la un expeditor. După ce procesează mesajul de publicare, receptorul confirmă expeditorului printr-un pachet PUBREC. În situația în care expeditorul nu primește acest pachet PUBREC de la receptor, va retransmite pachetul PUBLISH cu un steag duplicat (DUP) până când obține o confirmare.
Expeditorul stochează pachetul PUBREC primit de la receptor și răspunde cu un pachet PUBREL. Odată ce receptorul primește pachetul PUBREL, răspunde cu un pachet PUBCOMP. Între timp, expeditorul stochează o referință la identificatorul pachetului PUBLISH original. Acest pas este crucial pentru a evita procesarea mesajului de două ori.
Procesul se finalizează atunci când receptorul trimite pachetul PUBCOMP înapoi către expeditor, semnalând astfel încheierea procesării. Această metodă asigură o livrare exactă și o gestionare corectă a mesajelor, împiedicând procesarea duplicată a aceluiași mesaj.

## Stocare sesiuni cu posibilitatea de expirare/ștergere

În cadrul pachetului CONNECT, un client care se conectează are posibilitatea să configureze un interval de expirare a sesiunii în secunde. Acest interval determină perioada în care brokerul menține informațiile referitoare la sesiunea respectivului client după ce acesta se deconectează. Atunci când intervalul de expirare a sesiunii este setat la 0 și pachetul CONNECT nu conține o valoare de expirare, informațiile referitoare la sesiune sunt șterse imediat ce conexiunea la rețea a clientului se închide.

## Bibliografie

- https://mqtt.org/?fbclid=IwAR3TXXPFza54hpk1keqAlGLtGgRCniL2mRXaQQLYrKpr7RlMIJOSEABWljM
- https://www.hivemq.com/mqtt-5/
- https://www.hivemq.com/mqtt-essentials/
- https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
