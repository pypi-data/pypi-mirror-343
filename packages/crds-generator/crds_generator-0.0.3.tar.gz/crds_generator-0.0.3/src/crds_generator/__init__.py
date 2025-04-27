from typing import Any, Literal, Type

from pydantic import (
    BaseModel,
    ConfigDict,
    GetJsonSchemaHandler,
    field_serializer,
    model_validator,
)
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue
from pydantic_core import core_schema as cs


class Metadata(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )

    name: str


class Names(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )

    kind: str
    plural: str
    singular: str
    shortNames: list[str]


class Schema(BaseModel):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: cs.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        return cleaning(handler, json_schema)


class AdditionalPrinterColumns(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )

    name: str
    type: str
    description: str
    jsonPath: str


class Version(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )

    name: str
    served: bool
    storage: bool
    schema: Type[Schema]
    additionalPrinterColumns: list[AdditionalPrinterColumns]

    @field_serializer("schema")
    def serialize_schema(self, schema: BaseModel):
        return {
            "openAPIV3Schema": schema.model_json_schema(
                schema_generator=GenerateOptionalJsonSchema
            ),
        }


class Spec(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )

    scope: Literal["Namespaced", "Cluster"]
    group: str
    names: Names
    versions: list[Version]


def cleaning(handler: GetJsonSchemaHandler, schema: dict[str, Any]):
    schema = handler.resolve_ref_schema(schema)

    if "title" in schema:
        del schema["title"]

    for key in ["items"]:
        if key in schema:
            schema[key] = cleaning(handler, schema[key])

    for key in ["properties"]:
        if key in schema:
            for k in schema[key]:
                schema[key][k] = cleaning(handler, schema[key][k])

    for key in ["anyOf"]:
        if key in schema:
            for i in range(len(schema[key])):
                schema[key][i] = cleaning(handler, schema[key][i])

    return schema


class GenerateOptionalJsonSchema(GenerateJsonSchema):
    def nullable_schema(self, schema: cs.NullableSchema) -> JsonSchemaValue:
        return self.generate_inner(schema["schema"])


class CustomResourceDefinition(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )

    apiVersion: str = "apiextensions.k8s.io/v1"
    kind: str = "CustomResourceDefinition"
    metadata: Metadata
    spec: Spec

    @model_validator(mode="before")
    def inject_name(cls, values: dict[str, Any]) -> dict[str, Any]:
        metadata = values.get("metadata", {})
        metadata["name"] = (
            f"{values['spec']['names']['plural']}.{values['spec']['group']}"
        )
        values["metadata"] = metadata
        return values


def generate_crd(crd: CustomResourceDefinition):
    return crd.model_dump()
