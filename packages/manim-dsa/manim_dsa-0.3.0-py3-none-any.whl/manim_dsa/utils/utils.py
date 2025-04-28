from __future__ import annotations

from manim import *
from manim.typing import Vector3D


def set_text(old_manim_text: Text, new_text: str) -> Text:
    """
    Replace the content of an existing Manim Text object with new text while preserving its style.

    Parameters
    ----------
    old_manim_text : Text
        The original Manim Text object whose content is being replaced.
    new_text : str
        The new text content to set.

    Returns
    -------
    Text
        A new Text object with the updated content, matching the style and position of the original text.
    """
    NewText = type(old_manim_text)
    res = (
        NewText(
            str(new_text), font=old_manim_text.font, font_size=old_manim_text.font_size
        )
        .match_style(old_manim_text)
        .move_to(old_manim_text)
    )
    return res


def TextReplace(scene: Scene, scene_mobj1: Group, mObj1: Text, mObj2: Text):
    """
    Replace one text object with another in a scene using animations.

    Parameters
    ----------
    scene : Scene
        The Manim Scene where the animation takes place.
    scene_mobj1 : Group
        The group containing `mObj1`, which is replaced in this group.
    mObj1 : Text
        The original text object to be replaced.
    mObj2 : Text
        The text object whose content will replace `mObj1`.

    Notes
    -----
    The animation consists of fading out the old text (`mObj1`) while animating
    the new text (`mObj2`) into its position.
    """
    old_mobj = mObj1.copy()
    scene_mobj1 -= mObj1
    mObj1 = set_text(mObj1, str(mObj2.text))
    scene_mobj1 += mObj1
    new_mobj = mObj1.copy()
    mObj1.set_opacity(0)
    scene.play(
        ReplacementTransform(mObj2.copy(), new_mobj),
        ApplyMethod(old_mobj.set_opacity, 0),
    )
    mObj1.set_opacity(1)
    new_mobj.set_opacity(0)


class Labelable:
    """
    A mixin class that provides functionality to add a label to Manim objects.

    Attributes
    ----------
    label : Text or None
        The label associated with the object, if any.
    """

    def __init__(self):
        """
        Initialize the Labelable object with no label.
        """
        super().__init__()
        self.label = None

    def add_label(
        self,
        text: Text,
        direction: Vector3D = UP,
        buff: float = 0.5,
        **kwargs,
    ) -> Labelable:
        """
        Add a label to the object.

        Parameters
        ----------
        text : Text
            The Text object to use as the label.
        direction : Vector3D, optional
            The direction to place the label relative to the object (default is `UP`).
        buff : float, optional
            The distance between the object and the label (default is 0.5).
        **kwargs : dict
            Additional keyword arguments for positioning.

        Returns
        -------
        Labelable
            The instance with the label added.
        """
        self.label = text
        self.label.next_to(self, direction, buff, **kwargs)
        return self

    def has_label(self) -> bool:
        """
        Check if the object has a label.

        Returns
        -------
        bool
            `True` if the object has a label, otherwise `False`.
        """
        return self.label is not None


class Highlightable:
    """
    A mixin class that provides functionality to highlight and unhighlight Manim objects.

    Attributes
    ----------
    highlighting : VMobject or None
        The highlight effect associated with the object, if any.
    """

    def __init__(self):
        """
        Initialize the Highlightable object with no highlighting.
        """
        super().__init__()
        self.__target = None
        self.highlighting = None

    def _add_highlight(self, target: VMobject):
        """
        Internal method to set up highlighting for a target VMobject.

        Parameters
        ----------
        target : VMobject
            The object to highlight.
        """
        self.__target = target
        self.highlighting = (
            target.copy().set_fill(opacity=0).set_z_index(self.__target.z_index + 1)
        )
        self.set_highlight()

    def highlight(
        self, stroke_color: ManimColor = RED, stroke_width: float = 8
    ) -> Highlightable:
        """
        Highlight the object with the specified stroke color and width.

        Parameters
        ----------
        stroke_color : ManimColor, optional
            The color of the highlight stroke (default is `RED`).
        stroke_width : float, optional
            The width of the highlight stroke (default is 8).

        Returns
        -------
        Highlightable
            The instance with the highlight applied.
        """
        self.set_highlight(stroke_color, stroke_width)
        # Since the target object could have been scaled or moved, scale and move self.highlighting
        self.highlighting.width = self.__target.width
        self.highlighting.height = self.__target.height
        self.highlighting.move_to(self.__target)
        self += self.highlighting
        return self

    @override_animate(highlight)
    def _highlight_animation(
        self,
        stroke_color: ManimColor = RED,
        stroke_width: float = 8,
        anim_args=None,
    ) -> Animation:
        """
        Animation for highlighting the object.

        Parameters
        ----------
        stroke_color : ManimColor, optional
            The color of the highlight stroke (default is `RED`).
        stroke_width : float, optional
            The width of the highlight stroke (default is 8).
        anim_args : dict, optional
            Additional arguments for the animation.

        Returns
        -------
        Animation
            The animation for highlighting.
        """
        self.highlight(stroke_color, stroke_width)
        return Create(self.highlighting, **anim_args)

    def set_highlight(self, stroke_color: ManimColor = RED, stroke_width: float = 8):
        """
        Set the highlight properties.

        Parameters
        ----------
        stroke_color : ManimColor, optional
            The color of the highlight stroke (default is `RED`).
        stroke_width : float, optional
            The width of the highlight stroke (default is 8).
        """
        self.highlighting.set_stroke(stroke_color, stroke_width)

    def unhighlight(self) -> Highlightable:
        """
        Remove the highlight from the object.

        Returns
        -------
        Highlightable
            The instance with the highlight removed.
        """
        self -= self.highlighting
        return self

    @override_animate(unhighlight)
    def _unhighlight_animation(self, anim_args=None) -> Animation:
        """
        Animation for unhighlighting the object.

        Parameters
        ----------
        anim_args : dict, optional
            Additional arguments for the animation.

        Returns
        -------
        Animation
            The animation for unhighlighting.
        """
        if anim_args is None:
            anim_args = {}

        self.unhighlight()
        return FadeOut(self.highlighting, **anim_args)
