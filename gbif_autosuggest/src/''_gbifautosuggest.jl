# AUTO GENERATED FILE - DO NOT EDIT

export ''_gbifautosuggest

"""
    ''_gbifautosuggest(;kwargs...)

A GbifAutosuggest component.

Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `label` (String; required): A label that will be printed when this component is rendered.
- `value` (Bool | Real | String | Dict | Array; optional): The value displayed in the input.
"""
function ''_gbifautosuggest(; kwargs...)
        available_props = Symbol[:id, :label, :value]
        wild_props = Symbol[]
        return Component("''_gbifautosuggest", "GbifAutosuggest", "gbif_autosuggest", available_props, wild_props; kwargs...)
end

