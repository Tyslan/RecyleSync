STREET_END_POINT = "streets"

STREET_ZIP_CODE = "zipcodes"
STREET_QUERY = "q"


class StreetRequest:
    def __init__(self, zip_code_id: str, query: str):
        self.params = {STREET_ZIP_CODE: zip_code_id, STREET_QUERY: query}
        self.path = STREET_END_POINT

    @classmethod
    def parse_web_response(cls, response: dict, language: str = "nl") -> list:
        items = response["items"]
        result = []
        for item in items:
            id = item["id"]
            names = item["names"]
            street_name = names[language]
            result.append(Street(id,  street_name))
        return result


class Street:
    def __init__(self, id: str, name: str,):
        self.id = id
        self.name = name

    def __str__(self):
        return f"Id: {self.id}, name: {self.name}"
