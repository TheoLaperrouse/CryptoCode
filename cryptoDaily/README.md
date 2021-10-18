# CryptoDaily :

## Description

Script permettant de mettre à jour une fiche Google Sheet avec toutes les valeurs des Cryptos sur un compte Binance.

## Technologies :

Cette application est faite grâce à Python3 et différentes APIs :
- API de Google pour l'accès à Google Sheet.
- API de Binance pour la récupération du prix des cryptos et du nombre de Cryptos.

## QuickStart

Créer une Clé API depuis Binance qui permet d'accéder en lecture à vos Cryptomonnaie.

Créer un accès pour Google Sheet à l'aide de l'API Google.

Définir les variables d'environnement binance_api et binance_key sur votre ordinateur.

Installation des librairies requises :
```pip3 install -r requirements.txt```

Lancement du Script :
```python3 scriptCrypto.py```

## Autres Informations :

Fichier Cryptomonnaie -> Template Excell pour appliquer le script

Script envVariable.sh -> Définir une variable d'environnement sur Linux indéfiniment.

Le script se relance automatiquement toutes les 10 minutes

## Autres projets dans le même dossier:

CryptoRapport : Pour être alerter lorsque le rapport entre 2 cryptomonnaies dépasse un seuil
