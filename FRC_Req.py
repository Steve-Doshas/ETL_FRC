import os, re, io
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
import pymysql

from datetime import datetime
from dateutil.relativedelta import relativedelta


pd.options.mode.copy_on_write = True

def etl_frc():

    # Charger le fichier .env pour récupérer les variables d'environnement
    load_dotenv()
    # Récupérer les informations de connexion aux bases de données depuis les variables d'environnement
    SUGAR_URL_CONNECT = os.getenv('SUGAR_URL_CONNECT')

    # Créer une connexion à la base de données SUGAR
    engine_sug = create_engine(f"mysql+pymysql://{os.getenv('SUGAR_USER')}:{os.getenv('SUGAR_PWORD')}@{os.getenv('SUGAR_HOST')}/{os.getenv('SUGAR_DB')}")

    try:
        connection_sug = engine_sug.connect()
        print("Connexion réussie à la base de données SUGAR distante.")
    # Gérer les exceptions en cas d'erreur lors de la connexion
    except Exception as e:
        print(f"Erreur lors de la connexion : {e}")

    sql_query = ''' 
            SELECT 
                frc.id, 
                frc.name,
                frc.date_entered,
                frc.description,
                frc.code_projet,
                frc.ligne_comptable_genesys,
                frc.acronyme,
                frc.status,
                frc.etatav,
                frc.date_debut,
                frc.date_fin_initiale,
                frc.programme_cadre,
                frc.call_frc,
                frc.ligne_soumission,
                frc.contract_number,
                frc.new_date_end,
                frc.deadline_montage,
                frc.instrument,
                frc.nb_etape,
                frc.nb_partenaire,
                frc.nb_periode,
                frc.wp_it,
                frc.subvention_inserm_initiale,
                frc.subvention_inserm_actuelle,
                frc.subvention_it_initiale,
                frc.subvention_it_actuelle,
                frc.subvention_totale,
                frc.informations_complementaires,
                frc.team_id,
                frc.team_set_id,
                frc.assigned_user_id,
                frc.delegation_regionale_id,
                frc.organisme_coordinateur_id,
                frc.bailleur_id,
                frc.scientifique_principal_id,
                frc.subvention_partenaires,
                frc.annee_financement,
                frc.ga_number,
                frc.totale_initial,
                ru.name AS ru_name,
                ru.acronyme AS ru_acronyme
            FROM frc
            LEFT JOIN researchunitsfrc_frc AS rufrc 
                ON frc.id = rufrc.frc_id
            LEFT JOIN researchunitsfrc_researchunits AS rufrcru 
                ON rufrc.researchunitsfrc_id = rufrcru.researchunitsfrc_id
            LEFT JOIN researchunits AS ru 
                ON rufrcru.researchunits_id = ru.id
            WHERE frc.deleted = 0;
    '''


    # Exécuter la requête SQL sur la base de données SUGAR via la connexion active
    result = connection_sug.execute(text(sql_query))
    df_frc = pd.read_sql_query(text(sql_query), connection_sug)

    sql_query = ''' 
	SELECT 
	    opp.id, opp.date_entered, opp.name, opp.campaign_id, opp.lead_source, opp.date_closed, opp.sales_stage, opp.sales_status, 
    	    opp.assigned_user_id, opp.service_start_date, opp.is_escalated, opp.denorm_account_name, 
    	    opp_c.nbdays_open_c, opp_c.modele_opportunity_c, opp_c.other_lead_source_c, opp_c.offre_c, 
    	    opp_c.opp_number_c, opp_c.importance_c, opp_con.contact_id, opp_con.contact_role,
	    rucon.status, ru.acronyme
	FROM opportunities AS opp 
	JOIN opportunities_cstm AS opp_c
	    ON opp.id = opp_c.id_c
	LEFT JOIN opportunities_contacts AS opp_con
	    ON opp.id = opp_con.opportunity_id AND opp_con.deleted = 0
	LEFT JOIN researchunitscontacts_contacts AS rucon_con
	    ON rucon_con.contacts_id = opp_con.contact_id
	LEFT JOIN researchunitscontacts AS rucon
	    ON rucon.id = rucon_con.researchunitscontacts_id
	LEFT JOIN researchunitscontacts_researchunits AS rucon_ru
	    ON rucon_ru.researchunitscontacts_id = rucon_con.researchunitscontacts_id
	LEFT JOIN researchunits AS ru
	    ON ru.id = rucon_ru.researchunits_id
	WHERE opp.deleted = 0
	  AND opp_c.isduplicated_c = 0
	  AND opp_c.modele_opportunity_c = 'frc';
	'''
	# Exécuter la requête SQL sur la base de données SUGAR via la connexion active
    result = connection_sug.execute(text(sql_query))
    df_opp = pd.read_sql_query(text(sql_query), connection_sug)
    df_opp = df_opp[df_opp.status != 'etait_rattache_a']

    return df_frc, df_opp


