"""Shared UI components — pure rx.* only."""
import reflex as rx


def corners() -> rx.Component:
    return rx.fragment(
        rx.box(class_name="ag-c ag-c-tl"),
        rx.box(class_name="ag-c ag-c-tr"),
        rx.box(class_name="ag-c ag-c-bl"),
        rx.box(class_name="ag-c ag-c-br"),
    )


def glass(*children, pad="24px", extra="", **kw) -> rx.Component:
    # Merge any caller-supplied class_name with our base ag-glass class.
    caller_cn = kw.pop("class_name", "")
    merged_cn = " ".join(filter(None, ["ag-glass", extra, caller_cn]))
    padding = kw.pop("padding", pad)
    return rx.box(*children, class_name=merged_cn, padding=padding, **kw)


def hud(txt, extra="", **kw) -> rx.Component:
    caller_cn = kw.pop("class_name", "")
    merged_cn = " ".join(filter(None, ["ag-h", extra, caller_cn]))
    return rx.text(txt, class_name=merged_cn, **kw)


def btn(label, **kw) -> rx.Component:
    return rx.box(label, class_name="ag-btn", cursor="pointer", **kw)
