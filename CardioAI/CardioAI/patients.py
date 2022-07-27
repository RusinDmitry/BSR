import pandas as pd
from os.path import join
from utils import load_config, save_data
from datetime import datetime
from joblib import load
from tensorflow.keras.models import load_model


class Patients:
    def __init__(self):
        self.__config = load_config("./configs/configs.json")
        self.__model = load('./models/miokard_dt_v1.joblib')
        self.__columns = list(self.__config.keys())
        self.__groups_columns = self.get_groups_params(self.__config)
        self.__dataframe = pd.DataFrame(columns=self.__columns)

    @staticmethod
    def get_groups_params(config):
        groups = {}
        for key, value in config.items():
            if not value['group'] is None:
                name_group = value['group']
                if not name_group in groups:
                    groups[name_group] = []
                groups[name_group].append(key)
        return groups

    def to_dict(self, columns, orient='rows'):
        tmp = self.__dataframe[columns]
        return tmp.to_dict(orient)

    def add_entry(self, kwargs):
        self.get_record_default_values()

        crow = len(self.__dataframe)
        for key, value in kwargs.items():
            if key in self.__groups_columns:
                if type(value) == list:
                    if len(value):
                        for column in value:
                            self.__dataframe.loc[crow - 1, column] = 1
                else:
                    if value is not None:
                        self.__dataframe.loc[crow - 1, value] = 1
            else:
                if value in [True, False]:
                    value = 1 if value == True else 0
                self.__dataframe.at[crow - 1, key] = value

        print(self.__dataframe)

    def get_record_default_values(self):
        record = []
        for name, value in self.__config.items():
            record.append(value['default'])
        self.__dataframe = pd.concat([self.__dataframe, pd.DataFrame([record], columns=self.__columns)], ignore_index=True)

    def upload_data(self):
        if not self.__dataframe.empty:
            file_name = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
            path = join('./uploading', f'{file_name}.csv')
            save_data(self.__dataframe, path)

    def get_forecast_complication(self, ):
        return [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    def get_forecasting_fatal_outcome(self):
        input_data =  self.get_dataframe()
        answer = self.__model.predict(input_data)[0]
        print(answer)
        if answer == 0:
            return [0,100]
        else:
            return [100,0]    
   

    def get_dataframe(self):
        df_out = pd.DataFrame()
        now = pd.Timestamp('now')
        df_out['AGE'] = (now-pd.to_datetime(self.__dataframe['date_birth'])).astype('<m8[Y]')
        df_out['SEX'] = self.__dataframe['gender'].replace(["женский","мужской"],[0,1]).astype('float')
        df_out['INF_ANAM'] = self.__dataframe['number_myocardial_infarctions']
        df_out['STENOK_AN'] = self.__dataframe['duration_stenocardia']
        df_out['FK_STENOK'] = self.__dataframe['functional_class_stenocardia']
        df_out['IBS_POST'] = self.__dataframe['characteristics_ashd']        
        df_out['GB'] = self.__dataframe['hypertension']
        
        df_out['SIM_GIPERT'] = self.__dataframe['symptomatic_hypertension']
        df_out['DLIT_AG'] = self.__dataframe['arterial_hypertension_duration']
        df_out['ZSN_A'] = self.__dataframe['chronic_heart_failure']
        df_out['nr_11'] = self.__dataframe['rhythm_disturbances_anamnesis']
        df_out['nr_01'] = self.__dataframe['atrial_extrasystole_anamnesis']
        df_out['nr_02'] = self.__dataframe['ventricular_extrasystole_anamnesis']
        df_out['nr_03'] = self.__dataframe['paroxysms_atrial_fibrillation_anamnesis']
        df_out['nr_04'] = self.__dataframe['permanent_form_atrial_fibrillation_anamnesis']
        df_out['nr_07'] = self.__dataframe['ventricular_fibrillation_anamnesis']
        df_out['nr_08'] = self.__dataframe['ventricular_paroxysmal_tachycardia_anamnesis']
        df_out['np_01'] = self.__dataframe['AV_block_one_degree_anamnesis']
        df_out['np_04'] = self.__dataframe['AV_block_three_degree_anamnesis']
        df_out['np_05'] = self.__dataframe['left_bundle_anterior_branch_block_anamnesis']
        df_out['np_07'] = self.__dataframe['left_bundle_branch_incomplete_block_anamnesis']
        df_out['np_08'] = self.__dataframe['left bundle_branch_full_block_anamnesis']
        df_out['np_09'] = self.__dataframe['right_bundle_branch_incomplete_block_anamnesis']
        df_out['np_10'] = self.__dataframe['right_bundle_branch_full_block_anamnesis']
        df_out['endocr_01'] = self.__dataframe['diabetes_anamnesis']
        df_out['endocr_02'] = self.__dataframe['obesity_anamnesis']
        df_out['endocr_03'] = self.__dataframe['thyrotoxicosis_anamnesis']
        df_out['zab_leg_01'] = self.__dataframe['chronical_bronchitis_anamnesis']
        df_out['zab_leg_02'] = self.__dataframe['obstructive_chronic_bronchitis_anamnesis']
        df_out['zab_leg_03'] = self.__dataframe['bronchial_asthma_anamnesis']
        df_out['zab_leg_04'] = self.__dataframe['chronic_pneumonia_anamnesis']
        df_out['zab_leg_06'] = self.__dataframe['pulmonary_tuberculosis_anamnesis']
        df_out['S_AD_ORIT'] = self.__dataframe['systolic_pressure']
        df_out['D_AD_ORIT'] = self.__dataframe['diastolic_pressure']
        df_out['O_L_POST'] = self.__dataframe['pulmonary_edema_intensive_care_unit']
        df_out['K_SH_POST'] = self.__dataframe['cardiogenic_shock_intensive_care_unit']
        df_out['MP_TP_POST'] = self.__dataframe['paroxysms_atrial_fibrillation_intensive_care_unit']
        df_out['SVT_POST'] = self.__dataframe['paroxysm_supraventricular_tachycardia_intensive_care_unit']
        df_out['GT_POST'] = self.__dataframe['paroxysm_ventricular_tachycardia_intensive_care_unit']
        df_out['FIB_G_POST'] = self.__dataframe['ventricular_fibrillation_intensive_care_unit']
        df_out['ant_im'] = self.__dataframe['infarction_anterior_wall_left_ventricle']
        df_out['lat_im'] = self.__dataframe['infarction_lateral_wall_left_ventricle']
        df_out['inf_im'] = self.__dataframe['infarction_inferior_wall_left_ventricle']
        
        df_out['post_im'] = self.__dataframe['infarction_inferior_wall_left_ventricle']
        df_out['IM_PG_P'] = self.__dataframe['right_ventricular_myocardial_infarction']
        df_out['ritm_ecg_p_01'] = self.__dataframe['sinus rhythm']
        df_out['ritm_ecg_p_02'] = self.__dataframe['atrial_fibrillation']
        df_out['ritm_ecg_p_04'] = self.__dataframe['atrial_rhythm']
        df_out['ritm_ecg_p_06'] = self.__dataframe['idioventricular_rhythm']
        df_out['ritm_ecg_p_07'] = self.__dataframe['sinus_tachycardia']
        df_out['ritm_ecg_p_08'] = self.__dataframe['sinus_bradycardia']
        df_out['n_r_ecg_p_01'] = self.__dataframe['atrial_extrasystole_ecg']
        df_out['n_r_ecg_p_02'] = self.__dataframe['frequent_atrial_extrasystoles_ecg']
        df_out['n_r_ecg_p_03'] = self.__dataframe['ventricular_extrasystole_ecg']
        df_out['n_r_ecg_p_04'] = self.__dataframe['frequent_ventricular_extrasystole_ecg']
        df_out['n_r_ecg_p_05'] = self.__dataframe['paroxysms_atrial_fibrillation_ecg']
        df_out['n_r_ecg_p_06'] = self.__dataframe['permanent_form_atrial_fibrillation_ecg']
        df_out['n_r_ecg_p_08'] = self.__dataframe['supraventricular_paroxysmal_tachycardia_ecg']
        df_out['n_r_ecg_p_09'] = self.__dataframe['ventricular_paroxysmal_tachycardia_ecg']
        df_out['n_r_ecg_p_10'] = self.__dataframe['ventricular_fibrillation_ecg']
        df_out['n_p_ecg_p_01'] = self.__dataframe['sinoatrial blockade_ecg']
        df_out['n_p_ecg_p_03'] = self.__dataframe['AV_block_one_degree_ecg']
        df_out['n_p_ecg_p_04'] = self.__dataframe['AV_block_two_degree_one_type_ecg']
        df_out['n_p_ecg_p_05'] = self.__dataframe['AV_block_two_degree_two_type_ecg']
        df_out['n_p_ecg_p_06'] = self.__dataframe['AV_block_three_degree_ecg']
        df_out['n_p_ecg_p_07'] = self.__dataframe['left_bundle_anterior_branch_his_ecg']
        df_out['n_p_ecg_p_08'] = self.__dataframe['left_bundle_posterior_branch_block_ecg']
        df_out['n_p_ecg_p_09'] = self.__dataframe['left_bundle_branch_incomplete_block_ecg']
        df_out['n_p_ecg_p_10'] = self.__dataframe['left bundle_branch_full_block_ecg']
        df_out['n_p_ecg_p_11'] = self.__dataframe['right_bundle_branch_incomplete_block_ecg']
        df_out['n_p_ecg_p_12'] = self.__dataframe['right_bundle_branch_full_block_ecg']
        df_out['fibr_ter_01'] = self.__dataframe['celiasum_750']
        df_out['fibr_ter_02'] = self.__dataframe['celiasum_1_mln']
        df_out['fibr_ter_03'] = self.__dataframe['streptodecasum_3']
        df_out['fibr_ter_05'] = self.__dataframe['streptasum']
        df_out['fibr_ter_06'] = self.__dataframe['celiasum_500']
        df_out['fibr_ter_07'] = self.__dataframe['celiasum_250']
        df_out['fibr_ter_08'] = self.__dataframe['streptodecasum_1_5']
        df_out['GIPO_K'] = self.__dataframe['hypokalemia']
        
        df_out['K_BLOOD'] = self.__dataframe['potassium_content']
        df_out['GIPER_NA'] = self.__dataframe['increasing_sodium']
        df_out['NA_BLOOD'] = self.__dataframe['sodium']
        df_out['ALT_BLOOD'] = self.__dataframe['alt']
        df_out['AST_BLOOD'] = self.__dataframe['ast']
        df_out['L_BLOOD'] = self.__dataframe['leukocytes']
        df_out['ROE'] = self.__dataframe['erythrocytes']
        df_out['TIME_B_S'] = self.__dataframe['time_anginal_attack']
        df_out['NA_KB'] = self.__dataframe['narcotic_analgesics_cardio_team']
        df_out['NOT_NA_KB'] = self.__dataframe['nonnarcotic_analgesics_cardio_team']
        df_out['LID_KB'] = self.__dataframe['lidocaine_cardio_team']
        df_out['NITR_S'] = self.__dataframe['liquid_nitrates_intensive_care_unit']
        df_out['LID_S_n'] = self.__dataframe['lidocaine_intensive_care_unit']
        
        df_out['B_BLOK_S_n'] = self.__dataframe['beta_blockers_intensive_care_unit']
        df_out['ANT_CA_S_n'] = self.__dataframe['calcium_antagonists_intensive_care_unit']
        df_out['GEPAR_S_n'] = self.__dataframe['anticoagulants_intensive_care_unit']
        df_out['ASP_S_n'] = self.__dataframe['aspirin_intensive_care_unit']
        df_out['TIKL_S_n'] = self.__dataframe['ticklid_intensive_care_unit']
        df_out['TRENT_S_n'] = self.__dataframe['trental_intensive_care_unit']
        
        
        for column in df_out.columns:     
            try:
                df_out[column] = df_out[column].astype('float')
            except Exception:
                print(column)
            
        
        df_full = pd.read_csv('./datasets/knn_zero_day_data.csv')  
        df_full.append(df_out)
        for column in df_full.columns:
            df_full[column] =(df_full[column] - df_full[column].min()) / (df_full[column].max() - df_full[column].min()) 
        input_data = df_full.iloc[-1:]
        
        return input_data
        

    def get_forecasting_cause_fatal_outcome(self):
        return [15, 30, 45, 60, 75, 90, 100]