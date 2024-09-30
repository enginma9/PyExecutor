import feedparser
from Tree import *
from Helpers import heading

if __name__ == "__main__":
    from os import getcwd

def test_w_feed( url ):
    feed = feedparser.parse( url )
    #print( get_tree_diagram( feed, url ) )
    for line in get_tree_diagram( feed, url ).split("\n"):
       print( line )
    return feed


if __name__ == "__main__":
    print( __file__ )
    print( getcwd() )
    feed = test_w_feed( "https://www.englishclub.com/ref/idiom-of-the-day.xml" )
    print( type( feed['entries' ][0][ 'title' ] ) )
    heading( "Globals", 50 )
    print( get_tree_diagram( globals(), "Globals" ) )

    #print( type( globals() ) )