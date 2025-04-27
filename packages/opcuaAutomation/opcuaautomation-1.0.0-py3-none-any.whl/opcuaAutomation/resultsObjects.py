class OpcuaConnectResult():
    def __init__(self, p_success: bool = None,
                 p_error: str = None):
        """Represents the result of an OPC UA connection attempt.

        Args:
            success (bool, optional): Success or not of the connection.
            error (str, optional): Error code of the connection.
        """
        self.success = p_success
        self.error = p_error


class OpcuaReadResult():
    def __init__(self, p_value: str = None,
                 p_node_type: str = None,
                 p_success: bool = None,
                 p_error: str = None):
        """Represents the result of an OPC UA node read operation.

        Args:
            value (str, optional): Value of the node readed.
            node_type (str, optional): Type of the node readed.
            success (bool, optional): Succes or not of the reading.
            error (str, optional): Error code of the reading.
        """
        self.value = p_value
        self.node_type = p_node_type
        self.success = p_success
        self.error = p_error


class OpcuaWriteResult():
    def __init__(self, p_success: bool = None,
                 p_error: str = None):
        """Represents the result of an OPC UA node write operation.

        Args:
            success (bool, optional): Succes or not of the reading.
            error (str, optional): Error code of the reading.
        """
        self.success = p_success
        self.error = p_error
