import json

def get_countries():
    with open("data/countries.json", "r") as file:
        return {entry["name"]: entry for entry in json.load(file)}

if __name__ == "__main__":
    countries = get_countries()
    print(countries)