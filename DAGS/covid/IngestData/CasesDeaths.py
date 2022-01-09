from pandas import read_json
from io import StringIO
from requests import get
from numpy import log10

save_path = r'../data'



class Cases_Deaths:
  
    def __init__(self):
        self.url = "https://opendata.ecdc.europa.eu/covid19/nationalcasedeath/json"
        self.save_path = save_path

        
    def ingest(self):
        df =  read_json(
                    StringIO(get(self.url).text)
                            ).sort_values(['country','year_week'])
        print(f'Data Downloaded from {self.url}')
        objects_columns = df.select_dtypes('object').nunique()
        columns_to_drop = objects_columns[lambda x: x==1].index.values
        if len(columns_to_drop) != 0:
            for col in columns_to_drop:
                df.drop(col,axis=1,inplace=True)
        else:
            pass
        df[['rate_14_day','weekly_count','cumulative_count']] = df.sort_values('year_week').groupby(['country_code','indicator'],as_index=False)[['rate_14_day','weekly_count','cumulative_count']].fillna(method='ffill').fillna(0)
        year_week =df.year_week.str.split('-')
        df['year'] = year_week.apply(lambda x: x[0])
        df['weeknum'] =  year_week.apply(lambda x: x[1])
        self.df = df
    
    def save_df_to_csv(self,df,filename):
        df.to_csv(f'{self.save_path}/{filename}.csv',index=False)
        
    
    def Pivot_Indicators(self):
        df = self.df
        def pivot_table_indicator(df,indicator='cases'):
            cols_to_change = {}
            for col in ['weekly_count', 'cumulative_count', 'rate_14_day']:
                cols_to_change[col] = f"{indicator}_{col}"
            df= df.copy().query(f"indicator=='{indicator}' & -country.str.contains('total')")\
            .rename(columns=cols_to_change)
            return df.drop("indicator",axis=1)

    
    
        df = pivot_table_indicator(df, indicator='cases')\
        .merge(pivot_table_indicator(df, indicator='deaths'),
                  on=['country', 'country_code', 'continent', 'population','year_week']
              ,how='outer')
        self.df_wide = df
        self.save_df_to_csv(df,'cases_deaths_countries')
        
    def Worldwide(self):
        df = self.df_wide.groupby(['year_week'])[['cases_weekly_count','deaths_weekly_count']].sum().reset_index()
        self.save_df_to_csv(df
                       ,'cases_deaths_worldwide')
    
    def Last_reported_week(self):
        df = self.df.groupby(['country_code','year','indicator'],as_index=False)\
        .weeknum.max()\
        .set_index(['country_code','indicator'])\
        .assign(last_year =  lambda x: x.groupby(['country_code','indicator']).year.transform(lambda value: value.max()==value ))\
        .query('last_year').reset_index().merge(self.df, on= ['country_code','year','weeknum','indicator'],how='inner')
        df['log_scale'] = df.groupby('indicator').rate_14_day.transform(log10)
        self.save_df_to_csv(df,'Lasted_cases_deaths_countries')
        



class HospitalAdmission:

    def __init__(self):
        self.url = 'https://opendata.ecdc.europa.eu/covid19/hospitalicuadmissionrates/csv/data.csv'
        self.save_path = save_path

    def ingest(self):
        self.df = pd.read_csv(self.url)

    def pivot_df(self):
        return self.df.assign(year_week= lambda x: x.year_week.str.replace('W',''))\
        .pivot_table(index=['country','year_week'],columns=['indicator'],values='value')\
        .reset_index()

class Vaccionation:

    def __init__(self):
        self.url = 'https://opendata.ecdc.europa.eu/covid19/vaccine_tracker/csv/data.csv'

    def ingest(self):
        self.df = pd.read_csv('https://opendata.ecdc.europa.eu/covid19/vaccine_tracker/csv/data.csv')\
            .rename(columns={
                                'YearWeekISO': 'year_week', 
                                'ReportingCountry':'Alpha-2 code'
                            }
                )
    def groupby_country_week(self):
        return self.df.groupby(['Alpha-2 code','year_week'],as_index=False)[[ 'NumberDosesReceived',
       'NumberDosesExported', 'FirstDose', 'FirstDoseRefused', 'SecondDose',
       'DoseAdditional1', 'UnknownDose']].sum()