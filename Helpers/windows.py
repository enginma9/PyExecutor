def retrieve_sizes( some_size ):
    width = some_size.width()
    height = some_size.height()
    return width, height, str( width ) + "x" + str( height )

def measure( window ):
    #Normal size
    set_width  = 200
    set_height = 100

    #Grab available
    avail_width  = window.screen().availableSize().width()
    avail_height = window.screen().availableSize().height()

    #window.showNormal()
    window.resize( set_width, set_height )
    normal_width = window.frameSize().width()
    normal_height = window.frameSize().height()

    #print( normal_width, normal_height, set_width, set_height )
    # Set amounts to adjust window size by
    win_width_diff  = normal_width - set_width 
    win_height_diff =  normal_height - set_height

    return avail_width, avail_height, win_width_diff, win_height_diff


def split_both( window_1, window_2 ):
    """ ? """
    window_1.showNormal()
    window_2.showNormal()
    avail_width, avail_height, win_width_diff, win_height_diff = measure( window_1 )
    print( avail_width, avail_height, win_width_diff, win_height_diff )
    W = int( ( avail_width - win_width_diff ) / 2 )
    H = int( ( avail_height - win_height_diff ) )
    print( H, W )
    window_1.move( 0, 0 )
    window_2.move( W, 0 )
    window_1.resize( W, H )
    window_2.resize( W, H )
    window_1.activateWindow()
    window_2.activateWindow()

def split_right( window ):
    """ ? """
    window.showNormal()
    avail_width, avail_height, win_width_diff, win_height_diff = measure( window )
    #print( avail_width, avail_height, win_width_diff, win_height_diff )
    W = int( ( avail_width - win_width_diff ) / 2 )
    H = int( avail_height - win_height_diff )
    #print( H, W )
    window.move( W, 0 )
    window.resize( W, H )
    window.activateWindow()

def split_left( window ): 
    """ ? """    
    avail_width, avail_height, win_width_diff, win_height_diff = measure( window )
    window.showNormal()
    avail_width, avail_height, win_width_diff, win_height_diff = measure( window )
    #print( avail_width, avail_height, win_width_diff, win_height_diff )
    W = int( ( avail_width - win_width_diff ) / 2 )
    H = int( avail_height - win_height_diff )
    #print( H, W )
    window.move( 0, 0 )
    window.resize( W, H )
    window.activateWindow()


def split_four( window_1, window_2, window_3, window_4 ):
    """ ? """
    window_1.showNormal()
    window_2.showNormal()
    window_3.showNormal()
    window_4.showNormal()
    avail_width, avail_height, win_width_diff, win_height_diff = measure( window_1 )

    W = int( ( avail_width - win_width_diff ) / 2 )
    H = int( ( avail_height - win_height_diff ) / 2 )

    window_1.move( 0, 0 )
    window_2.move( W, 0 )
    window_3.move( 0, H )
    window_4.move( W, H )

    window_1.resize( W, H )
    window_2.resize( W, H )
    window_3.resize( W, H )
    window_4.resize( W, H )

    window_1.activateWindow()
    window_2.activateWindow()
    window_3.activateWindow()
    window_4.activateWindow()

#split_both( editory, editor1 )
#split_four( editor1, editory, editorx, editorz )
#split_left( editory )
#split_right( editory )
