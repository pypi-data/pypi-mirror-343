import xcffib
import struct
import io
from dataclasses import dataclass

MAJOR_VERSION = 1
MINOR_VERSION = 4
key = xcffib.ExtensionKey("GLX")
_events = {}
_errors = {}
from . import xproto


@dataclass(init=False)
class GenericError(xcffib.Error):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Error.__init__(self, unpacker)
        base = unpacker.offset
        self.bad_value, self.minor_opcode, self.major_opcode = unpacker.unpack(
            "xx2xIHB21x"
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", -1))
        buf.write(
            struct.pack(
                "=x2xIHB21x", self.bad_value, self.minor_opcode, self.major_opcode
            )
        )
        return buf.getvalue()


BadGeneric = GenericError
_errors[-1] = GenericError


@dataclass(init=False)
class BadContextError(xcffib.Error):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Error.__init__(self, unpacker)
        base = unpacker.offset
        self.bad_value, self.minor_opcode, self.major_opcode = unpacker.unpack(
            "xx2xIHB21x"
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 0))
        buf.write(
            struct.pack(
                "=x2xIHB21x", self.bad_value, self.minor_opcode, self.major_opcode
            )
        )
        return buf.getvalue()


BadBadContext = BadContextError
_errors[0] = BadContextError


@dataclass(init=False)
class BadContextStateError(xcffib.Error):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Error.__init__(self, unpacker)
        base = unpacker.offset
        self.bad_value, self.minor_opcode, self.major_opcode = unpacker.unpack(
            "xx2xIHB21x"
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 1))
        buf.write(
            struct.pack(
                "=x2xIHB21x", self.bad_value, self.minor_opcode, self.major_opcode
            )
        )
        return buf.getvalue()


BadBadContextState = BadContextStateError
_errors[1] = BadContextStateError


@dataclass(init=False)
class BadDrawableError(xcffib.Error):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Error.__init__(self, unpacker)
        base = unpacker.offset
        self.bad_value, self.minor_opcode, self.major_opcode = unpacker.unpack(
            "xx2xIHB21x"
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 2))
        buf.write(
            struct.pack(
                "=x2xIHB21x", self.bad_value, self.minor_opcode, self.major_opcode
            )
        )
        return buf.getvalue()


BadBadDrawable = BadDrawableError
_errors[2] = BadDrawableError


@dataclass(init=False)
class BadPixmapError(xcffib.Error):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Error.__init__(self, unpacker)
        base = unpacker.offset
        self.bad_value, self.minor_opcode, self.major_opcode = unpacker.unpack(
            "xx2xIHB21x"
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 3))
        buf.write(
            struct.pack(
                "=x2xIHB21x", self.bad_value, self.minor_opcode, self.major_opcode
            )
        )
        return buf.getvalue()


BadBadPixmap = BadPixmapError
_errors[3] = BadPixmapError


@dataclass(init=False)
class BadContextTagError(xcffib.Error):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Error.__init__(self, unpacker)
        base = unpacker.offset
        self.bad_value, self.minor_opcode, self.major_opcode = unpacker.unpack(
            "xx2xIHB21x"
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 4))
        buf.write(
            struct.pack(
                "=x2xIHB21x", self.bad_value, self.minor_opcode, self.major_opcode
            )
        )
        return buf.getvalue()


BadBadContextTag = BadContextTagError
_errors[4] = BadContextTagError


@dataclass(init=False)
class BadCurrentWindowError(xcffib.Error):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Error.__init__(self, unpacker)
        base = unpacker.offset
        self.bad_value, self.minor_opcode, self.major_opcode = unpacker.unpack(
            "xx2xIHB21x"
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 5))
        buf.write(
            struct.pack(
                "=x2xIHB21x", self.bad_value, self.minor_opcode, self.major_opcode
            )
        )
        return buf.getvalue()


BadBadCurrentWindow = BadCurrentWindowError
_errors[5] = BadCurrentWindowError


@dataclass(init=False)
class BadRenderRequestError(xcffib.Error):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Error.__init__(self, unpacker)
        base = unpacker.offset
        self.bad_value, self.minor_opcode, self.major_opcode = unpacker.unpack(
            "xx2xIHB21x"
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 6))
        buf.write(
            struct.pack(
                "=x2xIHB21x", self.bad_value, self.minor_opcode, self.major_opcode
            )
        )
        return buf.getvalue()


BadBadRenderRequest = BadRenderRequestError
_errors[6] = BadRenderRequestError


@dataclass(init=False)
class BadLargeRequestError(xcffib.Error):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Error.__init__(self, unpacker)
        base = unpacker.offset
        self.bad_value, self.minor_opcode, self.major_opcode = unpacker.unpack(
            "xx2xIHB21x"
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 7))
        buf.write(
            struct.pack(
                "=x2xIHB21x", self.bad_value, self.minor_opcode, self.major_opcode
            )
        )
        return buf.getvalue()


BadBadLargeRequest = BadLargeRequestError
_errors[7] = BadLargeRequestError


@dataclass(init=False)
class UnsupportedPrivateRequestError(xcffib.Error):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Error.__init__(self, unpacker)
        base = unpacker.offset
        self.bad_value, self.minor_opcode, self.major_opcode = unpacker.unpack(
            "xx2xIHB21x"
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 8))
        buf.write(
            struct.pack(
                "=x2xIHB21x", self.bad_value, self.minor_opcode, self.major_opcode
            )
        )
        return buf.getvalue()


BadUnsupportedPrivateRequest = UnsupportedPrivateRequestError
_errors[8] = UnsupportedPrivateRequestError


@dataclass(init=False)
class BadFBConfigError(xcffib.Error):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Error.__init__(self, unpacker)
        base = unpacker.offset
        self.bad_value, self.minor_opcode, self.major_opcode = unpacker.unpack(
            "xx2xIHB21x"
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 9))
        buf.write(
            struct.pack(
                "=x2xIHB21x", self.bad_value, self.minor_opcode, self.major_opcode
            )
        )
        return buf.getvalue()


BadBadFBConfig = BadFBConfigError
_errors[9] = BadFBConfigError


