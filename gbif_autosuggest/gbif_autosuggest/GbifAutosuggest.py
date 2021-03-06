# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class GbifAutosuggest(Component):
    """A GbifAutosuggest component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- label (string; required):
    A label that will be printed when this component is rendered.

- value (boolean | number | string | dict | list; optional):
    The value displayed in the input."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, label=Component.REQUIRED, value=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'label', 'value']
        self._type = 'GbifAutosuggest'
        self._namespace = 'gbif_autosuggest'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'label', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['label']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(GbifAutosuggest, self).__init__(**args)
