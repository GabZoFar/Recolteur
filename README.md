Bot Récolteur Dofus Retro

Un bot de récolte automatisé utilisant la vision par ordinateur pour détecter et interagir avec les éléments du jeu. Le bot peut détecter des ressources et les récolter.

## Fonctionnalités

	•	Interface graphique (GUI) avec fonctions de démarrage/arrêt
	•	Détection et récolte automatique des ressources
	•	Automatisation du système de combat
	•	Correspondance de motifs avec OpenCV
	•	Seuils de détection configurables

## Prérequis

	•	Python 3.x
	•	Les bibliothèques Python suivantes (à installer avec pip) :
	•	PyQt6
	•	pyautogui
	•	opencv-python
	•	numpy
	•	pillow
	•	scipy

## Installation

	1.	Clonez le dépôt
	2.	Installez les dépendances requises : pip install -r requirements.txt
	3.	Placez vos images de motifs (*.png) dans le même répertoire que l’exécutable :
	•	Chanvre1.png à Chanvre10.png (motifs des ressources)
	•	Faucher.png (motif pour l’action de récolte)
	•	carrerouge1.png à carrerouge3.png (indicateurs de combat)
	•	tireloigne.png (action de combat)
	•	protector1.png à protector3.png (motifs pour les combats)
	•	Fincombat.png (indicateur de fin de combat)

## Utilisation

Exécution à partir du code source

	1.	Lancez la version GUI : python app_gui.py
	2.	Ou lancez la version console : python app.py

## Exécution de l’exécutable .exe

En cours de développement : python build_exe.py
	2.	Lancez l’exécutable généré Recolteur.exe dans le dossier dist.

## Fonctionnement

	1.	Le bot analyse en continu l’écran à la recherche de motifs de ressources.
	2.	Lorsqu’une ressource est trouvée, il déplace le curseur et clique pour interagir.
	3.	Si un combat est détecté (carré rouge), il passe en mode combat et exécute la séquence de combat.
	4.	Le bot conserve un historique des positions cliquées pour éviter de cliquer plusieurs fois au même endroit.

## Contrôles

	•	Bouton Démarrer : Lance la séquence de récolte
	•	Bouton Arrêter : Arrête le bot en toute sécurité
	•	Touche ESC : Arrêt d’urgence pendant une séquence de combat

## Licence

Ce projet est sous licence MIT - consultez le fichier LICENSE pour plus de détails.

## Avertissement

L’utilisation d’outils d’automatisation peut enfreindre les conditions d’utilisation de certains jeux. Utilisez-les à vos risques et périls.

# ---- EN 🇺🇸 ----

# Dofus Harvester Bot

An automated harvesting bot that uses computer vision to detect and interact with game elements. The bot can detect resources and harvest them.

## Features

- GUI interface with start/stop functionality
- Automated resource detection and harvesting
- Combat system automation
- Pattern matching using OpenCV
- Configurable detection thresholds

## Prerequisites

- Python 3.x
- The following Python packages (install via pip):
  - PyQt6
  - pyautogui
  - opencv-python
  - numpy
  - pillow
  - scipy

## Installation

1. Clone the repository:
2. Install the required dependencies: pip install -r requirements.txt
3. Place your pattern images (*.png) in the same directory as the executable:
- Chanvre1.png through Chanvre10.png (resource patterns)
- Faucher.png (harvesting action pattern)
- carrerouge1.png through carrerouge3.png (combat indicators)
- tireloigne.png (combat action)
- protector1.png through protector3.png (combat patterns)
- Fincombat.png (end combat indicator)

## Usage

### Running from Source

1. Run the GUI version: python app_gui.py
2. Or run the console version:
3. python app.py

### Running the Executable
WIP : python build_exe.py


2. Run the generated executable `Recolteur.exe` in the `dist` folder

## How it Works

1. The bot continuously scans the screen for resource patterns
2. When a resource is found, it moves the cursor and clicks to interact
3. If combat is detected (red square), it enters combat mode and executes the combat sequence
4. The bot maintains a history of clicked locations to avoid clicking the same spot repeatedly

## Controls

- **Start Button**: Begins the harvesting sequence
- **Stop Button**: Safely stops the bot's operation
- **ESC Key**: Emergency stop during combat sequence

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Warning

Use of automation tools may be against the terms of service of some games. Use at your own risk.

