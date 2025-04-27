import customtkinter as ctk

class CTk7SegmentDisplay(ctk.CTkFrame):
    def __init__(self,master=None,**kwargs):
        self.bgColor=kwargs.pop("fg_color","#000000")
        self.segmentColor=kwargs.pop("text_color","#ff0000")
        self.disabledColor=kwargs.pop("text_color_disabled","#101010")
        self.thickness=kwargs.pop("thickness",15)
        self.segDistance=kwargs.pop("segment_distance",5)
        self.width=kwargs.pop("width",100)
        self.height=kwargs.pop("height",200)
        super().__init__(master,**kwargs)
        self.canvas=ctk.CTkCanvas(self,width=self.width,height=self.height,bg=self.bgColor,highlightthickness=0)
        self.canvas.pack(fill="both",expand=True)
        def createPolygon(*args,**kw):
            positions=[]
            for i in range(0,len(args),2):
                xperc=args[i]/100
                yperc=args[i+1]/200
                positions.extend((xperc*self.width,yperc*self.height))
            polygon=self.canvas.create_polygon(*positions,**kw)
            return polygon
        t=self.thickness
        d=self.segDistance
        self.segments={
            "0":createPolygon(d, 0, (100-d), 0, (100-d-t), t, (d+t), t,outline=""),
            "1":createPolygon(0, d, 0, (100-d), t, (100-d-t), t, (d+t),outline=""),
            "2":createPolygon(100, d, 100, (100-d), (100-t), (100-d-t), (100-t), (d+t),outline=""),
            "3":createPolygon(d, 100, (d+t/2), (100-t/2), (100-d-t/2), (100-t/2), (100-d), 100, (100-d-t/2), (100+t/2), (d+t/2), (100+t/2),outline=""),
            "4":createPolygon(0, (100+d), 0, (200-d), t, (200-d-t), t, (100+d+t), outline=""),
            "5":createPolygon(100, (100+d), 100, (200-d), (100-t), (200-d-t), (100-t), (100+d+t),outline=""),
            "6":createPolygon(d, 200, (100-d), 200, (100-d-t), (200-t), (d+t), (200-t),outline=""),
        }
        self.segmentMap={
            "":"",
            " ":"",
            "0":"012456",
            "1":"25",
            "2":"02346",
            "3":"02356",
            "4":"1235",
            "5":"01356",
            "6":"013456",
            "7":"025",
            "8":"0123456",
            "9":"012356",
            "A":"012345",
            "B":"0123456",
            "C":"0146",
            "D":"012456",
            "E":"01346",
            "F":"0134",
            "G":"013456",
            "H":"12345",
            "I":"14",
            "J":"2456",
            "K":"12345",
            "L":"146",
            "M":"01245",
            "N":"12345",
            "O":"012456",
            "P":"01234",
            "Q":"01235",
            "R":"012345",
            "S":"01356",
            "T":"014",
            "U":"12456",
            "V":"12456",
            "W":"123456",
            "X":"12345",
            "Y":"12356",
            "Z":"02346",
            "a":"023456",
            "b":"13456",
            "c":"346",
            "d":"23456",
            "e":"012346",
            "f":"0134",
            "g":"012356",
            "h":"1345",
            "i":"4",
            "j":"2456",
            "k":"12345",
            "l":"14",
            "m":"01245",
            "n":"345",
            "o":"3456",
            "p":"01234",
            "q":"01235",
            "r":"34",
            "s":"01356",
            "t":"1346",
            "u":"456",
            "v":"456",
            "w":"123456",
            "x":"12345",
            "y":"12356",
            "z":"02346",
            "-":"3",
            "_":"6",
            "(":"0146",
            ")":"0256",
            "[":"0146",
            "]":"0256",
            "{":"0146",
            "}":"0256",
            "=":"36",
            "\\":"135",
            "/":"234",
            "<":"1456",
            ">":"2456",
        }
        self.setNumber("")
    def getState(self,segment): return self.canvas.itemcget(segment,"fill")==self.segmentColor
    def setState(self,segment,state): self.canvas.itemconfig(segment,fill=self.segmentColor if state else self.disabledColor)
    def getFullState(self): return "".join(s for s in self.segments if self.getState(self.segments[s]))
    def setFullState(self,state):
        for s in self.segments: self.setState(self.segments[s],s in state)
    def setNumber(self,number):
        if number in self.segmentMap:
            for segment in self.segments:
                if segment in self.segmentMap[number]:
                    if self.getState(self.segments[segment])==False: self.setState(self.segments[segment],True)
                else:
                    self.setState(self.segments[segment],False)
    def configure(self,**kwargs):
        self.bgColor=kwargs.pop("fg_color",self.bgColor)
        self.segmentColor2=kwargs.pop("text_color",self.segmentColor)
        self.disabledColor2=kwargs.pop("text_color_disabled",self.disabledColor)
        self.thickness=kwargs.pop("thickness",self.thickness)
        self.segDistance=kwargs.pop("segment_distance",self.segDistance)
        self.width=kwargs.pop("width",self.width)
        self.height=kwargs.pop("height",self.height)
        super().configure(**kwargs)
        self.canvas.configure(width=self.width,height=self.height,bg=self.bgColor,highlightthickness=0)
        if self.segmentColor!=self.segmentColor2:
            self.segmentColor=self.segmentColor2
            state=self.getFullState()
            self.setFullState(state)
        elif self.disabledColor!=self.disabledColor2:
            self.disabledColor=self.disabledColor2
            state=self.getFullState()
            self.setFullState(state)

class CTkBlinkingColon(ctk.CTkFrame):
    def __init__(self,master=None,**kwargs):
        self.bgColor=kwargs.pop("fg_color","#000000")
        self.segmentColor=kwargs.pop("text_color","#ff0000")
        self.disabledColor=kwargs.pop("text_color_disabled","#101010")
        super().__init__(master,**kwargs)
        self.width=self.cget("width")
        self.height=self.cget("height")
        self.canvas=ctk.CTkCanvas(self,width=self.width,height=self.height,bg=self.bgColor,highlightthickness=0)
        self.canvas.pack(fill="both",expand=True)
        def createPolygon(*args,**kw):
            positions=[]
            for i in range(0,len(args),2):
                xperc=args[i]/20
                yperc=args[i+1]/200
                positions.extend((xperc*self.width,yperc*self.height))
            polygon=self.canvas.create_polygon(*positions,**kw)
            return polygon
        self.segments={
            "0":createPolygon(0,70,20,70,20,90,0,90,outline=""),
            "1":createPolygon(0,110,20,110,20,130,0,130,outline=""),
        }
        self.setState(False)
    def getState(self): return self.canvas.itemcget(self.segments["0"],"fill")==self.segmentColor
    def setState(self,state):
        for segment in self.segments: self.canvas.itemconfig(self.segments[segment],fill=self.segmentColor if state else self.disabledColor)
    def configure(self,**kwargs):
        self.bgColor=kwargs.pop("fg_color",self.bgColor)
        self.segmentColor2=kwargs.pop("text_color",self.segmentColor)
        self.disabledColor2=kwargs.pop("text_color_disabled",self.disabledColor)
        super().configure(**kwargs)
        self.width=self.cget("width")
        self.height=self.cget("height")
        self.canvas.configure(width=self.width,height=self.height,bg=self.bgColor,highlightthickness=0)
        if self.segmentColor!=self.segmentColor2:
            self.segmentColor=self.segmentColor2
            state=self.getState()
            self.setState(state)
        elif self.disabledColor!=self.disabledColor2:
            self.disabledColor=self.disabledColor2
            state=self.getState()
            self.setState(state)
