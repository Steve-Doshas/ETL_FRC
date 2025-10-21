#!/bin/bash
# run_main.sh
# Usage:
#   ./run_main.sh [param_date] [param_option] [param_date2]
# - param_date : YYYY-MM-DD (défaut = aujourd'hui)
# - param_option : "", "Y" (fins d'année) ou "T" (fins de trimestre)
# - param_date2 : YYYY-MM-DD (requis si option ≠ "", défaut = aujourd'hui)

# --- Paramètre 1 : date principale ---
param_date=${1:-$(date +%F)}

# --- Paramètre 2 : option (vide, Y, T) ---
param_option_raw=${2:-}
param_option=$(echo "$param_option_raw" | tr '[:lower:]' '[:upper:]')

# --- Paramètre 3 : s’il est requis mais non fourni, on met la date du jour ---
param_date2=${3:-}

# --- Fonctions utilitaires ---
is_date() { [[ "$1" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; }

# --- Vérifications ---
if ! is_date "$param_date"; then
  echo "❌ param_date doit être au format YYYY-MM-DD"
  exit 1
fi

if [[ -n "$param_option" && ! "$param_option" =~ ^(Y|T)$ ]]; then
  echo "❌ param_option doit être vide, 'Y' (fins d'année) ou 'T' (fins de trimestre)"
  exit 1
fi

# Si option non vide mais pas de date2 → date du jour
if [[ -n "$param_option" && -z "$param_date2" ]]; then
  param_date2=$(date +%F)
fi

# Vérification de la deuxième date
# suppose que is_date() est déjà défini au-dessus
if [[ -n "$param_option" ]] && ! is_date "$param_date2"; then
  echo "❌ param_date2 doit être au format YYYY-MM-DD"
  exit 1
fi

# Vérifie l'ordre chronologique
if [[ -n "$param_option" ]]; then
  if [[ $(date -d "$param_date2" +%s) -lt $(date -d "$param_date" +%s) ]]; then
    echo "❌ param_date2 doit être postérieure ou égale à param_date"
    exit 1
  fi
fi

# --- Fonctions ---
run_main() {
  local d="$1"
  echo "___________________"
  echo "execution du service pour le $d"
  docker container run --rm --env-file .env --name service_sc_frc -v "/media/ProjetBI":/app/data/ -v LOG:/app/log etl_sc_frc:v2 $d
}

# --- Cas 1 : option vide → un seul appel ---
if [[ -z "$param_option" ]]; then
  run_main "$param_date"
  exit 0
fi

# --- Cas 2 : option non vide → générer les dates ---
start_s=$(date -d "$param_date" +%s)
end_s=$(date -d "$param_date2" +%s)
start_year=$(date -d "$param_date" +%Y)
end_year=$(date -d "$param_date2" +%Y)

# Fins de trimestre
q_ends=("03-31" "06-30" "09-30" "12-31")

for (( y=start_year; y<=end_year; y++ )); do
  if [[ "$param_option" == "Y" ]]; then
    cand="${y}-12-31"
    cand_s=$(date -d "$cand" +%s)
    if [[ $cand_s -ge $start_s && $cand_s -le $end_s ]]; then
      run_main "$cand"
    fi
  elif [[ "$param_option" == "T" ]]; then
    for md in "${q_ends[@]}"; do
      cand="${y}-${md}"
      cand_s=$(date -d "$cand" +%s)
      if [[ $cand_s -ge $start_s && $cand_s -le $end_s ]]; then
        run_main "$cand"
      fi
    done
  fi
done