from canonical_transformer import get_mapping_of_column_pairs
from .types_consts import VALUES_FOR_TYPE, KEY_FOR_FUND_TYPE
from .menu2110_consts import KEY_FOR_FUND_CODE_IN_MENU2110, KEY_FOR_FUND_NAME_IN_MENU2110
from fund_insight_engine.fund_data_retriever.menu_data import fetch_menu2210

def get_dfs_funds_by_type(date_ref=None):
    df = fetch_menu2210(date_ref=date_ref)
    dfs = dict(tuple(df.groupby(KEY_FOR_FUND_TYPE)))
    return dfs

def get_df_funds_by_type(key_for_type, date_ref=None):
    dfs = get_dfs_funds_by_type(date_ref=date_ref)
    COLS_TO_KEEP = [KEY_FOR_FUND_CODE_IN_MENU2110, KEY_FOR_FUND_NAME_IN_MENU2110, KEY_FOR_FUND_TYPE]
    df = dfs[key_for_type][COLS_TO_KEEP].set_index(KEY_FOR_FUND_CODE_IN_MENU2110)
    return df

    # VALUES_FOR_TYPE = ['주식혼합', '혼합자산', '채권혼합', '주식형', '변액']

def get_df_funds_equity_mixed(date_ref=None):
    return get_df_funds_by_type('주식혼합', date_ref=date_ref)

def get_df_funds_bond_mixed(date_ref=None):
    return get_df_funds_by_type('채권혼합', date_ref=date_ref)

def get_df_funds_multi_asset(date_ref=None):
    return get_df_funds_by_type('혼합자산', date_ref=date_ref)

def get_df_funds_equity(date_ref=None):
    return get_df_funds_by_type('주식형', date_ref=date_ref)

def get_df_funds_variable(date_ref=None):
    return get_df_funds_by_type('변액', date_ref=date_ref)

def get_mapping_fund_names_by_type(key_for_type, date_ref=None):
    df = get_df_funds_by_type(key_for_type, date_ref=date_ref)
    return get_mapping_of_column_pairs(df.reset_index(), key_col=KEY_FOR_FUND_CODE_IN_MENU2110, value_col=KEY_FOR_FUND_NAME_IN_MENU2110)

def get_mapping_fund_names_equity_mixed(date_ref=None):
    return get_mapping_fund_names_by_type('주식혼합', date_ref=date_ref)

def get_mapping_fund_names_bond_mixed(date_ref=None):
    return get_mapping_fund_names_by_type('채권혼합', date_ref=date_ref)

def get_mapping_fund_names_multi_asset(date_ref=None):
    return get_mapping_fund_names_by_type('혼합자산', date_ref=date_ref)

def get_mapping_fund_names_equity(date_ref=None):
    return get_mapping_fund_names_by_type('주식형', date_ref=date_ref)

def get_mapping_fund_names_variable(date_ref=None):
    return get_mapping_fund_names_by_type('변액', date_ref=date_ref)