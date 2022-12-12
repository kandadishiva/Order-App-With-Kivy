from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
import socket
import threading
import time
try:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((socket.gethostname(),1024))
except:
    print("Error due to inactive server")

Window.size = (360,600)

class WindowManager(ScreenManager,MDApp):
    Error = None
    def set_screen(self,root):
        root.current = "Home"
        root.transition.direction = "right"

    def set_seller_homepage(self,root):
        root.current="Seller Homepage"
        root.transition.direction = "right"

    def return_sellerHomePage(self,root):
        root.current="Seller Homepage"
        root.transition.direction="right"

    def closeDialog(self,inst):
        self.Error.dismiss()

    def side(self,root,a):
        if(a==1):
            msg=" CustomerSide "
        else:
            msg=" SellerSide "
        print(msg)
        try:
            s.send(bytes(msg,"ascii"))
            if(a==1):
                root.current = "CustomerPage"
            else:
                root.current = "SellerLoginPage"
        except:
            print("Server is not active")
        pass

    def CustomerSignIn(self,root):
        username = root.ids.user.text
        password = root.ids.pwd.text
        OrderedCardNames=["root.ids.OrderedCanteen1","root.ids.OrderedCanteen2","root.ids.OrderedCanteen3","root.ids.OrderedCanteen4","root.ids.OrderedCanteen5"]
        UserError=None
        PasswordError=None
        if(username.isdecimal() == False):
            self.Error = MDDialog(text="Enter the Correct Username", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(len(password)==0):
            self.Error = MDDialog(text="Enter the Password", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        else:
            try:
                Newid=username
                username=" ExitUser "+username+" "
                s.send(bytes(username, "ascii"))
                result = s.recv(1024)
                check=result.decode("ascii")
                print(check)
                if(check=="ok"):
                    password = " Existpassword " + password + " " + username + " "
                    s.send(bytes(password, "ascii"))
                    result = s.recv(1024)
                    finall=result.decode("ascii")
                    print(finall)
                    if(finall=="ok"):
                        a=" SendInfo"+username
                        s.send(bytes(a,"ascii"))
                        info=s.recv(1024).decode("ascii")
                        info=info.split(" ")
                        print(info)
                        Name=info[3]
                        Name=list(Name)
                        for i in range(0,len(Name)):
                            if Name[i]=="-":
                                Name[i]=" "
                        Name="".join(Name)
                        root.ids.HomeUserName.text=Name

                        Detailes = " GettheOrdersDetailes " + "UserName " + Newid + " "
                        s.send(bytes(Detailes.encode('ascii')))
                        res = s.recv(1024).decode('ascii')
                        res=res.split("**")
                        print(res)
                        ans=res[2].split("//")
                        print(ans)
                        for i in range(1,len(ans)):
                            sol=ans[i].split("&&")
                            print(sol)
                            if i==1:
                                root.ids.OrderedCanteenName1.text="[b]"+sol[6]+"[/b]"
                                root.ids.OrderedCollegeName1.text=sol[4]
                                root.ids.OrderedCanteenAddress1.text=sol[8]
                                root.ids.OrderedOrderNo1.text = "[b]Order No : "+sol[10]+"[/b]"
                                root.ids.OrderedCanteenName1.hint_text =sol[10]
                            elif i==2:
                                root.ids.OrderedCanteenName2.text="[b]"+sol[6]+"[/b]"
                                root.ids.OrderedCollegeName2.text=sol[4]
                                root.ids.OrderedCanteenAddress2.text=sol[8]
                                root.ids.OrderedOrderNo2.text = "[b]Order No : "+sol[10]+"[/b]"
                                root.ids.OrderedCanteenName2.hint_text = sol[10]
                            elif i==3:
                                root.ids.OrderedCanteenName3.text="[b]"+sol[6]+"[/b]"
                                root.ids.OrderedCollegeName3.text=sol[4]
                                root.ids.OrderedCanteenAddress3.text=sol[8]
                                root.ids.OrderedOrderNo3.text = "[b]Order No : "+sol[10]+"[/b]"
                                root.ids.OrderedCanteenName3.hint_text = sol[10]
                            elif i==4:
                                root.ids.OrderedCanteenName4.text="[b]"+sol[6]+"[/b]"
                                root.ids.OrderedCollegeName4.text=sol[4]
                                root.ids.OrderedCanteenAddress4.text=sol[8]
                                root.ids.OrderedOrderNo4.text = "[b]Order No : "+sol[10]+"[/b]"
                                root.ids.OrderedCanteenName4.hint_text = sol[10]
                            elif i==5:
                                root.ids.OrderedCanteenName5.text="[b]"+sol[6]+"[/b]"
                                root.ids.OrderedCollegeName5.text=sol[4]
                                root.ids.OrderedCanteenAddress5.text=sol[8]
                                root.ids.OrderedOrderNo5.text = "[b]Order No : "+sol[10]+"[/b]"
                                root.ids.OrderedCanteenName5.hint_text = sol[10]
                        for i in range(0,int(res[1])):
                            a = OrderedCardNames[i] + ".opacity"
                            b = OrderedCardNames[i] + ".disabled"

                            exec("%s = %d" % (a, 1))
                            exec("%s = False" % (b))
                        for i in range(int(res[1]), 5):
                            a = OrderedCardNames[i] + ".opacity"
                            b = OrderedCardNames[i] + ".disabled"

                            exec("%s = %d" % (a, 0))
                            exec("%s = True" % (b))
                        root.current="Home"
                    else:
                        self.Error = MDDialog(text="Enter the Correct Password", buttons=[
                            MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                         on_release=self.closeDialog)])
                        self.Error.open()
                else:
                    self.Error = MDDialog(text="Enter the Correct Username", buttons=[
                        MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                     on_release=self.closeDialog)])
                    self.Error.open()
            except:
                print("Server is not active")
        pass

    def NewUser(self,root):
        Newid=root.ids.NewNo.text
        if (Newid.isdecimal() == False):
            self.Error = MDDialog(text="Enter the Number", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        else:
            NewidNo=" NewUser "+Newid+" "
            s.send(bytes(NewidNo,"ascii"))
            result=s.recv(1024).decode("ascii")
            print(result)
            if(result=="ok"):
                root.ids.No.text = Newid
                root.current = "OTP"
            else:
                self.Error = MDDialog(text="Number Already Exists", buttons=[
                    MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                 on_release=self.closeDialog)])
                self.Error.open()
    pass

    def NewUserOtp(self,root):
        Newid=root.ids.No.text
        if(Newid.isdecimal()==False):
            self.Error = MDDialog(text="Enter the Number", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        else:
            NewidNo = " NewUser " + Newid + " "
            s.send(bytes(NewidNo, "ascii"))
            result = s.recv(1024).decode("ascii")
            print(result)
            if (result == "ok"):
                root.ids.Luser.text=Newid
                root.current = "CreatePassword"
            else:
                self.Error= MDDialog(text ="Number Already Exists",buttons=[
                    MDFlatButton(text="Ok",theme_text_color="Custom",text_color=self.theme_cls.primary_color,
                                 on_release=self.closeDialog)])
                self.Error.open()
        pass

    def NewPassword(self,root):
        Newuser=root.ids.Luser.text
        Password1=root.ids.Pass1.text
        Password2=root.ids.Pass2.text
        Special = "!@#$%^&*()/?<>"
        char="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
        num="1234567890"
        Spe="error"
        cha="error"
        nu="error"
        if(Newuser.isdecimal()==False):
            self.Error = MDDialog(text="Enter the correct username", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(Password1=="" or Password2==""):
            self.Error = MDDialog(text="Enter the Password", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(Password1!=Password2):
            self.Error = MDDialog(text="Password and conform should be same", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(len(Password1)<8):
            self.Error = MDDialog(text="Password should be greater than 8", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        else:
            for i in Password1:
                if i in Special:
                    Spe="ok"
                if i in char:
                    cha="ok"
                if i in num:
                    nu="ok"
            if(Spe=="ok" and cha=="ok" and nu=="ok"):
                NewidNo = " NewUser " + Newuser + " "
                s.send(bytes(NewidNo, "ascii"))
                result = s.recv(1024).decode("ascii")
                print(result)
                if (result == "ok"):
                    print("User ok")
                    UpdatePassword=" UpdatePassword "+Password1+" "+"UserName "+Newuser+" "
                    s.send(bytes(UpdatePassword,"ascii"))
                    res=s.recv(1024).decode("ascii")
                    if(res=="ok"):
                        root.current="Detailes"
                    else:
                        print("error")
                else:
                    print("No Already exists")
            else:
                self.Error = MDDialog(text="Enter the correct password", buttons=[
                    MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                 on_release=self.closeDialog)])
                self.Error.open()
        pass

    def DetailesPage(self,root,a=20):
        OrderedCardNames=["root.ids.OrderedCanteen1","root.ids.OrderedCanteen2","root.ids.OrderedCanteen3","root.ids.OrderedCanteen4","root.ids.OrderedCanteen5"]
        if a==1:
            Username=root.ids.Luser.text
            Name=root.ids.name.text
            Email=root.ids.email.text
            if(Name==""):
                self.Error = MDDialog(text="Enter the name", buttons=[
                    MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                 on_release=self.closeDialog)])
                self.Error.open()
            elif(Email==""):
                self.Error = MDDialog(text="enter the Email", buttons=[
                    MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                 on_release=self.closeDialog)])
                self.Error.open()
            else:
                Mname = list(Name)
                for i in range(0, len(Mname)):
                    if Mname[i] == " ":
                        Mname[i] = "-"
                Name = "".join(Mname)
                Detailes=" Detailes UserName "+Username+" Name "+Name+" Email "+Email+" "
                s.send(bytes(Detailes,"ascii"))
                result = s.recv(1024).decode("ascii")
                a=20
        if a==20:
            UserId = root.ids.Luser.text
            UserId1 = root.ids.user.text
            if (UserId1 != ""):
                Newid = UserId1
            else:
                Newid = UserId
            a = " SendInfo ExitUser " + Newid+" "
            s.send(bytes(a, "ascii"))
            info = s.recv(1024).decode("ascii")
            info = info.split(" ")
            print(info)
            Name = info[3]
            Name = list(Name)
            for i in range(0, len(Name)):
                if Name[i] == "-":
                    Name[i] = " "
            Name = "".join(Name)
            root.ids.HomeUserName.text = Name

            Detailes = " GettheOrdersDetailes " + "UserName " + Newid + " "
            s.send(bytes(Detailes.encode('ascii')))
            res = s.recv(1024).decode('ascii')
            res = res.split("**")
            print(res)
            ans = res[2].split("//")
            print(ans)
            for i in range(1, len(ans)):
                sol = ans[i].split("&&")
                if i == 1:
                    root.ids.OrderedCanteenName1.text = "[b]" + sol[6] + "[/b]"
                    root.ids.OrderedCollegeName1.text = sol[4]
                    root.ids.OrderedCanteenAddress1.text = sol[8]
                    root.ids.OrderedOrderNo1.text = "[b]Order No : " + sol[10] + "[/b]"
                    root.ids.OrderedCanteenName1.hint_text = sol[10]
                elif i == 2:
                    root.ids.OrderedCanteenName2.text = "[b]" + sol[6] + "[/b]"
                    root.ids.OrderedCollegeName2.text = sol[4]
                    root.ids.OrderedCanteenAddress2.text = sol[8]
                    root.ids.OrderedOrderNo2.text = "[b]Order No : " + sol[10] + "[/b]"
                    root.ids.OrderedCanteenName2.hint_text = sol[10]
                elif i == 3:
                    root.ids.OrderedCanteenName3.text = "[b]" + sol[6] + "[/b]"
                    root.ids.OrderedCollegeName3.text = sol[4]
                    root.ids.OrderedCanteenAddress3.text = sol[8]
                    root.ids.OrderedOrderNo3.text = "[b]Order No : " + sol[10] + "[/b]"
                    root.ids.OrderedCanteenName3.hint_text = sol[10]
                elif i == 4:
                    root.ids.OrderedCanteenName4.text = "[b]" + sol[6] + "[/b]"
                    root.ids.OrderedCollegeName4.text = sol[4]
                    root.ids.OrderedCanteenAddress4.text = sol[8]
                    root.ids.OrderedOrderNo4.text = "[b]Order No : " + sol[10] + "[/b]"
                    root.ids.OrderedCanteenName4.hint_text = sol[10]
                elif i == 5:
                    root.ids.OrderedCanteenName5.text = "[b]" + sol[6] + "[/b]"
                    root.ids.OrderedCollegeName5.text = sol[4]
                    root.ids.OrderedCanteenAddress5.text = sol[8]
                    root.ids.OrderedOrderNo5.text = "[b]Order No : " + sol[10] + "[/b]"
                    root.ids.OrderedCanteenName5.hint_text = sol[10]
            for i in range(0, int(res[1])):
                a = OrderedCardNames[i] + ".opacity"
                b = OrderedCardNames[i] + ".disabled"

                exec("%s = %d" % (a, 1))
                exec("%s = False" % (b))
            for i in range(int(res[1]),5):
                a = OrderedCardNames[i] + ".opacity"
                b = OrderedCardNames[i] + ".disabled"

                exec("%s = %d" % (a, 0))
                exec("%s = True" % (b))
            root.current="Home"

        pass

    def logout(self,root):
        root.ids.Luser.text=""
        root.ids.No.text=""
        root.ids.NewNo.text=""
        root.ids.user.text=""
        root.ids.Pass1.text=""
        root.ids.Pass2.text=""
        root.ids.name.text=""
        root.ids.email.text=""
        root.ids.pwd.text=""
        root.current="CustomerPage"

        pass
    def SellerLoginin(self,root):
        Username = root.ids.SellerUser.text
        SPassword=root.ids.SellerPwd.text
        cardslist=["root.ids.CustomerOrder1","root.ids.CustomerOrder2","root.ids.CustomerOrder3","root.ids.CustomerOrder4","root.ids.CustomerOrder5","root.ids.CustomerOrder6","root.ids.CustomerOrder7","root.ids.CustomerOrder8","root.ids.CustomerOrder9","root.ids.CustomerOrder10"]
        if(Username==""):
            self.Error = MDDialog(text="enter the Phone No", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(SPassword==""):
            self.Error = MDDialog(text="enter the Password", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(len(Username)!=10 or Username.isdecimal()==False):
            self.Error = MDDialog(text="enter the Correct Phone No", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        else:
            check=" NewSeller "+Username+" "
            s.send(bytes(check,"ascii"))
            result=s.recv(1024).decode("ascii")
            print(result)
            if(result=="Number Exists"):
                PasswordCheck=" CheckSellerPassword "+SPassword+" Username "+Username+" "
                s.send(bytes(PasswordCheck,"ascii"))
                result=s.recv(1024).decode("ascii")
                print(result)
                if(result=="ok"):
                    Detailes=" GetTheSellerOrdersList "+"Phno "+Username+" "
                    s.send(bytes(Detailes.encode('ascii')))
                    res=s.recv(1024).decode('ascii')
                    res=res.split("//")
                    print(res)

                    for i in range(1,len(res)):
                        ans=res[i].split("&&")
                        if ans[5] == "Ordered":
                            progress = 5
                        elif ans[5] == "Accepted":
                            progress = 25
                        elif ans[5] == "InKitchen":
                            progress = 50
                        elif ans[5] == "Ready":
                            progress = 75
                        elif ans[5] == "Delivered":
                            progress = 100
                        if i==1:
                            root.ids.SellerOrderStatus1.text=ans[5]
                            root.ids.SellerOrderStatusValue1.value=progress
                            root.ids.SellerOrderNo1.text="[b]Order No : "+ans[1]+"[/b]"
                            root.ids.SellerNoofItemsAndCost1.text=ans[7]+" Items Ordered               Total cost : "+ans[3]
                        elif i==2:
                            root.ids.SellerOrderStatus2.text = ans[5]
                            root.ids.SellerOrderStatusValue2.value = progress
                            root.ids.SellerOrderNo2.text = "[b]Order No : " + ans[1] + "[/b]"
                            root.ids.SellerNoofItemsAndCost2.text = ans[7] + " Items Ordered               Total cost : " + ans[3]
                        elif i==3:
                            root.ids.SellerOrderStatus3.text = ans[5]
                            root.ids.SellerOrderStatusValue3.value = progress
                            root.ids.SellerOrderNo3.text = "[b]Order No : " + ans[1] + "[/b]"
                            root.ids.SellerNoofItemsAndCost3.text = ans[7] + " Items Ordered               Total cost : " + ans[3]
                        elif i==4:
                            root.ids.SellerOrderStatus4.text = ans[5]
                            root.ids.SellerOrderStatusValue4.value = progress
                            root.ids.SellerOrderNo4.text = "[b]Order No : " + ans[1] + "[/b]"
                            root.ids.SellerNoofItemsAndCost4.text = ans[7] + " Items Ordered               Total cost : " + ans[3]
                        elif i==5:
                            root.ids.SellerOrderStatus5.text = ans[5]
                            root.ids.SellerOrderStatusValue5.value = progress
                            root.ids.SellerOrderNo5.text = "[b]Order No : " + ans[1] + "[/b]"
                            root.ids.SellerNoofItemsAndCost5.text = ans[7] + " Items Ordered               Total cost : " + ans[3]
                        elif i==6:
                            root.ids.SellerOrderStatus6.text = ans[5]
                            root.ids.SellerOrderStatusValue6.value = progress
                            root.ids.SellerOrderNo6.text = "[b]Order No : " + ans[1] + "[/b]"
                            root.ids.SellerNoofItemsAndCost6.text = ans[7] + " Items Ordered               Total cost : " + ans[3]
                        elif i==7:
                            root.ids.SellerOrderStatus7.text = ans[5]
                            root.ids.SellerOrderStatusValue7.value = progress
                            root.ids.SellerOrderNo7.text = "[b]Order No : " + ans[1] + "[/b]"
                            root.ids.SellerNoofItemsAndCost7.text = ans[7] + " Items Ordered               Total cost : " + ans[3]
                        elif i==8:
                            root.ids.SellerOrderStatus8.text = ans[5]
                            root.ids.SellerOrderStatusValue8.value = progress
                            root.ids.SellerOrderNo8.text = "[b]Order No : " + ans[1] + "[/b]"
                            root.ids.SellerNoofItemsAndCost8.text = ans[7] + " Items Ordered               Total cost : " + ans[3]
                        elif i==9:
                            root.ids.SellerOrderStatus9.text = ans[5]
                            root.ids.SellerOrderStatusValue9.value = progress
                            root.ids.SellerOrderNo9.text = "[b]Order No : " + ans[1] + "[/b]"
                            root.ids.SellerNoofItemsAndCost9.text = ans[7] + " Items Ordered               Total cost : " + ans[3]
                        elif i==10:
                            root.ids.SellerOrderStatus10.text = ans[5]
                            root.ids.SellerOrderStatusValue10.value = progress
                            root.ids.SellerOrderNo10.text = "[b]Order No : " + ans[1] + "[/b]"
                            root.ids.SellerNoofItemsAndCost10.text = ans[7] + " Items Ordered               Total cost : " + ans[3]

                    for i in range(0, len(res)-1):
                        a = cardslist[i] + ".opacity"
                        b = cardslist[i] + ".disabled"

                        exec("%s = %d" % (a, 1))
                        exec("%s = False" % (b))
                    for i in range(len(res)-1, 10):
                        a = cardslist[i] + ".opacity"
                        b = cardslist[i] + ".disabled"

                        exec("%s = %d" % (a, 0))
                        exec("%s = True" % (b))
                    root.current="Seller Homepage"
                else:
                    self.Error = MDDialog(text="enter the Correct Password", buttons=[
                        MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                     on_release=self.closeDialog)])
                    self.Error.open()
            else:
                self.Error = MDDialog(text="enter the Correct Phone No", buttons=[
                    MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                 on_release=self.closeDialog)])
                self.Error.open()
        print(Username)
        print(SPassword)
        pass
    def SellerSignIn(self,root):
        Newid=root.ids.NewSPh.text
        if(Newid.isdecimal()==False):
            self.Error = MDDialog(text="enter the Number", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(len(Newid)!=10):
            self.Error = MDDialog(text="enter the Correct Number", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        else:
            username = " NewUser " + Newid + " "
            s.send(bytes(username, "ascii"))
            result = s.recv(1024)
            check = result.decode("ascii")
            print(check)
            if(check=="ok"):
                username=" NewSeller "+ Newid +" "
                s.send(bytes(username,"ascii"))
                result=s.recv(1024).decode("ascii")
                print(result)
                if(result=="ok"):
                    root.ids.SOtpPh.text=Newid

                    root.current="SellerOTP"
                else:
                    self.Error = MDDialog(text="Number Already Exists", buttons=[
                        MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                     on_release=self.closeDialog)])
                    self.Error.open()
            else:
                self.Error = MDDialog(text="Number Already Exists", buttons=[
                    MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                 on_release=self.closeDialog)])
                self.Error.open()
        pass

    def SellerNewOtp(self,root):
        Newid=root.ids.SOtpPh.text
        if (Newid.isdecimal() == False):
            self.Error = MDDialog(text="enter the Number", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif (len(Newid) != 10):
            self.Error = MDDialog(text="enter the Correct Number", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        else:
            username = " NewUser " + Newid + " "
            s.send(bytes(username, "ascii"))
            result = s.recv(1024)
            check = result.decode("ascii")
            print(check)
            if (check == "ok"):
                username = " NewSeller " + Newid + " "
                s.send(bytes(username, "ascii"))
                result = s.recv(1024).decode("ascii")
                print(result)
                if (result == "ok"):
                    root.ids.Suser.text=Newid
                    root.current = "SellerCreatePassword"
                else:
                    self.Error = MDDialog(text="Number Already Exists", buttons=[
                        MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                     on_release=self.closeDialog)])
                    self.Error.open()
            else:
                self.Error = MDDialog(text="Number Already Exists", buttons=[
                    MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                 on_release=self.closeDialog)])
                self.Error.open()
        pass

    def SellerNewPassword(self,root):
        Newid=root.ids.Suser.text
        SPass1=root.ids.SPass1.text
        SPass2=root.ids.SPass2.text
        Special = "!@#$%^&*()/?<>"
        char = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
        num = "1234567890"
        Spe = "error"
        cha = "error"
        nu = "error"
        space="ok"
        if(Newid.isdecimal()==False or len(Newid)!=10):
            self.Error = MDDialog(text="Enter the Correct Number", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(SPass1==""):
            self.Error = MDDialog(text="Enter the Password", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(SPass1!=SPass2):
            self.Error = MDDialog(text="Password and Confirm Password", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(len(SPass1)<8):
            self.Error = MDDialog(text="Password should be greater than 8 letters", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        else:
            for i in SPass1:
                if i in Special:
                    Spe="ok"
                if i in char:
                    cha="ok"
                if i in num:
                    nu="ok"
                if i==" ":
                    space="Error"
            if (Spe == "ok" and cha == "ok" and nu == "ok" and space=="ok"):
                NewidNo = " NewUser " + Newid + " "
                s.send(bytes(NewidNo, "ascii"))
                result = s.recv(1024).decode("ascii")
                print(result)
                if (result == "ok"):
                    username = " NewSeller " + Newid + " "
                    s.send(bytes(username, "ascii"))
                    result = s.recv(1024).decode("ascii")
                    print(result)
                    if (result == "ok"):
                        print("User ok")
                        Data = " Insert-Seller-Ph&Password " + SPass1 + " " + "UserName " + Newid + " "
                        s.send(bytes(Data, "ascii"))
                        res = s.recv(1024).decode("ascii")
                        if (res == "ok"):
                            root.current = "SellerType"
                        else:
                            print("error")
                    else:
                        self.Error = MDDialog(text="No Already Exists", buttons=[
                            MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                         on_release=self.closeDialog)])
                        self.Error.open()
                else:
                    self.Error = MDDialog(text="No Already Exists", buttons=[
                        MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                     on_release=self.closeDialog)])
                    self.Error.open()
            else:
                self.Error = MDDialog(text="Enter the correct password", buttons=[
                    MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                 on_release=self.closeDialog)])
                self.Error.open()
        pass
    def SellerCanteenDetailes(self,root):
        CName=root.ids.CollegeName.text
        CCanteenName=root.ids.CanteenName.text
        COwnerName=root.ids.CanteenOwnerName.text
        COwnerNo=root.ids.CanteenOwnerNo.text
        CAddress=root.ids.CanteenAddress.text
        Newid = root.ids.Suser.text
        if(CName==""):
            self.Error = MDDialog(text="Enter the College Name", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(CCanteenName==""):
            self.Error = MDDialog(text="Enter the Canteen Name", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(COwnerName==""):
            self.Error = MDDialog(text="Enter the Owner Name", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()

        elif(COwnerNo==""):
            self.Error = MDDialog(text="Enter the Owner Number", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(CAddress==""):
            self.Error = MDDialog(text="Enter the Canteen Address", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(COwnerNo.isdecimal()==False or len(COwnerNo)!=10):
            self.Error = MDDialog(text="Enter the Correct Owner Number", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        else:
            CName=list(CName)
            for i in range(0,len(CName)):
                if CName[i]==" ":
                    CName[i]="-"
            CName="".join(CName)
            COwnerName=list(COwnerName)
            for i in range(0,len(COwnerName)):
                if(COwnerName[i]==" "):
                    COwnerName[i]="-"
            COwnerName="".join(COwnerName)
            CCanteenName=list(CCanteenName)
            for i in range(0,len(CCanteenName)):
                if (CCanteenName[i] == " "):
                    CCanteenName[i]= "-"
            CCanteenName="".join(CCanteenName)
            CAddress=list(CAddress)
            for i in range(0,len(CAddress)):
                if (CAddress[i] == " "):
                    CAddress[i] = "-"
            CAddress="".join(CAddress)
            print("ok")
            Detailes=" SellerCanteenDetailes "+"UserName "+Newid+" CollegeName "+CName+" CanteenName "+CCanteenName+" OwnerName "+COwnerName+" CanteenAddress "+CAddress+" OwnerNo "+COwnerNo+" "
            s.send(bytes(Detailes, "ascii"))
            result = s.recv(1024).decode("ascii")
            print(result)
            if(result=="ok"):
                root.current="Seller Homepage"
        pass

    def AddFood(self,root):
        root.current = "SellerFoodAdding"
        root.transition.direction = "left"
        pass
    def FoodCategory(self):
        self.menu_list=[
            {
                "viewclass":"OneLineListItem",
                "text":"Snacks",
                "on_release":lambda x="Snacks":self.SetFoodCatagory("Snacks")
            },
            {
                "viewclass":"OneLineListItem",
                "text":"Lunch",
                "on_release": lambda x="Lunch": self.SetFoodCatagory("Lunch")
            },
            {
                "viewclass":"OneLineListItem",
                "text":"Dinner",
                "on_release": lambda x="Dinner": self.SetFoodCatagory("Dinner")
            },
            {
                "viewclass":"OneLineListItem",
                "text":"Others",
                "on_release": lambda x="Others": self.SetFoodCatagory("Others")
            }
        ]
        self.menu=MDDropdownMenu(
            caller=self.ids.select,
            items=self.menu_list,
            position="bottom",
            width_mult=2
        )
        self.menu.open()
        pass
    def SetFoodCatagory(self,a):
        self.ids.select.text=a
        pass
    def FoodType(self):
        self.menu_Type=[
            {
                "viewclass":"OneLineListItem",
                "text":"Veg",
                "on_release":lambda x="Veg":self.SetFoodType("Veg")
            },
            {
                "viewclass":"OneLineListItem",
                "text":"Non-Veg",
                "on_release": lambda x="Non-Veg": self.SetFoodType("Non-Veg")
            }
        ]
        self.Food=MDDropdownMenu(
            caller=self.ids.FoodSelect,
            items=self.menu_Type,
            position="bottom",
            width_mult=2
        )
        self.Food.open()

    def SetFoodType(self,a):
        self.ids.FoodSelect.text=a
        pass

    def AddImage(self):
        self.menu_Type = [
            {
                "viewclass": "OneLineListItem",
                "text": "Veg Biryani",
                "on_release": lambda x="Veg Biryani": self.SetAddImage("Veg Biryani")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Chicken Biryani",
                "on_release": lambda x="Chicken Biryani": self.SetAddImage("Chicken Biryani")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Mutton Biryani",
                "on_release": lambda x="Mutton Biryani": self.SetAddImage("Mutton Biryani")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Meals",
                "on_release": lambda x="Meals": self.SetAddImage("Meals")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Chicken Parotta",
                "on_release": lambda x="Chicken Parotta": self.SetAddImage("Chicken Parotta")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Veg Noodles",
                "on_release": lambda x="Veg Noodles": self.SetAddImage("Veg Noodles")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Chicken Noodles",
                "on_release": lambda x="Chicken Noodles": self.SetAddImage("Chicken Noodles")
            },
        ]
        self.Images = MDDropdownMenu(
            caller=self.ids.ImageInfo,
            items=self.menu_Type,
            position="bottom",
            width_mult=3
        )
        self.Images.open()

    def SetAddImage(self,a):
        self.ids.ImageInfo.text=a

    def returnFoodlist(self,root):
        root.current = "SellerFoodlist"
        root.transition.direction = "right"

    def SellerAddFood(self,root):
        Dish=root.ids.DishName.text
        Count=root.ids.Quantity.text
        Price=root.ids.FoodPrice.text
        Type=root.ids.FoodSelect.text
        Category=root.ids.select.text
        img=root.ids.ImageInfo.text
        UserId=root.ids.SellerUser.text
        UserId1=root.ids.Suser.text

        imglist=["Veg Biryani","Chicken Biryani","Mutton Biryani","Meals","Chicken Parotta","Veg Noodles","Chicken Noodles"]
        if(UserId1!=""):
            Newid=UserId1
        else:
            Newid=UserId
        print(Newid)
        if(len(Dish)==0):
            self.Error = MDDialog(text="Enter the Dish Name", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif (img == "Select"):
            self.Error = MDDialog(text="Select Image", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(Type=="Select"):
            self.Error = MDDialog(text="Select Veg/NonVeg", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(Category=="Select"):
            self.Error = MDDialog(text="Select Food Category", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(Count.isdigit()==False):
            self.Error = MDDialog(text="Enter Correct Quantity", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif(Price.isdigit()==False):
            self.Error = MDDialog(text="Enter Correct Price", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        else:
            Dish=list(Dish)
            for i in range(0,len(Dish)):
                if(Dish[i]==" "):
                    Dish[i]="-"
            Dish="".join(Dish)
            print(Dish)
            print(Count)
            print(Price)
            print(Type)
            print(Category)
            img=imglist.index(img)
            Detailes=" SellerAddFood "+"DishName "+Dish+" Phno "+Newid+" FoodType "+Type+" FoodCategory "+Category+" Quantity "+Count+" Price "+Price+" Image "+str(img)+" "
            s.send(bytes(Detailes,"ascii"))
            result = s.recv(1024).decode("ascii")
            result=result.split(" ")
            print(result[1])
            if(result[1]=="ok"):
                root.ids.ItemNo.text="Item No = "+result[0]
                root.ids.DishName.text = ""
                root.ids.Quantity.text = ""
                root.ids.FoodPrice.text = ""
                root.ids.FoodSelect.text = "Select"
                root.ids.select.text = "Select"
                root.ids.ImageInfo.text = "Select"
                root.current="SellerFoodAddedSuccessfully"
        pass
    def GoToSellerFoodlist(self,root):
        UserId = root.ids.SellerUser.text
        UserId1 = root.ids.Suser.text
        AllIds=["root.ids.Sfood1","root.ids.Sfood2","root.ids.Sfood3","root.ids.Sfood4","root.ids.Sfood5"]
        AllLabelIds=["SF1Label1-SF1Label2","SF2Label1-SF2Label2","SF3Label1-SF3Label2","SF4Label1-SF4Label2","SF5Label1-SF5Label2"]
        imglist = ["Veg Biryani", "Chicken Biryani", "Mutton Biryani", "Meals", "Chicken Parotta", "Veg Noodles","Chicken Noodles"]
        imgOlist=["VegBiryani.png","ChickenBiryani.png","MuttonBiryani.png","Meals.png","ChickenParotta.png","vegnoodles.png","ChickenNoodles.png"]
        if (UserId1 != ""):
            Newid = UserId1
        else:
            Newid = UserId
        print(Newid)
        Detailes=" GetTheCount "+" Phno "+Newid+" "
        s.send(bytes(Detailes,"ascii"))
        result=s.recv(1024).decode("ascii")
        print(result)
        ans=result.split("_")
        Detailes=ans[2]
        sol=Detailes.split("**")
        Detailes=sol[1]
        Detailes1=sol[2]
        Detailes=Detailes.split("//")
        Detailes1=Detailes1.split("//")
        print(Detailes)
        print(Detailes1)

        for i in range(1,int(ans[0])+1):
            info=Detailes[i].split("&&")
            info1=Detailes1[i].split("&&")
            z=AllLabelIds[i-1].split("-")
            amt="Quantity : "+info1[5]+"          Price : "+info[11]+"Rs"
            name="[b]"+info[3]+"[/b]"
            imgname=imgOlist[int(info[5])]
            if(i==1):
                root.ids.SF1Label1.text=name
                root.ids.SF1Label2.text=amt
                root.ids.SF1Image.source=imgname
                root.ids.SF1Label1.hint_text=info[1]
            elif(i==2):
                root.ids.SF2Label1.text=name
                root.ids.SF2Label2.text = amt
                root.ids.SF2Image.source = imgname
                root.ids.SF2Label1.hint_text = info[1]
            elif(i==3):
                root.ids.SF3Label1.text=name
                root.ids.SF3Label2.text = amt
                root.ids.SF3Image.source = imgname
                root.ids.SF3Label1.hint_text = info[1]
            elif(i==4):
                root.ids.SF4Label1.text=name
                root.ids.SF4Label2.text = amt
                root.ids.SF4Image.source = imgname
                root.ids.SF4Label1.hint_text = info[1]
            elif(i==5):
                root.ids.SF5Label1.text=name
                root.ids.SF5Label2.text = amt
                root.ids.SF5Image.source = imgname
                root.ids.SF5Label1.hint_text = info[1]
            #exec("%s" %(a))
            print(info)
        for i in range(0,int(ans[0])):
            a=AllIds[i]+".opacity"
            b=AllIds[i]+".disabled"

            exec("%s = %d" %(a,1))
            exec("%s = False" %(b))

        #a="root.ids.Sfood1.disabled"
        #exec("%s = False" % (a))

        root.current="SellerFoodlist"
        root.transition.direction = "right"
        pass

    def GoInFoodDetailes(self,root,a="0"):
        UserId = root.ids.SellerUser.text
        UserId1 = root.ids.Suser.text
        imgOlist = ["VegBiryani.png", "ChickenBiryani.png", "MuttonBiryani.png", "Meals.png", "ChickenParotta.png",
                    "vegnoodles.png", "ChickenNoodles.png"]
        if (UserId1 != ""):
            Newid = UserId1
        else:
            Newid = UserId
        print("Yaa pressed",a)
        if(a=="1"):
            Itemno=root.ids.SF1Label1.hint_text
            print(root.ids.SF1Label1.hint_text)
        elif(a=="2"):
            Itemno = root.ids.SF2Label1.hint_text
            print(root.ids.SF2Label1.hint_text)
        elif(a=="3"):
            Itemno = root.ids.SF3Label1.hint_text
            print(root.ids.SF3Label1.hint_text)
        elif(a=="4"):
            Itemno = root.ids.SF4Label1.hint_text
            print(root.ids.SF4Label1.hint_text)
        elif(a=="5"):
            Itemno = root.ids.SF5Label1.hint_text
            print(root.ids.SF5Label1.hint_text)

        Detailes = " GetFoodDetailes " + "PhNo " + Newid + " ItemNo " + Itemno + " "
        s.send(bytes(Detailes, "ascii"))
        result = s.recv(1024).decode("ascii")
        ans=result.split("&&")
        print(ans)
        root.ids.SFIinfo0.source=imgOlist[int(ans[5])]
        root.ids.SFDinfo1.text="[b]"+ans[3]+"[/b]"
        root.ids.SFDinfo2.text="Quantity : "+ans[11]+"          Price : "+ans[13]+"Rs"
        root.ids.SFDinfo3.text ="No of Orders :          "+ans[15]
        root.ids.SFDinfo3.hint_text=Itemno
        root.current="SellerFoodOrders1"
        root.transition.direction = "left"

    def FoodCategoryEdit(self):
        self.menu_list=[
            {
                "viewclass":"OneLineListItem",
                "text":"Snacks",
                "on_release":lambda x="Snacks":self.SetFoodCatagoryEdit("Snacks")
            },
            {
                "viewclass":"OneLineListItem",
                "text":"Lunch",
                "on_release": lambda x="Lunch": self.SetFoodCatagoryEdit("Lunch")
            },
            {
                "viewclass":"OneLineListItem",
                "text":"Dinner",
                "on_release": lambda x="Dinner": self.SetFoodCatagoryEdit("Dinner")
            },
            {
                "viewclass":"OneLineListItem",
                "text":"Others",
                "on_release": lambda x="Others": self.SetFoodCatagoryEdit("Others")
            }
        ]
        self.menu=MDDropdownMenu(
            caller=self.ids.FCategoryEdit,
            items=self.menu_list,
            position="bottom",
            width_mult=2
        )
        self.menu.open()
        pass
    def SetFoodCatagoryEdit(self,a):
        self.ids.FCategoryEdit.text=a
        pass
    def FoodTypeEdit(self):
        self.menu_Type=[
            {
                "viewclass":"OneLineListItem",
                "text":"Veg",
                "on_release":lambda x="Veg":self.SetFoodTypeEdit("Veg")
            },
            {
                "viewclass":"OneLineListItem",
                "text":"Non-Veg",
                "on_release": lambda x="Non-Veg": self.SetFoodTypeEdit("Non-Veg")
            }
        ]
        self.Food=MDDropdownMenu(
            caller=self.ids.FTypeEdit,
            items=self.menu_Type,
            position="bottom",
            width_mult=2
        )
        self.Food.open()

    def SetFoodTypeEdit(self,a):
        self.ids.FTypeEdit.text=a
        pass

    def AddImageEdit(self):
        self.menu_Type = [
            {
                "viewclass": "OneLineListItem",
                "text": "Veg Biryani",
                "on_release": lambda x="Veg Biryani": self.SetAddImageEdit("Veg Biryani")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Chicken Biryani",
                "on_release": lambda x="Chicken Biryani": self.SetAddImageEdit("Chicken Biryani")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Mutton Biryani",
                "on_release": lambda x="Mutton Biryani": self.SetAddImageEdit("Mutton Biryani")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Meals",
                "on_release": lambda x="Meals": self.SetAddImageEdit("Meals")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Chicken Parotta",
                "on_release": lambda x="Chicken Parotta": self.SetAddImageEdit("Chicken Parotta")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Veg Noodles",
                "on_release": lambda x="Veg Noodles": self.SetAddImageEdit("Veg Noodles")
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Chicken Noodles",
                "on_release": lambda x="Chicken Noodles": self.SetAddImageEdit("Chicken Noodles")
            },
        ]
        self.Images = MDDropdownMenu(
            caller=self.ids.ImageNoEdit,
            items=self.menu_Type,
            position="bottom",
            width_mult=3
        )
        self.Images.open()

    def SetAddImageEdit(self,a):
        self.ids.ImageNoEdit.text=a

    def returnFoodDetailes(self,root):
        root.current="SellerFoodOrders1"
        root.transition.direction = "right"

    def CustomizeFoodDetailes(self,root):
        UserId = root.ids.SellerUser.text
        UserId1 = root.ids.Suser.text
        imglist = ["Veg Biryani", "Chicken Biryani", "Mutton Biryani", "Meals", "Chicken Parotta", "Veg Noodles",
                   "Chicken Noodles"]
        if (UserId1 != ""):
            Newid = UserId1
        else:
            Newid = UserId
        ItemNo=root.ids.SFDinfo3.hint_text
        print("Yess man Tell")
        print(ItemNo)
        Detailes = " GetFoodDetailes " + "PhNo " + Newid + " ItemNo " + ItemNo + " "
        s.send(bytes(Detailes, "ascii"))
        result = s.recv(1024).decode("ascii")
        ans = result.split("&&")
        print(ans)
        root.ids.DNameEdit.text=ans[3]
        root.ids.ImageNoEdit.text=imglist[int(ans[5])]
        root.ids.FTypeEdit.text=ans[7]
        root.ids.FCategoryEdit.text=ans[9]
        root.ids.QuantityEdit.text=ans[11]
        root.ids.PriceEdit.text=ans[13]
        root.current="EditFoodDetailes"
        root.transition.direction = "left"

    def UpdateFoodDetailes(self,root):
        UserId = root.ids.SellerUser.text
        UserId1 = root.ids.Suser.text
        if (UserId1 != ""):
            Newid = UserId1
        else:
            Newid = UserId
        imglist = ["Veg Biryani", "Chicken Biryani", "Mutton Biryani", "Meals", "Chicken Parotta", "Veg Noodles",
                   "Chicken Noodles"]
        DName=root.ids.DNameEdit.text
        DName=DName.replace(' ','-')
        Imgno=str(imglist.index(root.ids.ImageNoEdit.text))
        FType=root.ids.FTypeEdit.text
        FCategory=root.ids.FCategoryEdit.text
        Quantity=root.ids.QuantityEdit.text
        Price=root.ids.PriceEdit.text
        ItemNo = root.ids.SFDinfo3.hint_text
        Detailes=" UpdateFoodDetailes Phno "+Newid+" ItemNo "+ItemNo+" DishName "+DName+" ImageNo "+Imgno+" Type "+FType+" Category "+FCategory+" Quantity "+Quantity+" Price "+Price+" "
        s.send(bytes(Detailes,'ascii'))
        res=s.recv(1024).decode('ascii')
        print(res)
        if(res=="Ok"):
            root.current="UpdationDoneSuccessfully"

    def GotoCanteenList(self,root,q=0):
        CListIds=["root.ids.Clist1","root.ids.Clist2","root.ids.Clist3","root.ids.Clist4","root.ids.Clist5"]
        UserId = root.ids.Luser.text
        UserId1 = root.ids.user.text
        if (UserId1 != ""):
            Newid = UserId1
        else:
            Newid = UserId
        print(Newid)
        message=" GetTheCanteensList "+"UserId "+Newid+" "
        s.send(bytes(message.encode('ascii')))
        res=s.recv(1024).decode('ascii')
        print(res)
        res=res.split("**")
        print(res[1])
        Detailes=res[1].split("//")
        for i in range(1,len(Detailes)):
            ans=Detailes[i].split("&&")
            print(ans)
            CanteenName="     [b]"+ans[3]+"[/b]"
            CollegeName="     "+ans[1]
            Address="     "+ans[5]

            if i==1:
                root.ids.CCanteenName1.text=CanteenName
                root.ids.CCollegeName1.text=CollegeName
                root.ids.CAddress1.text=Address
                root.ids.CAddress1.hint_text =ans[7]
            elif i==2:
                root.ids.CCanteenName2.text = CanteenName
                root.ids.CCollegeName2.text = CollegeName
                root.ids.CAddress2.text = Address
                root.ids.CAddress2.hint_text = ans[7]
            elif i==3:
                root.ids.CCanteenName3.text = CanteenName
                root.ids.CCollegeName3.text = CollegeName
                root.ids.CAddress3.text = Address
                root.ids.CAddress3.hint_text = ans[7]
            elif i==4:
                root.ids.CCanteenName4.text = CanteenName
                root.ids.CCollegeName4.text = CollegeName
                root.ids.CAddress4.text = Address
                root.ids.CAddress4.hint_text = ans[7]
            elif i==5:
                root.ids.CCanteenName5.text = CanteenName
                root.ids.CCollegeName5.text = CollegeName
                root.ids.CAddress5.text = Address
                root.ids.CAddress5.hint_text = ans[7]
        for i in range(0,int(res[0])):
            a = CListIds[i] + ".opacity"
            b = CListIds[i] + ".disabled"

            exec("%s = %d" % (a, 1))
            exec("%s = False" % (b))

        root.current="CanteensList"
        if(q==3):
            root.transition.direction = "right"
        else:
            root.transition.direction = "left"

        pass

    def GoInCanteenFoodList(self,root,a=20,q=5):
        FoodCardIds=["root.ids.CFoodlist1","root.ids.CFoodlist2","root.ids.CFoodlist3","root.ids.CFoodlist4","root.ids.CFoodlist5"]
        if a==1:
            No=root.ids.CAddress1.hint_text
        elif a==2:
            No = root.ids.CAddress2.hint_text
        elif a==3:
            No = root.ids.CAddress3.hint_text
        elif a==4:
            No = root.ids.CAddress4.hint_text
        elif a==5:
            No = root.ids.CAddress5.hint_text
        else:
            No= root.ids.SelectedFoodName.hint_text
        Detailes = " GetTheFoodListForCustomer "+"PhNo "+No+" "
        s.send(bytes(Detailes.encode('ascii')))
        res = s.recv(1024).decode('ascii')
        res = res.split("**")
        print(res)
        info=res[1].split("//")
        for i in range(1,int(res[0])+1):
            imgOlist = ["VegBiryani.png", "ChickenBiryani.png", "MuttonBiryani.png", "Meals.png", "ChickenParotta.png",
                        "vegnoodles.png", "ChickenNoodles.png"]
            ans=info[i].split("&&")
            Foodname="[b]"+ans[3]+"[/b]"
            price=ans[11]
            CanteenName=ans[13]
            CollegeName=ans[15]
            imgpic=imgOlist[int(ans[5])]
            ItemNo=No+" "+ans[1]
            if(ans[7]=="Non-Veg"):
                col="red"
            else:
                col="green"
            if i==1:
                root.ids.CFoodName1.text=Foodname
                root.ids.CCollegeAndCanteenName1.text=CanteenName+","+CollegeName+"          Rs "+price+" for one"
                root.ids.FIconColor1.color=col
                root.ids.CFoodImage1.source=imgpic
                root.ids.CFoodName1.hint_text = ItemNo
                root.ids.CCollegeAndCanteenName1.hint_text="0"
            elif i==2:
                root.ids.CFoodName2.text = Foodname
                root.ids.CCollegeAndCanteenName2.text = CanteenName + "," + CollegeName+"          Rs "+price+" for one"
                root.ids.FIconColor2.color = col
                root.ids.CFoodImage2.source = imgpic
                root.ids.CFoodName2.hint_text = ItemNo
                root.ids.CCollegeAndCanteenName2.hint_text="0"
            elif i==3:
                root.ids.CFoodName3.text = Foodname
                root.ids.CCollegeAndCanteenName3.text = CanteenName + "," + CollegeName+"          Rs "+price+" for one"
                root.ids.FIconColor3.color = col
                root.ids.CFoodImage3.source = imgpic
                root.ids.CFoodName3.hint_text = ItemNo
                root.ids.CCollegeAndCanteenName3.hint_text="0"
            elif i==4:
                root.ids.CFoodName4.text = Foodname
                root.ids.CCollegeAndCanteenName4.text = CanteenName + "," + CollegeName+"          Rs "+price+" for one"
                root.ids.FIconColor4.color = col
                root.ids.CFoodImage4.source = imgpic
                root.ids.CFoodName4.hint_text = ItemNo
                root.ids.CCollegeAndCanteenName4.hint_text="0"
            elif i==5:
                root.ids.CFoodName5.text = Foodname
                root.ids.CCollegeAndCanteenName5.text = CanteenName + "," + CollegeName+"          Rs "+price+" for one"
                root.ids.FIconColor5.color = col
                root.ids.CFoodImage5.source = imgpic
                root.ids.CFoodName5.hint_text = ItemNo
                root.ids.CCollegeAndCanteenName5.hint_text="0"
            print(ans)
        for i in range(0,int(res[0])):
            a = FoodCardIds[i] + ".opacity"
            b = FoodCardIds[i] + ".disabled"

            exec("%s = %d" % (a, 1))
            exec("%s = False" % (b))
        for i in range(int(res[0]),5):
            a = FoodCardIds[i] + ".opacity"
            b = FoodCardIds[i] + ".disabled"

            exec("%s = %d" % (a, 0))
            exec("%s = True" % (b))
        root.current="FoodListAccordingly"
        if q==0:
            root.transition.direction = "right"
        else:
            root.transition.direction = "left"
        print(No)
        pass
    def FoodDetailesSelected(self,root,a=25):
        imgOlist = ["VegBiryani.png", "ChickenBiryani.png", "MuttonBiryani.png", "Meals.png", "ChickenParotta.png",
                    "vegnoodles.png", "ChickenNoodles.png"]
        if a==1:
            ItemNo=root.ids.CFoodName1.hint_text
            Quantity = root.ids.CCollegeAndCanteenName1.hint_text
        elif a==2:
            ItemNo = root.ids.CFoodName2.hint_text
            Quantity = root.ids.CCollegeAndCanteenName2.hint_text
        elif a==3:
            ItemNo = root.ids.CFoodName3.hint_text
            Quantity = root.ids.CCollegeAndCanteenName3.hint_text
        elif a==4:
            ItemNo = root.ids.CFoodName4.hint_text
            Quantity = root.ids.CCollegeAndCanteenName4.hint_text
        elif a==5:
            ItemNo = root.ids.CFoodName5.hint_text
            Quantity = root.ids.CCollegeAndCanteenName5.hint_text
        print(ItemNo)
        ItemNo=ItemNo.split(' ')
        Detailes=" GetTheSelectedFoodDetailes "+"PhNo "+ItemNo[0]+" ItemNo "+ItemNo[1]+" "
        s.send(bytes(Detailes.encode('ascii')))
        res = s.recv(1024).decode('ascii')
        res=res.split("&&")
        print(res)
        if res[6]=="Non-Veg":
            root.ids.SelectedFoodIcon.color="red"
        else:
            root.ids.SelectedFoodIcon.color = "green"
        root.ids.SelectedFood.opacity=1
        root.ids.SelectedFood.disabled=False
        root.ids.SelectedFoodImage.source=imgOlist[int(res[4])]
        root.ids.SelectedFoodName.text=res[2]
        root.ids.SelectedFoodClgAndCanteen.text=res[10]+","+res[12]
        root.ids.SelectedFoodCanteenAddress.text=res[14]
        root.ids.SelectedFoodPrice.text="Price : Rs "+res[16]+" for one "

        root.ids.SelectedFoodName.hint_text=ItemNo[0]
        root.ids.SelectedFoodClgAndCanteen.hint_text=ItemNo[0]+" "+res[18]
        root.ids.SelectedOrderFoodClgAndCanteen.hint_text="Nothing"

        if Quantity=="0":
            root.ids.SelectedFoodQuantity.text="1"
        else:
            root.ids.SelectedFoodQuantity.text=Quantity

        root.current="SelectedFoodOrder"
        root.transition.direction = "left"
        pass

    def SelectedFoodOrderDetailes(self,root,a=80):
        imgOlist = ["VegBiryani.png", "ChickenBiryani.png", "MuttonBiryani.png", "Meals.png", "ChickenParotta.png",
                    "vegnoodles.png", "ChickenNoodles.png"]
        if a==1:
            ItemNo=root.ids.COFoodName1.hint_text
            Quantity=root.ids.CCollegeAndCanteenName1.hint_text
        elif a==2:
            ItemNo=root.ids.COFoodName2.hint_text
            Quantity = root.ids.CCollegeAndCanteenName2.hint_text
        elif a==3:
            ItemNo=root.ids.COFoodName3.hint_text
            Quantity = root.ids.CCollegeAndCanteenName3.hint_text
        elif a==4:
            ItemNo=root.ids.COFoodName4.hint_text
            Quantity = root.ids.CCollegeAndCanteenName4.hint_text
        elif a==5:
            ItemNo=root.ids.COFoodName5.hint_text
            Quantity = root.ids.CCollegeAndCanteenName5.hint_text
        else:
            if(root.ids.SelectedOrderFoodClgAndCanteen.hint_text=="Nothing"):
                ItemNo = root.ids.SelectedFoodClgAndCanteen.hint_text
                Quantity = root.ids.SelectedFoodQuantity.text
            else:
                ItemNo = root.ids.SelectedOrderFoodClgAndCanteen.hint_text
                Quantity = root.ids.SelectedOrderFoodQuantity.text

        ItemNo = ItemNo.split(' ')
        print(ItemNo)
        print(Quantity)
        Detailes = " GetTheSelectedFoodDetailes " + "PhNo " + ItemNo[0] + " ItemNo " + ItemNo[1] + " "
        s.send(bytes(Detailes.encode('ascii')))
        res = s.recv(1024).decode('ascii')
        res = res.split("&&")
        print(res)
        if res[6] == "Non-Veg":
            root.ids.SelectedFoodIcon.color = "red"
        else:
            root.ids.SelectedFoodIcon.color = "green"
        root.ids.SelectedFoodDetailes.opacity = 1
        root.ids.SelectedFoodDetailes.disabled = False

        root.ids.SelectedOrderFoodImage.source = imgOlist[int(res[4])]
        root.ids.SelectedOrderFoodName.text = res[2]
        root.ids.SelectedOrderFoodClgAndCanteen.text = res[10] + "," + res[12]
        root.ids.SelectedOrderFoodCanteenAddress.text = res[14]
        root.ids.SelectedOrderFoodPrice.text = "Price : Rs " + res[16] + " for one "

        root.ids.SelectedOrderFoodClgAndCanteen.hint_text = ItemNo[0] + " " + res[18]
        root.ids.SelectedOrderFoodName.hint_text = ItemNo[0]
        if Quantity=="0":
            root.ids.SelectedOrderFoodQuantity.text="1"
        else:
            root.ids.SelectedOrderFoodQuantity.text = Quantity
        root.current = "SelectedFoodOrderBuying"
        root.transition.direction = "left"
        pass
    def GoBackToFoodListAfterSelecting(self,root,a,b=35):
        FoodCardIds = ["root.ids.COFoodlist1", "root.ids.COFoodlist2", "root.ids.COFoodlist3", "root.ids.COFoodlist4",
                       "root.ids.COFoodlist5"]

        imgOlist = ["VegBiryani.png", "ChickenBiryani.png", "MuttonBiryani.png", "Meals.png", "ChickenParotta.png",
                    "vegnoodles.png", "ChickenNoodles.png"]
        if a==1:
            ItemNo=root.ids.SelectedFoodClgAndCanteen.hint_text
            Quantity=root.ids.SelectedFoodQuantity.text
        else:
            ItemNo=root.ids.SelectedOrderFoodClgAndCanteen.hint_text
            Quantity=root.ids.SelectedOrderFoodQuantity.text
        ItemNo = ItemNo.split(" ")
        print(ItemNo)
        print("Quantity "+Quantity)
        Detailes=" CheckQuantityAvailabel "+"Phno "+ItemNo[0]+" ItemNo "+ItemNo[1]+" Quantity "+Quantity+" "
        s.send(bytes(Detailes.encode('ascii')))
        res=s.recv(1024).decode('ascii')
        if (Quantity.isdecimal()==False) and (b==35):
            self.Error = MDDialog(text="Enter the Correct Quantity", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        elif int(Quantity)<=0 and b==35:
            self.Error = MDDialog(text="Enter the Correct Quantity", buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                             on_release=self.closeDialog)])
            self.Error.open()
        else:
            Detailes = " CheckQuantityAvailabel " + "Phno " + ItemNo[0] + " ItemNo " + ItemNo[1] + " Quantity " + Quantity + " "
            s.send(bytes(Detailes.encode('ascii')))
            res = s.recv(1024).decode('ascii')
            if res=="Error":
                self.Error = MDDialog(text="That much Quantity is Not Availabel", buttons=[
                    MDFlatButton(text="OK", theme_text_color="Custom", text_color=self.theme_cls.primary_color,
                                 on_release=self.closeDialog)])
                self.Error.open()
            else:
                if(b==35):
                    if((root.ids.CFoodName1.hint_text).split(' ')[1]==ItemNo[1]):
                        root.ids.CCollegeAndCanteenName1.hint_text = Quantity

                    elif ((root.ids.CFoodName2.hint_text).split(' ')[1]==ItemNo[1]):
                        root.ids.CCollegeAndCanteenName2.hint_text = Quantity

                    elif ((root.ids.CFoodName3.hint_text).split(' ')[1]==ItemNo[1]):
                        root.ids.CCollegeAndCanteenName3.hint_text = Quantity

                    elif ((root.ids.CFoodName4.hint_text).split(' ')[1]==ItemNo[1]):
                        root.ids.CCollegeAndCanteenName4.hint_text = Quantity

                    elif ((root.ids.CFoodName5.hint_text).split(' ')[1]==ItemNo[1]):
                        root.ids.CCollegeAndCanteenName5.hint_text = Quantity


                No=ItemNo[0]
                Detailes = " GetTheFoodListForCustomer " + "PhNo " + No + " "
                s.send(bytes(Detailes.encode('ascii')))
                res = s.recv(1024).decode('ascii')
                res = res.split("**")
                print(res)
                info = res[1].split("//")
                cost=0
                c=0
                for i in range(1, int(res[0]) + 1):
                    ans = info[i].split("&&")
                    Foodname = "[b]" + ans[3] + "[/b]"
                    price = ans[11]
                    CanteenName = ans[13]
                    CollegeName = ans[15]
                    imgpic = imgOlist[int(ans[5])]
                    ItemNo = No + " " + ans[1]
                    if (ans[7] == "Non-Veg"):
                        col = "red"
                    else:
                        col = "green"
                    if i == 1:
                        root.ids.COFoodName1.text = Foodname
                        root.ids.COCollegeAndCanteenName1.text = CanteenName + "," + CollegeName + "          Rs " + price + " for one"
                        root.ids.FOIconColor1.color = col
                        root.ids.COFoodImage1.source = imgpic
                        root.ids.COFoodName1.hint_text = ItemNo
                        cost=cost+(int(root.ids.CCollegeAndCanteenName1.hint_text)*float(price))
                        if(root.ids.CCollegeAndCanteenName1.hint_text!="0"):
                            c=c+1
                    elif i == 2:
                        root.ids.COFoodName2.text = Foodname
                        root.ids.COCollegeAndCanteenName2.text = CanteenName + "," + CollegeName + "          Rs " + price + " for one"
                        root.ids.FOIconColor2.color = col
                        root.ids.COFoodImage2.source = imgpic
                        root.ids.COFoodName2.hint_text = ItemNo
                        cost = cost + (int(root.ids.CCollegeAndCanteenName2.hint_text) * float(price))
                        if (root.ids.CCollegeAndCanteenName2.hint_text != "0"):
                            c = c + 1
                    elif i == 3:
                        root.ids.COFoodName3.text = Foodname
                        root.ids.COCollegeAndCanteenName3.text = CanteenName + "," + CollegeName + "          Rs " + price + " for one"
                        root.ids.FOIconColor3.color = col
                        root.ids.COFoodImage3.source = imgpic
                        root.ids.COFoodName3.hint_text = ItemNo
                        cost = cost + (int(root.ids.CCollegeAndCanteenName3.hint_text) * float(price))
                        if (root.ids.CCollegeAndCanteenName3.hint_text != "0"):
                            c = c + 1
                    elif i == 4:
                        root.ids.COFoodName4.text = Foodname
                        root.ids.COCollegeAndCanteenName4.text = CanteenName + "," + CollegeName + "          Rs " + price + " for one"
                        root.ids.FOIconColor4.color = col
                        root.ids.COFoodImage4.source = imgpic
                        root.ids.COFoodName4.hint_text = ItemNo
                        if (root.ids.CCollegeAndCanteenName4.hint_text != "0"):
                            c = c + 1
                        cost = cost + (int(root.ids.CCollegeAndCanteenName4.hint_text) * float(price))
                    elif i == 5:
                        root.ids.COFoodName5.text = Foodname
                        root.ids.COCollegeAndCanteenName5.text = CanteenName + "," + CollegeName + "          Rs " + price + " for one"
                        root.ids.FOIconColor5.color = col
                        root.ids.COFoodImage5.source = imgpic
                        root.ids.COFoodName5.hint_text = ItemNo
                        cost = cost + (int(root.ids.CCollegeAndCanteenName5.hint_text) * float(price))
                        if (root.ids.CCollegeAndCanteenName5.hint_text != "0"):
                            c = c + 1
                    print(ans)
                for i in range(0, int(res[0])):
                    a = FoodCardIds[i] + ".opacity"
                    b = FoodCardIds[i] + ".disabled"

                    exec("%s = %d" % (a, 1))
                    exec("%s = False" % (b))
                for i in range(int(res[0]), 5):
                    a = FoodCardIds[i] + ".opacity"
                    b = FoodCardIds[i] + ".disabled"

                    exec("%s = %d" % (a, 0))
                    exec("%s = True" % (b))
                root.ids.PriceToolBar.title=str(c)+" Items Rs "+str(cost)+"          Pay"
                root.current="FoodListAccordinglyForBuying"
                if b==35:
                    root.transition.direction = "left"
                else:
                    root.transition.direction = "right"
        pass

    def AfterPaymentSuccessfull(self,root):

        UserId = root.ids.Luser.text
        UserId1 = root.ids.user.text
        if (UserId1 != ""):
            Newid = UserId1
        else:
            Newid = UserId

        no=(root.ids.COFoodName1.hint_text).split(' ')[0]
        ItemNo = "CustomerPhNo&&"+Newid+"&&SellerPhoneNo&&"+no+"&&Items&&"
        if root.ids.CCollegeAndCanteenName1.hint_text!="0" and root.ids.COFoodName1.hint_text!="0":
            ItemNo=ItemNo+(root.ids.COFoodName1.hint_text).split(' ')[1]+"**"+root.ids.CCollegeAndCanteenName1.hint_text+"&&"
        if root.ids.CCollegeAndCanteenName2.hint_text!="0" and root.ids.COFoodName2.hint_text!="0":
            ItemNo = ItemNo + (root.ids.COFoodName2.hint_text).split(' ')[1]+"**"+root.ids.CCollegeAndCanteenName2.hint_text+"&&"
        if root.ids.CCollegeAndCanteenName3.hint_text!="0" and root.ids.COFoodName3.hint_text!="0":
            ItemNo = ItemNo + (root.ids.COFoodName3.hint_text).split(' ')[1]+"**"+root.ids.CCollegeAndCanteenName3.hint_text+"&&"
        if root.ids.CCollegeAndCanteenName4.hint_text!="0" and root.ids.COFoodName4.hint_text!="0":
            ItemNo = ItemNo + (root.ids.COFoodName4.hint_text).split(' ')[1]+"**"+root.ids.CCollegeAndCanteenName4.hint_text+"&&"
        if root.ids.CCollegeAndCanteenName5.hint_text!="0" and root.ids.COFoodName5.hint_text!="0":
            ItemNo = ItemNo + (root.ids.COFoodName5.hint_text).split(' ')[1]+"**"+root.ids.CCollegeAndCanteenName5.hint_text+"&&"
        print(ItemNo)
        Detailes=" GettheOrderedFoodList "+ItemNo+" "
        s.send(bytes(Detailes.encode('ascii')))
        res=s.recv(1024).decode('ascii')
        res=res.split("&&")
        print(res)
        root.ids.PaymentAmount.text="Total Money Spent : "+res[3]
        root.ids.OtpAfterPayment.text="OTP = "+res[1]
        root.current="PaymentSuccessfull"
        root.transition.direction="left"
        pass

    def GotoOrderedFoodList(self,root,a):
        FoodCardIds = ["root.ids.OrderedItemListNo1", "root.ids.OrderedItemListNo2", "root.ids.OrderedItemListNo3", "root.ids.OrderedItemListNo4",
                       "root.ids.OrderedItemListNo5"]

        imgOlist = ["VegBiryani.png", "ChickenBiryani.png", "MuttonBiryani.png", "Meals.png", "ChickenParotta.png",
                    "vegnoodles.png", "ChickenNoodles.png"]
        UserId = root.ids.Luser.text
        UserId1 = root.ids.user.text
        if (UserId1 != ""):
            Newid = UserId1
        else:
            Newid = UserId
        print("ya pressed")
        if a==1:
            orderno=root.ids.OrderedCanteenName1.hint_text
        elif a==2:
            orderno = root.ids.OrderedCanteenName2.hint_text
        elif a==3:
            orderno = root.ids.OrderedCanteenName3.hint_text
        elif a==4:
            orderno = root.ids.OrderedCanteenName4.hint_text
        elif a==5:
            orderno = root.ids.OrderedCanteenName5.hint_text
        Detailes=" GetTheOrderFoodList "+"Phno "+Newid+" OrderNo "+orderno+" "
        s.send(bytes(Detailes.encode('ascii')))
        res=s.recv(1024).decode('ascii')
        print(res)
        res=res.split("//")
        NoofItems=str(len(res)-1)
        ans=res[0].split("&&")
        if ans[3]=="Ordered":
            progress=5
        elif ans[3]=="Accepted":
            progress=25
        elif ans[3]=="InKitchen":
            progress=50
        elif ans[3]=="Ready":
            progress=75
        elif ans[3]=="Delivered":
            progress=100
        root.ids.StatusType.text=ans[3]
        root.ids.ProgressBarStatus.value = progress
        root.ids.OrderNoPrint.text="[b]Order No : "+ans[1]+"[/b]"
        root.ids.TotalItemsOrdered.text=NoofItems+" Items Ordered               Total cost :"+ans[5]
        print("We need to check")
        print(res)
        for i in range(1,len(res)):
            a=res[i].split("&&")
            if i==1:
                root.ids.OrderedItemImage1.source=imgOlist[int(a[9])]
                root.ids.OrderedItemFoodName1.text="[b]"+a[7]+"[/b]"
                root.ids.OrderedItemQuantity1.text="Quantity : "+a[3]
                root.ids.OrderedItemPrice1.text="Price   : "+a[5]
            elif i==2:
                root.ids.OrderedItemImage2.source = imgOlist[int(a[9])]
                root.ids.OrderedItemFoodName2.text = "[b]" + a[7] + "[/b]"
                root.ids.OrderedItemQuantity2.text = "Quantity : " + a[3]
                root.ids.OrderedItemPrice2.text = "Price   : " + a[5]
            elif i==3:
                root.ids.OrderedItemImage3.source = imgOlist[int(a[9])]
                root.ids.OrderedItemFoodName3.text = "[b]" + a[7] + "[/b]"
                root.ids.OrderedItemQuantity3.text = "Quantity : " + a[3]
                root.ids.OrderedItemPrice3.text = "Price   : " + a[5]
            elif i==4:
                root.ids.OrderedItemImage4.source = imgOlist[int(a[9])]
                root.ids.OrderedItemFoodName4.text = "[b]" + a[7] + "[/b]"
                root.ids.OrderedItemQuantity4.text = "Quantity : " + a[3]
                root.ids.OrderedItemPrice4.text = "Price   : " + a[5]
            elif i==5:
                root.ids.OrderedItemImage5.source = imgOlist[int(a[9])]
                root.ids.OrderedItemFoodName5.text = "[b]" + a[7] + "[/b]"
                root.ids.OrderedItemQuantity5.text = "Quantity : " + a[3]
                root.ids.OrderedItemPrice5.text = "Price   : " + a[5]
        for i in range(0,len(res)-1):
            a = FoodCardIds[i] + ".opacity"
            b = FoodCardIds[i] + ".disabled"

            exec("%s = %d" % (a, 1))
            exec("%s = False" % (b))
        for i in range(len(res)-1, 5):
            a = FoodCardIds[i] + ".opacity"
            b = FoodCardIds[i] + ".disabled"

            exec("%s = %d" % (a, 0))
            exec("%s = True" % (b))
        print(res)
        root.current="OrderedCanteenFoodList"
        pass

    def GoInSellerOrderDetailes(self,root,a):
        FoodCardIds = ["root.ids.SellerOrderedItemListNo1", "root.ids.SellerOrderedItemListNo2", "root.ids.SellerOrderedItemListNo3",
                       "root.ids.SellerOrderedItemListNo4",
                       "root.ids.SellerOrderedItemListNo5"]
        imgOlist = ["VegBiryani.png", "ChickenBiryani.png", "MuttonBiryani.png", "Meals.png", "ChickenParotta.png",
                    "vegnoodles.png", "ChickenNoodles.png"]
        UserId = root.ids.SellerUser.text
        UserId1 = root.ids.Suser.text
        if (UserId1 != ""):
            Newid = UserId1
        else:
            Newid = UserId
        if a==1:
            OrderNo=root.ids.SellerOrderNo1.text
        elif a==2:
            OrderNo = root.ids.SellerOrderNo2.text
        elif a==3:
            OrderNo = root.ids.SellerOrderNo3.text
        elif a==4:
            OrderNo = root.ids.SellerOrderNo4.text
        elif a==5:
            OrderNo = root.ids.SellerOrderNo5.text
        elif a==6:
            OrderNo = root.ids.SellerOrderNo6.text
        elif a==7:
            OrderNo = root.ids.SellerOrderNo7.text
        elif a==8:
            OrderNo = root.ids.SellerOrderNo8.text
        elif a==9:
            OrderNo = root.ids.SellerOrderNo9.text
        elif a==10:
            OrderNo = root.ids.SellerOrderNo10.text
        OrderNo=OrderNo.split(" ")
        OrderNo=OrderNo[3].split("[")
        OrderNo=OrderNo[0]
        print(OrderNo)
        Message=" GetSellerOrderFoodDetailes UserName "+Newid+" OrderNo "+OrderNo+" "
        s.send(bytes(Message.encode('ascii')))
        res=s.recv(1024).decode('ascii')
        print(res)
        sol=res.split("//")
        print(sol)
        for i in range(1,len(sol)-1):
            ans=sol[i].split("**")
            print(ans)
            if i==1:
                root.ids.SellerOrderNoPrint.text=OrderNo
                root.ids.SellerStatusType.text=ans[2]
                if ans[2] == "Ordered":
                    progress = 5
                elif ans[2] == "Accepted":
                    progress = 25
                elif ans[2] == "InKitchen":
                    progress = 50
                elif ans[2] == "Ready":
                    progress = 75
                elif ans[2] == "Delivered":
                    progress = 100

                root.ids.SellerProgressBarStatus.value=progress
                root.ids.SellerTotalItemsOrdered.text=str(len(sol)-3)+" Items Ordered               Total cost:"+ans[4]
            elif i==2:
                root.ids.SellerOrderedItemFoodName1.text="[b]"+ans[4]+"[/b]"
                root.ids.SellerOrderedItemImage1.source=imgOlist[int(ans[6])]
                root.ids.SellerOrderedItemQuantity1.text="Quantity : "+ans[8]
                root.ids.SellerOrderedItemPrice1.text="Price : "+ans[10]
            elif i==3:
                root.ids.SellerOrderedItemFoodName2.text="[b]"+ans[4]+"[/b]"
                root.ids.SellerOrderedItemImage2.source=imgOlist[int(ans[6])]
                root.ids.SellerOrderedItemQuantity2.text="Quantity : "+ans[8]
                root.ids.SellerOrderedItemPrice2.text="Price : "+ans[10]
            elif i==4:
                root.ids.SellerOrderedItemFoodName3.text="[b]"+ans[4]+"[/b]"
                root.ids.SellerOrderedItemImage3.source=imgOlist[int(ans[6])]
                root.ids.SellerOrderedItemQuantity3.text="Quantity : "+ans[8]
                root.ids.SellerOrderedItemPrice3.text="Price : "+ans[10]
            elif i==5:
                root.ids.SellerOrderedItemFoodName4.text="[b]"+ans[4]+"[/b]"
                root.ids.SellerOrderedItemImage4.source=imgOlist[int(ans[6])]
                root.ids.SellerOrderedItemQuantity4.text="Quantity : "+ans[8]
                root.ids.SellerOrderedItemPrice4.text="Price : "+ans[10]
            elif i==6:
                root.ids.SellerOrderedItemFoodName5.text="[b]"+ans[4]+"[/b]"
                root.ids.SellerOrderedItemImage5.source=imgOlist[int(ans[6])]
                root.ids.SellerOrderedItemQuantity5.text="Quantity : "+ans[8]
                root.ids.SellerOrderedItemPrice5.text="Price : "+ans[10]

        for i in range(0,len(sol)-3):
            a = FoodCardIds[i] + ".opacity"
            b = FoodCardIds[i] + ".disabled"

            exec("%s = %d" % (a, 1))
            exec("%s = False" % (b))
        for i in range(len(sol)-2, 2):
            a = FoodCardIds[i] + ".opacity"
            b = FoodCardIds[i] + ".disabled"

            exec("%s = %d" % (a, 0))
            exec("%s = True" % (b))
        root.current="SellerOrderFoodListAndStatus"
        pass
kv=Builder.load_file("app_info.kv")


class MyApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return WindowManager()

MyApp().run()
