### Razvoj v lokalnem kubernetes (k8s) okolju

Mapa vsebuje preprosto [flask](https://flask.palletsprojects.com/en/1.1.x/) aplikacijo `app.py`, ki predstavlja API za merilna mesta. Aplikacija sprejema GET poizvedbe na poti /api/v1/idmms, kjer sprejem  parameter `idmm` (ID merilnega mesta). Sprejeti idmm uporabi v SQL poizvedbi, s katero iz baze pridobi ostale podatke o merilnem mestu in jih posreduje v obliki JSON v odgovoru na prejeto GET poizvedbo. 

Ker bomo v produkciji poganjali aplikacije na kubernetes gruči (Openshift/OKD), je smiselno lokalni razvoj izvajati na kar se da podobnem okolju. V mapi so poleg aplikacije prisotni kubernetes manifesti, ki definirajo način zgona aplikacije na kubernetes platformi. Poleg manifestov za aplikacijo, so še manifesti za zagon lokalne infrastrukturo, ki jo potrebuje aplikacija. V našem primeru je to podatkovna baza postgres s postgis ektenzijo, poleg tega pa si bomo zagnali tudi spletno aplikacijo [Adminer](https://www.adminer.org/), ki nam bo omogočila, da skozi uporabniški vmesnik pregledujemo podatkovno bazo. 

Pri razvoju na lokalnem kubernetes okolju si bomo pomagali z orodjem [Tilt](https://tilt.dev/). 

##### Postavitev lokalnega kubernetes okolja 

Po pregledu različnih [možnosti](https://docs.tilt.dev/choosing_clusters.html), predlagam uporabo orodja [k3d](https://k3d.io/) za postavitev lokalnega okolja.  Argumenti za uporabo so:
- hitra postavitev in izbris okolja (znotraj docker vsebnika)
- integriran lokalen register slik za vsebnike
- integriran ingress kontroler

Predno postavimo lokalno kubernetes okolje bomo inštalirali tudi CLI orodje [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/), ki nam omogoča delo s kubernetes gručo.

```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```


Navodila za inštalacijo in uporabo orodja [k3d](https://k3d.io/)  najdemo na omenjeni povezavi. Inštalacija:

```
wget -q -O - https://raw.githubusercontent.com/rancher/k3d/main/install.sh | bash
```
Zagon lokalnega registra:
```
k3d registry create myregistry.localhost --port 5111
```
Zagon kubernetes okolja z vključitvijo registra in ingress kontrolerja:
```
k3d cluster create newcluster --registry-use k3d-myregistry.localhost:5111 --api-port 6550 -p "8081:80@loadbalancer"

```

Sedaj lahko pogledamo osnovne informacije o kubernetes gruči:
```
kubectl cluster-info
```

##### Način dela

Kaj potrebujemo za zagon aplikacije v kubernetes gruči:
1. [Kodo aplikacije](app.py)
2. [Dockerfile](Dockerfile) za izgradnjo slike
3. Manifeste, večje število .yaml datotek


Zaganjanje aplikacije v kubernetes gruči zahteva izvedbo sledečih korakov:
1. Izgradnja slike za vsebnik
2. Potisk slike vsebnika v register slik
3. Zagon vsebnika v gruči (preko manifestov)

Zato, da nam ob vsaki spremebi kode teh korakov ni potrebno izvajati ročno si lahko pri razvoju pomagamo z orodjem [Tilt](https://tilt.dev/), ki bo te korake za nas izvajal na samodejen način.

[Inštalacija](https://docs.tilt.dev/install.html) orodja Tilt:
```
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

Ko imamo orodje inštalirano lahko pogledamo način uporabe za primer [Python+Flask](https://docs.tilt.dev/example_python.html)

Korake, katere želimo, da jih za nas izvaja Tilt definiramo v datoteki [Tiltfile](Tiltfile). Ker smo uporabil orodje k3d nam ni potrebno posebej specificirati, da želimo uporabiti to gručo, Tilt bo sam uporabil gručo, ki je namenjena lokalnemu razvoju.

Zagon orodja: 
```
tilt up
```

Sedaj lahko začnemo s pisanjem kode, Tilt pa bo samodejno spravljal v kubernetes gručo nove verzije kode.


##### Možna težava
Jaz sem naletel pri delu na naslednjo težavo:
[Pods evicted due to lack of disk space](https://k3d.io/faq/faq/#pods-evicted-due-to-lack-of-disk-space),
ki sem jo razrešil, tako da smem pobrisal slike in vsebnike, ki jih nisem uporabljal z `docker system prune`