ZIP_CODES_END_POINT = "zipcodes"

ZIP_CODES_QUERY = "q"


class CityRequest:
    def __init__(self, zip_code: int):
        self.path = ZIP_CODES_END_POINT
        self.params = {ZIP_CODES_QUERY: zip_code}

    @classmethod
    def parse_web_response(cls, response: dict, language: str = "nl") -> list:
        items = response["items"]
        result = []
        for item in items:
            zip_code = item["code"]
            id = item["id"]
            available = item["available"]
            for name in item["names"]:
                city_name = name[language]
                result.append(City(id, zip_code, city_name, available))
        return result


class City:
    def __init__(self, id: str, zip_code: int, name: str, available: bool):
        self.id = id
        self.zip_code = zip_code
        self.name = name
        self.available = available

    def __str__(self):
        return f"Id: {self.id}, zip_code: {self.zip_code}, name: {self.name}, available: {self.available}"
