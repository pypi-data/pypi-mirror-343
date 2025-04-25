"""Mouse bindings to the viewer."""

import numpy as np


def crosshair(viewer, event):
    """Enable crosshair."""
    if "Alt" not in event.modifiers:
        return

    if not viewer.cross_hair.visible:
        viewer.cross_hair.visible = True

    # on mouse press
    if event.type == "mouse_press":
        viewer.cross_hair.position = event.position
        viewer.events.crosshair(position=event.position)
        yield

    # on mouse move
    while event.type == "mouse_move" and "Alt" in event.modifiers:
        viewer.cross_hair.position = event.position
        viewer.events.crosshair(position=event.position)
        yield

    # on mouse release
    if viewer.cross_hair.auto_hide:
        viewer.cross_hair.visible = False
    yield


def zoom(viewer, event):
    """Enable zoom."""
    if "Shift" not in event.modifiers or viewer.dims.ndisplay == 3:
        return

    if not viewer.zoom_box.visible:
        viewer.zoom_box.visible = True

    # on mouse press
    press_position = None
    if event.type == "mouse_press":
        press_position = event.position
        viewer.zoom_box.bounds = (press_position, press_position)
        # viewer.events.crosshair(position=event.position)
        yield

    # on mouse move
    while event.type == "mouse_move" and "Shift" in event.modifiers:
        if press_position is None:
            continue
        position = event.position
        viewer.zoom_box.bounds = (press_position, position)
        # viewer.events.crosshair(position=event.position)
        yield

    # on mouse release
    viewer.zoom_box.visible = False
    viewer.events.zoom(value=viewer.zoom_box.extents())
    yield


def double_click_to_zoom_reset(viewer, event):
    """Zoom in on double click by zoom_factor; zoom out with Alt."""
    if viewer.layers.selection.active and viewer.layers.selection.active.mode != "pan_zoom":
        return

    if "Control" in event.modifiers:
        viewer.reset_view()
    else:
        # if Alt held down, zoom out instead
        zoom_factor = 0.5 if "Alt" in event.modifiers else 2
        viewer.camera.zoom *= zoom_factor
        if viewer.dims.ndisplay == 3 and viewer.dims.ndim == 3:
            viewer.camera.center = np.asarray(viewer.camera.center) + (
                np.asarray(event.position)[np.asarray(viewer.dims.displayed)] - np.asarray(viewer.camera.center)
            ) * (1 - 1 / zoom_factor)
        else:
            viewer.camera.center = np.asarray(viewer.camera.center)[-2:] + (
                np.asarray(event.position)[-2:] - np.asarray(viewer.camera.center)[-2:]
            ) * (1 - 1 / zoom_factor)
