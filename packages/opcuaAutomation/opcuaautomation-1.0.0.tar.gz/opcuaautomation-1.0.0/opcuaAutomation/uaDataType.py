from opcua import ua


def getVariantType(value):
    """Get the OPC UA variant type of a given value.
    Support the types bool, int, float and str.

    Args:
        value: The value to determine the variant type for.

    Returns:
        int: The OPC UA variant type.
    """
    if isinstance(value, bool):
        return ua.VariantType.Boolean
    elif isinstance(value, int):
        return ua.VariantType.Int16
    elif isinstance(value, float):
        return ua.VariantType.Float
    elif isinstance(value, str):
        return ua.VariantType.String
    else:
        raise ValueError(f"Unsupported type {type(value)}"
                         "for OPC UA variant")
