#Pamela
## WUT ?
[Pamela](http://pamela.urlab.be/) est est l'outil que [UrLab](http://urlab.be) utilise pour savoir qui est pour l'instant au hackerspace.
### Comment ça marche ?
Le client pamela tourne sur 131.urlab.be qui est la gateaway du hackerspace. Le client récupère le contenu de la table arp de la machine toutes les minutes et l'envoie avec ØMQ au serveur (qui tourne sur rainbowdash.urlab.be)

Sur le serveur, les correspondances MAC address -> ip, owner et nom de machine/d'interface sont stockées et updatées s'il le faut.

Ensuite, toutes les machines ayant fait une apparition dans la table arp de 131.urlab.be depuis moins de 5 min sont affichées sur [pamela](http://pampam.urlab.be/pamela/) (ici, version de dev.)

### Technologies
* ØMQ pour pusher les données sur le serveur
* Django pour l'api
* supervisord pour maintenir tous les process vivants
* gunicorn pour le cgi
* et nginx pour le serveur web

### Comment l'employer ? API
À terme, il y aura du js pour interagir avec l'api. Pour l'instant, il faut se contenter d'un browser/de curl :

* `http://pampam.urlab.be/pamela/` : renvoie en json une liste de machines présentes.
* `http://pampam.urlab.be/pamela/get` : renvoie en json l'owner et la machine associés à la mac associée à l'ip qui a effectué la requête
* `http://pampam.urlab.be/pamela/set` : requête POST : attend un ou 2 champs : `owner` et `machine` et modifie l'owner et/ou la machine associés à la mac associée à l'ip qui a effectué la requête


## Deploy
Client et serveur sont faits pour touner sur 2 machines différentes, mais c'est pas obligé

	git clone git://github.com/UrLab/pamela.git
### Client
Install :

	cd client
	virtualenv --distribute --no-site-packages ve
	source ve/bin/activate
	pip install -r requirements.txt

Configure :

* changer `INTERFACE = 'en0'` par l'interface réseau à scanner
* changer `"tcp://127.0.0.1:5000"` par l'adresse du serveur
* changer `time.sleep(10)` par 	`time.sleep(60)` (c'est plus raisonnable)

Run :

	supervisord -c supervisord.ini 

C'est tout, votre client tourne et push les macs sur le serveur

### Serveur
Install :

	cd server
	virtualenv --distribute --no-site-packages ve
	source ve/bin/activate
	pip install -r requirements.txt
	chmod +x manage.py
	./manage.py syncdb

Run :

	supervisord -c supervisord.ini 

Et voilà, votre serveur écoute sur `http://0.0.0.0:8000`

## Future and tout doux

* créer une 3e partie (sur laquelle pointera pamela.urlab.be) qui contiendra tout plein de fichiers statiques html/js pour utiliser/afficher et interagir avec la partie serveur/l'api qui sera sur api.urlab.be ;
* Auto deploy pour puller les dernières modifs, passer l'app django en debug=False, mettre la bonne interface pour le scan arp et reloader ce qu'il faut ;
* Migrer la space api sur la partie serveur de pamela ;
* Faire de l'api une vraie api avec des vraies urls et un truc du genre REST.

## Guidelines
Si vous commitez, ajoutez [server], [client] ou [interface] devant votre message

Le but est de séparer le projet en 3 :
* Le client, qui récupère des données au hackerspace (pour l'instant uniquement les mac, mais pourquoi pas la t° ? )
* le serveur qui ne fait que api (à terme, sur `api.urlab.be`)
* l'interface, uniquement des fichiers statiques en html/js/css qui vont pomper des données sur le serveur (à terme, sur `pamela.urlab.be`)

## Privacy
Par défaut, si vous êtes au hackerspace, votre adresse MAC se retrouvera sur l'api. Si vous êtes contre, il suffit d'ajouter une correspondance mac -> owner contenant  `owner='Anonymous'` (respectez la convention svp) et `machine=''`

Et si vous en avez rien à foutre, tapez votre nom ou votre pseudo ;) (ou le nom de votre chat)
