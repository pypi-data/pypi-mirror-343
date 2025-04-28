# impactmap/tenants.py
import os

class TenantsAPI:
    def __init__(self, client):
        self.client = client
        self.internal_api_key = os.getenv("IMPACTMAP_INTERNAL_API_KEY")

    def list(self):
        """List all tenants (requires IMPACTMAP_INTERNAL_API_KEY)."""
        if not self.internal_api_key:
            raise Exception("IMPACTMAP_INTERNAL_API_KEY is not set. Please set it in your environment.")
        # This endpoint is based on the npm SDK
        return self.client.request("GET", "/saas/api/tenants")

    def get(self, slug):
        """Get a specific tenant by slug."""
        tenants = self.list()
        return next((t for t in tenants if t.get("slug") == slug), None)
