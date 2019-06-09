from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import os


def load_usafips(data_path):
    return(parse_file(data_path, True))

def fmatch(row,minscore,choices):
    match_choice = [x.lower() for x in choices]
    answer = process.extract(str(row).lower(),match_choice,limit = 1)
    print(answer)
    choice,score = answer[0]
    index = match_choice.index(choice)
    return choices[index] if score >= minscore else None




def render(table, params):
    state_column = params['state']
    county_column = params['county']
    # fuzz_boolean = params['fuzzy']
    fuzz_tolerance = params['tolerance']
    addfips_boolean = params['addfips']


    # If no column is selected, do nothing. By convention, Workbench modules
    # should output their input until enough parameters are supplied.
    if not state_column:
        return table

    # df_fips = load_usafips(data_path=  '/data/usa_fips.csv')
    df_fips = pd.read_csv('usa_fips.csv')
    #cleaning only state
    if not county_column:
        # if fuzz_boolean:
        state_choices = list(df_fips.state_name.unique())
        table['state_name_fips'] = table.apply(lambda x : fmatch(x[state_column],fuzz_tolerance, state_choices),axis=1)

        if addfips_boolean:
           table['state_code_fips'] = table.merge(df_fips.loc[:,['statefp','state_name']].drop_duplicates(['statefp','state_name']), left_on='state_name_fips', right_on='state_name', how='left')['statefp']

        # else:
        #    table['state_code_fips'] = table.merge(df_fips.loc[:,['statefp','state_name']].drop_duplicates(['statefp','state_name']), left_on='name', right_on='state_name', how='left')['statefp']

    #cleaning county and state
    else:
        state_choices = list(df_fips.state_name.unique())
        table['state_name_fips'] = table.apply(lambda x : fmatch(x[state_column],fuzz_tolerance, state_choices),axis=1)


        try :
            table['county_name_fips'] = table.apply(lambda x : fmatch(x[county_column],fuzz_tolerance, list(df_fips.loc[df_fips.state_name == x['state_name_fips']].county_name)),axis=1)
        except StopIteration:
            return()

        if addfips_boolean:
            table['state_code_fips'] = table.merge(df_fips.loc[:,['statefp','state_name']].drop_duplicates(['statefp','state_name']), left_on='state_name_fips', right_on='state_name', how='left')['statefp']
            table['county_code_fips'] = table.merge(df_fips, left_on=['state_name_fips','county_name_fips'], right_on=['state_name','county_name'], how='left')['countyfp']


            print(0)




    return(table)
