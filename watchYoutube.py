from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def generate_next_urls(base_url, params_increment, num_urls=5):
    """
    Generate the next URLs by incrementing parameters.

    :param base_url: The base URL from videostatsWatchtimeUrl.baseUrl.
    :param params_increment: A dictionary specifying how much to increment each parameter.
    :param num_urls: The number of URLs to generate.
    :return: A list of generated URLs.
    """
    # Parse the base URL
    parsed_url = urlparse(base_url)
    query_params = parse_qs(parsed_url.query)

    # Convert query parameters to a mutable dictionary
    mutable_params = {k: float(v[0]) if v[0].replace('.', '', 1).isdigit() else v[0] for k, v in query_params.items()}

    # Generate URLs
    urls = []
    for _ in range(num_urls):
        # Increment parameters
        for key, increment in params_increment.items():
            if key in mutable_params:
                mutable_params[key] = float(mutable_params[key]) + increment

        # Rebuild query string
        updated_query = urlencode({k: v for k, v in mutable_params.items()}, doseq=True)
        new_url = urlunparse(parsed_url._replace(query=updated_query))
        urls.append(new_url)

    return urls

# Base URL from videostatsWatchtimeUrl.baseUrl
base_url = "https://s.youtube.com/api/stats/watchtime?cl=704070159&docid=WPt0x2ABl4k&ei=NplZZ-7IFrvBvcAPhebBmQ4&fexp=&ns=yt&plid=AAYo_uoWrNTdOzGt&referrer=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DWPt0x2ABl4k&sdetail=rv%3AWPt0x2ABl4k&sourceid=yw&el=detailpage&len=10348&of=BYCh469UR_dSvfqRtKB5tQ&osid=AAAAAB7bxzQ%3AAOeUNAbt6XPkZWi23eQ9xWoS6gkzsKoiFA&subscribed=1&uga=m37&vm=CAIQABgEOjJBSHFpSlRKR003V2RYVWZodDhjZzhjbVEzNU1UekdlODREeWpNMnFlb2VFaTItd1BfUWJcQUZVQTZSU0gtUEU3T3JrRGVvWEx0cDJPcU1CZjNySEdSMTUyaTBrWlpfbTZrVF9fdUZaMDQ3amhDZER2elBaaFludERnbTdCX0JHNVozWnhndXRORGllWkZhblO4AQE"

# Increments for parameters based on observed pattern
params_increment = {
    "cmt": 10.0,  # Current Media Time
    "rt": 10.0,   # Real-Time
    "st": 10.0,   # Start Time
    "et": 10.0,   # End Time
    "lact": 1000, # Last Active Time (ms)
    "rtn": 1,     # Return
}

# Generate the next URLs
next_urls = generate_next_urls(base_url, params_increment, num_urls=5)

# Print the generated URLs
for i, url in enumerate(next_urls, start=1):
    print(f"URL {i}: {url}")