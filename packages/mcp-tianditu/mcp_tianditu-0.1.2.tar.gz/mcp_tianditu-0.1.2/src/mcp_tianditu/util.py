import xml.etree.ElementTree as ET

def xml_to_dict(xml_string):
    """更简洁的标准库实现，将XML转换为字典"""
    
    def _process_element(element):
        result = {}
        
        # 添加属性
        if element.attrib:
            result.update(element.attrib)
            
        # 处理子元素或文本
        children = list(element)
        if not children:
            text = element.text
            if text and text.strip():
                if not result:  # 如果没有属性，直接返回文本
                    return text.strip()
                result['text'] = text.strip()
            return result
            
        # 处理子元素
        for child in children:
            tag = child.tag
            child_data = _process_element(child)
            
            if tag in result:
                if not isinstance(result[tag], list):
                    result[tag] = [result[tag]]
                result[tag].append(child_data)
            else:
                result[tag] = child_data
                
        return result
    
    root = ET.fromstring(xml_string)
    return {root.tag: _process_element(root)}