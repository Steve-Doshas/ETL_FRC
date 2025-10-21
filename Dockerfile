FROM ubuntu:latest
# Met à jour les packages et installe python3, pip et venv
RUN apt-get update && apt-get install -y python3-pip python3-venv && apt-get clean
# Crée un environnement virtuel
RUN python3 -m venv /app/app-env
# Active l'environnement virtuel et installe les dépendances
COPY requirement.txt /app/requirement.txt
RUN /bin/bash -c "source /app/app-env/bin/activate && pip install -r /app/requirement.txt"
# Copie les fichiers nécessaires

COPY FRC_Req.py /app/FRC_Req.py
COPY update_frc.py /app/update_frc.py
# Définit le répertoire de travail
WORKDIR /app
# Commande pour exécuter le script Python
CMD ["/bin/bash", "-c", "source /app/app-env/bin/activate && python3 update_frc.py u>>./log/service_sc_frc$(date +'%Y-%m-%d').log"]
VOLUME ["/app/log"]