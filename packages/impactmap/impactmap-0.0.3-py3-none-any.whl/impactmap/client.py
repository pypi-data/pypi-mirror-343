# impactmap/client.py
from .projects import ProjectsAPI
from .tenants import TenantsAPI
from .contacts import ContactsAPI
from .impact_metrics import ImpactMetricsAPI

class ImpactMap:
    def __init__(self, api_key: str, base_url: str = "https://api.impactmap.io/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.projects = ProjectsAPI(self)
        self.contacts = ContactsAPI(self)
        self.impact_metrics = ImpactMetricsAPI(self)
        self.tenants = TenantsAPI(self)

    def request(self, method: str, path: str, data=None, params=None):
        """Basic HTTP request helper."""
        import requests
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = requests.request(method, url, headers=headers, json=data, params=params)
        if not response.ok:
            raise Exception(f"HTTP error! status: {response.status_code}, body: {response.text}")
        return response.json()
