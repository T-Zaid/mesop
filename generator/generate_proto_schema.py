import generator.component_spec_pb2 as pb
from generator.format_types import format_proto_xtype
from generator.utils import (
  snake_case,
  upper_camel_case,
)


def generate_proto_schema(spec: pb.ComponentSpec) -> str:
  fields: list[str] = []
  index = 0

  for prop in spec.input_props:
    index += 1
    fields.append(
      f"{format_proto_xtype(prop.type)} {snake_case(prop.name)} = {index};"
    )
  for prop in spec.output_props:
    index += 1
    fields.append(
      f"string on_{snake_case(prop.event_name)}_handler_id = {index};"
    )

  for native_event in spec.input.native_events:
    index += 1
    fields.append(f"string on_{native_event}_handler_id = {index};")

  if len(spec.input.directive_names):
    index += 1
    fields.append(f"int32 type_index = {index};")

  message_contents = (
    "{\n" + "\n".join(["  " + field for field in fields]) + "\n}"
  )

  return f"""
syntax = "proto2";

package mesop.components.{spec.input.name};

message {upper_camel_case(spec.input.name)}Type {message_contents}

  """
