
# Task 3a
def views_by_browser(df):
    return df["visitor_useragent"].value_counts()
    
# Task 3b
def views_by_browser_parsed(df):
    # Parse user agent
    df["visitor_useragent"] = df["visitor_useragent"].apply(parse_user_agent)

    return df["visitor_useragent"].value_counts()


# According to
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Browser_detection_using_the_user_agent
def parse_user_agent(user_agent: str):

    user_agents = {
        "Firefox": "Firefox",
        "Seamonkey": "Seamonkey",
        "Chrome": "Chrome",
        "Chromium": "Unknown",
        "Safari": "Safari",
        "OPR": "Opera",
        "Opera": "Opera",
        "MSIE": "IE",
        "Trident": "IE",
    }

    for key in user_agents:
        if user_agent.__contains__(key):
            return user_agents[key]

    return "Unknown"
