import ipywidgets as widgets
from IPython.display import display


def DEFINE(name: str, default, options: list = [], type: str = ''):
    _DEFINE_param(True, name, default, options, type)


def _DEFINE_param(universal: bool, name: str, default, options: list = [], type: str = ''):
    if universal and type == '':
        if isinstance(default, int):
            type = 'IntText'
        if isinstance(default, float):
            type = 'FloatText'
        if isinstance(default, bool):
            type = 'Checkbox'
        if isinstance(default, list) and default and not options:
            options = default
            default = options[0]
        if options:
            type = 'Select'
        type = 'Text' if type == '' else type

    setattr(PARAMS, name, default)

    if type == 'Select':
        widget = widgets.Dropdown(value=default, description=name, options=options)
    else:
        widget = eval('widgets.{}(value=default, description=name)'.format(type))

    def on_value_change(change):
        setattr(PARAMS, name, change['new'])

    widget.observe(on_value_change, names='value')

    display(widget)


def DEFINE_string(name: str, default, help: str = 'for compatibility with tf.flags only'):
    _DEFINE_param(False, name, default, type='Text')


def DEFINE_boolean(name: str, default, help: str = 'for compatibility with tf.flags only'):
    _DEFINE_param(False, name, default, type='Checkbox')


def DEFINE_float(name: str, default, help: str = 'for compatibility with tf.flags only'):
    _DEFINE_param(False, name, default, type='FloatText')


def DEFINE_integer(name: str, default, help: str = 'for compatibility with tf.flags only'):
    _DEFINE_param(False, name, default, type='IntText')


def DEFINE_enum(name: str, default, options: list = [], help: str = 'for compatibility with tf.flags only'):
    if isinstance(default, list) and default and not options:
        options = default
        default = options[0]
    _DEFINE_param(False, name, default, options, type='Select')


def DEFINE_multi_enum(name: str, default, options: list = [], help: str = 'for compatibility with tf.flags only'):
    if not isinstance(default, list):
        default = [default]
    _DEFINE_param(False, name, default, options, type='SelectMultiple')


class PARAMS(object):
    pass
