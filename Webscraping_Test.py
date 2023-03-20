import requests
import pandas as pd

def main():

    # Create session object
    session = requests.Session()

    def get_response(url):
        """Function to retry a failed get request"""
        try:
            # GET request the API
            response = session.get(url, timeout=10)
        except (requests.exceptions.ReadTimeout, 
                requests.exceptions.ConnectionError):
            print("Request timed out, trying again.\n")
            response = get_response(url)
        return response

    # 1: Webscrape the data
    url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
    r = get_response(url)
    r_string = r.content.decode("utf-8")
    splitted_td = r_string.split('<a href=')

    # 2: Find correct file
    for string in splitted_td:

        if "2022-02-07 14:03" in string:
            to_parse = string
            break
    
    # 3: Download file
    csv_name = string.split('"')[1]
    download_url = url + csv_name
    new_req = get_response(download_url).content
    with open("download_weather.csv", "wb") as file:
        file.write(new_req)
    df = pd.read_csv("download_weather.csv")

    # 4: With Pandas find highest X
    df = df.sort_values('HourlyDryBulbTemperature', ascending=False)

    # 5: Print highest records
    print(df.head(5))


if __name__ == '__main__':
    main()
