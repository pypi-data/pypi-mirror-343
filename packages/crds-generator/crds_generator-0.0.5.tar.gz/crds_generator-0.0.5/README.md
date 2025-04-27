# crds-generator

This tool was created to generate a simple kubernetes crds from a pydantic-like object.

You can install it as shown below:
```bash
pip install crds-generator
```

You can create a CRDS with the code below:
```python
from typing import Literal, Optional
import yaml
from crds_generator import CustomResourceDefinition, Schema, generate_crd, AdditionalPrinterColumns 


class Server(Schema):
    name: str
    cpu_type: str
    gpu_type: str
    os: Literal["mac", "linux"]

class Spec(Schema):
    servers: list[Server]
    budget: int

class Status(Schema):
    ping_result: bool

class ServerPool(Schema):
    spec: Spec
    status: Status = None


apc = AdditionalPrinterColumns(
    name="Name",
    type="string",
    description="Server Name",
    jsonPath= ".spec.servers[*].name"
)

print(
    yaml.dump(
        generate_crd(
            CustomResourceDefinition(
                spec={
                    "scope": "Namespaced",
                    "group": "example.com",
                    "names": {
                        "kind": "ServerPool",
                        "plural": "serverpools",
                        "singular": "serverpool",
                        "shortNames": ["sp"],
                    },
                    "versions": [
                        {
                            "name": "v1",
                            "served": True,
                            "storage": True,
                            "schema": ServerPool,
                            "additionalPrinterColumns": [
                                apc
                            ],
                        }
                    ],
                },
            )
        )
    )
)
```

then print
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: serverpools.example.com
spec:
  group: example.com
  names:
    kind: ServerPool
    plural: serverpools
    shortNames:
    - sp
    singular: serverpool
  scope: Namespaced
  versions:
  - additionalPrinterColumns:
    - description: Server Name
      jsonPath: .spec.servers[*].name
      name: Name
      type: string
    name: v1
    schema:
      openAPIV3Schema:
        properties:
          spec:
            properties:
              budget:
                type: integer
              servers:
                items:
                  properties:
                    cpu_type:
                      type: string
                    gpu_type:
                      type: string
                    name:
                      type: string
                    os:
                      enum:
                      - mac
                      - linux
                      type: string
                  required:
                  - name
                  - cpu_type
                  - gpu_type
                  - os
                  type: object
                type: array
            required:
            - servers
            - budget
            type: object
          status:
            properties:
              ping_result:
                type: boolean
            required:
            - ping_result
            type: object
        required:
        - spec
        type: object
    served: true
    storage: true
```