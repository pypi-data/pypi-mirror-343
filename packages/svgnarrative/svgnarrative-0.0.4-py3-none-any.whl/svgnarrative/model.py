from bs4 import BeautifulSoup
from copy import copy

def set_style_attr (e, key, value):
    if not 'style' in e.attrs: e.attrs['style'] = ''
    
    # read
    style = e.attrs['style'].split(';')
    props = {}
    for i in range(len(style)):
        elements = style[i].split(':')
        if len(elements)!=2: continue
        props[elements[0]] = elements[1]
    
    # modify
    if value==None:
        if key in props: del props[key]
    else:
        props[key] = value
    
    # write
    e.attrs['style'] = ';'.join(map(lambda k: '%s:%s'%(k, props[k]), props.keys()))

def set_attr (e, key, value):
    e.attrs[key] = value

def get_attr (e, key):
    return e.attrs[key]

def set_stroke_color (e, color):
    if e.name=='g':
        for child in e.children:
            if child!=None:
                set_stroke_color(child, color)
    elif e.name in ['path', 'rect', 'text', 'ellipse']:
        set_style_attr(e, 'stroke', color)
    else:
        print('Warning: Don\'t know how to set stroke color for tag type "%s"' % e.name)

def set_stroke_miterlimit (e, miterlimit):
    if e.name=='g':
        for child in e.children:
            if child!=None:
                set_stroke_miterlimit(child, miterlimit)
    elif e.name in ['path', 'rect', 'text', 'ellipse']:
        set_style_attr(e, 'stroke-miterlimit', miterlimit)
    else:
        print('Warning: Don\'t know how to set stroke miterlimit for tag type "%s"' % e.name)

def set_stroke_dasharray (e, dasharray):
    if e.name=='g':
        for child in e.children:
            if child!=None:
                set_stroke_dasharray(child, dasharray)
    elif e.name in ['path', 'rect', 'text', 'ellipse']:
        set_style_attr(e, 'stroke-dasharray', ', '.join(map(lambda e: str(e), dasharray)))
    else:
        print('Warning: Don\'t know how to set stroke dasharray for tag type "%s"' % e.name)

def set_stroke_dashoffset (e, dashoffset):
    if e.name=='g':
        for child in e.children:
            if child!=None:
                set_stroke_dashoffset(child, dashoffset)
    elif e.name in ['path', 'rect', 'text', 'ellipse']:
        set_style_attr(e, 'stroke-dashoffset', str(dashoffset))
    else:
        print('Warning: Don\'t know how to set stroke dashoffset for tag type "%s"' % e.name)

def set_start_marker (e, marker):
    set_style_attr(e, 'marker-start', marker)

def set_end_marker (e, marker):
    set_style_attr(e, 'marker-end', marker)

def set_fill_color (e, color):
    set_style_attr(e, 'fill', color)

def set_fill_opacity (e, opacity):
    set_style_attr(e, 'fill-opacity', opacity)

def set_display (e, display):
    set_style_attr(e, 'display', display)

def highlight (e, color):
    if e.name=='path':
        set_stroke_color(e, color)
    elif e.name=='rect':
        set_stroke_color(e, color)
    elif e.name=='ellipse':
        set_stroke_color(e, color)
    elif e.name=='text':
        set_fill_color(e, color)
    elif e.name=='g':
        for child in e.children:
            highlight(child, color)
    else:
        print('Error: Don\'t know how to highlight "%s". Skipping ...' % e.name)

