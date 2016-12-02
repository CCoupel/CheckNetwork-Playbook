# CheckNetwork-Playbook
Le playbook vérifie
1) si le serveur SRV est joignable en SSH, si non on sort avec le code: SRC ERROR
2) si le service est accessible depuis SRC vers DST:PORT/Proto, si oui, on sort avec le code OK
3) si le serveur DST est joignable en SSH, si non on sort avec le code:DST ERROR
4) lance un mini serveur sur DST en écoute sur DST:PORT/Proto en tache de fond
5) si le service est accessible depuis SRC vers DST:PORT/Proto, si oui, on sort avec le code OK
6) sinon on termine avec le code NO ACCESS with private service

Les états de sortie sont donc:
SRC ERROR: Le serveur SRC source n'est pas accessible en SSH
OK: Le serveurs SRC est accessible avec le service deja focntionnel
DST ERROR: Le serveur DST n'est pas accessible avec le service initial et n'est pas accessible via SSH
NO ACCESS witj private service: Le serveur DST n'est pas accessible sur son port de service 

2 nouveaux modules pour le faire:

sockClient :
    "BindIP": {"required": True, "type": "str"},
    "Port": {"required": True, "type": "int"},
    "Message": {"default": "", "type": "str"},
    "Timeout": {"default": 5, "type": "int"},
    "Protocol": {"default": "tcp", "choices": ['tcp', 'udp'i,'http'], "type": 'str',}
envoie le contenu de MESSAGE au serveur BindIP sur le port Port/Protocol et vérifie si le retour est identique.
Si le protocol est http, MESSAGE n'est pas utilisé. Il vérifie que le code retour du serveur HTTP est 2xx ou 3xx

sockServer:
    "BindIP": {""default": "0.0.0.0", "type": "str"},
    "Port": {"required": True, "type": "int"},
    "Protocol": {"default": "tcp","choices": ['tcp', 'udp'i,'http'], "type": 'str',},
Ecoute sur l'adresse BindIP et le port Port/Protocol et ré-émet ce qu'il recoit.
Si le protocol est http, il envoie systématiquement le code erreur 200.

Le script RunTest.sh lance le test en prenant comme entrée le fichier checkNet-matrix.yml dont le contenu est:
matrix:
  - {SRC: 192.168.124.218, DST: 192.168.124.219, Port: 2222, Proto: tcp}
  - {SRC: 192.168.124.219, DST: 192.168.124.218, Port: 2222, Proto: tcp}
   - {SRC: 192.168.124.218, DST: 192.168.124.219, Port: 2222, Proto: http, BACKEND: 192.168.124.218, BACKENDPort: 1234, Message: ''}
  - {SRC: 192.168.124.219, DST: 192.168.124.218, Port: 222, Proto: http, BACKEND: 192.168.124.219, BACKENDPort: 1234, Message: ''}
 

Aprés execution, ce fichier est mis a jour en ajoutant l'état ainsi que les messages de retour des 2 tests.:
matrix:
  - {SRC: 192.168.124.218, DST: 192.168.124.219, Port: 2222, Proto: tcp, Message: 'test',Status: NO ACCESS with netcat, Result1: [], Result2: []}
  - {SRC: 192.168.124.219, DST: 192.168.124.218, Port: 2222, Proto: tcp, Message: 'test',Status: OK, Result1: [], Result2: [u'test']}
