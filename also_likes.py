
def get_readers(df, doc_id):
    # Only events concerning documents
    df = df.loc[df["subject_type"] == "doc"]
    # Only events concerning this document
    df = df.loc[df["subject_doc_id"] == doc_id]
    # Only reads
    df = filter_read_events(df)

    return df["visitor_uuid"].unique()

def get_documents_read(df, user_id):
    # Only events concerning documents
    df = df.loc[df["subject_type"] == "doc"]
    # Only events concerning this user
    df = df.loc[df["visitor_uuid"] == user_id]
    # Only reads
    df = filter_read_events(df)

    return df["subject_doc_id"].unique()

          
def filter_read_events(df): 
    return df.loc[(df["event_type"] == "pageread") | 
            (df["event_type"] == "read") | 
            (df["event_type"] == "pagereadtime")]
