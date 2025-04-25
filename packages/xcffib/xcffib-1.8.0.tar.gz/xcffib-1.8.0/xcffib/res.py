import xcffib
import struct
import io
from dataclasses import dataclass

MAJOR_VERSION = 1
MINOR_VERSION = 2
key = xcffib.ExtensionKey("X-Resource")
_events = {}
_errors = {}
from . import xproto


@dataclass(init=False)
class Client(xcffib.Struct):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Struct.__init__(self, unpacker)
        base = unpacker.offset
        self.resource_base, self.resource_mask = unpacker.unpack("II")
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=II", self.resource_base, self.resource_mask))
        return buf.getvalue()

    fixed_size = 8

    @classmethod
    def synthetic(cls, resource_base, resource_mask):
        self = cls.__new__(cls)
        self.resource_base = resource_base
        self.resource_mask = resource_mask
        return self


@dataclass(init=False)
class Type(xcffib.Struct):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Struct.__init__(self, unpacker)
        base = unpacker.offset
        self.resource_type, self.count = unpacker.unpack("II")
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=II", self.resource_type, self.count))
        return buf.getvalue()

    fixed_size = 8

    @classmethod
    def synthetic(cls, resource_type, count):
        self = cls.__new__(cls)
        self.resource_type = resource_type
        self.count = count
        return self


@dataclass(init=False)
class ClientIdMask:
    ClientXID = 1 << 0
    LocalClientPID = 1 << 1


@dataclass(init=False)
class ClientIdSpec(xcffib.Struct):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Struct.__init__(self, unpacker)
        base = unpacker.offset
        self.client, self.mask = unpacker.unpack("II")
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=II", self.client, self.mask))
        return buf.getvalue()

    fixed_size = 8

    @classmethod
    def synthetic(cls, client, mask):
        self = cls.__new__(cls)
        self.client = client
        self.mask = mask
        return self


@dataclass(init=False)
class ClientIdValue(xcffib.Struct):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Struct.__init__(self, unpacker)
        base = unpacker.offset
        self.spec = ClientIdSpec(unpacker)
        (self.length,) = unpacker.unpack("I")
        unpacker.pad("I")
        self.value = xcffib.List(unpacker, "I", self.length // 4)
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(
            self.spec.pack()
            if hasattr(self.spec, "pack")
            else ClientIdSpec.synthetic(*self.spec).pack()
        )
        buf.write(struct.pack("=I", self.length))
        buf.write(xcffib.pack_list(self.value, "I"))
        return buf.getvalue()

    @classmethod
    def synthetic(cls, spec, length, value):
        self = cls.__new__(cls)
        self.spec = spec
        self.length = length
        self.value = value
        return self


@dataclass(init=False)
class ResourceIdSpec(xcffib.Struct):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Struct.__init__(self, unpacker)
        base = unpacker.offset
        self.resource, self.type = unpacker.unpack("II")
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=II", self.resource, self.type))
        return buf.getvalue()

    fixed_size = 8

    @classmethod
    def synthetic(cls, resource, type):
        self = cls.__new__(cls)
        self.resource = resource
        self.type = type
        return self


@dataclass(init=False)
class ResourceSizeSpec(xcffib.Struct):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Struct.__init__(self, unpacker)
        base = unpacker.offset
        self.spec = ResourceIdSpec(unpacker)
        self.bytes, self.ref_count, self.use_count = unpacker.unpack("III")
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(
            self.spec.pack()
            if hasattr(self.spec, "pack")
            else ResourceIdSpec.synthetic(*self.spec).pack()
        )
        buf.write(struct.pack("=I", self.bytes))
        buf.write(struct.pack("=I", self.ref_count))
        buf.write(struct.pack("=I", self.use_count))
        return buf.getvalue()

    @classmethod
    def synthetic(cls, spec, bytes, ref_count, use_count):
        self = cls.__new__(cls)
        self.spec = spec
        self.bytes = bytes
        self.ref_count = ref_count
        self.use_count = use_count
        return self


@dataclass(init=False)
class ResourceSizeValue(xcffib.Struct):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Struct.__init__(self, unpacker)
        base = unpacker.offset
        self.size = ResourceSizeSpec(unpacker)
        (self.num_cross_references,) = unpacker.unpack("I")
        unpacker.pad(ResourceSizeSpec)
        self.cross_references = xcffib.List(
            unpacker, ResourceSizeSpec, self.num_cross_references
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(
            self.size.pack()
            if hasattr(self.size, "pack")
            else ResourceSizeSpec.synthetic(*self.size).pack()
        )
        buf.write(struct.pack("=I", self.num_cross_references))
        buf.write(xcffib.pack_list(self.cross_references, ResourceSizeSpec))
        return buf.getvalue()

    @classmethod
    def synthetic(cls, size, num_cross_references, cross_references):
        self = cls.__new__(cls)
        self.size = size
        self.num_cross_references = num_cross_references
        self.cross_references = cross_references
        return self


@dataclass(init=False)
class QueryVersionReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.server_major, self.server_minor = unpacker.unpack("xx2x4xHH")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class QueryVersionCookie(xcffib.Cookie):
    reply_type = QueryVersionReply


@dataclass(init=False)
class QueryClientsReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.num_clients,) = unpacker.unpack("xx2x4xI20x")
        self.clients = xcffib.List(unpacker, Client, self.num_clients)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class QueryClientsCookie(xcffib.Cookie):
    reply_type = QueryClientsReply


@dataclass(init=False)
class QueryClientResourcesReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.num_types,) = unpacker.unpack("xx2x4xI20x")
        self.types = xcffib.List(unpacker, Type, self.num_types)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class QueryClientResourcesCookie(xcffib.Cookie):
    reply_type = QueryClientResourcesReply


