import io


class OutputRedirector( io.StringIO ):
    """
    Custom class to redirect stdout and stderr to capture outputs and errors.
    """
    def __init__( self, output_widget, combined_widget, prefix ):
        super().__init__()
        self.output_widget = output_widget  # The QListWidget where output/errors will be displayed
        self.combined_widget = combined_widget  # The combined log widget
        self.prefix = prefix  # Prefix to identify whether it's stdout or stderr

    def write( self, msg ):
        """
        This method is called whenever something is written to stdout or stderr.
        It appends the message to the QListWidget as a single item and also logs it to the combined widget.
        """
        stripped_msg = msg.strip()

        if stripped_msg:
            # Add the message to the specific output widget (stdout or stderr)
            self.output_widget.addItem( msg )

            # Add the message with prefix to the combined log widget
            self.combined_widget.addItem( self.prefix + msg )

    def flush( self ):
        pass