def sc_frc(df, df_opp, date):
    proj_en_prod = df[(df.status=="en_cours") & (df.etatav.isin(['production']))]['id'].nunique()
    proj_termine = df[(df.status=="en_cours") & (df.etatav.isin(['termine']))]['id'].nunique()

    df_opp['service_start_date'] = pd.to_datetime(df_opp['service_start_date'], errors='coerce')
    prospect_cy = df_opp[(df_opp['service_start_date'].dt.year == datetime.now().year) & (df_opp['sales_stage'].isin(['initiee', 'marque_interet']))]['opp_number_c'].nunique()
    prospect_py = df_opp[(df_opp['service_start_date'].dt.year != datetime.now().year)  & (df_opp['sales_stage'].isin(['initiee', 'marque_interet']))]['opp_number_c'].nunique()
    ru_en_prod = df[(df.status=="en_cours") & (df.etatav.isin(['production'])) & (df.ru_acronyme != "")]['ru_acronyme'].nunique()

    df['deadline_montage'] = pd.to_datetime(df['deadline_montage'], errors='coerce')
    df['ismounted'] = (~df.status.isin(["en_prospection","sans_suite"])) & (df.etatav != "pre_montage" )
    df['isevaluated'] = (df['status'].isin(["sans_suite", "non_finance", "non_gere","en_cours","clos"])) & (df['etatav'].isin(["evaluation", "negocation","production","termine", "non_gere"]))
    df['isfounded'] = ((df['status']=="en_cours") & (df['etatav'].isin(["negocation","production","termine", "non_gere"]))) | ((df['status']=="clos") & (df['etatav'].isin(["production","termine", "non_gere"])))
    df['annee_financement'] = df['annee_financement'].fillna('')

    df['sryear'] = df.apply(lambda x : x['deadline_montage'].year if x['annee_financement'] == '' else int(x['annee_financement']), axis=1)

    montage_cy = df[(df['deadline_montage'].dt.year == date.year) & (df['ismounted'])]['code_projet'].nunique()
    depose_cy = df[(df['deadline_montage'].dt.year == date.year) & (df['isevaluated'])]['code_projet'].nunique()
    montage_sr = df[(df['sryear'] == date.year) & (df['ismounted'])]['code_projet'].nunique()
    founded = df[(df['sryear'] == date.year) & (df['isfounded'])]['code_projet'].nunique()
    
    srate = np.round(100*founded/montage_sr,1)

    df_fi = df.groupby(['id']).first().reset_index()
    financement = int(df_fi[
                (df_fi['annee_financement'] == str(date.year)) &
                (df_fi['status'].isin(["en_cours"])) & 
                (df_fi['etatav'].isin(["negocation"]))
        ]['subvention_inserm_initiale'].sum())

    return pd.DataFrame({'date': [date],
			 'en prod': [proj_en_prod],
			 'termine': [proj_termine],
                         'prospect_cy' : [prospect_cy],
                         'prospect_py' : [prospect_py],
                         'montes' : [montage_cy],
                         'deposes': [depose_cy],
                         'finances': [founded],
                         'succes rate': [srate],
                         'financement_inserm': [financement],
			 'ru_prod': [ru_en_prod]})
