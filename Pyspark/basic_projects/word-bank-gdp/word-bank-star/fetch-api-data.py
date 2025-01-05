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

    def api_calls(self, parameters):
        self.log.info(f"API : {self.url}, Parameters : {parameters}")
        response = requests.get(f"{self.url}", params=parameters) if parameters else requests.get(f"{self.url}")
        if response.status_code == 200:
            self.log.info("successfully fetched the data with parameters provided")
            print(response.json())
        else:
            self.log.warning(f"Hello person, there's a {response.status_code} error with your request")
            self.log.warning(f"Response content: {response.text}")
        return response

    def fetch_data(self):
        self.log.info(f'Fetching data from World Bank API...')
        try:
            full_data = []
            param = {}
            resp = self.api_calls(param).json()
            if resp[0]['pages'] > 0:
                for i in range(1, resp[0]['pages'] + 1):
                    param['page'] = str(i)
                    resp1 = self.api_calls(param).json()
                    full_data.extend(resp1[1])

            return full_data

        except requests.exceptions.RequestException as e:
            self.log.error(f'Error fetching data from API as {e}')
            return None

    def write_data(self, data) -> None:
        self.log.info(f'Saving data to {output_path}...')
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(self.output_path, "w") as f:
                for record in data:
                    json.dump(record, f) # type: ignore
                    f.write("\n")

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
