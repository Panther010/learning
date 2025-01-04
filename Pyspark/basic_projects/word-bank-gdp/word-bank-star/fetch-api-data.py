import logging
import os
import json
import requests

class APIWordBank:

    def __init__(self, url, out_path):
        self.url = url
        self.output_path = out_path

        formatter = '%(levelname)s : %(filename)s : %(lineno)d : %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        self.log = logging.getLogger('logger')

    def fetch_data(self):
        self.log.info(f'Fetching data from World Bank API...')
        try:
            response = requests.get(self.url)
            print(response)
            response.raise_for_status()
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            self.log.error(f'Error fetching data from API as {e}')
            return None

    def write_data(self, data) -> None:
        self.log.info(f'Saving data to {output_path}...')
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(self.output_path, "w") as f:
                json.dump(data, f, indent=4)  # type: ignore

        except Exception as e:
            self.log.error(f'Error while writing data to path {self.output_path} error details: {e}')
            raise e

    def main(self) -> None:
        response_data = self.fetch_data()
        self.write_data(response_data)


if __name__ == '__main__':
    api_url = "https://api.worldbank.org/v2/country?format=json"
    output_path = '../../../input_data/raw/world_bank_countries.json'
    word_bank = APIWordBank(api_url, output_path)
    word_bank.main()
