import json
import dicttoxml

def obj_to_xml(obj_dict):
    #get region attributes dictionary
    #Now, just get name of the object
    #so, here is the example region we are getting: 
    #
    #{"shape_attributes":
    #   {"name":"rect",
    #    "x":323,
    #    "y":172,
    #    "width":35,
    #    "height":45},
    # "region_attributes":
    #    {"type":
    #       {"full":true}
    #    }
    # 
    # }
    try:
        xml_st = '<object>'
        xml_st += '<name>'
        print(list(obj_dict['region_attributes']['type'].keys())[0])
        xml_st += list(obj_dict['region_attributes']['type'].keys())[0]
        xml_st += '</name>'
        #random stuff I don't know purpose for
        xml_st += '<pose>Left</pose> \
                  <truncated>0</truncated> \
                  <difficult>0</difficult>'
        ###Add the coordinates###
        xml_st += '<bndbox>'
        ###Getting xmin, ymin, xmax and ymax####
        ##xmax: x + width, xmin: x
        ##same for y
        xml_st += '<xmin>'
        xml_st += str(obj_dict['shape_attributes']['x'])
        xml_st += '</xmin>'
        xml_st += '<ymin>'
        xml_st += str(obj_dict['shape_attributes']['y'])
        xml_st += '</ymin>'
        xml_st += '<xmax>'
        xml_st += str(obj_dict['shape_attributes']['x'] + obj_dict['shape_attributes']['width'])
        xml_st += '</xmax>'
        xml_st += '<ymax>'
        xml_st += str(obj_dict['shape_attributes']['y'] + obj_dict['shape_attributes']['height'])
        xml_st += '</ymax>'
        xml_st += '</bndbox>'
        xml_st += '</object>'
        return xml_st
    except:
        return None


def convert_file(folder, im_dict):
    file_name = folder + '_' + im_dict['filename'][:-3] + 'xml'
    file_path = os.path.join(os.path.abspath(folder), file_name)
    xml_str = '<annotation>'
    xml_str += '<folder>'
    xml_str += folder
    xml_str += '</folder>'
    xml_str += '<filename>'
    xml_str += file_name
    xml_str += '</filename>'
    ##Add size: 
    xml_str += '<size>\
                <width> 1280 </width>\
                <height> 720 </height>\
                <depth> 1 </depth>\
                </size>'
    #Random extra args
    xml_str += '<segmented>0</segmented>'
    #So now, iterate through the regions attribute and keep adding 
    #the objects found
    regs = im_dict['regions']
    for reg in regs:
        obj_xml = obj_to_xml(reg)
        if obj_xml is not None:
            xml_str += obj_xml
    #So, starting string with annotation: 
    #get dictionary of file
    xml_str += '</annotation>'
    
    #Save the file to the directory
    x_fi = open(file_path, 'w')
    x_fi.write(xml_str)
    x_fi.close()



if __name__ == '__main__':
    import os
    json_file_name = "CAT_601_extracted_Final.json"
    folder_name = "CAT_601"
    f = open(json_file_name, 'r')
    fd = json.load(f)
    f.close()
    for imgs in fd:
        print(imgs)
        convert_file(folder_name, fd[imgs])
    
    