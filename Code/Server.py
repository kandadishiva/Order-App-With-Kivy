import socket
import threading
import mysql.connector
import random

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),1024))
s.listen(5)

#Database server detailes connection
MyDb=mysql.connector.connect(host="localhost",user="root",passwd="",database="orderapp")
if(MyDb):
    print("Connection Sucessfull")
else:
    print("Connction was Not Sucessfull")
Cursor=MyDb.cursor()

def check(message,Client):
    a=str(message)
    print(a)
    msg=a.split(" ")
    try:
        if(msg[1]=="ExitUser"):
            print("hloo")
            command="SELECT * FROM `customer_login_detailes` WHERE PhNo="+msg[2]
            Cursor.execute(command)
            res=Cursor.fetchall()
            print(res)
            if(res==[]):
                Client.send("Error".encode('ascii'))
            else:
                user = res[0]
                FinallUser = user[0]
                if(FinallUser==int(msg[2])):
                    Client.send("ok".encode('ascii'))
                else:
                    Client.send("Error".encode('ascii'))
        elif(msg[1]=="Existpassword"):
            command="SELECT * FROM `customer_login_detailes` WHERE PhNo="+msg[5]
            Cursor.execute(command)
            res=Cursor.fetchall()
            user=res[0]
            Password=user[1]
            if(Password==msg[2]):
                Client.send("ok".encode('ascii'))
            else:
                Client.send("Error".encode('ascii'))
        elif(msg[1]=="NewUser"):
            print("New User")
            command="SELECT * FROM `customer_login_detailes` WHERE PhNo="+msg[2]
            Cursor.execute(command)
            res=Cursor.fetchall()
            print(res)
            if(res==[]):
                Client.send("ok".encode('ascii'))
            else:
                Client.send("Error Alreay Exists".encode('ascii'))
        elif(msg[1]=="UpdatePassword"):
            UserName=int(msg[4])
            Password=msg[2]
            Detailes=(UserName,Password)
            print(Detailes)
            command="INSERT INTO customer_login_detailes(PhNo,PASSWORD)VALUES"+str(Detailes)
            Cursor.execute(command)
            MyDb.commit()
            Client.send("ok".encode('ascii'))

        elif(msg[1]=="Detailes"):
            UserName=int(msg[3])
            Name=msg[5]
            Email=msg[7]
            Mname = list(Name)
            for i in range(0, len(Mname)):
                if Mname[i] == "-":
                    Mname[i] = " "
            Name = "".join(Mname)
            Detailes=(UserName,Name,Email)
            command="INSERT INTO customer_personal_detailes(PhNo,Name,Email)VALUES"+str(Detailes)
            Cursor.execute(command)
            MyDb.commit()
            print(command)
            TableName="customer_"+str(UserName)+"_orders"
            Command="Create Table "+TableName+" (OrderNo int ,CustomerNo bigint, SellerNo bigint,Item1_No_Quantity_Price varchar(100),Item2_No_Quantity_Price varchar(100),Item3_No_Quantity_Price varchar(100),Item4_No_Quantity_Price varchar(100),Item5_No_Quantity_Price varchar(100),TotalCost float,Status varchar(100),PRIMARY KEY(OrderNo),FOREIGN key(OrderNo) REFERENCES all_orders_customer_seller(OrderNo),FOREIGN KEY(CustomerNo) REFERENCES customer_login_detailes(PhNo),FOREIGN KEY (SellerNo) REFERENCES seller_login_detailes(PhNo))"
            Cursor.execute(Command)
            MyDb.commit()
            Client.send("ok".encode('ascii'))
        elif(msg[1]=="SendInfo"):
            command="SELECT * FROM customer_personal_detailes WHERE PhNo="+msg[3]
            Cursor.execute(command)
            res = Cursor.fetchall()
            ans=list(res[0])
            print(ans)
            Name=list(ans[1])
            for i in range(0,len(Name)):
                if(Name[i]==" "):
                    Name[i]="-"
            Name="".join(Name)
            info="Username "+str(ans[0])+" Name "+Name+" Email "+ans[2]
            Client.send(info.encode("ascii"))
        elif(msg[1]=="NewSeller"):
            command="SELECT * FROM seller_login_detailes WHERE PhNo="+msg[2]
            Cursor.execute(command)
            res=Cursor.fetchall()
            if(res==[]):
                Client.send("ok".encode("ascii"))
            else:
                Client.send("Number Exists".encode("ascii"))
        elif(msg[1]=="Insert-Seller-Ph&Password"):
            UserName = int(msg[4])
            Password = msg[2]
            Detailes = (UserName, Password)
            print(Detailes)
            command = "INSERT INTO seller_login_detailes(PhNo,PASSWORD)VALUES" + str(Detailes)
            Cursor.execute(command)
            MyDb.commit()
            Client.send("ok".encode('ascii'))
        elif(msg[1]=="SellerCanteenDetailes"):
            UserName=int(msg[3])
            CollegeName=list(msg[5])
            CanteenName=list(msg[7])
            OwnerName=list(msg[9])
            CanteenAddress=list(msg[11])
            OwnerNo=int(msg[13])
            TableCanteenName=CanteenName.copy()
            print("ok")
            for i in range(0,len(CollegeName)):
                if CollegeName[i]=="-":
                    CollegeName[i]=" "
            for i in range(0,len(CanteenName)):
                if CanteenName[i]=="-":
                    CanteenName[i]=" "
            for i in range(0,len(OwnerName)):
                if OwnerName[i]=="-":
                    OwnerName[i]=" "
            for i in range(0,len(CanteenAddress)):
                if CanteenAddress[i]=="-":
                    CanteenAddress[i]=" "
            for i in range(0,len(TableCanteenName)):
                if TableCanteenName[i]=="-":
                    TableCanteenName[i]="_"
            TableCanteenName="".join(TableCanteenName)
            CollegeName="".join(CollegeName)
            CanteenName="".join(CanteenName)
            OwnerName="".join(OwnerName)
            CanteenAddress="".join(CanteenAddress)
            detailes=(UserName,CollegeName,CanteenName,OwnerName,OwnerNo,CanteenAddress)
            command="INSERT INTO seller_shop_detailes values "+str(detailes)
            Cursor.execute(command)
            MyDb.commit()
            print(command)
            TableName="SFDetailes_"+TableCanteenName+"_"+str(UserName)
            TableName1 = "SOrders_" + TableCanteenName + "_" + str(UserName)
            detailes=(UserName,CollegeName,CanteenName,TableName,TableName1)
            command="Insert into seller_foodtable_name values "+str(detailes)
            Cursor.execute(command)
            MyDb.commit()
            command="Create Table "+TableName+"(Dish_No int,DishName varchar(200),ImageNo int,PhNo bigint,FoodType varchar(100),FoodCategory varchar(100),Price float,Primary Key(Dish_No),FOREIGN key(PhNo) REFERENCES seller_foodtable_name(PhNo))"
            Cursor.execute(command)
            MyDb.commit()
            print(command)
            command="Create Table "+TableName1+"(Dish_No int,DishName varchar(200),Quantity int,PendingOrders int,CompletedOrders int,TotalOrders int,FoodStatus varchar(100),Primary Key(Dish_No),FOREIGN key(Dish_No) REFERENCES "+TableName+"(Dish_No))"
            print(command)
            Cursor.execute(command)
            MyDb.commit()
            TableName="seller_"+str(UserName)+"_orders"
            Command="Create Table "+TableName+"(OrderNo int ,CustomerNo bigint, SellerNo bigint,Item1_No_Quantity_Price varchar(100),Item2_No_Quantity_Price varchar(100),Item3_No_Quantity_Price varchar(100),Item4_No_Quantity_Price varchar(100),Item5_No_Quantity_Price varchar(100),TotalCost float,Status varchar(100),PRIMARY KEY(OrderNo),FOREIGN key(OrderNo) REFERENCES all_orders_customer_seller(OrderNo),FOREIGN KEY(CustomerNo) REFERENCES customer_login_detailes(PhNo),FOREIGN KEY (SellerNo) REFERENCES seller_login_detailes(PhNo))"
            print(Command)
            Cursor.execute(Command)
            MyDb.commit()
            Client.send("ok".encode('ascii'))
        elif(msg[1]=="CheckSellerPassword"):
            Command="SELECT PASSWORD FROM seller_login_detailes where PhNo="+msg[4]
            Cursor.execute(Command)
            res = Cursor.fetchall()
            password=res[0]
            if(password[0]==msg[2]):
                Client.send("ok".encode('ascii'))
            else:
                Client.send("Error".encode('ascii'))
            print(res)
        elif(msg[1]=="SellerAddFood"):
            Command="Select FoodListTableName,OrdersListTableName from seller_foodtable_name where Phno ="+msg[5]
            Cursor.execute(Command)
            res=Cursor.fetchall()
            name=res[0][0]
            name1=res[0][1]
            Command="Select count(*) from "+name
            Cursor.execute(Command)
            res=Cursor.fetchall()
            no=int(res[0][0])+1
            Dish=list(msg[3])
            for i in range(0,len(Dish)):
                if Dish[i]=="-":
                    Dish[i]=" "
            Dish="".join(Dish)
            values=(no,Dish,int(msg[15]),int(msg[5]),msg[7],msg[9],float(msg[13]))
            Command="Insert INTO "+name+" values "+str(values)
            Cursor.execute(Command)
            MyDb.commit()
            print(Command)
            values=(no,Dish,int(msg[11]),0,0,0,"Enable")
            Command="Insert INTO "+name1+" values "+str(values)
            print(Command)
            Cursor.execute(Command)
            MyDb.commit()
            print(Command)
            ans=str(no)+" ok "
            Client.send(ans.encode('ascii'))

        elif msg[1]=="GetTheCount":
            Command="select FoodListTableName,OrdersListTableName from seller_foodtable_name where Phno = "+msg[4]
            Cursor.execute(Command)
            res=Cursor.fetchall()
            name = res[0][0]
            name1=res[0][1]
            Command = "Select * from " + name+" Limit 5"
            Cursor.execute(Command)
            res = Cursor.fetchall()
            ans="**"
            for i in res:
                print(i)
                ans=ans+"//ItemNo&&"+str(i[0])+"&&DishName&&"+i[1]+"&&ImageNo&&"+str(i[2])+"&&Type&&"+i[4]+"&&Category&&"+i[5]+"&&Price&&"+str(i[6])
                print(ans)
            ans=ans+"**"
            Command = "Select * from " + name1 + " Limit 5"
            Cursor.execute(Command)
            res = Cursor.fetchall()
            for i in res:
                ans=ans+"//ItemNo&&"+str(i[0])+"&&DishName&&"+i[1]+"&&Quanitity&&"+str(i[2])+"&&PendingOrders&&"+str(i[3])+"&&CompletedOrders&&"+str(i[4])+"&&TotalOrders&&"+str(i[5])+"&&Status&&"+i[6]
            length=str(len(res))
            Client.send((length+"_ok_"+ans).encode('ascii'))

        elif msg[1]=="GetFoodDetailes":
            Command = "select FoodListTableName,OrdersListTableName from seller_foodtable_name where Phno = " + msg[3]
            Cursor.execute(Command)
            res = Cursor.fetchall()
            name = res[0][0]
            name1=res[0][1]
            Command = "Select * from " + name + " Where Dish_No = "+msg[5]
            Cursor.execute(Command)
            res = Cursor.fetchall()
            i=res[0]
            Command="Select * from "+name1+" Where Dish_No = "+msg[5]
            Cursor.execute(Command)
            res=Cursor.fetchall()
            j=res[0]
            ans="ItemNo&&"+str(i[0])+"&&DishName&&"+i[1]+"&&ImageNo&&"+str(i[2])+"&&Type&&"+i[4]+"&&Category&&"+i[5]+"&&Quanitity&&"+str(j[2])+"&&Price&&"+str(i[6])+"&&Orders&&"+str(j[3])
            Client.send(ans.encode('ascii'))
            print(res)

        elif msg[1]=="UpdateFoodDetailes":
            Command = "select FoodListTableName,OrdersListTableName from seller_foodtable_name where Phno = " + msg[3]
            Cursor.execute(Command)
            res = Cursor.fetchall()
            name = res[0][0]
            name1 = res[0][1]
            DName=msg[7].replace('-',' ')
            Command="Update "+name+" Set DishName = '"+DName+"' , ImageNo = "+msg[9]+" , FoodType = '"+msg[11]+"' , FoodCategory = '"+msg[13]+"' , Price = "+msg[17]+" Where Dish_No = "+msg[5]
            print(Command)
            Cursor.execute(Command)
            MyDb.commit()
            Command="Update "+name1+" Set DishName = '"+DName+"' , Quantity = "+msg[15]+" Where Dish_No = "+msg[5]
            print(Command)
            Cursor.execute(Command)
            MyDb.commit()
            Client.send("Ok".encode('ascii'))

        elif msg[1]=="GetTheCanteensList":
            Command="select CollegeName,CanteenName,CanteenAddress,PhNo from seller_shop_detailes"
            Cursor.execute(Command)
            res=Cursor.fetchall()
            no=len(res)
            print(res)
            ans=""
            for i in res:
                ans = ans+"//CollegeName&&"+i[0]+"&&CanteenName&&"+i[1]+"&&Address&&"+i[2]+"&&Phno&&"+str(i[3])
            Client.send((str(no)+"**"+ans).encode('ascii'))

        elif msg[1]=="GetTheFoodListForCustomer":
            Command="Select FoodListTableName,OrdersListTableName,CollegeName,CanteenName from seller_foodtable_name where Phno = "+msg[3]
            Cursor.execute(Command)
            res=Cursor.fetchall()
            print(res)
            name=res[0][0]
            name1=res[0][1]
            clgname=res[0][2]
            canteenName=res[0][3]
            No=str(len(res))
            Command = "Select * from " + name + " Where Dish_No in "+"(Select Dish_No from " + name1 + " WHERE FoodStatus ='Enable') Limit 5"
            print(Command)
            Cursor.execute(Command)
            res = Cursor.fetchall()
            print(res)
            No = str(len(res))
            ans=No+"**"
            for i in res:
                ans=ans+"//ItemNo&&"+str(i[0])+"&&DishName&&"+i[1]+"&&ImageNo&&"+str(i[2])+"&&Type&&"+i[4]+"&&Category&&"+i[5]+"&&Price&&"+str(i[6])+"&&CanteenName&&"+canteenName+"&&CollegeName&&"+clgname
                print(ans)
            Client.send((ans).encode('ascii'))
        elif msg[1]=="GetTheSelectedFoodDetailes":
            Command = "Select FoodListTableName,OrdersListTableName,CollegeName,CanteenName from seller_foodtable_name where Phno = " +msg[3]
            Cursor.execute(Command)
            res = Cursor.fetchall()
            print(res)
            name = res[0][0]
            name1 = res[0][1]
            clgname = res[0][2]
            canteenName = res[0][3]
            No = str(len(res))
            Command="Select CanteenAddress from seller_shop_detailes where Phno = "+msg[3]
            Cursor.execute(Command)
            res=Cursor.fetchall()
            Address=res[0][0]
            Command="Select * from "+name+" where Dish_No = "+msg[5]
            Cursor.execute(Command)
            res=Cursor.fetchall()
            i=res[0]
            ans="&&FoodName&&"+i[1]+"&&ImageNO&&"+str(i[2])+"&&FoodType&&"+i[4]+"&&FoodCategory&&"+i[5]+"&&CollegeName&&"+clgname+"&&CanteenName&&"+canteenName+"&&CanteenAddress&&"+Address+"&&Price&&"+str(i[6])+"&&ItemNo&&"+str(i[0])
            Client.send(ans.encode('ascii'))
            print(res)
        elif msg[1]=="CheckQuantityAvailabel":
            Command = "Select OrdersListTableName from seller_foodtable_name where Phno = " +msg[3]
            Cursor.execute(Command)
            res = Cursor.fetchall()
            print(res)
            Command="Select Quantity From "+res[0][0]+" Where Dish_No = "+msg[5]
            Cursor.execute(Command)
            res=Cursor.fetchall()
            print(res)
            if(res[0][0]>=int(msg[7])):
                result="Ok"
            else:
                result="Error"
            Client.send(result.encode('ascii'))
        elif msg[1]=="GettheOrderedFoodList":
            ColumnName=["Item1_No_Quantity","Item2_No_Quantity","Item3_No_Quantity","Item4_No_Quantity","Item5_No_Quantity"]
            OrderColumnName=["Item1_No_Quantity_Price","Item2_No_Quantity_Price","Item3_No_Quantity_Price","Item4_No_Quantity_Price","Item5_No_Quantity_Price"]
            print("ya")
            ans=msg[2].split("&&")
            Command = "Select FoodListTableName,OrdersListTableName from seller_foodtable_name where Phno = " +ans[3]
            Cursor.execute(Command)
            res=Cursor.fetchall()
            name=res[0][0]
            name1=res[0][1]
            cost=0
            c=0
            while True:
                otp = random.randint(100000, 999999)
                Command="Select * from all_orders_customer_seller where OrderNo = "+str(otp)
                Cursor.execute(Command)
                so=Cursor.fetchall()
                if(len(so)==0):
                    break

            Detailes="("+ans[1]+","+ans[3]
            OrderInfo="("+str(otp)+","+ans[1]+","+ans[3]

            for i in range(5,len(ans)-1):
                sol=ans[i].split("**")
                ItemNoQty=",'"+sol[0]+"_"+sol[1]+"'"
                Detailes=Detailes+ItemNoQty
                Command= "Select Price from "+name+" Where Dish_No = "+sol[0]
                Cursor.execute(Command)
                res1=Cursor.fetchall()
                cost=cost+(int(sol[1])*float(res1[0][0]))
                ItemNoQtyPrice=",'"+sol[0]+"_"+sol[1]+"_"+str(res1[0][0])+"'"
                OrderInfo=OrderInfo+ItemNoQtyPrice

                Command = "Select * from "+name1+" Where Dish_No = "+sol[0]
                Cursor.execute(Command)
                res2=Cursor.fetchall()
                Qty=res2[0][2]-int(sol[1])
                Pending=res2[0][3]+int(sol[1])
                Total=res2[0][5]+int(sol[1])

                Command="Update "+name1+" Set Quantity = "+str(Qty)+", PendingOrders = "+str(Pending)+",TotalOrders = "+str(Total)+" where Dish_No = "+sol[0]
                Cursor.execute(Command)
                MyDb.commit()
                c=c+1

            Detailes=Detailes+","+str(cost)+",'Ordered',"+str(otp)+")"
            Detailes1="(CustomerNo,SellerNo"

            OrderInfo = OrderInfo + "," + str(cost) + ",'Ordered')"
            OrderInfo1="(OrderNo,CustomerNo,SellerNo"
            for i in range(0,c):
                Detailes1=Detailes1+","+ColumnName[i]
                OrderInfo1=OrderInfo1+","+OrderColumnName[i]
            Detailes1=Detailes1+",TotalPrice,Status,OrderNo)"
            Command="Insert Into all_orders_customer_seller "+Detailes1+" values "+Detailes
            print(Command)
            Cursor.execute(Command)
            MyDb.commit()

            OrderInfo1=OrderInfo1+",TotalCost,Status)"
            TableName="customer_"+ans[1]+"_orders"
            Command ="Insert Into "+TableName+" "+OrderInfo1+" Values "+OrderInfo
            print(Command)
            Cursor.execute(Command)
            MyDb.commit()
            TableName="seller_"+ans[3]+"_orders"
            Command="Insert Into "+TableName+" "+OrderInfo1+" Values "+OrderInfo
            Cursor.execute(Command)
            MyDb.commit()
            Detailes="OrderNo&&"+str(otp)+"&&Cost&&"+str(cost)
            Client.send(Detailes.encode('ascii'))
            print(ans)

        elif msg[1]=="GettheOrdersDetailes":
            TableName="customer_"+msg[3]+"_orders"
            Command="Select SellerNo,OrderNo from "+TableName+" Limit 5"
            Cursor.execute(Command)
            res=Cursor.fetchall()
            no=len(res)
            ans="OrderedDetailes**"+str(no)+"**"
            for i in res:
                Command="Select CollegeName,CanteenName,CanteenAddress from seller_shop_detailes Where Phno = "+str(i[0])
                Cursor.execute(Command)
                res1=Cursor.fetchall()
                ans=ans+"//&&PhNo&&"+str(i[0])+"&&CollegeName&&"+res1[0][0]+"&&CanteenName&&"+res1[0][1]+"&&CanteenAddress&&"+res1[0][2]+"&&OrderNo&&"+str(i[1])

            Client.send(ans.encode('ascii'))

        elif msg[1]=="GetTheOrderFoodList":
            TableName="customer_"+msg[3]+"_orders"
            Command="Select * from "+TableName+" Where OrderNo = "+msg[5]
            print(Command)
            Cursor.execute(Command)
            res=Cursor.fetchall()
            print(res)
            SellerNo=res[0][2]
            ans="OrderNo&&"+str(res[0][0])+"&&Status&&"+res[0][9]+"&&TotalCost&&"+str(res[0][8])
            Command="Select FoodListTableName from seller_foodtable_name where Phno = "+str(res[0][2])
            Cursor.execute(Command)
            sol = Cursor.fetchall()
            for i in range(3,8):
                if res[0][i]==None:
                    break
                else:
                    a=res[0][i].split("_")
                    Command="Select DishName,ImageNo,FoodType,FoodCategory from "+sol[0][0]+" Where Dish_No = "+a[0]
                    print(Command)
                    Cursor.execute(Command)
                    b = Cursor.fetchall()
                    ans=ans+"//ItemNo&&"+a[0]+"&&Quantity&&"+a[1]+"&&Price&&"+a[2]+"&&DishName&&"+b[0][0]+"&&ImageNo&&"+str(b[0][1])+"&&FoodType&&"+b[0][2]+"&&FoodCategory&&"+b[0][3]
            print(ans)

            Client.send(ans.encode('ascii'))
        elif msg[1]=="GetTheSellerOrdersList":
            TableName="seller_"+msg[3]+"_orders"
            Command="Select * from "+TableName+" Limit 10"
            Cursor.execute(Command)
            res=Cursor.fetchall()
            print(res)
            ans=""

            for i in res:
                count=0
                for j in range(3,8):
                    if i[j]==None:
                        break
                    else:
                        count=count+1
                ans=ans+"//OrderNo&&"+str(i[0])+"&&TotalCost&&"+str(i[8])+"&&Status&&"+i[9]+"&&ItemsCount&&"+str(count)
            Client.send(ans.encode('ascii'))

        elif msg[1]=="GetSellerOrderFoodDetailes":
            TableName="seller_"+msg[3]+"_orders"
            Command="Select FoodListTableName from seller_foodtable_name WHERE PhNo="+msg[3]
            Cursor.execute(Command)
            res = Cursor.fetchall()
            print(res)
            TableName1=res[0][0]
            Command="Select * from "+TableName+" Where OrderNo="+msg[5]
            Cursor.execute(Command)
            res = Cursor.fetchall()
            print(res)
            Detailes="//**OrderStatus**"+res[0][9]+"**Price**"+str(res[0][8])+"**//"
            for i in res:
                for j in range(3,len(i)-2):
                    if(i[j]!=None):
                        ans=i[j].split("_")
                        Command="Select DishName,ImageNo,FoodType,FoodCategory from "+TableName1+" Where Dish_No="+ans[0]
                        print(Command)
                        Cursor.execute(Command)
                        sol=Cursor.fetchall()
                        print(sol)
                        Detailes=Detailes+"**DishNo**"+ans[0]+"**DishName**"+sol[0][0]+"**ImageNo**"+str(sol[0][1])+"**Quantity**"+ans[1]+"**Price**"+ans[2]+"**FoodType**"+sol[0][2]+"**FoodCategory**"+sol[0][3]+"**//"
            print(Detailes)
            Client.send(Detailes.encode('ascii'))

    except:
        print("Error occured man")
    print(msg)
def RecieveMessage(Client):
    while True:
        try:
            msg = Client.recv(1024)
            print(msg.decode("ascii"))
            check(msg,Client)
        except:
            print("The ", Client, "Has left")
            break

def SendMessage(Client):
    while True:
        try:
            message=input("")
            Client.send(message.encode('ascii'))
        except:
            print("Error occured")
def AcceptServer():
    while True:
        clt,adr=s.accept()
        print("connection to ",clt,"Was Sucessfully done   ",adr)
        T1=threading.Thread(target=RecieveMessage ,args=(clt,))
        T2=threading.Thread(target=SendMessage,args=(clt,))
        T1.start()
        T2.start()

AcceptServer()
