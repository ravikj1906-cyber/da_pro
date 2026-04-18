def get_basic_info(df):
    return {
        "Shape": df.shape,
        "Columns": df.columns.tolist(),
        "Missing Values": df.isnull().sum()
    }

def get_statistics(df, column):
    return df[column].describe()