from canonical_transformer import get_mapping_of_column_pairs
from fund_insight_engine.fund_data_retriever.menu_data import fetch_menu2210
from fund_insight_engine.fund_data_retriever.fund_codes.divisions_consts import MAPPING_DIVISION

def get_mapping_fund_names_by_division(key_for_division, date_ref=None):
    df = fetch_menu2210(date_ref=date_ref)
    managers = MAPPING_DIVISION[key_for_division]
    df = df[df['매니저'].isin(managers)]
    COLS_TO_KEEP = ['펀드코드', '펀드명']
    df = df[COLS_TO_KEEP]
    return get_mapping_of_column_pairs(df, key_col='펀드코드', value_col='펀드명')

def get_mapping_fund_names_division_01(date_ref=None):
    return get_mapping_fund_names_by_division('division_01', date_ref=date_ref)

def get_mapping_fund_names_division_02(date_ref=None):
    return get_mapping_fund_names_by_division('division_02', date_ref=date_ref)

def get_fund_codes_division_01(date_ref=None):
    return list(get_mapping_fund_names_division_01(date_ref=date_ref).keys())

def get_fund_codes_division_02(date_ref=None):
    return list(get_mapping_fund_names_division_02(date_ref=date_ref).keys())
