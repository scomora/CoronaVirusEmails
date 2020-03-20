import requests

API_URLS = {
    "GLOBAL_STATS_URL": "https://thevirustracker.com/free-api?global=stats",
    "COUNTRY_STATS_URL": "https://thevirustracker.com/free-api?countryTotal=",      # to have country code appended
    "FULL_TIMELINE_URL": "https://thevirustracker.com/timeline/map-data.json",
    "COUNTRY_TIMELINE_URL": "https://thevirustracker.com/free-api?countryTimeline=" # to have country code appended
}


def fetchGlobalStats():
    URL = API_URLS["GLOBAL_STATS_URL"]
    # return getAndJsonifyRequest(URL)


def getResponseFromVirusTrackerAPI(URL):
    return requests.get(url=URL)


def fetchCountryStats(countryCode):
    URL = "".join([API_URLS["COUNTRY_STATS_URL"], countryCode])
    response = getResponseFromVirusTrackerAPI(URL)
    if 'json' in response.headers.get("Content-Type"):
        return response.json()["countrydata"][0]
    else:
        return response


