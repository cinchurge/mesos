# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mesos/executor/executor.proto

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
  name='mesos/executor/executor.proto',
  package='mesos.executor',
  syntax='proto2',
  serialized_pb=_b('\n\x1dmesos/executor/executor.proto\x12\x0emesos.executor\x1a\x11mesos/mesos.proto\"\xf0\x07\n\x05\x45vent\x12(\n\x04type\x18\x01 \x01(\x0e\x32\x1a.mesos.executor.Event.Type\x12\x34\n\nsubscribed\x18\x02 \x01(\x0b\x32 .mesos.executor.Event.Subscribed\x12\x38\n\x0c\x61\x63knowledged\x18\x03 \x01(\x0b\x32\".mesos.executor.Event.Acknowledged\x12,\n\x06launch\x18\x04 \x01(\x0b\x32\x1c.mesos.executor.Event.Launch\x12\x37\n\x0claunch_group\x18\x08 \x01(\x0b\x32!.mesos.executor.Event.LaunchGroup\x12(\n\x04kill\x18\x05 \x01(\x0b\x32\x1a.mesos.executor.Event.Kill\x12.\n\x07message\x18\x06 \x01(\x0b\x32\x1d.mesos.executor.Event.Message\x12*\n\x05\x65rror\x18\x07 \x01(\x0b\x32\x1b.mesos.executor.Event.Error\x1a\xb6\x01\n\nSubscribed\x12*\n\rexecutor_info\x18\x01 \x02(\x0b\x32\x13.mesos.ExecutorInfo\x12,\n\x0e\x66ramework_info\x18\x02 \x02(\x0b\x32\x14.mesos.FrameworkInfo\x12$\n\nslave_info\x18\x03 \x02(\x0b\x32\x10.mesos.SlaveInfo\x12(\n\x0c\x63ontainer_id\x18\x04 \x01(\x0b\x32\x12.mesos.ContainerID\x1a\'\n\x06Launch\x12\x1d\n\x04task\x18\x01 \x02(\x0b\x32\x0f.mesos.TaskInfo\x1a\x37\n\x0bLaunchGroup\x12(\n\ntask_group\x18\x01 \x02(\x0b\x32\x14.mesos.TaskGroupInfo\x1aN\n\x04Kill\x12\x1e\n\x07task_id\x18\x01 \x02(\x0b\x32\r.mesos.TaskID\x12&\n\x0bkill_policy\x18\x02 \x01(\x0b\x32\x11.mesos.KillPolicy\x1a<\n\x0c\x41\x63knowledged\x12\x1e\n\x07task_id\x18\x01 \x02(\x0b\x32\r.mesos.TaskID\x12\x0c\n\x04uuid\x18\x02 \x02(\x0c\x1a\x17\n\x07Message\x12\x0c\n\x04\x64\x61ta\x18\x01 \x02(\x0c\x1a\x18\n\x05\x45rror\x12\x0f\n\x07message\x18\x01 \x02(\t\"\x83\x01\n\x04Type\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0e\n\nSUBSCRIBED\x10\x01\x12\n\n\x06LAUNCH\x10\x02\x12\x10\n\x0cLAUNCH_GROUP\x10\x08\x12\x08\n\x04KILL\x10\x03\x12\x10\n\x0c\x41\x43KNOWLEDGED\x10\x04\x12\x0b\n\x07MESSAGE\x10\x05\x12\t\n\x05\x45RROR\x10\x06\x12\x0c\n\x08SHUTDOWN\x10\x07\"\x8c\x04\n\x04\x43\x61ll\x12&\n\x0b\x65xecutor_id\x18\x01 \x02(\x0b\x32\x11.mesos.ExecutorID\x12(\n\x0c\x66ramework_id\x18\x02 \x02(\x0b\x32\x12.mesos.FrameworkID\x12\'\n\x04type\x18\x03 \x01(\x0e\x32\x19.mesos.executor.Call.Type\x12\x31\n\tsubscribe\x18\x04 \x01(\x0b\x32\x1e.mesos.executor.Call.Subscribe\x12+\n\x06update\x18\x05 \x01(\x0b\x32\x1b.mesos.executor.Call.Update\x12-\n\x07message\x18\x06 \x01(\x0b\x32\x1c.mesos.executor.Call.Message\x1aw\n\tSubscribe\x12-\n\x14unacknowledged_tasks\x18\x01 \x03(\x0b\x32\x0f.mesos.TaskInfo\x12;\n\x16unacknowledged_updates\x18\x02 \x03(\x0b\x32\x1b.mesos.executor.Call.Update\x1a+\n\x06Update\x12!\n\x06status\x18\x01 \x02(\x0b\x32\x11.mesos.TaskStatus\x1a\x17\n\x07Message\x12\x0c\n\x04\x64\x61ta\x18\x02 \x02(\x0c\";\n\x04Type\x12\x0b\n\x07UNKNOWN\x10\x00\x12\r\n\tSUBSCRIBE\x10\x01\x12\n\n\x06UPDATE\x10\x02\x12\x0b\n\x07MESSAGE\x10\x03\x42#\n\x19org.apache.mesos.executorB\x06Protos')
  ,
  dependencies=[mesos_dot_mesos__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_EVENT_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='mesos.executor.Event.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUBSCRIBED', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LAUNCH', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LAUNCH_GROUP', index=3, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='KILL', index=4, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ACKNOWLEDGED', index=5, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE', index=6, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=7, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SHUTDOWN', index=8, number=7,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=946,
  serialized_end=1077,
)
_sym_db.RegisterEnumDescriptor(_EVENT_TYPE)

