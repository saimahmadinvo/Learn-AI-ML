from pydantic import BaseModel, ValidationError, model_validator
from AiServices import askai
import json


# -----------------------------
# Pydantic Models
# -----------------------------

class UMLNode(BaseModel):
    node_id: int
    node_name: str


class UMLRelation(BaseModel):
    node_source: int
    node_target: int


class NodeObject(BaseModel):
    node_array: list[UMLNode]
    node_relation: list[UMLRelation]

    @model_validator(mode="after")
    def validate_relationships(self):
        """Ensure every relationship references an existing node_id."""
        valid_ids = {node.node_id for node in self.node_array}

        for relation in self.node_relation:
            if relation.node_source not in valid_ids:
                raise ValueError(
                    f"node_source {relation.node_source} does not exist."
                )

            if relation.node_target not in valid_ids:
                raise ValueError(
                    f"node_target {relation.node_target} does not exist."
                )

        return self


# -----------------------------
# User Input
# -----------------------------

user_prompt = input("Enter your system details: ")

# -----------------------------
# Ask AI
# -----------------------------

response = askai(
    user_prompt,
    system_prompt="""
You are an expert software architect.

Your task is to analyze the user's software description and convert it into a UML graph represented as JSON.

Return ONLY valid JSON.

The JSON must exactly match this structure:

{
    "node_array": [
        {
            "node_id": 1,
            "node_name": "Example"
        }
    ],
    "node_relation": [
        {
            "node_source": 1,
            "node_target": 2
        }
    ]
}

Rules:

- Identify all important classes/entities/components.
- Every entity becomes exactly one node.
- node_id starts from 1 and increases sequentially.
- node_name should be singular and in PascalCase.
- node_source and node_target must reference existing node_ids.
- Do not duplicate nodes.
- Only create relationships that are clearly implied.
- If no relationships exist, return an empty node_relation array.
- If no entities can be identified, return empty arrays.

Return ONLY JSON.
""",
    temperature=0, 
    stream: True
)

# -----------------------------
# Parse JSON
# -----------------------------

try:
    data = json.loads(response)
except json.JSONDecodeError as e:
    print("The AI did not return valid JSON.")
    print(e)
    exit()

# -----------------------------
# Validate with Pydantic
# -----------------------------

try:
    uml = NodeObject.model_validate(data)

    print("\n========== UML Nodes ==========")
    for node in uml.node_array:
        print(f"ID: {node.node_id} | Name: {node.node_name}")

    print("\n====== UML Relationships ======")
    if uml.node_relation:
        for relation in uml.node_relation:
            print(f"{relation.node_source} --> {relation.node_target}")
    else:
        print("No relationships found.")

except ValidationError as e:
    print("\nValidation Error:")
    print(e)
except ValueError as e:
    print("\nRelationship Validation Error:")
    print(e)