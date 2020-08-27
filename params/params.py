import ipywidgets as widgets
from IPython.display import display


def DEFINE(  # pylint: disable=invalid-name
        name: str,
        default,
        options: list = [],
        type: str = '',
        **args):
    """Registers a generic Flag object.

    NOTE: in the docstrings of all DEFINE* functions, "registers" is short
    for "creates a new flag and registers it".

    Auxiliary function: clients should use the specialized DEFINE_<type>
    function instead.

    Args:
      parser: ArgumentParser, used to parse the flag arguments.
      name: str, the flag name.
      default: The default value of the flag.
      help: str, the help message.
      flag_values: FlagValues, the FlagValues instance with which the flag will be
        registered. This should almost never need to be overridden.
      serializer: ArgumentSerializer, the flag serializer instance.
      module_name: str, the name of the Python module declaring this flag. If not
        provided, it will be computed using the stack trace of this call.
      **args: dict, the extra keyword args that are passed to Flag __init__.

    Returns:
      a handle to defined flag.
    """
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


def DEFINE_string(name: str, default, **args):
    _DEFINE_param(False, name, default, type='Text')


def DEFINE_boolean(name: str, default, **args):
    _DEFINE_param(False, name, default, type='Checkbox')


def DEFINE_float(name: str, default, **args):
    _DEFINE_param(False, name, default, type='FloatText')


def DEFINE_integer(name: str, default, **args):
    _DEFINE_param(False, name, default, type='IntText')


def DEFINE_enum(name: str, default, options: list = [], **args):
    if isinstance(default, list) and default and not options:
        options = default
        default = options[0]
    _DEFINE_param(False, name, default, options, type='Select')


def DEFINE_multi_enum(name: str, default, options: list = [], **args):
    if not isinstance(default, list):
        default = [default]
    _DEFINE_param(False, name, default, options, type='SelectMultiple')


class PARAMS(object):
    def set_default(self, name, value):
        """Changes the default value of the named flag object.

        The flag's current value is also updated if the flag is currently using
        the default value, i.e. not specified in the command line, and not set
        by FLAGS.name = value.

        Args:
          name: str, the name of the flag to modify.
          value: The new default value.
        """
        setattr(self, name, value)
