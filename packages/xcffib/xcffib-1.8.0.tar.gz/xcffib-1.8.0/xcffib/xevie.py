import xcffib
import struct
import io
from dataclasses import dataclass

MAJOR_VERSION = 1
MINOR_VERSION = 0
key = xcffib.ExtensionKey("XEVIE")
_events = {}
_errors = {}


@dataclass(init=False)
class QueryVersionReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.server_major_version, self.server_minor_version = unpacker.unpack(
            "xx2x4xHH20x"
        )
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class QueryVersionCookie(xcffib.Cookie):
    reply_type = QueryVersionReply


@dataclass(init=False)
class StartReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        unpacker.unpack("xx2x4x24x")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class StartCookie(xcffib.Cookie):
    reply_type = StartReply


@dataclass(init=False)
class EndReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        unpacker.unpack("xx2x4x24x")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class EndCookie(xcffib.Cookie):
    reply_type = EndReply


@dataclass(init=False)
class Datatype:
    Unmodified = 0
    Modified = 1


@dataclass(init=False)
class Event(xcffib.Struct):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Struct.__init__(self, unpacker)
        base = unpacker.offset
        unpacker.unpack("32x")
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=32x"))
        return buf.getvalue()

    fixed_size = 32


@dataclass(init=False)
class SendReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        unpacker.unpack("xx2x4x24x")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class SendCookie(xcffib.Cookie):
    reply_type = SendReply


@dataclass(init=False)
class SelectInputReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        unpacker.unpack("xx2x4x24x")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class SelectInputCookie(xcffib.Cookie):
    reply_type = SelectInputReply


@dataclass(init=False)
class xevieExtension(xcffib.Extension):
    def QueryVersion(self, client_major_version, client_minor_version, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xHH", client_major_version, client_minor_version))
        return self.send_request(0, buf, QueryVersionCookie, is_checked=is_checked)

    def Start(self, screen, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", screen))
        return self.send_request(1, buf, StartCookie, is_checked=is_checked)

    def End(self, cmap, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", cmap))
        return self.send_request(2, buf, EndCookie, is_checked=is_checked)

    def Send(self, event, data_type, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2x"))
        buf.write(
            event.pack() if hasattr(event, "pack") else Event.synthetic(*event).pack()
        )
        buf.write(struct.pack("=I", data_type))
        buf.write(
            struct.pack(
                "=64x",
            )
        )
        return self.send_request(3, buf, SendCookie, is_checked=is_checked)

    def SelectInput(self, event_mask, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", event_mask))
        return self.send_request(4, buf, SelectInputCookie, is_checked=is_checked)


xcffib._add_ext(key, xevieExtension, _events, _errors)
