import os
import requests
import json
from dotenv import load_dotenv


def main(id):
    load_dotenv()
    api_key = os.getenv('RAGIC_API_2')

    base_url = 'https://ap12.ragic.com/cancerfree/articles/4'
    params = {'api': '', 'v': 3}

    data = {
        1003463: "No"
    }

    json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
    # print("Sending JSON data:", json_data.decode('utf-8'))

    response = requests.post(f"{base_url}/{id}",
                             headers={'Authorization': f'Basic {api_key}',
                                      "Content-Type": "application/json; charset=utf-8"},
                             params=params,
                             data=json.dumps(data, ensure_ascii=False))
    #if response.status_code == 200:
        #print(f"Entry {id} updated successfully.")
    #else:
        #print(f"Failed to update Entry {id}: {response.text}")


if __name__ == "__main__":
    main()
