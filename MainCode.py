from tabulate import tabulate 
import mysql.connector as sqlcon 
import random 
mycon=sqlcon.connect(host='localhost',user='root',passwd='12345',database='SHOP') 
cur=mycon.cursor() 
def enterbill(ebill,discount,amount): 
x=""+str(ebill) 
blist=[] 
cur.execute('select BILL_NO from bill') 
bdata=cur.fetchall() 
for i in bdata: 
for j in i: 
blist.append(j) 
while True: 
i=random.randint(100000,999999) 
if i not in blist: 
            billno=i 
            break 
    cur.execute('INSERT INTO BILL VALUES (%s,%s,%s,%s)',(billno,x,discount,amount)) 
    mycon.commit()      
def buy(): 
    cur.execute('select sno,pcode,product,price from products') 
    data=cur.fetchall() 
    head=['S.no','PCode','Product Name','Price'] 
    print(tabulate(data, headers=head, tablefmt="grid")) 
    b,l,ebill=[],[],[] 
    total=0 
    while True: 
                st=input('Enter the S.no of the product you want to buy or press N to exit: ') 
                if st not in ['N','n']: 
                    st=int(st) 
                    for i in data: 
                        if i[0]==st: 
                            b.append(i[0]) 
                            ebill.append([i[2],i[3]]) 
                            total+=i[3]  
                else: 
                    flag=False 
                    cc=input('\nDo you have a discount coupon?(Y/N): ') 
                    if cc in ['Y','y']: 
                             dis=input('Enter dicount coupon code: ') 
                             cur.execute('select * from DISCOUNT_COUPONS') 
                             disdata=cur.fetchall() 
                             for d in disdata: 
                                 l.append(d[0])  
                             if dis.upper() not in l: 
                                 print('\nInvalid discount coupon code!') 
                             else: 
                                 for v in disdata: 
                                     if dis.upper()==v[0]: 
                                         total2=total-(total*v[1]/100) 
                                         print('\nDiscount coupon successfully applied!') 
                                         flag=True 
                                     else: 
                                         pass 
                    else:           
                        pass 
                    bill=[] 
                    for j in b: 
                        for k in data: 
                            if j==k[0]: 
                                bill.append([k[2],k[3]]) 
                    head2=['Product Name','Price'] 
                    print(tabulate(ebill, headers=head2, tablefmt="grid"))                     
                    if flag==True: 
                        print('\nInitial amount: ',total) 
                        print('Discounted amount: ',total2) 
                        print('Total amount to be paid is: ',total2) 
                        discount=total-total2 
                        enterbill(ebill,discount,total2) 
                        break 
                    else: 
                        print('Total amount to be paid is: ',total) 
                        enterbill(ebill,0,total) 
                        break 
  
def items(): 
    cur.execute('select * from products') 
    items=cur.fetchall() 
    head3=['S.no','PCode','Product Name','Price','Stock','Expiry Date'] 
print(tabulate(items, headers=head3, tablefmt="grid")) 
def bills(): 
cur.execute('select * from bill') 
bill=cur.fetchall()     
head4=['Bill no','Items','Discount','Total Amount'] 
print(tabulate(bill, headers=head4, tablefmt="grid")) 
while True: 
ch=int(input('\n1.Want to buy something?\n2.Administer your shop\n3.Exit\nEnter your choice: ')) 
if ch==1: 
buy() 
elif ch==2: 
while True: 
ad=int(input('\n1.Want to see the list of products present\n2.Want to revisit old bills\n3.Exit\nEnter your choice: ')) 
if ad==1: 
items() 
elif ad==2: 
bills() 
else: 
break            
else: 
break 
mycon.close() 
