![Mon Image](https://github.com/Steve-Doshas/BI/blob/main/Liseret%20Inserm%20T.png)

# Service : 
|-----------|-----------|
|-----------|-----------|
| **Nom** |**ETL_FRC**| 
| *Périodicité d’exécution*   | A 4h00 UTC. Tous les jours de la semaine|
| *Description* | Ce service automatise la création et mise à jour de fichiers csv de référence contenant les informations actualisées et utiles concernant les FRC et les prospects FRC. Il génère également un fichier de synthèse avec les statistiques trimestrielles.
| *Version* | **1.0** |
| *Code* | FRC_Req.py & update_frc.py|
| *Log du service* |service_sc_frc$(date +'%Y-%m-%d').log|

# Sources :

|BD|Tables|
|-----------|-----------|
|Sugar|frc, researchunitsfrc, researchunitsfrc_frc, researchunitsfrc_researchunits, researchunits, opportunities, opportunities_cstm, opportunities_contacts, researchunitscontacts_contacts, researchunitscontacts, researchunitscontacts_researchunits|

# Sorties :

## Fichier 1 : FRC lastupdate

|Nom | **Sugar_frc_lastupdate.csv**|
|-----------|-----------|
|Chemin | Défini par la variable d'environnement SAVE_PATH|
|Type de fichiers| csv utf-8-sig|

|Données|Description|Comment|
|-----------|-----------|-----------|
|id| Identifiant unique du FRC|Page FRC(Production, _Projet_sanssuite_CY, _Projet_nonfinance_CY, _Projet_finance_prod_CY, _Projet_terminant, _Projet_terminé, _Projet_Clos_CY, _SR_mountedfounded)|
|name| Nom du projet FRC|??|
|date_entered| Date de création de l'enregistrement|Page FRC(_Projet_qualif_CY)|
|description| Description du projet|??|
|code_projet| Code unique du projet|??|
|ligne_comptable_genesys|Ligne comptable Genesys|??|
|acronyme| Acronyme du projet|??|
|status| Statut du projet|Page FRC(_Projet_qualif_CY, _Projet_sanssuite_CY, _Projet_nonfinance_CY, _Projet_Clos_CY, , is_founded, is_mounted)|
|etatav| État d'avancement|evaluation, montage_etape1, montage_etape2, negocation, non_gere, pre_montage, production, termine - Page FRC( |
|date_debut| Date de début du projet|Page FRC( date_cle)|
|date_fin_initiale| Date de fin initiale prévue|Page FRC(_Projet_terminant, _Projet_Clos_CY)|
|programme_cadre| Programme cadre du financement|??|
|call_frc| Appel à projet FRC|??|
|ligne_soumission| Ligne de soumission|??|
|contract_number| Numéro de contrat|??|
|new_date_end| Nouvelle date de fin|Page FRC(_Projet_terminant)|
|deadline_montage| Date limite de montage|Page FRC(_Projet_sanssuite_CY, _Projet_nonfinance_CY, _SRyear)|
|instrument| Instrument de financement|??|
|nb_etape| Nombre d'étapes|??|
|nb_partenaire| Nombre de partenaires|??|
|nb_periode| Nombre de périodes|??|
|wp_it| Work package IT|??|
|subvention_inserm_initiale| Subvention INSERM initiale|??|
|subvention_inserm_actuelle| Subvention INSERM actuelle|??|
|subvention_it_initiale| Subvention IT initiale|??|
|subvention_it_actuelle| Subvention IT actuelle|??|
|subvention_totale| Subvention totale|??|
|informations_complementaires||??|
|team_id| Identifiant de l'équipe|??|
|team_set_id| Identifiant du set d'équipe|??|
|assigned_user_id| Identifiant de l'utilisateur assigné|??|
|delegation_regionale_id| Identifiant de la délégation régionale|??|
|organisme_coordinateur_id| Identifiant de l'organisme coordinateur|??|
|bailleur_id| Identifiant du bailleur|??|
|scientifique_principal_id| Identifiant du scientifique principal|??|
|subvention_partenaires| Subvention des partenaires|??|
|annee_financement|Année de financement|Page FRC(_Projet_finance_CY)|
|ga_number| Numéro GA|??|
|totale_initial| Montant total initial|??|
|ru_name| Nom de l'unité de recherche|??|
|ru_acronyme| Acronyme de l'unité de recherche|Page FRC(_NB_ru)|

## Fichier 2 : Prospects FRC lastupdate

|Nom | **Sugar_prospect_frc_lastupdate.csv**|
|-----------|-----------|
|Chemin | Défini par la variable d'environnement SAVE_PATH|
|Type de fichiers| csv utf-8-sig|

|Données|Description|Comment|
|-----------|-----------|-----------|
|id| Identifiant unique|Page Prospect|
|date_entered| Date de création de l'enregistrement|??|
|name| Nom de l'opportunité|??|
|campaign_id| Identifiant de campagne|??|
|lead_source| Source du lead|??|
|date_closed| Date de clôture|??|
|sales_stage| Étape de vente|initiee, marque_interet, sans_suite, transformee Page FRC(Statut ds prospections en cours) |
|sales_status| Statut de vente|In Progress, New|
|assigned_user_id| Identifiant de l'utilisateur assigné|??|
|service_start_date| Date de début de service|??|
|is_escalated| Indicateur d'escalation|??|
|denorm_account_name| Nom du compte dénormalisé|??|
|nbdays_open_c| Nombre de jours ouvert|Page FRC(MEDIAN)|
|modele_opportunity_c| Modèle d'opportunité|??|
|other_lead_source_c| Autre source de lead|??|
|offre_c| Offre|??|
|opp_number_c| Numéro d'opportunité|??|
|importance_c| Importance|??|
|contact_id| Identifiant du contact|??|
|contact_role| Rôle du contact|??|
|status| Statut du contact dans l'unité|??|
|acronyme| Acronyme de l'unité de recherche|Page FRC(_NBRU)|

## Fichier 3 : Summary trimestriel

|Nom | **Sugar_frc_summary.csv**|
|-----------|-----------|
|Chemin | Défini par la variable d'environnement SAVE_PATH|
|Type de fichiers| csv utf-8-sig|
|Récurrence| Données Trimestrielles (31/03, 30/06, 30/09, 31/12, date du jour)|

|Données|Description|Comment|
|-----------|-----------|-----------|
|date| Date de génération de la statistique|Rapport ScoreCard(_FRC_mnt, _FRC_prod, _FRC_proj, _FRC_pros, _FRC_ru, _FRC_sr, FRC_Daylabel) FRC et Synthèse|
|en prod| Nombre de projets en production||Rapport ScoreCard(_FRC_prod, _FRC_prod_sum) FRC et Synthèse|
|termine| Nombre de projets terminés|??|
|prospect_cy| Prospects année courante|Rapport ScoreCard(_FRC_pros, _FRC_pros_sum) FRC et Synthèse|
|prospect_py| Prospects années précédentes|??|
|montes| Projets montés année courante|Rapport ScoreCard(_FRC_proj, _FRC_proj_sum) FRC et Synthèse|
|deposes| Projets déposés année courante|??|
|finances| Projets financés|??|
|succes rate| Taux de succès|Rapport ScoreCard(_FRC_sr, _FRC_sr_sum) FRC et Synthèse|
|financement_inserm| Financement INSERM total|Rapport ScoreCard(_FRC_mnt, _FRC_mnt_sum ) FRC et Synthèse|
|ru_prod| Unités de recherche en production|Rapport ScoreCard(_FRC_ru, _FRC_ru_sum) FRC et Synthèse|

# Fonctions  :

-`etl_frc()` : Fonction principale qui extrait, transforme et charge les données FRC depuis Sugar. Retourne deux DataFrames
- df_frc : données principales FRC
- df_opp : données prospects/opportunités FRC

-`sc_frc()` : Fonction qui génère les statistiques de synthèse trimestrielles à partir des données FRC et prospects.

