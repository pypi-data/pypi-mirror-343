from opcua import Client
import resultsObjects
import uaDataType
import time
import logging


class client_OPC_UA():
    """This class represents an OPC UA client which can connect to an OPC UA
    server, read and write node values.
    """

    def __init__(self, p_URL: str, p_retry_attempts: int = 20,
                 p_retry_delay: int = 5, p_log_level: str = "WARNING"):
        """Initialize the OPC UA client with connection parameters.

        Args:
            p_URL (str): URL of the OPC UA server to connect to.
            p_retry_attempts (int, optional): Number of connection attempts.
                Defaults to 20.
            p_retry_delay (int, optional): Delay between two connection
                attempts. Defaults to 5.
            p_log_level (str, optional): Setup the client's logger level of
                logging in the terminal and the logfile. Defaults to "WARNING".
        """
        self.url = p_URL
        self.retry_attempts = p_retry_attempts
        self.retry_delay = p_retry_delay
        self.log_level = p_log_level
        self.client = Client(self.url)

        # Configure logger for the client
        self.logger = logging.getLogger("client_OPC_UA_logger")
        self.logger.setLevel(self.log_level)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(name)s - %(filename)s - '
            '%(funcName)s - %(message)s'
        ))
        self.logger.addHandler(handler)

        # Disable logs from the opcua library
        logging.getLogger("opcua").setLevel(logging.WARNING)

    def connect(self, retry: bool = True):
        """Connect to the OPC UA server.
        This function attempts to connect to the server. If retry is True and
        the connection fails, it retries the connection
        a specified number of times with a delay between attempts.

        Args:
            retry (bool, optional): Enable connection retry. Defaults to True.

        Returns:
            OpcuaConnectResult: Result of the connection operation.
        """

        for attempt in range(self.retry_attempts):
            try:
                self.client.connect()
                self.logger.info(
                    "Successfully connected to the OPC UA server "
                )
                return resultsObjects.OpcuaConnectResult(p_success=True,
                                                         p_error=None)
            except Exception as e:
                if retry:
                    return resultsObjects.OpcuaConnectResult(p_success=False,
                                                             p_error=e)
                self.logger.error(
                    f"Failed to connect to the OPC UA server: {e}"
                )
                self.logger.warning(
                    f"Attempt {attempt + 1}/{self.retry_attempts} failed. "
                    f"Retrying in {self.retry_delay} seconds... : {e}"
                )
                time.sleep(self.retry_delay)
        return resultsObjects.OpcuaConnectResult(p_success=False,
                                                 p_error="Max attempts "
                                                 "reached")

    def set_connection_parameters(self, p_retry_attempts: int = None,
                                  p_retry_delay: int = None):
        if p_retry_attempts is not None:
            self.retry_attempts = p_retry_attempts
        if p_retry_delay is not None:
            self.retry_delay = p_retry_delay

    def set_log_level(self, p_log_level: str = None):
        if p_log_level is not None:
            self.log_level = p_log_level
            self.logger.setLevel(self.log_level)

    def disconnect(self):
        """Disconnect from the OPC UA server.
        """
        if self.client is not None:
            try:
                self.client.disconnect()  # Correction ici
                return resultsObjects.OpcuaConnectResult(p_success=True,
                                                         p_error=None)
            except Exception as e:
                self.logger.error(
                        f"Failed to disconnect from the OPC UA server: {e}"
                    )
                return resultsObjects.OpcuaConnectResult(p_success=False,
                                                         p_error=e)

    def read_value(self, namespace: int, id: int):
        """Read a value from an OPC UA node. The node is identified by its
        namespace and identifier. The function returns the value and its type.

        Args:
            namespace (int): Namespace of the node to read from.
            id (int): Identifier of the node to read from.

        Returns:
            OpcuaReadResult: Result of the read operation.
        """
        if self.client is not None:
            client_node = self.client.get_node(f'ns={namespace};i={id}')
            try:
                client_node_value = client_node.get_value()
                self.logger.debug(
                        f"Value read from node ns={namespace};i={id}: "
                        f"{client_node_value}"
                    )
                return resultsObjects.OpcuaReadResult(
                    p_value=client_node_value,
                    p_node_type=type(client_node_value).__name__,
                    p_success=True
                )
            except Exception as e:
                self.logger.error(
                        f"Failed to read from OPC UA node "
                        f"ns={namespace};i={id}: {e}"
                    )
                return resultsObjects.OpcuaReadResult(
                    p_success=False,
                    p_error=e
                )
        else:
            self.logger.error(
                    f"Failed to read from OPC UA node "
                    f"ns={namespace};i={id}: Client is not declared"
                    )
            return resultsObjects.OpcuaReadResult(p_success=False,
                                                  p_error="Client not declared"
                                                  )

    def write_value(self, namespace: int,
                    id: int,
                    value: any,
                    p_variant_type: int = None):
        """Write a value to an OPC UA node. Variant type is determined
        automatically based on the value type unless specified.

        Args:
            namespace (int): Namespace of the node to write to.
            id (int): Identifier of the node to write to.
            value (any): Value to write to the node.
            p_variant_type (int, optional): Variant type of the value.

        Returns:
            OpcuaWriteResult: Result of the write operation.
        """
        if p_variant_type is None:
            variant_type = uaDataType.getVariantType(value)
        else:
            variant_type = p_variant_type

        if self.client is not None:
            client_node = self.client.get_node(f'ns={namespace};i={id}')
            # client_node_dv = ua.DataValue(ua.Variant(value, variant_type))
            try:
                client_node.set_value(value, variant_type)
                self.logger.debug(f"Value written to node "
                                  f"ns={namespace};i={id}: {value} "
                                  f"(type: {variant_type})")
                return resultsObjects.OpcuaWriteResult(p_success=True,
                                                       p_error=None)
            except Exception as e:
                self.logger.error(f"Failed to write to OPC UA node "
                                  f"ns={namespace};i={id}: {e}")
                return resultsObjects.OpcuaWriteResult(p_success=False,
                                                       p_error=e)
        else:
            self.logger.error(
                    f"Failed to write to OPC UA node "
                    f"ns={namespace};i={id}: Client is not declared"
                    )
            return resultsObjects.OpcuaWriteResult(p_success=False,
                                                   p_error="Client not "
                                                   "declared")
