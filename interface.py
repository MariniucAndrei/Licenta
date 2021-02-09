import wx
import FakeNews

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title = "Fake News", size = (1500,800))

        self.panel = MyPanel(self)

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL)

        self.label1 = wx.StaticText(self, label = "Which is the field of the news?", pos = (50,30), size = (1000,30))

        fields = ['politics','sport','medicine','economic','lifestyle']
        self.choice = wx.Choice(self, choices = fields, pos = (50, 60), size = (500, 30))

        self.label2 = wx.StaticText(self, label = "What do you think about this news?", pos = (50, 90), size = (1000,30))

        label = ['FAKE', 'REAL']
        self.choice1 = wx.Choice(self, choices = label, pos = (50,120), size =(500,30))

        self.label3 = wx.StaticText(self, label = "", pos = (50, 180), size = (1000,50))
        self.label3.SetFont(font)

        self.labelRez = wx.StaticText(self, label = "", pos = (300, 700), size = (1000,50))
        self.labelRez.SetFont(font)

        self.choice1.Bind(wx.EVT_CHOICE, self.OnChoice)

        self.label4 = wx.StaticText(self, label = "Insert news title here:", pos = (50, 230), size = (1000,50))
        self.text_ctrlTitle = wx.TextCtrl(self, pos=(50, 280), size = (1000,30), style = wx.TE_MULTILINE)

        self.label5 = wx.StaticText(self, label = "Insert news text here:", pos = (50, 330), size = (1000,50))
        self.text_ctrlText = wx.TextCtrl(self, pos=(50, 380), size = (1000,300), style = wx.TE_MULTILINE)

        my_btn = wx.Button(self, label='Check news', pos=(50, 700), size = (100,50))
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)

    def OnChoice(self, event):
        self.label3.SetLabel("You think that the news from " + self.choice.GetString(self.choice.GetSelection()) + 
        " is " + self.choice1.GetString(self.choice1.GetSelection()) + "!")

    def on_press(self, event):
        with open("news.csv", "a") as outputfile:
            outputfile.write("\n 13123," + str(self.text_ctrlTitle.GetValue()) + "," + str(self.text_ctrlText.GetValue()).replace(",", "") +
             "," + str(self.choice1.GetString(self.choice1.GetSelection())))
        res = FakeNews.func("13123," + str(self.text_ctrlTitle.GetValue()) + "," + str(self.text_ctrlText.GetValue()).replace(",", "") +
         "," + str(self.choice1.GetString(self.choice1.GetSelection())))
        if str(res) == "['FAKE']":
            self.labelRez.SetLabel("This news is FAKE!")
        else:
            self.labelRez.SetLabel("This news is REAL!")

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent=None, title="Fake News")
        self.frame.Show()
        return True

app = MyApp()
app.MainLoop()