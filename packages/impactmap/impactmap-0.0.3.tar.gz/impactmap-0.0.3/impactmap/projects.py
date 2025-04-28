# impactmap/projects.py
class ProjectsAPI:
    def __init__(self, client):
        self.client = client

    def list(self):
        """List all projects."""
        return self.client.request("GET", "/projects")

    def get(self, project_id):
        """Get a specific project by ID."""
        return self.client.request("GET", f"/projects/{project_id}")

    def create(self, data):
        """Create a new project."""
        return self.client.request("POST", "/projects", data=data)

    def update(self, project_id, data):
        """Update a project."""
        return self.client.request("PATCH", f"/projects/{project_id}", data=data)

    def delete(self, project_id):
        """Delete a project."""
        return self.client.request("DELETE", f"/projects/{project_id}")