class Model:
    def __init__ (self, filename: str):
        self.filename = filename
        with open(filename) as fo:
            self.root = BeautifulSoup(''.join(fo.readlines()), features = 'xml')
    
    def store (self, filename):
        lines = [str(self.root)]
        with open(filename, 'w') as fo:
            fo.writelines(lines)
    
    def hide (self, ids):
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            set_display(e, 'none')
    
    def show (self, ids):
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            set_display(e, 'display')
    
    def set_text (self, identifier, text):
        e = self.root.find(id=identifier)
        if e==None:
            print('Error: Unable to look up tag for id "%s" in set_text' % identifier)
            return
        e.string.replace_with(text)
    
    def set_attr (self, ids, key, value):
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            if e==None:
                print('Error: Unable to look up tag for id "%s" in set_attr' % identifier)
                return
            set_attr(e, key, value)
    
    def get_attr (self, identifier, key):
        e = self.root.find(id=identifier)
        if e==None:
            print('Error: Unable to look up tag for id "%s" in get_attr' % identifier)
            return
        return get_attr(e, key)
    
    def check_ids (self, idmap, silent=False):
        result = True
        
        for key in idmap:
            values = idmap[key]
            if type(values)!=list:
                values = [values]
            for value in values:
                e = self.root.find(id=value)
                if not silent: print('Value "%s" of key "%s"%s found'%(value, key, " not" if e==None else ""))
                if e==None: result = False
        
        return result
    
    def fill (self, ids, color):
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            set_fill_color(e, color)
    
    def fill_opacity (self, ids, opacity):
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            set_fill_opacity(e, opacity)
    
    # TODO: Note that support for defaults is not implemented for preserve=False
    def stroke (self, ids, color, miterlimit=None, dasharray=None, dashoffset=None, preserve=True):
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            set_stroke_color(e, color)
            if miterlimit!=None or not preserve:
              set_stroke_miterlimit(e, miterlimit)
            if dasharray!=None or not preserve:
              set_stroke_dasharray(e, dasharray)
            if dashoffset!=None or not preserve:
              set_stroke_dashoffset(e, dashoffset)
              
    
    def highlight (self, ids, highlight_color):
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            if e==None:
                print('Error: Unable to look up identifier "%s"' % identifier)
                return
            highlight(e, highlight_color)
    
    def lowlight (self, ids):
        pass
    
    def set_start_marker (self, ids, marker):
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            if e==None:
                print('Error: Unable to look up identifier "%s"' % identifier)
                return
            set_start_marker(e, marker)
    
    def set_end_marker (self, ids, marker):
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            if e==None:
                print('Error: Unable to look up identifier "%s"' % identifier)
                return
            set_end_marker(e, marker)
    
    def set_xlink_href (self, ids, value):
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            if e==None:
                print('Error: Unable to look up identifier "%s"' % identifier)
                return
            set_attr(e, 'xlink:href', value)
    
    def insert (self, model, prefix, x, y, scale=1.0):
        # clone model
        c = copy(model.root)
        
        # prefix all ids in clone
        for tag in c.select('[id]'):
            tag['id'] = prefix + tag['id']
        
        # insert group tag
        g = self.root.new_tag('g', transform='translate(%s %s) scale(%s %s)'%(str(x), str(y), str(scale), str(scale)))
        self.root.svg.append(g)
        
        # insert tags
        for child in c.svg.children:
            if child.name in ['g', 'path']:
                g.append(child)

if __name__ == "__main__":
    ids = {
        'tickbox1': 'path819',
        'tickbox2': 'path819-3',
        'tickbox3': 'path819-6',
        'tickbox2text': 'tspan846',
        'tickbox2text': 'text848',
        'tickbox3text': 'tspan850',
        'box': 'path817',
        'boxtext': 'flowPara860',
    }
    
    t = Model("../var/thing.svg")
    
    m = Model("../var/test1.svg")
    m.check_ids(ids)
    m.hide(ids['tickbox1'])
    m.store("test1.svg")
    m.show([ids['tickbox1']])
    m.store("test2.svg")
    m.set_text(ids['tickbox2text'], "Red")
    m.set_text(ids['boxtext'], "Once upon a time in a land far far away ...")
    m.store("test3.svg")
    
    for i in range(3):
        m.insert(t, 'thing%d_' % i, 10*i, 15*i)
    m.store("test4.svg")