@dataclass(init=False)
class QueryClientPixmapBytesReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.bytes, self.bytes_overflow = unpacker.unpack("xx2x4xII")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class QueryClientPixmapBytesCookie(xcffib.Cookie):
    reply_type = QueryClientPixmapBytesReply


@dataclass(init=False)
class QueryClientIdsReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.num_ids,) = unpacker.unpack("xx2x4xI20x")
        self.ids = xcffib.List(unpacker, ClientIdValue, self.num_ids)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class QueryClientIdsCookie(xcffib.Cookie):
    reply_type = QueryClientIdsReply


@dataclass(init=False)
class QueryResourceBytesReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.num_sizes,) = unpacker.unpack("xx2x4xI20x")
        self.sizes = xcffib.List(unpacker, ResourceSizeValue, self.num_sizes)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class QueryResourceBytesCookie(xcffib.Cookie):
    reply_type = QueryResourceBytesReply


@dataclass(init=False)
class resExtension(xcffib.Extension):
    def QueryVersion(self, client_major, client_minor, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xBB", client_major, client_minor))
        return self.send_request(0, buf, QueryVersionCookie, is_checked=is_checked)

    def QueryClients(self, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2x"))
        return self.send_request(1, buf, QueryClientsCookie, is_checked=is_checked)

    def QueryClientResources(self, xid, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", xid))
        return self.send_request(
            2, buf, QueryClientResourcesCookie, is_checked=is_checked
        )

    def QueryClientPixmapBytes(self, xid, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", xid))
        return self.send_request(
            3, buf, QueryClientPixmapBytesCookie, is_checked=is_checked
        )

    def QueryClientIds(self, num_specs, specs, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", num_specs))
        buf.write(xcffib.pack_list(specs, ClientIdSpec))
        return self.send_request(4, buf, QueryClientIdsCookie, is_checked=is_checked)

    def QueryResourceBytes(self, client, num_specs, specs, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", client, num_specs))
        buf.write(xcffib.pack_list(specs, ResourceIdSpec))
        return self.send_request(
            5, buf, QueryResourceBytesCookie, is_checked=is_checked
        )


xcffib._add_ext(key, resExtension, _events, _errors)
