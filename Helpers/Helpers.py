import inspect

def get_globals():
    caller_frame = inspect.currentframe().f_back
    caller_globals = caller_frame.f_globals
    for item in caller_globals: 
        print( item )

def print_list( x_list ):
    for item in x_list:
        print( item )

# same as print_list( dir( object ) )
def print_attributes( object ):
    for item in dir( object ):
        print( item )

def print_keys( dict_obj ):
    for item in dict_obj.keys():
        print( item )

def print_nested( d, name="?" ):
    keys_list = []
    get_nested_keys( d, keys_list, name )
    print_list( keys_list )
    return keys_list

# Will dig for keys.
# when hitting list, will only use first item, this is intentional.  
# Most RSS feeds have the same keys duplicated in each of the array.   
# Top level cannot be a list.
def get_nested_keys( d, keys, prefix ):
    for k, v in d.items():
        if isinstance( v, list ):
            if len(v) > 0:
                get_nested_keys( v[0], keys, f'{prefix}:{k}:0' )
        if isinstance( v, dict ):
            get_nested_keys( v, keys, f'{prefix}:{k}' )
        else:
            keys.append( f'{prefix}:{k}' )

def divider( number=25 ):
    print( "#"*number ) # Only saves so much typing, but I like it.

def heading( text="", length=0  ):
    """Helper to keep test code a little more organized"""
    if length >= 0 and isinstance( length, int ) and isinstance( text, str ):
        # 0,0 no text, no length : 
        if text == "" and length == 0:
            length = 25
        elif text != "" and length == 0:
            length = len( text ) + 2
        print( "#"*length + "\n# " + text + "\n" + "#"*length  )
    else:
        print( "heading() parameter error" )

def c_header( heading, length=0 ): # In case you also use C/C++ 
    """ Heading, but for C++ """
    if length == 0 and heading == "":
        length = 50
    elif length == 0:
        length = len( heading ) + 4
    head_str = "//" + "="*length + "\n// " + heading + "\n//" + "="*length
    return head_str

def var_header( heading="", length=0, block_symbol="=", comment_symbol="#" ):
    """More customizable headers"""
    if length == 0 and heading == "":
        length = 50
    elif length == 0:
        length = len( heading ) + 4
    if len( block_symbol ) != 1:
        length = int( length / len( block_symbol ) )
        
    head_str = comment_symbol + block_symbol*length + "\n" + comment_symbol + " " + heading + "\n" + comment_symbol + "" + block_symbol*length
    return head_str
    

if __name__ == '__main__':
    heading( "testing" )
    heading( "divider(30)", 40 )
    divider(30)
    heading( "divider()" )
    divider()
    heading( "Blank Heading" )
    heading("",40)
    heading()
    heading(4)
    divider()
    print( c_header( "C/++ Heading" ) )
    print( var_header( "x" ) )
    print( var_header(  ) )
    print( var_header( "Kitty", 0, "-", "//" ) )
    print( var_header( "Kitty", 0, "*", "//" ) )
    print( var_header( "Kitty", 0, "=", "//" ) )
    print( var_header( "Kitty", 0, "~", "//" ) )
    print( var_header( "Kitty", 0, "<3", "//" ) )
    print( var_header( "Kitty", 0, "<3", "<3" ) )
