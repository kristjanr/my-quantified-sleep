def garmin_connect_request_headers():
    # Use Google Chrome.
    # Go to your https://connect.garmin.com/modern/dailySummary/sleep, open up the dev tools and find the GET request to
    # https://connect.garmin.com/modern/proxy/wellness-service/wellness/dailySleepsByDate?startDate=2019-02-07&endDate=2019-02-28&_=1551423303056
    # Get the cookie and referer heads from the request headers and put them into the dictionary below.
    #
    # PS: I just usually copy the whole request as cURL and then convert it to python at
    # https://curl.trillworks.com/ because it is easier and faster
    #
    # PPS: Actually, copying only the cookie will work as well.
    # But this way Garmin may find out that you are not doing this call via browser more easily.

    headers = {
        'cookie': '',
        'referer': '',
    }
    return headers
