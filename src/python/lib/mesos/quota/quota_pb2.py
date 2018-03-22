# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mesos/quota/quota.proto

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
  name='mesos/quota/quota.proto',
  package='mesos.quota',
  syntax='proto2',
  serialized_pb=_b('\n\x17mesos/quota/quota.proto\x12\x0bmesos.quota\x1a\x11mesos/mesos.proto\"P\n\tQuotaInfo\x12\x0c\n\x04role\x18\x01 \x01(\t\x12\x11\n\tprincipal\x18\x02 \x01(\t\x12\"\n\tguarantee\x18\x03 \x03(\x0b\x32\x0f.mesos.Resource\"V\n\x0cQuotaRequest\x12\x14\n\x05\x66orce\x18\x01 \x01(\x08:\x05\x66\x61lse\x12\x0c\n\x04role\x18\x02 \x01(\t\x12\"\n\tguarantee\x18\x03 \x03(\x0b\x32\x0f.mesos.Resource\"4\n\x0bQuotaStatus\x12%\n\x05infos\x18\x01 \x03(\x0b\x32\x16.mesos.quota.QuotaInfoB \n\x16org.apache.mesos.quotaB\x06Protos')
  ,
  dependencies=[mesos_dot_mesos__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_QUOTAINFO = _descriptor.Descriptor(
  name='QuotaInfo',
  full_name='mesos.quota.QuotaInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='role', full_name='mesos.quota.QuotaInfo.role', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='principal', full_name='mesos.quota.QuotaInfo.principal', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='guarantee', full_name='mesos.quota.QuotaInfo.guarantee', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=59,
  serialized_end=139,
)


_QUOTAREQUEST = _descriptor.Descriptor(
  name='QuotaRequest',
  full_name='mesos.quota.QuotaRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='force', full_name='mesos.quota.QuotaRequest.force', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='role', full_name='mesos.quota.QuotaRequest.role', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='guarantee', full_name='mesos.quota.QuotaRequest.guarantee', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=141,
  serialized_end=227,
)


_QUOTASTATUS = _descriptor.Descriptor(
  name='QuotaStatus',
  full_name='mesos.quota.QuotaStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='infos', full_name='mesos.quota.QuotaStatus.infos', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=229,
  serialized_end=281,
)

_QUOTAINFO.fields_by_name['guarantee'].message_type = mesos_dot_mesos__pb2._RESOURCE
_QUOTAREQUEST.fields_by_name['guarantee'].message_type = mesos_dot_mesos__pb2._RESOURCE
_QUOTASTATUS.fields_by_name['infos'].message_type = _QUOTAINFO
DESCRIPTOR.message_types_by_name['QuotaInfo'] = _QUOTAINFO
DESCRIPTOR.message_types_by_name['QuotaRequest'] = _QUOTAREQUEST
DESCRIPTOR.message_types_by_name['QuotaStatus'] = _QUOTASTATUS

QuotaInfo = _reflection.GeneratedProtocolMessageType('QuotaInfo', (_message.Message,), dict(
  DESCRIPTOR = _QUOTAINFO,
  __module__ = 'mesos.quota.quota_pb2'
  # @@protoc_insertion_point(class_scope:mesos.quota.QuotaInfo)
  ))
_sym_db.RegisterMessage(QuotaInfo)

QuotaRequest = _reflection.GeneratedProtocolMessageType('QuotaRequest', (_message.Message,), dict(
  DESCRIPTOR = _QUOTAREQUEST,
  __module__ = 'mesos.quota.quota_pb2'
  # @@protoc_insertion_point(class_scope:mesos.quota.QuotaRequest)
  ))
_sym_db.RegisterMessage(QuotaRequest)

QuotaStatus = _reflection.GeneratedProtocolMessageType('QuotaStatus', (_message.Message,), dict(
  DESCRIPTOR = _QUOTASTATUS,
  __module__ = 'mesos.quota.quota_pb2'
  # @@protoc_insertion_point(class_scope:mesos.quota.QuotaStatus)
  ))
_sym_db.RegisterMessage(QuotaStatus)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\026org.apache.mesos.quotaB\006Protos'))
# @@protoc_insertion_point(module_scope)