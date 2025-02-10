from datetime import datetime

import requests
from demo_temp.src.core.entities.producer import Producer
from demo_temp.src.core.entities.opencti.connector import Connector


class FetchSarielAPI(Producer):

    def produce(self):

        today_date = datetime.today().strftime('%Y-%m-%d')
        url = f"https://raw.githubusercontent.com/sari3l/Poc-Monitor/refs/heads/main/dateLog/{today_date}.json"
        Connector()._logger.info(f"Fetching data from {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()

            # Return the fetched JSON data
            json_data = response.json()
            self.queue.put(json_data)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

