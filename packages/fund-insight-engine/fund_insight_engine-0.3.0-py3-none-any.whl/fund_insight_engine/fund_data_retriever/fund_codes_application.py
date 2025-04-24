from .menu_data import fetch_menu2210

def get_dfs_funds_by_class(date_ref=None):
    df = fetch_menu2210(date_ref=date_ref)
    df_code_class = df[['펀드코드', '클래스구분']]
    dfs = dict(tuple(df_code_class.groupby('클래스구분')))
    return dfs

def get_df_funds_by_class(key_for_class, date_ref=None):
    dfs = get_dfs_funds_by_class(date_ref=date_ref)
    df = dfs[key_for_class].set_index('펀드코드')
    return df

KEYS_FOR_CLASS = ['운용펀드', '일반', '클래스펀드', '-']

def get_df_funds_mothers(date_ref=None):
    return get_df_funds_by_class('운용펀드', date_ref=date_ref)

def get_df_funds_generals(date_ref=None):
    return get_df_funds_by_class('일반', date_ref=date_ref)

def get_df_funds_class(date_ref=None):
    return get_df_funds_by_class('클래스펀드', date_ref=date_ref)

def get_df_funds_nonclassified(date_ref=None):
    return get_df_funds_by_class('-', date_ref=date_ref)

def get_fund_codes_by_class(key_for_class, date_ref=None):
    df = get_df_funds_by_class(key_for_class, date_ref=date_ref)
    return df.index.tolist()

def get_fund_codes_mothers(date_ref=None):
    return get_fund_codes_by_class('운용펀드', date_ref=date_ref)

def get_fund_codes_generals(date_ref=None):
    return get_fund_codes_by_class('일반', date_ref=date_ref)

def get_fund_codes_class(date_ref=None):
    return get_fund_codes_by_class('클래스펀드', date_ref=date_ref)

def get_fund_codes_nonclassified(date_ref=None):
    return get_fund_codes_by_class('-', date_ref=date_ref)
