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
    print( "#"*number )

def heading( text="", length=0  ):
    if length >= 0 and isinstance( length, int ) and isinstance( text, str ):
        # 0,0 no text, no length : 
        if text == "" and length == 0:
            length = 25
        elif text != "" and length == 0:
            length = len( text ) + 2
        print( "#"*length + "\n# " + text + "\n" + "#"*length  )
    else:
        print( "heading() parameter error" )

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

