# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mesos/slave/oversubscription.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mesos import mesos_pb2 as mesos_dot_mesos__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mesos/slave/oversubscription.proto',
  package='mesos.slave',
  syntax='proto2',
  serialized_pb=_b('\n\"mesos/slave/oversubscription.proto\x12\x0bmesos.slave\x1a\x11mesos/mesos.proto\"\x84\x02\n\rQoSCorrection\x12-\n\x04type\x18\x01 \x02(\x0e\x32\x1f.mesos.slave.QoSCorrection.Type\x12-\n\x04kill\x18\x02 \x01(\x0b\x32\x1f.mesos.slave.QoSCorrection.Kill\x1a\x82\x01\n\x04Kill\x12(\n\x0c\x66ramework_id\x18\x01 \x01(\x0b\x32\x12.mesos.FrameworkID\x12&\n\x0b\x65xecutor_id\x18\x02 \x01(\x0b\x32\x11.mesos.ExecutorID\x12(\n\x0c\x63ontainer_id\x18\x03 \x01(\x0b\x32\x12.mesos.ContainerID\"\x10\n\x04Type\x12\x08\n\x04KILL\x10\x01\x42\x1a\n\x10org.apache.mesosB\x06Protos')
  ,
  dependencies=[mesos_dot_mesos__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_QOSCORRECTION_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='mesos.slave.QoSCorrection.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='KILL', index=0, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=315,
  serialized_end=331,
)
_sym_db.RegisterEnumDescriptor(_QOSCORRECTION_TYPE)


_QOSCORRECTION_KILL = _descriptor.Descriptor(
  name='Kill',
  full_name='mesos.slave.QoSCorrection.Kill',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='framework_id', full_name='mesos.slave.QoSCorrection.Kill.framework_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='executor_id', full_name='mesos.slave.QoSCorrection.Kill.executor_id', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='container_id', full_name='mesos.slave.QoSCorrection.Kill.container_id', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=183,
  serialized_end=313,
)

_QOSCORRECTION = _descriptor.Descriptor(
  name='QoSCorrection',
  full_name='mesos.slave.QoSCorrection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='mesos.slave.QoSCorrection.type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='kill', full_name='mesos.slave.QoSCorrection.kill', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_QOSCORRECTION_KILL, ],
  enum_types=[
    _QOSCORRECTION_TYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=71,
  serialized_end=331,
)

_QOSCORRECTION_KILL.fields_by_name['framework_id'].message_type = mesos_dot_mesos__pb2._FRAMEWORKID
_QOSCORRECTION_KILL.fields_by_name['executor_id'].message_type = mesos_dot_mesos__pb2._EXECUTORID
_QOSCORRECTION_KILL.fields_by_name['container_id'].message_type = mesos_dot_mesos__pb2._CONTAINERID
_QOSCORRECTION_KILL.containing_type = _QOSCORRECTION
_QOSCORRECTION.fields_by_name['type'].enum_type = _QOSCORRECTION_TYPE
_QOSCORRECTION.fields_by_name['kill'].message_type = _QOSCORRECTION_KILL
_QOSCORRECTION_TYPE.containing_type = _QOSCORRECTION
DESCRIPTOR.message_types_by_name['QoSCorrection'] = _QOSCORRECTION

QoSCorrection = _reflection.GeneratedProtocolMessageType('QoSCorrection', (_message.Message,), dict(

  Kill = _reflection.GeneratedProtocolMessageType('Kill', (_message.Message,), dict(
    DESCRIPTOR = _QOSCORRECTION_KILL,
    __module__ = 'mesos.slave.oversubscription_pb2'
    # @@protoc_insertion_point(class_scope:mesos.slave.QoSCorrection.Kill)
    ))
  ,
  DESCRIPTOR = _QOSCORRECTION,
  __module__ = 'mesos.slave.oversubscription_pb2'
  # @@protoc_insertion_point(class_scope:mesos.slave.QoSCorrection)
  ))
_sym_db.RegisterMessage(QoSCorrection)
_sym_db.RegisterMessage(QoSCorrection.Kill)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\020org.apache.mesosB\006Protos'))
# @@protoc_insertion_point(module_scope)