_CALL_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='mesos.executor.Call.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUBSCRIBE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UPDATE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1545,
  serialized_end=1604,
)
_sym_db.RegisterEnumDescriptor(_CALL_TYPE)


_EVENT_SUBSCRIBED = _descriptor.Descriptor(
  name='Subscribed',
  full_name='mesos.executor.Event.Subscribed',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='executor_info', full_name='mesos.executor.Event.Subscribed.executor_info', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='framework_info', full_name='mesos.executor.Event.Subscribed.framework_info', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='slave_info', full_name='mesos.executor.Event.Subscribed.slave_info', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='container_id', full_name='mesos.executor.Event.Subscribed.container_id', index=3,
      number=4, type=11, cpp_type=10, label=1,
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
  serialized_start=470,
  serialized_end=652,
)

_EVENT_LAUNCH = _descriptor.Descriptor(
  name='Launch',
  full_name='mesos.executor.Event.Launch',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='task', full_name='mesos.executor.Event.Launch.task', index=0,
      number=1, type=11, cpp_type=10, label=2,
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
  serialized_start=654,
  serialized_end=693,
)

_EVENT_LAUNCHGROUP = _descriptor.Descriptor(
  name='LaunchGroup',
  full_name='mesos.executor.Event.LaunchGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_group', full_name='mesos.executor.Event.LaunchGroup.task_group', index=0,
      number=1, type=11, cpp_type=10, label=2,
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
  serialized_start=695,
  serialized_end=750,
)

_EVENT_KILL = _descriptor.Descriptor(
  name='Kill',
  full_name='mesos.executor.Event.Kill',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_id', full_name='mesos.executor.Event.Kill.task_id', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='kill_policy', full_name='mesos.executor.Event.Kill.kill_policy', index=1,
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
  serialized_start=752,
  serialized_end=830,
)

_EVENT_ACKNOWLEDGED = _descriptor.Descriptor(
  name='Acknowledged',
  full_name='mesos.executor.Event.Acknowledged',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_id', full_name='mesos.executor.Event.Acknowledged.task_id', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uuid', full_name='mesos.executor.Event.Acknowledged.uuid', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
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
  serialized_start=832,
  serialized_end=892,
)

_EVENT_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='mesos.executor.Event.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='mesos.executor.Event.Message.data', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
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
  serialized_start=894,
  serialized_end=917,
)

_EVENT_ERROR = _descriptor.Descriptor(
  name='Error',
  full_name='mesos.executor.Event.Error',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='mesos.executor.Event.Error.message', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=919,
  serialized_end=943,
)

_EVENT = _descriptor.Descriptor(
  name='Event',
  full_name='mesos.executor.Event',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='mesos.executor.Event.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='subscribed', full_name='mesos.executor.Event.subscribed', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='acknowledged', full_name='mesos.executor.Event.acknowledged', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='launch', full_name='mesos.executor.Event.launch', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='launch_group', full_name='mesos.executor.Event.launch_group', index=4,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='kill', full_name='mesos.executor.Event.kill', index=5,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='message', full_name='mesos.executor.Event.message', index=6,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='error', full_name='mesos.executor.Event.error', index=7,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_EVENT_SUBSCRIBED, _EVENT_LAUNCH, _EVENT_LAUNCHGROUP, _EVENT_KILL, _EVENT_ACKNOWLEDGED, _EVENT_MESSAGE, _EVENT_ERROR, ],
  enum_types=[
    _EVENT_TYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=69,
  serialized_end=1077,
)


_CALL_SUBSCRIBE = _descriptor.Descriptor(
  name='Subscribe',
  full_name='mesos.executor.Call.Subscribe',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='unacknowledged_tasks', full_name='mesos.executor.Call.Subscribe.unacknowledged_tasks', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='unacknowledged_updates', full_name='mesos.executor.Call.Subscribe.unacknowledged_updates', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  serialized_start=1354,
  serialized_end=1473,
)

_CALL_UPDATE = _descriptor.Descriptor(
  name='Update',
  full_name='mesos.executor.Call.Update',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='mesos.executor.Call.Update.status', index=0,
      number=1, type=11, cpp_type=10, label=2,
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
  serialized_start=1475,
  serialized_end=1518,
)

_CALL_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='mesos.executor.Call.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='mesos.executor.Call.Message.data', index=0,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
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
  serialized_start=1520,
  serialized_end=1543,
)

