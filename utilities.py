def swap_attrs(obj1, obj2, attr_names):
    tmp = {}
    
    for name in attr_names:
        tmp[name] = getattr(obj1, name)
        setattr(obj1, name, getattr(obj2, name)) 
        setattr(obj2, name, tmp[name])

def copy_attrs(src_obj, dest_obj, attr_names):
    for name in attr_names:
        setattr(dest_obj, name, getattr(src_obj, name)) 

def convert(input_str):
    output = []
    for i in input_str :
        if i.isnumeric() :
            for j in range(int(i)): 
                output.append(0)
        else :
            output.append(i)
    return output