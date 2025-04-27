from pydantic import BaseModel, RootModel, Field
from typing import Literal
from enum import Enum


class ODINDBModelType(str, Enum):
    U8 = "u8"
    U16 = "u16"
    U32 = "u32"
    U64 = "u64"
    I8 = "i8"
    I16 = "i16"
    I32 = "i32"
    I64 = "i64"
    F32 = "f32"
    F64 = "f64"
    BOOL = "bool"
    CHAR = "char"

    @classmethod
    def from_string(cls, value: str) -> "ODINDBModelType":
        try:
            return cls(value)
        except KeyError:
            raise ValueError(f"Invalid type: {value}")


class OdinDBTypeDefinitionModel(BaseModel):
    type: Literal["type_definition"] = Field(default="type_definition", description="Type of the type definition")
    size: int = Field(description="Size of the structure in bytes")
    structure: "ODINDBModelType | list[ODINDBModelType] | dict[str, OdinDBTypeDefinitionModel | ODINDBModelType]" = (
        Field(description="Structure of the type definition, key value based")
    )


class OdinDBParameterModel(BaseModel):
    type: Literal["parameter"] = Field(default="parameter", description="Type of the parameter")
    name: str = Field(description="Name of the parameter")
    description: str = Field(description="Description of the parameter")
    global_id: int = Field(description="Global ID of the parameter")
    global_name: str = Field(description="Global name of the parameter")

    size: int = Field(description="Size of the parameter in bytes")
    element_type: str = Field(description="Type of the parameter")


class OdinDBParameterGroupModel(BaseModel):
    type: Literal["parameter_group"] = Field(default="parameter_group", description="Type of the parameter group")
    name: str = Field(description="Name of the parameter group")
    global_name: str = Field(description="Global name of the parameter group")
    description: str = Field(description="Description of the parameter group")
    parameters: "list[OdinDBParameterModel|OdinDBParameterGroupModel]" = Field(
        description="List of parameters in the group"
    )

    def as_flat_dict(self) -> dict[int, OdinDBParameterModel]:
        flat_dict = {}
        for param in self.parameters:
            if isinstance(param, OdinDBParameterModel):
                flat_dict[param.global_id] = param
            else:
                flat_dict.update(param.as_flat_dict())
        return flat_dict


class OdinDBModel(BaseModel):
    name: str
    description: str
    creation_timestamp: float  # Unix timestamp
    configuration_hash: int
    types: dict[str, OdinDBTypeDefinitionModel] | None = Field(description="Type definitions for the model")
    root: OdinDBParameterGroupModel
