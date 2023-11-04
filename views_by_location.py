import pandas as pd


# Task 2a
def views_by_country(df, doc_id):
    # Only events concerning documents
    df = df.loc[df["subject_type"] == "doc"]
    # Only events concerning this document
    df = df.loc[df["subject_doc_id"] == doc_id]

    # Only reads? Or only impressions?

    # df = df.loc[df["event_type"] == "read"]
    df = df.loc[df["event_type"] == "impression"]

    return df["visitor_country"].value_counts()


# Task 2b
def views_by_continent(df):

    # Rearrange the countries data to make it have two columns:
    # visitor_country and count
    df = df.reset_index().set_axis(["visitor_country", "count"], axis=1)

    codes = pd.read_csv("all.csv")
    # Create a dictionary of the form: {country_code : continent}
    codes = codes.set_index("alpha-2")["region"].to_dict()

    # Assign each country a continent
    df["continent"] = df["visitor_country"].apply(lambda x: codes[x])

    # For all present continents, find the sum of the counts of the
    # views from countries that belong to that continent
    out = {
        continent: df.loc[df["continent"] == continent]["count"].sum()
        for continent in df["continent"].unique()
    }

    
    return pd.Series(out, dtype='float64')
