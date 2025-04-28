# ImpactMap Python SDK

This is the official Python SDK for interacting with the ImpactMap API.

## Usage Example

```python
from impactmap import ImpactMap

client = ImpactMap(api_key="YOUR_API_KEY")
projects = client.projects.list()
print(projects)
```

## Features
- Simple, modern API for integrating with ImpactMap
- Mirrors the structure of the official JavaScript/TypeScript SDK
- Resource APIs: Projects, Contacts, Impact Metrics, Tenants

## TODO
- Implement authentication helpers
- Add CLI support
- Expand API coverage

## License
MIT
