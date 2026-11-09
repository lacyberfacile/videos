# La Cyber Facile — production vidéo

La cybersécurité et le réseau expliqués simplement, sans jargon.
TikTok & YouTube : **@lacyberfacile**

## Structure
- `engine/lcf.py` — moteur d'animation (PIL + ffmpeg), identité visuelle de la chaîne
- `shorts/NNN-sujet/` — un dossier par Short : `script.md` (texte + sources) et `render.py`
- `assets/branding/` — logo, bannière et script de génération

## Rendu d'un Short
```bash
python3 shorts/001-faux-colis-sms/render.py --audio-dir <dossier seg01.mp3…> --out short.mp4
```
Sans `--audio-dir`, rendu muet avec durées estimées (aperçu de l'animation).
