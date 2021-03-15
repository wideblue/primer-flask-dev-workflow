### Razvoj v docker vsebniku

Mapa vsebuje preprosto [flask](https://flask.palletsprojects.com/en/1.1.x/) aplikacijo `app.py`, ki predstavlja API za merilna mesta. Aplikacija sprejema GET poizvedbe na poti /api/v1/idmms, kjer sprejem  parameter `idmm` (ID merilnega mesta). Sprejeti idmm uporabi v SQL poizvedbi, s katero iz baze pridobi ostale podatke o merilnem mestu in jih posreduje v obliki JSON v odgovoru na prejeto GET poizvedbo. 

Ker bomo aplikacijo v produkciji izvajali znotraj docker vsebnika, je lahko koristno, da v njem izvajamo tudi lokalen razvoj aplikacije. Pri tem si lahko pomagamo z ekstenzijo za Visual Studio Code (VSC)  [Remote development] (https://aka.ms/vscode-remote/download/extension), podrobna navodila pa najdete na povezavi [Developing inside a Container](https://code.visualstudio.com/docs/remote/containers). 

Docker vsebniki nam pri lokalnem razvoju pomagajo tudi s tem, da si lahko preprosto zaženemo lokalno infrastrukturo, ki jo potrebuje aplikacija. V našem primeru je to podatkovna baza postgres s postgis ektenzijo, poleg tega pa si bomo zagnali tudi spletno aplikacijo [Adminer](https://www.adminer.org/), ki nam bo omogočila, da skozi uporabniški vmesnik pregledujemo podatkovno bazo. Vse storitve, ki jih želimo zagnati v vsebnikih so definirane v datoteki `docker-compose.local.yml`. Vsebnik za našo aplikacio se bo zagnal iz slike, ki se bo zgradila iz datoteke `Dockerfile`, vsebnika za podatkovno bazo in aplikacijo Adminer pa iz standardnih slik, ki so gostovane na [dockerhub](https://hub.docker.com/r/postgis/postgis) registru.

Mapa vsebuje tudi "dump" tabele idmm v podmapi `db_data_dump`, ki ga lahko uporabimo za zapolnitev naše lokalne instance baze. Ta podmapa bo vnešena kot "volume" v vsebnik za bazo, kar bo olajšalo zapolnitev baze.

Potek dela: Sledimo navodilom [Developing inside a Container](https://code.visualstudio.com/docs/remote/containers#_quick-start-open-an-existing-folder-in-a-container) in odpremo obstoječo mapo v vsebniku, pri čemer izberemo zagon na podlagi Docker Compose datoteke, ko se nam pokaže ta opcija in potem izberemo vsebnik `simple-fask-api`.

Ko se nam zaženejo vsi vsebniki lahko z ukozom `docker exec -it <ime-nasega-vsebnika-bazo> bash` zaženemo 
bash lupino v vsebniku za bazo in potem z ukazom 
```
gunzip -c /db_data_dump/idmm.gz | psql postgres -U postgres
```
napolnimo bazo.

V terminalu znotraj VSC-ja lahko zaženemo našo aplikacijo z 
```
python app.py 
```
in na url-ju http://localhost:8000/api/v1/idmms?idmm=1958 testiramo delovanje aplikacije 
Adminer lahko najdemo na url-ju http://localhost:8080

##### OPOZORILO
Pri tem načinu dela sem naletel na eno pomakljivost in sicer, če nisem posebej definiral uporabnika v vsebniku, ki je enak uporabniku zunaj vsebnika, je bil uporabnik v vsebniku "root", zato je bil lastnik vseh datotek, ki so bile ustvarjene pri razvoju v vsebniku, root. 
Remote development issue updateRemoteUserUID for Docker Compose
https://github.com/microsoft/vscode-remote-release/issues/2228
https://github.com/microsoft/vscode-remote-release/issues/49#issuecomment-489105458

Zadevo sem rešil tako, da sem v `Dockerfile` dodal 
```
RUN addgroup --gid 1000 damjan \
&& adduser --disabled-password --gecos "" --uid 1000 --gid 1000 damjan
```
v `.devcontainer/devcontainer.json`
pa opcijo
```
"remoteUser": "damjan"
```
Za svoje primere morate uporabiti ime, uid, ime grupe, gid svojega uporabnika.  

