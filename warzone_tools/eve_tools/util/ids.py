import requests
from django.core.cache import cache

class EveIDTranslator:
    EVE_API_URL = "https://esi.evetech.net/latest/universe/names/?datasource=tranquility"
    CACHE = {}

    @classmethod
    def translate_ids(cls, ids):
        """
        Translate a list of EVE Online IDs (factionID, systemID, etc.) into human-readable names.
        Uses a cache to minimize API calls.
        """
        ids_to_fetch = [id_ for id_ in ids if id_ not in cls.CACHE]

        if ids_to_fetch:
            try:
                response = requests.post(
                    cls.EVE_API_URL,
                    headers={
                        "accept": "application/json",
                        "Content-Type": "application/json",
                        "Cache-Control": "no-cache",
                    },
                    json=ids_to_fetch
                )
                response.raise_for_status()
                results = response.json()

                for result in results:
                    cls.CACHE[result['id']] = result['name']

            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch names from EVE API: {e}")
                return None

        return {id_: cls.CACHE.get(id_, "Unknown") for id_ in ids}

    @classmethod
    def translate_id(cls, id_):
        """Translate a single EVE Online ID into a human-readable name."""
        return cls.translate_ids([id_]).get(id_, "Unknown")