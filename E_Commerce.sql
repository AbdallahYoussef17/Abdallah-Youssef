use E_Commerce
Create Table Customer(
CustomerID int identity(1,1) primary key ,
Fname varchar(50) not null,
Lname varchar(50),
Caddress varchar(50),
phone varchar(11) not null,
Email varchar(50),
CONSTRAINT chk_Email_Gmail CHECK (Email LIKE '%@gmail.com')
)

insert into Customer(Fname,Lname,Caddress,phone,Email)
values ('Mohamed','Youssef','Qus','01016196978','MohamedYoussef@gmail.com');

Create Table OrderCustomer(
OrderID int identity(1,1) primary key,
orderDate date ,
OrderStatus varchar(50) not null,
TotalAmount money not null,
CID INT REFERENCES  Customer(CustomerID)
)
create table category (
CategoryID int identity(1,1) primary key,
CategoryName varchar(50) not null,
)
Create table product(
ProductID int identity(1,1) primary key,
Pname varchar(50) not null,
price money not null,
Stock_Quantity int not null,
Categoryid int references category(CategoryID)
)
Create Table OrderItem(
OItemID int identity(1,1) primary key,
Quantity int not null,
Unit_Price money not null,
Orderid int references OrderCustomer(OrderID),
productid int references Product(ProductID)
)
create Table ShippingDetails(
ShippingID int identity(1,1) primary key,
SAddress varchar(50) not null,
Carrier varchar(50),
ShippingDate date,
Ord_id int references OrderCustomer(OrderID),
Alter table ShippingDetails add  ShippingStatus varchar(50)
)
create Table Payment(
PayID int identity(1,1) primary key,
PayMethod varchar(50) not null,
PayDate date,
PayStatus varchar(50),
Ordid int references OrderCustomer(OrderID)
)