_CALL = _descriptor.Descriptor(
  name='Call',
  full_name='mesos.executor.Call',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='executor_id', full_name='mesos.executor.Call.executor_id', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='framework_id', full_name='mesos.executor.Call.framework_id', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='type', full_name='mesos.executor.Call.type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='subscribe', full_name='mesos.executor.Call.subscribe', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='update', full_name='mesos.executor.Call.update', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='message', full_name='mesos.executor.Call.message', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_CALL_SUBSCRIBE, _CALL_UPDATE, _CALL_MESSAGE, ],
  enum_types=[
    _CALL_TYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1080,
  serialized_end=1604,
)

_EVENT_SUBSCRIBED.fields_by_name['executor_info'].message_type = mesos_dot_mesos__pb2._EXECUTORINFO
_EVENT_SUBSCRIBED.fields_by_name['framework_info'].message_type = mesos_dot_mesos__pb2._FRAMEWORKINFO
_EVENT_SUBSCRIBED.fields_by_name['slave_info'].message_type = mesos_dot_mesos__pb2._SLAVEINFO
_EVENT_SUBSCRIBED.fields_by_name['container_id'].message_type = mesos_dot_mesos__pb2._CONTAINERID
_EVENT_SUBSCRIBED.containing_type = _EVENT
_EVENT_LAUNCH.fields_by_name['task'].message_type = mesos_dot_mesos__pb2._TASKINFO
_EVENT_LAUNCH.containing_type = _EVENT
_EVENT_LAUNCHGROUP.fields_by_name['task_group'].message_type = mesos_dot_mesos__pb2._TASKGROUPINFO
_EVENT_LAUNCHGROUP.containing_type = _EVENT
_EVENT_KILL.fields_by_name['task_id'].message_type = mesos_dot_mesos__pb2._TASKID
_EVENT_KILL.fields_by_name['kill_policy'].message_type = mesos_dot_mesos__pb2._KILLPOLICY
_EVENT_KILL.containing_type = _EVENT
_EVENT_ACKNOWLEDGED.fields_by_name['task_id'].message_type = mesos_dot_mesos__pb2._TASKID
_EVENT_ACKNOWLEDGED.containing_type = _EVENT
_EVENT_MESSAGE.containing_type = _EVENT
_EVENT_ERROR.containing_type = _EVENT
_EVENT.fields_by_name['type'].enum_type = _EVENT_TYPE
_EVENT.fields_by_name['subscribed'].message_type = _EVENT_SUBSCRIBED
_EVENT.fields_by_name['acknowledged'].message_type = _EVENT_ACKNOWLEDGED
_EVENT.fields_by_name['launch'].message_type = _EVENT_LAUNCH
_EVENT.fields_by_name['launch_group'].message_type = _EVENT_LAUNCHGROUP
_EVENT.fields_by_name['kill'].message_type = _EVENT_KILL
_EVENT.fields_by_name['message'].message_type = _EVENT_MESSAGE
_EVENT.fields_by_name['error'].message_type = _EVENT_ERROR
_EVENT_TYPE.containing_type = _EVENT
_CALL_SUBSCRIBE.fields_by_name['unacknowledged_tasks'].message_type = mesos_dot_mesos__pb2._TASKINFO
_CALL_SUBSCRIBE.fields_by_name['unacknowledged_updates'].message_type = _CALL_UPDATE
_CALL_SUBSCRIBE.containing_type = _CALL
_CALL_UPDATE.fields_by_name['status'].message_type = mesos_dot_mesos__pb2._TASKSTATUS
_CALL_UPDATE.containing_type = _CALL
_CALL_MESSAGE.containing_type = _CALL
_CALL.fields_by_name['executor_id'].message_type = mesos_dot_mesos__pb2._EXECUTORID
_CALL.fields_by_name['framework_id'].message_type = mesos_dot_mesos__pb2._FRAMEWORKID
_CALL.fields_by_name['type'].enum_type = _CALL_TYPE
_CALL.fields_by_name['subscribe'].message_type = _CALL_SUBSCRIBE
_CALL.fields_by_name['update'].message_type = _CALL_UPDATE
_CALL.fields_by_name['message'].message_type = _CALL_MESSAGE
_CALL_TYPE.containing_type = _CALL
DESCRIPTOR.message_types_by_name['Event'] = _EVENT
DESCRIPTOR.message_types_by_name['Call'] = _CALL

Event = _reflection.GeneratedProtocolMessageType('Event', (_message.Message,), dict(

  Subscribed = _reflection.GeneratedProtocolMessageType('Subscribed', (_message.Message,), dict(
    DESCRIPTOR = _EVENT_SUBSCRIBED,
    __module__ = 'mesos.executor.executor_pb2'
    # @@protoc_insertion_point(class_scope:mesos.executor.Event.Subscribed)
    ))
  ,

  Launch = _reflection.GeneratedProtocolMessageType('Launch', (_message.Message,), dict(
    DESCRIPTOR = _EVENT_LAUNCH,
    __module__ = 'mesos.executor.executor_pb2'
    # @@protoc_insertion_point(class_scope:mesos.executor.Event.Launch)
    ))
  ,

  LaunchGroup = _reflection.GeneratedProtocolMessageType('LaunchGroup', (_message.Message,), dict(
    DESCRIPTOR = _EVENT_LAUNCHGROUP,
    __module__ = 'mesos.executor.executor_pb2'
    # @@protoc_insertion_point(class_scope:mesos.executor.Event.LaunchGroup)
    ))
  ,

  Kill = _reflection.GeneratedProtocolMessageType('Kill', (_message.Message,), dict(
    DESCRIPTOR = _EVENT_KILL,
    __module__ = 'mesos.executor.executor_pb2'
    # @@protoc_insertion_point(class_scope:mesos.executor.Event.Kill)
    ))
  ,

  Acknowledged = _reflection.GeneratedProtocolMessageType('Acknowledged', (_message.Message,), dict(
    DESCRIPTOR = _EVENT_ACKNOWLEDGED,
    __module__ = 'mesos.executor.executor_pb2'
    # @@protoc_insertion_point(class_scope:mesos.executor.Event.Acknowledged)
    ))
  ,

  Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), dict(
    DESCRIPTOR = _EVENT_MESSAGE,
    __module__ = 'mesos.executor.executor_pb2'
    # @@protoc_insertion_point(class_scope:mesos.executor.Event.Message)
    ))
  ,

  Error = _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), dict(
    DESCRIPTOR = _EVENT_ERROR,
    __module__ = 'mesos.executor.executor_pb2'
    # @@protoc_insertion_point(class_scope:mesos.executor.Event.Error)
    ))
  ,
  DESCRIPTOR = _EVENT,
  __module__ = 'mesos.executor.executor_pb2'
  # @@protoc_insertion_point(class_scope:mesos.executor.Event)
  ))
