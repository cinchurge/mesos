# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mesos/module/hook.proto

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
  name='mesos/module/hook.proto',
  package='mesos',
  syntax='proto2',
  serialized_pb=_b('\n\x17mesos/module/hook.proto\x12\x05mesos\x1a\x11mesos/mesos.proto\"}\n\x1d\x44ockerTaskExecutorPrepareInfo\x12/\n\x13\x65xecutorEnvironment\x18\x01 \x01(\x0b\x32\x12.mesos.Environment\x12+\n\x0ftaskEnvironment\x18\x02 \x01(\x0b\x32\x12.mesos.EnvironmentB\x1a\n\x10org.apache.mesosB\x06Protos')
  ,
  dependencies=[mesos_dot_mesos__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_DOCKERTASKEXECUTORPREPAREINFO = _descriptor.Descriptor(
  name='DockerTaskExecutorPrepareInfo',
  full_name='mesos.DockerTaskExecutorPrepareInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='executorEnvironment', full_name='mesos.DockerTaskExecutorPrepareInfo.executorEnvironment', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='taskEnvironment', full_name='mesos.DockerTaskExecutorPrepareInfo.taskEnvironment', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=53,
  serialized_end=178,
)

_DOCKERTASKEXECUTORPREPAREINFO.fields_by_name['executorEnvironment'].message_type = mesos_dot_mesos__pb2._ENVIRONMENT
_DOCKERTASKEXECUTORPREPAREINFO.fields_by_name['taskEnvironment'].message_type = mesos_dot_mesos__pb2._ENVIRONMENT
DESCRIPTOR.message_types_by_name['DockerTaskExecutorPrepareInfo'] = _DOCKERTASKEXECUTORPREPAREINFO

DockerTaskExecutorPrepareInfo = _reflection.GeneratedProtocolMessageType('DockerTaskExecutorPrepareInfo', (_message.Message,), dict(
  DESCRIPTOR = _DOCKERTASKEXECUTORPREPAREINFO,
  __module__ = 'mesos.module.hook_pb2'
  # @@protoc_insertion_point(class_scope:mesos.DockerTaskExecutorPrepareInfo)
  ))
_sym_db.RegisterMessage(DockerTaskExecutorPrepareInfo)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\020org.apache.mesosB\006Protos'))
# @@protoc_insertion_point(module_scope)