@dataclass(init=False)
class BadPbufferError(xcffib.Error):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Error.__init__(self, unpacker)
        base = unpacker.offset
        self.bad_value, self.minor_opcode, self.major_opcode = unpacker.unpack(
            "xx2xIHB21x"
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 10))
        buf.write(
            struct.pack(
                "=x2xIHB21x", self.bad_value, self.minor_opcode, self.major_opcode
            )
        )
        return buf.getvalue()


BadBadPbuffer = BadPbufferError
_errors[10] = BadPbufferError


@dataclass(init=False)
class BadCurrentDrawableError(xcffib.Error):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Error.__init__(self, unpacker)
        base = unpacker.offset
        self.bad_value, self.minor_opcode, self.major_opcode = unpacker.unpack(
            "xx2xIHB21x"
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 11))
        buf.write(
            struct.pack(
                "=x2xIHB21x", self.bad_value, self.minor_opcode, self.major_opcode
            )
        )
        return buf.getvalue()


BadBadCurrentDrawable = BadCurrentDrawableError
_errors[11] = BadCurrentDrawableError


@dataclass(init=False)
class BadWindowError(xcffib.Error):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Error.__init__(self, unpacker)
        base = unpacker.offset
        self.bad_value, self.minor_opcode, self.major_opcode = unpacker.unpack(
            "xx2xIHB21x"
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 12))
        buf.write(
            struct.pack(
                "=x2xIHB21x", self.bad_value, self.minor_opcode, self.major_opcode
            )
        )
        return buf.getvalue()


BadBadWindow = BadWindowError
_errors[12] = BadWindowError


@dataclass(init=False)
class GLXBadProfileARBError(xcffib.Error):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Error.__init__(self, unpacker)
        base = unpacker.offset
        self.bad_value, self.minor_opcode, self.major_opcode = unpacker.unpack(
            "xx2xIHB21x"
        )
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 13))
        buf.write(
            struct.pack(
                "=x2xIHB21x", self.bad_value, self.minor_opcode, self.major_opcode
            )
        )
        return buf.getvalue()


BadGLXBadProfileARB = GLXBadProfileARBError
_errors[13] = GLXBadProfileARBError


@dataclass(init=False)
class PbufferClobberEvent(xcffib.Event):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Event.__init__(self, unpacker)
        base = unpacker.offset
        (
            self.event_type,
            self.draw_type,
            self.drawable,
            self.b_mask,
            self.aux_buffer,
            self.x,
            self.y,
            self.width,
            self.height,
            self.count,
        ) = unpacker.unpack("xx2xHHIIHHHHHH4x")
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 0))
        buf.write(
            struct.pack(
                "=x2xHHIIHHHHHH4x",
                self.event_type,
                self.draw_type,
                self.drawable,
                self.b_mask,
                self.aux_buffer,
                self.x,
                self.y,
                self.width,
                self.height,
                self.count,
            )
        )
        buf_len = len(buf.getvalue())
        if buf_len < 32:
            buf.write(struct.pack(("%dx" % (32 - buf_len))))
        return buf.getvalue()

    @classmethod
    def synthetic(
        cls,
        event_type,
        draw_type,
        drawable,
        b_mask,
        aux_buffer,
        x,
        y,
        width,
        height,
        count,
    ):
        self = cls.__new__(cls)
        self.event_type = event_type
        self.draw_type = draw_type
        self.drawable = drawable
        self.b_mask = b_mask
        self.aux_buffer = aux_buffer
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.count = count
        return self


_events[0] = PbufferClobberEvent


@dataclass(init=False)
class BufferSwapCompleteEvent(xcffib.Event):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Event.__init__(self, unpacker)
        base = unpacker.offset
        (
            self.event_type,
            self.drawable,
            self.ust_hi,
            self.ust_lo,
            self.msc_hi,
            self.msc_lo,
            self.sbc,
        ) = unpacker.unpack("xx2xH2xIIIIII")
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 1))
        buf.write(
            struct.pack(
                "=x2xH2xIIIIII",
                self.event_type,
                self.drawable,
                self.ust_hi,
                self.ust_lo,
                self.msc_hi,
                self.msc_lo,
                self.sbc,
            )
        )
        buf_len = len(buf.getvalue())
        if buf_len < 32:
            buf.write(struct.pack(("%dx" % (32 - buf_len))))
        return buf.getvalue()

    @classmethod
    def synthetic(cls, event_type, drawable, ust_hi, ust_lo, msc_hi, msc_lo, sbc):
        self = cls.__new__(cls)
        self.event_type = event_type
        self.drawable = drawable
        self.ust_hi = ust_hi
        self.ust_lo = ust_lo
        self.msc_hi = msc_hi
        self.msc_lo = msc_lo
        self.sbc = sbc
        return self


_events[1] = BufferSwapCompleteEvent


@dataclass(init=False)
class PBCET:
    Damaged = 32791
    Saved = 32792


@dataclass(init=False)
class PBCDT:
    Window = 32793
    Pbuffer = 32794


@dataclass(init=False)
class MakeCurrentReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.context_tag,) = unpacker.unpack("xx2x4xI20x")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class MakeCurrentCookie(xcffib.Cookie):
    reply_type = MakeCurrentReply


@dataclass(init=False)
class IsDirectReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.is_direct,) = unpacker.unpack("xx2x4xB23x")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class IsDirectCookie(xcffib.Cookie):
    reply_type = IsDirectReply


@dataclass(init=False)
class QueryVersionReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.major_version, self.minor_version = unpacker.unpack("xx2x4xII16x")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class QueryVersionCookie(xcffib.Cookie):
    reply_type = QueryVersionReply


