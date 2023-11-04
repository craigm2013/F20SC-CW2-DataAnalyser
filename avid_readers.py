def time_spent_by_users(df):
    # Only interested in page reads
    df = df.loc[df["event_type"] == "pagereadtime"]
    # Return sum of readtime for each user
    df = df.groupby("visitor_uuid")
    return df["event_readtime"].sum()


# Task 4
def top_ten_readers(all_readers):
    return all_readers.nlargest(10)
