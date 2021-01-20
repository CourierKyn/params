from typing import Collection

import ipywidgets as widgets
from IPython.display import display


def DEFINE(  # pylint: disable=invalid-name
        name: str,
        default,
        options: Collection = (),
        type: str = '',
        multiline: bool = False,
        **args):
    """Registers a generic Flag object.

    NOTE: in the docstrings of all DEFINE* functions, "registers" is short
    for "creates a new flag and registers it".

    Auxiliary function: clients should use the specialized DEFINE_<type>
    function instead.

    Args:
      name: str, the flag name.
      default: The default value of the flag.
      **args: dict, the extra keyword args that are passed to Flag __init__.
    """
    _DEFINE_param(True, name, default, options, type, multiline, **args)


def _DEFINE_param(universal: bool, name: str, default, options: Collection = (), type: str = '',
                  multiline: bool = False, **kwargs):
    if universal and not type:
        if multiline:
            type = 'Textarea'
        if isinstance(default, int):
            type = 'IntText'
        if isinstance(default, float):
            type = 'FloatText'
        if isinstance(default, bool):
            type = 'Checkbox'
        if isinstance(default, (list, tuple, set)) and default and not options:
            options = default
            default = next(iter(options))
        if options:
            if isinstance(default, (list, tuple, set)):
                type = 'SelectMultiple'
            else:
                type = 'Select'
        type = type if type else 'Text'

    setattr(PARAMS, name, default)

    kwargs['layout'] = kwargs.get('layout', widgets.Layout(width='99%'))

    if type == 'Select':
        widget = widgets.Dropdown(value=default, description=name, options=[*options], **kwargs)
    elif type == 'SelectMultiple':
        widget = widgets.SelectMultiple(value=[*default], description=name, options=[*options], **kwargs)
    else:
        widget_cls = eval('widgets.{}'.format(type))
        widget = widget_cls(value=default, description=name, **kwargs)
    PARAMS.widgets[name] = widget

    def on_value_change(change):
        setattr(PARAMS, name, change['new'])

    widget.observe(on_value_change, names='value')

    display(widget)


def DEFINE_string(name: str, default, help: str = 'for compatibility with absl.flags only', multiline: bool = False,
                  **args):
    if multiline:
        _DEFINE_param(False, name, default, type='Textarea', **args)
    else:
        _DEFINE_param(False, name, default, type='Text', **args)


def DEFINE_text(name: str, default, help: str = 'for compatibility with absl.flags only', **args):
    DEFINE_string(name, default, multiline=True, **args)


def DEFINE_boolean(name: str, default, help: str = 'for compatibility with absl.flags only', **args):
    _DEFINE_param(False, name, default, type='Checkbox', **args)


DEFINE_bool = DEFINE_boolean


def DEFINE_float(name: str, default, help: str = 'for compatibility with absl.flags only', **args):
    _DEFINE_param(False, name, default, type='FloatText', **args)


def DEFINE_integer(name: str, default, help: str = 'for compatibility with absl.flags only', **args):
    _DEFINE_param(False, name, default, type='IntText', **args)


def DEFINE_enum(name: str, default, options: Collection = (), help: str = 'for compatibility with absl.flags only',
                **args):
    if isinstance(default, (list, tuple, set)) and default and not options:
        options = default
        default = next(iter(options))
    _DEFINE_param(False, name, default, options, type='Select', **args)


def DEFINE_multi_enum(name: str, default: Collection, options: Collection,
                      help: str = 'for compatibility with absl.flags only',
                      **args):
    _DEFINE_param(False, name, default, options, type='SelectMultiple', **args)


class PARAMS(object):
    widgets = {}

    @classmethod
    def set_default(cls, name, value):
        """Changes the default value of the named flag object.

        The flag's current value is also updated.

        Args:
          name: str, the name of the flag to modify.
          value: The new default value.
        """
        cls.widgets[name].value = value
        setattr(cls, name, value)