_sym_db.RegisterMessage(Event)
_sym_db.RegisterMessage(Event.Subscribed)
_sym_db.RegisterMessage(Event.Launch)
_sym_db.RegisterMessage(Event.LaunchGroup)
_sym_db.RegisterMessage(Event.Kill)
_sym_db.RegisterMessage(Event.Acknowledged)
_sym_db.RegisterMessage(Event.Message)
_sym_db.RegisterMessage(Event.Error)

Call = _reflection.GeneratedProtocolMessageType('Call', (_message.Message,), dict(

  Subscribe = _reflection.GeneratedProtocolMessageType('Subscribe', (_message.Message,), dict(
    DESCRIPTOR = _CALL_SUBSCRIBE,
    __module__ = 'mesos.executor.executor_pb2'
    # @@protoc_insertion_point(class_scope:mesos.executor.Call.Subscribe)
    ))
  ,

  Update = _reflection.GeneratedProtocolMessageType('Update', (_message.Message,), dict(
    DESCRIPTOR = _CALL_UPDATE,
    __module__ = 'mesos.executor.executor_pb2'
    # @@protoc_insertion_point(class_scope:mesos.executor.Call.Update)
    ))
  ,

  Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), dict(
    DESCRIPTOR = _CALL_MESSAGE,
    __module__ = 'mesos.executor.executor_pb2'
    # @@protoc_insertion_point(class_scope:mesos.executor.Call.Message)
    ))
  ,
  DESCRIPTOR = _CALL,
  __module__ = 'mesos.executor.executor_pb2'
  # @@protoc_insertion_point(class_scope:mesos.executor.Call)
  ))
_sym_db.RegisterMessage(Call)
_sym_db.RegisterMessage(Call.Subscribe)
_sym_db.RegisterMessage(Call.Update)
_sym_db.RegisterMessage(Call.Message)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\031org.apache.mesos.executorB\006Protos'))
# @@protoc_insertion_point(module_scope)