@dataclass(init=False)
class GC:
    GL_CURRENT_BIT = 1 << 0
    GL_POINT_BIT = 1 << 1
    GL_LINE_BIT = 1 << 2
    GL_POLYGON_BIT = 1 << 3
    GL_POLYGON_STIPPLE_BIT = 1 << 4
    GL_PIXEL_MODE_BIT = 1 << 5
    GL_LIGHTING_BIT = 1 << 6
    GL_FOG_BIT = 1 << 7
    GL_DEPTH_BUFFER_BIT = 1 << 8
    GL_ACCUM_BUFFER_BIT = 1 << 9
    GL_STENCIL_BUFFER_BIT = 1 << 10
    GL_VIEWPORT_BIT = 1 << 11
    GL_TRANSFORM_BIT = 1 << 12
    GL_ENABLE_BIT = 1 << 13
    GL_COLOR_BUFFER_BIT = 1 << 14
    GL_HINT_BIT = 1 << 15
    GL_EVAL_BIT = 1 << 16
    GL_LIST_BIT = 1 << 17
    GL_TEXTURE_BIT = 1 << 18
    GL_SCISSOR_BIT = 1 << 19
    GL_ALL_ATTRIB_BITS = 16777215


@dataclass(init=False)
class GetVisualConfigsReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.num_visuals, self.num_properties = unpacker.unpack("xx2x4xII16x")
        self.property_list = xcffib.List(unpacker, "I", self.length)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetVisualConfigsCookie(xcffib.Cookie):
    reply_type = GetVisualConfigsReply


@dataclass(init=False)
class VendorPrivateWithReplyReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.retval,) = unpacker.unpack("xx2x4xI")
        self.data1 = xcffib.List(unpacker, "B", 24)
        unpacker.pad("B")
        self.data2 = xcffib.List(unpacker, "B", self.length * 4)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class VendorPrivateWithReplyCookie(xcffib.Cookie):
    reply_type = VendorPrivateWithReplyReply


@dataclass(init=False)
class QueryExtensionsStringReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.n,) = unpacker.unpack("xx2x4x4xI16x")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class QueryExtensionsStringCookie(xcffib.Cookie):
    reply_type = QueryExtensionsStringReply


@dataclass(init=False)
class QueryServerStringReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.str_len,) = unpacker.unpack("xx2x4x4xI16x")
        self.string = xcffib.List(unpacker, "c", self.str_len)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class QueryServerStringCookie(xcffib.Cookie):
    reply_type = QueryServerStringReply


@dataclass(init=False)
class GetFBConfigsReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.num_FB_configs, self.num_properties = unpacker.unpack("xx2x4xII16x")
        self.property_list = xcffib.List(unpacker, "I", self.length)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetFBConfigsCookie(xcffib.Cookie):
    reply_type = GetFBConfigsReply


@dataclass(init=False)
class QueryContextReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.num_attribs,) = unpacker.unpack("xx2x4xI20x")
        self.attribs = xcffib.List(unpacker, "I", self.num_attribs * 2)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class QueryContextCookie(xcffib.Cookie):
    reply_type = QueryContextReply


@dataclass(init=False)
class MakeContextCurrentReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.context_tag,) = unpacker.unpack("xx2x4xI20x")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class MakeContextCurrentCookie(xcffib.Cookie):
    reply_type = MakeContextCurrentReply


@dataclass(init=False)
class GetDrawableAttributesReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.num_attribs,) = unpacker.unpack("xx2x4xI20x")
        self.attribs = xcffib.List(unpacker, "I", self.num_attribs * 2)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetDrawableAttributesCookie(xcffib.Cookie):
    reply_type = GetDrawableAttributesReply


@dataclass(init=False)
class GenListsReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.ret_val,) = unpacker.unpack("xx2x4xI")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GenListsCookie(xcffib.Cookie):
    reply_type = GenListsReply


