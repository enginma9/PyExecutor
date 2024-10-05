

# Define pieces of the tree structure
submarker           = "│ "
final_space         = "─ "
final_w_sub_list    = "┬ "
sub_list_mid        = "├─"
sub_list_end        = "└─"
subm_no_more_items  = "  "
dot                 = ". "
    
# If an item in list is an empty dict "{}" then it will show a dead branch.  This is expected.  
def build_tree( subtree, passed_string, item_num, text, is_last=False ):
    own_str = str( passed_string )
    pass_str = str( passed_string )
    
    if is_last:
        own_str += sub_list_end # "└─"
        pass_str += subm_no_more_items # "  "
    else:
        own_str += sub_list_mid # "├─"
        pass_str += submarker # "| "
    
    # decide list or dict or neither
    if isinstance( subtree, list ): #if subitems
        own_str += final_w_sub_list + str( item_num ) + dot + text + "\n"# finish out here
        for i, item in enumerate( subtree ):
            if i == len( subtree ) - 1 : # if last
                pass_is_last = True
            else:
                pass_is_last = False
            pass_name = "[" + str( i ) + "]" 
            try:
                own_str += build_tree( item, pass_str, i+1, pass_name, pass_is_last ) 
            except:
                pass
    elif isinstance( subtree, dict ):
        #need code here
        own_str += final_w_sub_list + str( item_num ) + dot + text + "\n"
        for i, (key,value) in enumerate( subtree.items() ):
            if i == len( subtree ) - 1 : # if last
                pass_is_last = True
            else:
                pass_is_last = False
            pass_name = key
            if isinstance( value, str ):
                pass_name += " : \"" + value[:20] + " \""
            try:
                own_str += build_tree( value, pass_str, i+1, pass_name, pass_is_last ) 
            except:
                pass
    else:
        own_str += final_space + str( item_num ) + dot + text + "\n"
    return own_str

def get_tree_diagram(nested_list_or_dict, title):
    return_string = title + "\n" 
    if isinstance( nested_list_or_dict, list ): 
        for i, item in enumerate( nested_list_or_dict ):
            if i == len( nested_list_or_dict ) - 1: # if last
                pass_is_last = True
            else:
                pass_is_last = False
            pass_name = "[" + str(i) + "]"
            return_string += build_tree( item, "", i+1, pass_name, pass_is_last  )
    if isinstance( nested_list_or_dict, dict ):
        #need code here
        for i, ( key, value ) in enumerate( nested_list_or_dict.items() ):
            if i == len( nested_list_or_dict ) - 1: # if last
                pass_is_last = True
            else:
                pass_is_last = False
            return_string += build_tree( value, "", i+1, key, pass_is_last  )
    return return_string

def print_tree_diagram(nested_list_or_dict, title):
    print( get_tree_diagram(nested_list_or_dict, title) )

if __name__ == "__main__":
    # Test the function
    nested_structure = {
        "First Section": [
            "Task 1",
            "Task 2",
            ["Subtask 2.1", "Subtask 2.2", "Task 3"],
        ],
        "Second Section": ["Task 4", "Task 5"]
    }

    nest_list = [ [ [ 1, 2 ], [ 1, 2 ] ], [ [ 1, 2 ], [ 1, 2 ] ] ]

    print( get_tree_diagram( nest_list, "Testing" ) )
    print( get_tree_diagram( nested_structure, "Testing" ) )