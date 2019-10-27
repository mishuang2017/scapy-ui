from scapy.all import *
from flexx import flx

class FieldDesc():
    placeholder=None
    autocomp=None
    def __init__(self, title, type=str, autocomp=None, placeholder=None):
        self.title = title
        self.type = type
        self.autocomp = autocomp
        self.palceholder = placeholder

class PortDesc(FieldDesc):
    def __init__(self, title):
        super().__init__(title, int)
        self.autocomp = ("1","22","80", "8080","[1,4] #2", "(1,4) #4", "range(1,4) #3", "[(1,4),5,6] #5")
    
class ScapyTextField(flx.PyWidget):
    pkt = None
    def init(self, parent, name, flex=1):
        self._parent = parent
        self.name = name
        self.desc = parent.descs[name]
        with parent._cont:
            self.w = flx.LineEdit(flex=flex, title=self.desc.title)
        self._parent.fields.append(self)
        if self.desc.placeholder:
            self.w.set_placeholder_text(self.desc.placeholder)
        if self.desc.autocomp:
            self.w.set_autocomp(self.desc.autocomp)
    
    @flx.action
    def load_pkt(self, pkt):
        self.pkt = pkt
        v = pkt.fields.get(self.name,None)
        if type(v) == Net:
            v = v.repr
        elif type(v) == int:
            v = str(v)
        elif v == None:
            v = ""
        elif type(v) == str:
            pass
        else:
            v = repr(v)
        self.w.set_text(v)
        
    @flx.reaction('w.user_text')
    def update_pkt(self, *events):
        if not self.pkt:
            return
        text = events[-1]['new_value'].strip()
        try:
            if len(text):
                if self.desc.type != str:
                    text = eval(text)
                self._parent.pkt.setfieldval(self.name, text)
            else:
                self._parent.pkt.fields.pop(self.name, None)
            self._parent.on_update()
        except Exception as e:
            self.root.set_status(str(e))
        else:
            self.root.set_status("")
    