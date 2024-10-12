from Xlib import X, display, Xatom

def list_windows_with_pids():
    # Open a connection to the default X display (usually ":0")
    d = display.Display()

    # Get the root window of the default screen
    root = d.screen().root

    # Query the tree of windows
    root_window_info = root.query_tree()

    # Get the list of child windows (top-level windows on the root window)
    windows = root_window_info.children
    windows_properties = []
    # Loop over each window and try to get its PID
    for window in windows:
        pid = None
        try:
            # Get the _NET_WM_PID property (the PID of the process owning the window)
            pid_property = window.get_full_property(d.intern_atom('_NET_WM_PID'), Xatom.CARDINAL)

            if pid_property:
                # Extract the PID from the property value (which is an array)
                pid = pid_property.value[0]
                win_str = (f"Window ID: 0x{window.id:x},".ljust(25) + f" PID: {pid}")
                windows_properties.append( [ win_str, window.id, pid ] )
            else:
                ""#print(f"Window ID: 0x{window.id:x}, PID: Unknown")

        except Exception as e:
            print(f"Failed to get PID for Window ID 0x{window.id:x}: {e}")

    # Close the connection to the display when done
    d.close()
    return windows_properties
# Call the function to list windows with their PIDs


def print_windows():
    windows = list_windows_with_pids()
    for window in windows:
        print( window[0] + "  " + str( window[1] ).ljust(10) + f"0x{window[1]:x}".ljust(10) )

def get_windows_for_pid( pid ):
    windows = list_windows_with_pids()
    for window in windows:
        if window[2] == pid:
            print( window[0] )

def get_windows_for_pid( pid ):
    windows = list_windows_with_pids()
    window_list = []
    for window in windows:
        if window[2] == pid:
            window_list.append( window )
    return window_list