@dataclass(init=False)
class RenderModeReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.ret_val, self.n, self.new_mode = unpacker.unpack("xx2x4xIII12x")
        self.data = xcffib.List(unpacker, "I", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class RenderModeCookie(xcffib.Cookie):
    reply_type = RenderModeReply


@dataclass(init=False)
class RM:
    GL_RENDER = 7168
    GL_FEEDBACK = 7169
    GL_SELECT = 7170


@dataclass(init=False)
class FinishReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        unpacker.unpack("xx2x4x")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class FinishCookie(xcffib.Cookie):
    reply_type = FinishReply


@dataclass(init=False)
class ReadPixelsReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        unpacker.unpack("xx2x4x24x")
        self.data = xcffib.List(unpacker, "B", self.length * 4)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class ReadPixelsCookie(xcffib.Cookie):
    reply_type = ReadPixelsReply


@dataclass(init=False)
class GetBooleanvReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIB15x")
        self.data = xcffib.List(unpacker, "B", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetBooleanvCookie(xcffib.Cookie):
    reply_type = GetBooleanvReply


@dataclass(init=False)
class GetErrorReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.error,) = unpacker.unpack("xx2x4xi")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetErrorCookie(xcffib.Cookie):
    reply_type = GetErrorReply


@dataclass(init=False)
class GetFloatvReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIf12x")
        self.data = xcffib.List(unpacker, "f", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetFloatvCookie(xcffib.Cookie):
    reply_type = GetFloatvReply


@dataclass(init=False)
class GetIntegervReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIi12x")
        self.data = xcffib.List(unpacker, "i", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetIntegervCookie(xcffib.Cookie):
    reply_type = GetIntegervReply


@dataclass(init=False)
class GetLightfvReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIf12x")
        self.data = xcffib.List(unpacker, "f", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetLightfvCookie(xcffib.Cookie):
    reply_type = GetLightfvReply


@dataclass(init=False)
class GetLightivReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIi12x")
        self.data = xcffib.List(unpacker, "i", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetLightivCookie(xcffib.Cookie):
    reply_type = GetLightivReply


@dataclass(init=False)
class GetMapfvReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIf12x")
        self.data = xcffib.List(unpacker, "f", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetMapfvCookie(xcffib.Cookie):
    reply_type = GetMapfvReply


@dataclass(init=False)
class GetMapivReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIi12x")
        self.data = xcffib.List(unpacker, "i", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetMapivCookie(xcffib.Cookie):
    reply_type = GetMapivReply


@dataclass(init=False)
class GetMaterialfvReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIf12x")
        self.data = xcffib.List(unpacker, "f", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetMaterialfvCookie(xcffib.Cookie):
    reply_type = GetMaterialfvReply


@dataclass(init=False)
class GetMaterialivReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIi12x")
        self.data = xcffib.List(unpacker, "i", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetMaterialivCookie(xcffib.Cookie):
    reply_type = GetMaterialivReply


@dataclass(init=False)
class GetPixelMapfvReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIf12x")
        self.data = xcffib.List(unpacker, "f", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetPixelMapfvCookie(xcffib.Cookie):
    reply_type = GetPixelMapfvReply


@dataclass(init=False)
class GetPixelMapuivReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xII12x")
        self.data = xcffib.List(unpacker, "I", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetPixelMapuivCookie(xcffib.Cookie):
    reply_type = GetPixelMapuivReply


@dataclass(init=False)
class GetPixelMapusvReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIH16x")
        self.data = xcffib.List(unpacker, "H", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetPixelMapusvCookie(xcffib.Cookie):
    reply_type = GetPixelMapusvReply


@dataclass(init=False)
class GetPolygonStippleReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        unpacker.unpack("xx2x4x24x")
        self.data = xcffib.List(unpacker, "B", self.length * 4)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetPolygonStippleCookie(xcffib.Cookie):
    reply_type = GetPolygonStippleReply


@dataclass(init=False)
class GetStringReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.n,) = unpacker.unpack("xx2x4x4xI16x")
        self.string = xcffib.List(unpacker, "c", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetStringCookie(xcffib.Cookie):
    reply_type = GetStringReply


@dataclass(init=False)
class GetTexEnvfvReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIf12x")
        self.data = xcffib.List(unpacker, "f", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetTexEnvfvCookie(xcffib.Cookie):
    reply_type = GetTexEnvfvReply


@dataclass(init=False)
class GetTexEnvivReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIi12x")
        self.data = xcffib.List(unpacker, "i", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetTexEnvivCookie(xcffib.Cookie):
    reply_type = GetTexEnvivReply


@dataclass(init=False)
class GetTexGenfvReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIf12x")
        self.data = xcffib.List(unpacker, "f", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetTexGenfvCookie(xcffib.Cookie):
    reply_type = GetTexGenfvReply


@dataclass(init=False)
class GetTexGenivReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIi12x")
        self.data = xcffib.List(unpacker, "i", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetTexGenivCookie(xcffib.Cookie):
    reply_type = GetTexGenivReply


@dataclass(init=False)
class GetTexImageReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.width, self.height, self.depth = unpacker.unpack("xx2x4x8xiii4x")
        self.data = xcffib.List(unpacker, "B", self.length * 4)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetTexImageCookie(xcffib.Cookie):
    reply_type = GetTexImageReply


@dataclass(init=False)
class GetTexParameterfvReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIf12x")
        self.data = xcffib.List(unpacker, "f", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetTexParameterfvCookie(xcffib.Cookie):
    reply_type = GetTexParameterfvReply


@dataclass(init=False)
class GetTexParameterivReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIi12x")
        self.data = xcffib.List(unpacker, "i", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetTexParameterivCookie(xcffib.Cookie):
    reply_type = GetTexParameterivReply


@dataclass(init=False)
class GetTexLevelParameterfvReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIf12x")
        self.data = xcffib.List(unpacker, "f", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetTexLevelParameterfvCookie(xcffib.Cookie):
    reply_type = GetTexLevelParameterfvReply


@dataclass(init=False)
class GetTexLevelParameterivReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIi12x")
        self.data = xcffib.List(unpacker, "i", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetTexLevelParameterivCookie(xcffib.Cookie):
    reply_type = GetTexLevelParameterivReply


@dataclass(init=False)
class IsEnabledReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.ret_val,) = unpacker.unpack("xx2x4xI")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class IsEnabledCookie(xcffib.Cookie):
    reply_type = IsEnabledReply


@dataclass(init=False)
class IsListReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.ret_val,) = unpacker.unpack("xx2x4xI")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class IsListCookie(xcffib.Cookie):
    reply_type = IsListReply


@dataclass(init=False)
class AreTexturesResidentReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.ret_val,) = unpacker.unpack("xx2x4xI20x")
        self.data = xcffib.List(unpacker, "B", self.length * 4)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class AreTexturesResidentCookie(xcffib.Cookie):
    reply_type = AreTexturesResidentReply


@dataclass(init=False)
class GenTexturesReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        unpacker.unpack("xx2x4x24x")
        self.data = xcffib.List(unpacker, "I", self.length)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GenTexturesCookie(xcffib.Cookie):
    reply_type = GenTexturesReply


@dataclass(init=False)
class IsTextureReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.ret_val,) = unpacker.unpack("xx2x4xI")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class IsTextureCookie(xcffib.Cookie):
    reply_type = IsTextureReply


@dataclass(init=False)
class GetColorTableReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.width,) = unpacker.unpack("xx2x4x8xi12x")
        self.data = xcffib.List(unpacker, "B", self.length * 4)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetColorTableCookie(xcffib.Cookie):
    reply_type = GetColorTableReply


@dataclass(init=False)
class GetColorTableParameterfvReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIf12x")
        self.data = xcffib.List(unpacker, "f", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetColorTableParameterfvCookie(xcffib.Cookie):
    reply_type = GetColorTableParameterfvReply


@dataclass(init=False)
class GetColorTableParameterivReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIi12x")
        self.data = xcffib.List(unpacker, "i", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetColorTableParameterivCookie(xcffib.Cookie):
    reply_type = GetColorTableParameterivReply


@dataclass(init=False)
class GetConvolutionFilterReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.width, self.height = unpacker.unpack("xx2x4x8xii8x")
        self.data = xcffib.List(unpacker, "B", self.length * 4)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetConvolutionFilterCookie(xcffib.Cookie):
    reply_type = GetConvolutionFilterReply


@dataclass(init=False)
class GetConvolutionParameterfvReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIf12x")
        self.data = xcffib.List(unpacker, "f", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetConvolutionParameterfvCookie(xcffib.Cookie):
    reply_type = GetConvolutionParameterfvReply


@dataclass(init=False)
class GetConvolutionParameterivReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIi12x")
        self.data = xcffib.List(unpacker, "i", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetConvolutionParameterivCookie(xcffib.Cookie):
    reply_type = GetConvolutionParameterivReply


@dataclass(init=False)
class GetSeparableFilterReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.row_w, self.col_h = unpacker.unpack("xx2x4x8xii8x")
        self.rows_and_cols = xcffib.List(unpacker, "B", self.length * 4)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetSeparableFilterCookie(xcffib.Cookie):
    reply_type = GetSeparableFilterReply


@dataclass(init=False)
class GetHistogramReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.width,) = unpacker.unpack("xx2x4x8xi12x")
        self.data = xcffib.List(unpacker, "B", self.length * 4)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetHistogramCookie(xcffib.Cookie):
    reply_type = GetHistogramReply


@dataclass(init=False)
class GetHistogramParameterfvReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIf12x")
        self.data = xcffib.List(unpacker, "f", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetHistogramParameterfvCookie(xcffib.Cookie):
    reply_type = GetHistogramParameterfvReply


@dataclass(init=False)
class GetHistogramParameterivReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIi12x")
        self.data = xcffib.List(unpacker, "i", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetHistogramParameterivCookie(xcffib.Cookie):
    reply_type = GetHistogramParameterivReply


@dataclass(init=False)
class GetMinmaxReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        unpacker.unpack("xx2x4x24x")
        self.data = xcffib.List(unpacker, "B", self.length * 4)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetMinmaxCookie(xcffib.Cookie):
    reply_type = GetMinmaxReply


@dataclass(init=False)
class GetMinmaxParameterfvReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIf12x")
        self.data = xcffib.List(unpacker, "f", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetMinmaxParameterfvCookie(xcffib.Cookie):
    reply_type = GetMinmaxParameterfvReply


@dataclass(init=False)
class GetMinmaxParameterivReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIi12x")
        self.data = xcffib.List(unpacker, "i", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetMinmaxParameterivCookie(xcffib.Cookie):
    reply_type = GetMinmaxParameterivReply


@dataclass(init=False)
class GetCompressedTexImageARBReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.size,) = unpacker.unpack("xx2x4x8xi12x")
        self.data = xcffib.List(unpacker, "B", self.length * 4)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetCompressedTexImageARBCookie(xcffib.Cookie):
    reply_type = GetCompressedTexImageARBReply


@dataclass(init=False)
class GenQueriesARBReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        unpacker.unpack("xx2x4x24x")
        self.data = xcffib.List(unpacker, "I", self.length)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GenQueriesARBCookie(xcffib.Cookie):
    reply_type = GenQueriesARBReply


@dataclass(init=False)
class IsQueryARBReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.ret_val,) = unpacker.unpack("xx2x4xI")
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class IsQueryARBCookie(xcffib.Cookie):
    reply_type = IsQueryARBReply


@dataclass(init=False)
class GetQueryivARBReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIi12x")
        self.data = xcffib.List(unpacker, "i", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetQueryivARBCookie(xcffib.Cookie):
    reply_type = GetQueryivARBReply


@dataclass(init=False)
class GetQueryObjectivARBReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xIi12x")
        self.data = xcffib.List(unpacker, "i", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetQueryObjectivARBCookie(xcffib.Cookie):
    reply_type = GetQueryObjectivARBReply


@dataclass(init=False)
class GetQueryObjectuivARBReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.n, self.datum = unpacker.unpack("xx2x4x4xII12x")
        self.data = xcffib.List(unpacker, "I", self.n)
        self.bufsize = unpacker.offset - base


@dataclass(init=False)
class GetQueryObjectuivARBCookie(xcffib.Cookie):
    reply_type = GetQueryObjectuivARBReply


@dataclass(init=False)
class glxExtension(xcffib.Extension):
    def Render(self, context_tag, data_len, data, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context_tag))
        buf.write(xcffib.pack_list(data, "B"))
        return self.send_request(1, buf, is_checked=is_checked)

    def RenderLarge(
        self, context_tag, request_num, request_total, data_len, data, is_checked=False
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack("=xx2xIHHI", context_tag, request_num, request_total, data_len)
        )
        buf.write(xcffib.pack_list(data, "B"))
        return self.send_request(2, buf, is_checked=is_checked)

    def CreateContext(
        self, context, visual, screen, share_list, is_direct, is_checked=False
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack("=xx2xIIIIB3x", context, visual, screen, share_list, is_direct)
        )
        return self.send_request(3, buf, is_checked=is_checked)

    def DestroyContext(self, context, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context))
        return self.send_request(4, buf, is_checked=is_checked)

    def MakeCurrent(self, drawable, context, old_context_tag, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", drawable, context, old_context_tag))
        return self.send_request(5, buf, MakeCurrentCookie, is_checked=is_checked)

    def IsDirect(self, context, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context))
        return self.send_request(6, buf, IsDirectCookie, is_checked=is_checked)

    def QueryVersion(self, major_version, minor_version, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", major_version, minor_version))
        return self.send_request(7, buf, QueryVersionCookie, is_checked=is_checked)

    def WaitGL(self, context_tag, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context_tag))
        return self.send_request(8, buf, is_checked=is_checked)

    def WaitX(self, context_tag, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context_tag))
        return self.send_request(9, buf, is_checked=is_checked)

    def CopyContext(self, src, dest, mask, src_context_tag, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIIII", src, dest, mask, src_context_tag))
        return self.send_request(10, buf, is_checked=is_checked)

    def SwapBuffers(self, context_tag, drawable, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", context_tag, drawable))
        return self.send_request(11, buf, is_checked=is_checked)

    def UseXFont(self, context_tag, font, first, count, list_base, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIIIII", context_tag, font, first, count, list_base))
        return self.send_request(12, buf, is_checked=is_checked)

    def CreateGLXPixmap(self, screen, visual, pixmap, glx_pixmap, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIIII", screen, visual, pixmap, glx_pixmap))
        return self.send_request(13, buf, is_checked=is_checked)

    def GetVisualConfigs(self, screen, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", screen))
        return self.send_request(14, buf, GetVisualConfigsCookie, is_checked=is_checked)

    def DestroyGLXPixmap(self, glx_pixmap, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", glx_pixmap))
        return self.send_request(15, buf, is_checked=is_checked)

    def VendorPrivate(self, vendor_code, context_tag, data_len, data, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", vendor_code, context_tag))
        buf.write(xcffib.pack_list(data, "B"))
        return self.send_request(16, buf, is_checked=is_checked)

    def VendorPrivateWithReply(
        self, vendor_code, context_tag, data_len, data, is_checked=True
    ):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", vendor_code, context_tag))
        buf.write(xcffib.pack_list(data, "B"))
        return self.send_request(
            17, buf, VendorPrivateWithReplyCookie, is_checked=is_checked
        )

    def QueryExtensionsString(self, screen, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", screen))
        return self.send_request(
            18, buf, QueryExtensionsStringCookie, is_checked=is_checked
        )

    def QueryServerString(self, screen, name, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", screen, name))
        return self.send_request(
            19, buf, QueryServerStringCookie, is_checked=is_checked
        )

    def ClientInfo(
        self, major_version, minor_version, str_len, string, is_checked=False
    ):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", major_version, minor_version, str_len))
        buf.write(xcffib.pack_list(string, "c"))
        return self.send_request(20, buf, is_checked=is_checked)

    def GetFBConfigs(self, screen, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", screen))
        return self.send_request(21, buf, GetFBConfigsCookie, is_checked=is_checked)

    def CreatePixmap(
        self,
        screen,
        fbconfig,
        pixmap,
        glx_pixmap,
        num_attribs,
        attribs,
        is_checked=False,
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack("=xx2xIIIII", screen, fbconfig, pixmap, glx_pixmap, num_attribs)
        )
        buf.write(xcffib.pack_list(attribs, "I"))
        return self.send_request(22, buf, is_checked=is_checked)

    def DestroyPixmap(self, glx_pixmap, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", glx_pixmap))
        return self.send_request(23, buf, is_checked=is_checked)

    def CreateNewContext(
        self,
        context,
        fbconfig,
        screen,
        render_type,
        share_list,
        is_direct,
        is_checked=False,
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack(
                "=xx2xIIIIIB3x",
                context,
                fbconfig,
                screen,
                render_type,
                share_list,
                is_direct,
            )
        )
        return self.send_request(24, buf, is_checked=is_checked)

    def QueryContext(self, context, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context))
        return self.send_request(25, buf, QueryContextCookie, is_checked=is_checked)

    def MakeContextCurrent(
        self, old_context_tag, drawable, read_drawable, context, is_checked=True
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack("=xx2xIIII", old_context_tag, drawable, read_drawable, context)
        )
        return self.send_request(
            26, buf, MakeContextCurrentCookie, is_checked=is_checked
        )

    def CreatePbuffer(
        self, screen, fbconfig, pbuffer, num_attribs, attribs, is_checked=False
    ):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIIII", screen, fbconfig, pbuffer, num_attribs))
        buf.write(xcffib.pack_list(attribs, "I"))
        return self.send_request(27, buf, is_checked=is_checked)

    def DestroyPbuffer(self, pbuffer, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", pbuffer))
        return self.send_request(28, buf, is_checked=is_checked)

    def GetDrawableAttributes(self, drawable, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", drawable))
        return self.send_request(
            29, buf, GetDrawableAttributesCookie, is_checked=is_checked
        )

    def ChangeDrawableAttributes(
        self, drawable, num_attribs, attribs, is_checked=False
    ):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", drawable, num_attribs))
        buf.write(xcffib.pack_list(attribs, "I"))
        return self.send_request(30, buf, is_checked=is_checked)

    def CreateWindow(
        self,
        screen,
        fbconfig,
        window,
        glx_window,
        num_attribs,
        attribs,
        is_checked=False,
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack("=xx2xIIIII", screen, fbconfig, window, glx_window, num_attribs)
        )
        buf.write(xcffib.pack_list(attribs, "I"))
        return self.send_request(31, buf, is_checked=is_checked)

    def DeleteWindow(self, glxwindow, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", glxwindow))
        return self.send_request(32, buf, is_checked=is_checked)

    def SetClientInfoARB(
        self,
        major_version,
        minor_version,
        num_versions,
        gl_str_len,
        glx_str_len,
        gl_versions,
        gl_extension_string,
        glx_extension_string,
        is_checked=False,
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack(
                "=xx2xIIIII",
                major_version,
                minor_version,
                num_versions,
                gl_str_len,
                glx_str_len,
            )
        )
        buf.write(xcffib.pack_list(gl_versions, "I"))
        buf.write(xcffib.pack_list(gl_extension_string, "c"))
        buf.write(
            struct.pack(
                "=4x",
            )
        )
        buf.write(xcffib.pack_list(glx_extension_string, "c"))
        return self.send_request(33, buf, is_checked=is_checked)

    def CreateContextAttribsARB(
        self,
        context,
        fbconfig,
        screen,
        share_list,
        is_direct,
        num_attribs,
        attribs,
        is_checked=False,
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack(
                "=xx2xIIIIB3xI",
                context,
                fbconfig,
                screen,
                share_list,
                is_direct,
                num_attribs,
            )
        )
        buf.write(xcffib.pack_list(attribs, "I"))
        return self.send_request(34, buf, is_checked=is_checked)

    def SetClientInfo2ARB(
        self,
        major_version,
        minor_version,
        num_versions,
        gl_str_len,
        glx_str_len,
        gl_versions,
        gl_extension_string,
        glx_extension_string,
        is_checked=False,
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack(
                "=xx2xIIIII",
                major_version,
                minor_version,
                num_versions,
                gl_str_len,
                glx_str_len,
            )
        )
        buf.write(xcffib.pack_list(gl_versions, "I"))
        buf.write(xcffib.pack_list(gl_extension_string, "c"))
        buf.write(
            struct.pack(
                "=4x",
            )
        )
        buf.write(xcffib.pack_list(glx_extension_string, "c"))
        return self.send_request(35, buf, is_checked=is_checked)

    def NewList(self, context_tag, list, mode, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, list, mode))
        return self.send_request(101, buf, is_checked=is_checked)

    def EndList(self, context_tag, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context_tag))
        return self.send_request(102, buf, is_checked=is_checked)

    def DeleteLists(self, context_tag, list, range, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIIi", context_tag, list, range))
        return self.send_request(103, buf, is_checked=is_checked)

    def GenLists(self, context_tag, range, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIi", context_tag, range))
        return self.send_request(104, buf, GenListsCookie, is_checked=is_checked)

    def FeedbackBuffer(self, context_tag, size, type, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIii", context_tag, size, type))
        return self.send_request(105, buf, is_checked=is_checked)

    def SelectBuffer(self, context_tag, size, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIi", context_tag, size))
        return self.send_request(106, buf, is_checked=is_checked)

    def RenderMode(self, context_tag, mode, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", context_tag, mode))
        return self.send_request(107, buf, RenderModeCookie, is_checked=is_checked)

    def Finish(self, context_tag, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context_tag))
        return self.send_request(108, buf, FinishCookie, is_checked=is_checked)

    def PixelStoref(self, context_tag, pname, datum, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIIf", context_tag, pname, datum))
        return self.send_request(109, buf, is_checked=is_checked)

    def PixelStorei(self, context_tag, pname, datum, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIIi", context_tag, pname, datum))
        return self.send_request(110, buf, is_checked=is_checked)

    def ReadPixels(
        self,
        context_tag,
        x,
        y,
        width,
        height,
        format,
        type,
        swap_bytes,
        lsb_first,
        is_checked=True,
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack(
                "=xx2xIiiiiIIBB",
                context_tag,
                x,
                y,
                width,
                height,
                format,
                type,
                swap_bytes,
                lsb_first,
            )
        )
        return self.send_request(111, buf, ReadPixelsCookie, is_checked=is_checked)

    def GetBooleanv(self, context_tag, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIi", context_tag, pname))
        return self.send_request(112, buf, GetBooleanvCookie, is_checked=is_checked)

    def GetClipPlane(self, context_tag, plane, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIi", context_tag, plane))
        return self.send_request(113, buf, is_checked=is_checked)

    def GetDoublev(self, context_tag, pname, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", context_tag, pname))
        return self.send_request(114, buf, is_checked=is_checked)

    def GetError(self, context_tag, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context_tag))
        return self.send_request(115, buf, GetErrorCookie, is_checked=is_checked)

    def GetFloatv(self, context_tag, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", context_tag, pname))
        return self.send_request(116, buf, GetFloatvCookie, is_checked=is_checked)

    def GetIntegerv(self, context_tag, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", context_tag, pname))
        return self.send_request(117, buf, GetIntegervCookie, is_checked=is_checked)

    def GetLightfv(self, context_tag, light, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, light, pname))
        return self.send_request(118, buf, GetLightfvCookie, is_checked=is_checked)

    def GetLightiv(self, context_tag, light, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, light, pname))
        return self.send_request(119, buf, GetLightivCookie, is_checked=is_checked)

    def GetMapdv(self, context_tag, target, query, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, query))
        return self.send_request(120, buf, is_checked=is_checked)

    def GetMapfv(self, context_tag, target, query, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, query))
        return self.send_request(121, buf, GetMapfvCookie, is_checked=is_checked)

    def GetMapiv(self, context_tag, target, query, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, query))
        return self.send_request(122, buf, GetMapivCookie, is_checked=is_checked)

    def GetMaterialfv(self, context_tag, face, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, face, pname))
        return self.send_request(123, buf, GetMaterialfvCookie, is_checked=is_checked)

    def GetMaterialiv(self, context_tag, face, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, face, pname))
        return self.send_request(124, buf, GetMaterialivCookie, is_checked=is_checked)

    def GetPixelMapfv(self, context_tag, map, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", context_tag, map))
        return self.send_request(125, buf, GetPixelMapfvCookie, is_checked=is_checked)

    def GetPixelMapuiv(self, context_tag, map, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", context_tag, map))
        return self.send_request(126, buf, GetPixelMapuivCookie, is_checked=is_checked)

    def GetPixelMapusv(self, context_tag, map, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", context_tag, map))
        return self.send_request(127, buf, GetPixelMapusvCookie, is_checked=is_checked)

    def GetPolygonStipple(self, context_tag, lsb_first, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIB", context_tag, lsb_first))
        return self.send_request(
            128, buf, GetPolygonStippleCookie, is_checked=is_checked
        )

    def GetString(self, context_tag, name, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", context_tag, name))
        return self.send_request(129, buf, GetStringCookie, is_checked=is_checked)

    def GetTexEnvfv(self, context_tag, target, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, pname))
        return self.send_request(130, buf, GetTexEnvfvCookie, is_checked=is_checked)

    def GetTexEnviv(self, context_tag, target, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, pname))
        return self.send_request(131, buf, GetTexEnvivCookie, is_checked=is_checked)

    def GetTexGendv(self, context_tag, coord, pname, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, coord, pname))
        return self.send_request(132, buf, is_checked=is_checked)

    def GetTexGenfv(self, context_tag, coord, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, coord, pname))
        return self.send_request(133, buf, GetTexGenfvCookie, is_checked=is_checked)

    def GetTexGeniv(self, context_tag, coord, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, coord, pname))
        return self.send_request(134, buf, GetTexGenivCookie, is_checked=is_checked)

    def GetTexImage(
        self, context_tag, target, level, format, type, swap_bytes, is_checked=True
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack(
                "=xx2xIIiIIB", context_tag, target, level, format, type, swap_bytes
            )
        )
        return self.send_request(135, buf, GetTexImageCookie, is_checked=is_checked)

    def GetTexParameterfv(self, context_tag, target, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, pname))
        return self.send_request(
            136, buf, GetTexParameterfvCookie, is_checked=is_checked
        )

    def GetTexParameteriv(self, context_tag, target, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, pname))
        return self.send_request(
            137, buf, GetTexParameterivCookie, is_checked=is_checked
        )

    def GetTexLevelParameterfv(
        self, context_tag, target, level, pname, is_checked=True
    ):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIIiI", context_tag, target, level, pname))
        return self.send_request(
            138, buf, GetTexLevelParameterfvCookie, is_checked=is_checked
        )

    def GetTexLevelParameteriv(
        self, context_tag, target, level, pname, is_checked=True
    ):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIIiI", context_tag, target, level, pname))
        return self.send_request(
            139, buf, GetTexLevelParameterivCookie, is_checked=is_checked
        )

    def IsEnabled(self, context_tag, capability, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", context_tag, capability))
        return self.send_request(140, buf, IsEnabledCookie, is_checked=is_checked)

    def IsList(self, context_tag, list, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", context_tag, list))
        return self.send_request(141, buf, IsListCookie, is_checked=is_checked)

    def Flush(self, context_tag, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context_tag))
        return self.send_request(142, buf, is_checked=is_checked)

    def AreTexturesResident(self, context_tag, n, textures, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIi", context_tag, n))
        buf.write(xcffib.pack_list(textures, "I"))
        return self.send_request(
            143, buf, AreTexturesResidentCookie, is_checked=is_checked
        )

    def DeleteTextures(self, context_tag, n, textures, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIi", context_tag, n))
        buf.write(xcffib.pack_list(textures, "I"))
        return self.send_request(144, buf, is_checked=is_checked)

    def GenTextures(self, context_tag, n, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIi", context_tag, n))
        return self.send_request(145, buf, GenTexturesCookie, is_checked=is_checked)

    def IsTexture(self, context_tag, texture, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", context_tag, texture))
        return self.send_request(146, buf, IsTextureCookie, is_checked=is_checked)

    def GetColorTable(
        self, context_tag, target, format, type, swap_bytes, is_checked=True
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack("=xx2xIIIIB", context_tag, target, format, type, swap_bytes)
        )
        return self.send_request(147, buf, GetColorTableCookie, is_checked=is_checked)

    def GetColorTableParameterfv(self, context_tag, target, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, pname))
        return self.send_request(
            148, buf, GetColorTableParameterfvCookie, is_checked=is_checked
        )

    def GetColorTableParameteriv(self, context_tag, target, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, pname))
        return self.send_request(
            149, buf, GetColorTableParameterivCookie, is_checked=is_checked
        )

    def GetConvolutionFilter(
        self, context_tag, target, format, type, swap_bytes, is_checked=True
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack("=xx2xIIIIB", context_tag, target, format, type, swap_bytes)
        )
        return self.send_request(
            150, buf, GetConvolutionFilterCookie, is_checked=is_checked
        )

    def GetConvolutionParameterfv(self, context_tag, target, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, pname))
        return self.send_request(
            151, buf, GetConvolutionParameterfvCookie, is_checked=is_checked
        )

    def GetConvolutionParameteriv(self, context_tag, target, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, pname))
        return self.send_request(
            152, buf, GetConvolutionParameterivCookie, is_checked=is_checked
        )

    def GetSeparableFilter(
        self, context_tag, target, format, type, swap_bytes, is_checked=True
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack("=xx2xIIIIB", context_tag, target, format, type, swap_bytes)
        )
        return self.send_request(
            153, buf, GetSeparableFilterCookie, is_checked=is_checked
        )

    def GetHistogram(
        self, context_tag, target, format, type, swap_bytes, reset, is_checked=True
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack(
                "=xx2xIIIIBB", context_tag, target, format, type, swap_bytes, reset
            )
        )
        return self.send_request(154, buf, GetHistogramCookie, is_checked=is_checked)

    def GetHistogramParameterfv(self, context_tag, target, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, pname))
        return self.send_request(
            155, buf, GetHistogramParameterfvCookie, is_checked=is_checked
        )

    def GetHistogramParameteriv(self, context_tag, target, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, pname))
        return self.send_request(
            156, buf, GetHistogramParameterivCookie, is_checked=is_checked
        )

    def GetMinmax(
        self, context_tag, target, format, type, swap_bytes, reset, is_checked=True
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack(
                "=xx2xIIIIBB", context_tag, target, format, type, swap_bytes, reset
            )
        )
        return self.send_request(157, buf, GetMinmaxCookie, is_checked=is_checked)

    def GetMinmaxParameterfv(self, context_tag, target, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, pname))
        return self.send_request(
            158, buf, GetMinmaxParameterfvCookie, is_checked=is_checked
        )

    def GetMinmaxParameteriv(self, context_tag, target, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, pname))
        return self.send_request(
            159, buf, GetMinmaxParameterivCookie, is_checked=is_checked
        )

    def GetCompressedTexImageARB(self, context_tag, target, level, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIIi", context_tag, target, level))
        return self.send_request(
            160, buf, GetCompressedTexImageARBCookie, is_checked=is_checked
        )

    def DeleteQueriesARB(self, context_tag, n, ids, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIi", context_tag, n))
        buf.write(xcffib.pack_list(ids, "I"))
        return self.send_request(161, buf, is_checked=is_checked)

    def GenQueriesARB(self, context_tag, n, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIi", context_tag, n))
        return self.send_request(162, buf, GenQueriesARBCookie, is_checked=is_checked)

    def IsQueryARB(self, context_tag, id, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", context_tag, id))
        return self.send_request(163, buf, IsQueryARBCookie, is_checked=is_checked)

    def GetQueryivARB(self, context_tag, target, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, target, pname))
        return self.send_request(164, buf, GetQueryivARBCookie, is_checked=is_checked)

    def GetQueryObjectivARB(self, context_tag, id, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, id, pname))
        return self.send_request(
            165, buf, GetQueryObjectivARBCookie, is_checked=is_checked
        )

    def GetQueryObjectuivARB(self, context_tag, id, pname, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIII", context_tag, id, pname))
        return self.send_request(
            166, buf, GetQueryObjectuivARBCookie, is_checked=is_checked
        )


xcffib._add_ext(key, glxExtension, _events, _errors)
