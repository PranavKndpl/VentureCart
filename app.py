import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
from PIL import Image
import io
from datetime import datetime
import pandas as pd
import time

def connect_db():
    conn = sqlite3.connect("Shop.db")
    return conn

def create_table():
    conn = connect_db()
    cur = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Customers (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Password TEXT,
        Gender TEXT,
        Email TEXT
    );
    '''
    cur.execute(create_table_query)

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Employee (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Age INTEGER,
        Password TEXT,
        Post TEXT,
        Email TEXT
    );
    '''

    cur.execute(create_table_query)

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Products (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Image BLOB NOT NULL,
        Price TExt NOT NULL
    );
    '''

    cur.execute(create_table_query)

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Purchase (
        Id INTEGER,
        Name TEXT NOT NULL,
        Time TIME,
        Price TEXT NOT NULL
    );
    '''
    cur.execute(create_table_query)

    
    cur.execute("SELECT COUNT(*) FROM Employee")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO Employee (Name, Age, Password, Post, Email) VALUES ('Pranav', 19, 'abc123', 'Manager', 'Pranav@gmail.com')")
    
    conn.commit()
    conn.close()

def Add_Customer(name, pas, gen, mail):
    conn = connect_db()
    cur = conn.cursor()

    insert_query = '''
    INSERT INTO Customers (Name, Password, Gender, Email)
    VALUES (?, ?, ?, ?);
    '''
    cur.execute(insert_query, (name, pas, gen, mail))
    conn.commit()
    conn.close()

def Add_Employee(name, age, pas, post, mail):
    conn = connect_db()
    cur = conn.cursor()

    insert_query = '''
    INSERT INTO Employee (Name, Age, Password, Post, Email)
    VALUES (?, ?, ?, ?, ?);
    '''
    cur.execute(insert_query, (name, age, pas, post, mail))
    conn.commit()
    conn.close()


st.markdown(
    """
    <style>
    .title {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if 'title' not in st.session_state:
    st.session_state.title = "Sign Up"


if 'signed_in_C' not in st.session_state:
    st.session_state.signed_in_C = False

if 'signed_in_E' not in st.session_state:
    st.session_state.signed_in_E = False

if 'signed_in_M' not in st.session_state:
    st.session_state.signed_in_M = False

if 'selected' not in st.session_state:
    st.session_state.selected = "Sign Up" 

title_placeholder = st.empty()
title_placeholder.markdown(f'<h1 class="title">{st.session_state.title}</h1>', unsafe_allow_html=True)

def signup():
    st.session_state.title = "Sign-Up"
    title_placeholder.markdown(f'<h1 class="title">{st.session_state.title}</h1>', unsafe_allow_html=True)
   
    Name = st.text_input("Enter your user Name")
    mail = st.text_input("Enter your user Email")
    Password = st.text_input("Enter your user Password", type="password")
    Repass = st.text_input("Enter your Password again", type="password")
    Gender = st.radio("Gender", options=["Male", "Female"])

    if st.button("Submit"):
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("SELECT Email FROM Customers WHERE Email = ?", (mail,))
        existing_email = cur.fetchone()

        if Name or mail or Password == "":
            st.error("Cannot leave Empty")
        elif existing_email:
            st.error("This email is already registered. Please use a different email.")
        elif Password != Repass:
            st.error("Passwords do not match.")
        else:
            Add_Customer(Name, Password, Gender, mail)
            st.success("User  registered successfully")

        conn.close()

def signin():
    st.session_state.title = "Sign-In"
    title_placeholder.markdown(f'<h1 class="title">{st.session_state.title}</h1>', unsafe_allow_html=True)
    mail = st.text_input("Enter your Email",placeholder="Manager id - Pranav@gmail.com")
    Password = st.text_input("Enter your Password", type="password",placeholder="Password - abc123") 
    if st.button("Login"):
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("SELECT Password FROM Customers WHERE Email = ?", (mail,))
        customer_result = cur.fetchone()

        if customer_result:
            if Password == customer_result[0]:
                st.success("User logged in successfully")
                st.session_state.signed_in_C = True
                time.sleep(0.5)
                st.rerun()
                
            else:
                st.error("Incorrect password for the user.")
        else:
            cur.execute("SELECT Password, Post FROM Employee WHERE Email = ?", (mail,))
            employee_result = cur.fetchone()

            if employee_result:
                if Password == employee_result[0]:
                    if employee_result[1] == 'Manager':
                        st.success("Manager logged in successfully")
                        st.session_state.signed_in_M = True
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.success("Employee logged in successfully")
                        st.session_state.signed_in_E = True
                        time.sleep(0.5)
                        st.rerun()
                    
                else:
                    st.error("Incorrect password for the employee.")
            else:
                st.error("Email not found. Please check your credentials.")

        conn.commit()
        conn.close()


def show_customer():
    conn = connect_db()
    cur = conn.cursor()

    st.session_state.title = "Customers"
    title_placeholder.markdown(f'<h1 class="title">{st.session_state.title}</h1>', unsafe_allow_html=True)

    cur.execute("SELECT * FROM Customers")
    result = cur.fetchall()
    if not result:
        st.write("No Customers")
    else:
        headers = ["Id","Name", "Password", "Gender", "Email"]
        data_dicts = [
        {headers[0]: row[0], headers[1]: row[1], headers[2]: row[2], headers[3]: row[3], headers[4]: row[4]}
        for row in result
    ]

        st.dataframe(data_dicts)

    conn.commit()
    conn.close()


def show_employee():
    conn = connect_db()
    cur = conn.cursor()

    st.session_state.title = "Employees"
    title_placeholder.markdown(f'<h1 class="title">{st.session_state.title}</h1>', unsafe_allow_html=True)

    cur.execute("SELECT * FROM Employee")
    result = cur.fetchall()
    headers = ["Id","Name", "Age", "Password", "Post", "Email"]
    data_dicts = [
        {headers[0]: row[0], headers[1]: row[1], headers[2]: row[2], headers[3]: row[3], headers[4]: row[4], headers[5]: row[5]}
        for row in result
    ]

    st.dataframe(data_dicts)

    conn.commit()
    conn.close()

def show_profit():
    st.session_state.title = "Purchases"
    title_placeholder.markdown(f'<h1 class="title">{st.session_state.title}</h1>', unsafe_allow_html=True)
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM Purchase")
    result = cur.fetchall()

    if not result:
        st.write("No Sales Yet")
        conn.commit()
        conn.close()
        return

    else:
        headers = ["Id","Name", "Time", "Price"]
        data_dicts = [
            {headers[0]: row[0], headers[1]: row[1], headers[2]: row[2], headers[3]: row[3]}
            for row in result
        ]

        st.dataframe(data_dicts)

    query = "SELECT Name FROM Purchase"
    df = pd.read_sql(query, conn)


    purchase_counts = df['Name'].value_counts().reset_index()
    purchase_counts.columns = ['Product Name', 'Number of Purchases']

    st.write("Purchase Counts by Product Name")
    st.bar_chart(purchase_counts.set_index('Product Name'))

    cur.execute("SELECT SUM(Price) FROM Purchase")
    total_profit = cur.fetchone()[0]  

    if total_profit is not None :
        st.write(f"Total Profit: ${total_profit:.2f}")
    else:
        st.write("No profit data available.")

    conn.commit()
    conn.close()

def add_employee():
    st.session_state.title = "Add Employee"
    title_placeholder.markdown(f'<h1 class="title">{st.session_state.title}</h1>', unsafe_allow_html=True)

    conn = connect_db()
    cur = conn.cursor()

    Name = st.text_input("Enter Employee Name")
    Age = st.number_input("Enter Age", min_value=0, step=1)
    Password = st.text_input("Enter Password", type = "password")
    Repass = st.text_input("Enter your Password again", type="password")
    Post = st.selectbox("Select Post",options=["","Employee","Manager"])
    mail = st.text_input("Enter Email")

    if st.button("Submit"):
        cur.execute("SELECT Email FROM Employee WHERE Email = ?", (mail,))
        existing_email = cur.fetchone()

        if Name == "Clear Database":
            cur.execute("DROP TABLE IF EXISTS Customers;")
            cur.execute("DROP TABLE IF EXISTS Employee;")
            cur.execute("DROP TABLE IF EXISTS Products;")
            cur.execute("DROP TABLE IF EXISTS Purchase;")
            st.success("Database cleared")

            conn.commit()
            conn.close()
            return
        
        elif Name or Password or mail == "":
            st.error("cannot leave empty")
        elif existing_email:
            st.error("This email user is already Employed.")
        elif Password != Repass:
            st.error("Passwords do not match.")
        else:
            Add_Employee(Name, Age, Password, Post, mail)
            st.success("Employee Added successfully")

    conn.commit()
    conn.close()

def Remove_customer():
    conn = connect_db()
    cur = conn.cursor()

    st.session_state.title = "Remove Customer"
    title_placeholder.markdown(f'<h1 class="title">{st.session_state.title}</h1>', unsafe_allow_html=True)

    customer_id = st.number_input("Enter Customer Id", min_value=0, step=1)

    customer_id = int(customer_id) if customer_id is not None else None

    if st.button("Remove Customer"):
    
        remove_query = 'DELETE FROM Customers WHERE Id = ?'
        
        cur.execute(remove_query, (customer_id,))
        
        if cur.rowcount > 0:
            st.success(f"Customer with ID {customer_id} has been removed.")
        else:
            st.warning(f"No customer found with ID {customer_id}.")
        
    
    conn.commit()
    conn.close()

def save_product(name, uploaded_file, price):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        st.write("Added Product Preview:")
        st.image(image, caption="Uploaded Image", use_container_width=True)
        st.write(f"Name:{name}\nPrice:{price}")
        
        img_bytes = io.BytesIO()
        image.save(img_bytes, format=image.format)
        img_bytes = img_bytes.getvalue()
        
        conn = connect_db()
        cur = conn.cursor()
        
        try:
            cur.execute("INSERT INTO Products (Name, Image, Price) VALUES (?, ?,?)", (name, img_bytes,price))
            conn.commit()
            st.success("Product Added Successfully")
        except Exception as e:
            st.error(f"Error saving image: {e}")
        finally:
            conn.close()

def selectProduct():
    st.session_state.title = "Add Product"
    title_placeholder.markdown(f'<h1 class="title">{st.session_state.title}</h1>', unsafe_allow_html=True)

    name = st.text_input("Enter Product Name")
    price = st.text_input("Enter the price of the image", value="0")  
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if st.button("Submit"):
        if uploaded_file is not None:
            try:
                price = float(price)
                save_product(name, uploaded_file, price)
            except ValueError:
                st.error("Please enter a valid price.")
        else:
            st.error("Please upload an image.")


def Buy_product():
    conn = connect_db()
    cur = conn.cursor()

    st.session_state.title = "Shop Products"
    title_placeholder.markdown(f'<h1 class="title">{st.session_state.title}</h1>', unsafe_allow_html=True)

    cur.execute("SELECT Id, Name, Image, Price FROM Products")
    results = cur.fetchall()
    
    if results:
        
        images = [(product_id, Name, Image.open(io.BytesIO(img_data)), Price) for product_id, Name, img_data, Price in results]
        
        cols = st.columns(3)  
        
        for i, (product_id, name, img, price) in enumerate(images):
            with cols[i % 3]:  
                st.image(img, caption=f"{name} \n - Price: ${price}", use_container_width=True) 
                
                if st.button("Add to Cart", key=f"buy_{product_id}"):
                    if 'cart' not in st.session_state:
                        st.session_state.cart = []  
                    st.session_state.cart.append((product_id, img, name, price))  
                    st.success(f"{name} has been added to your cart.")
    else:
        st.write("No Products available in shop yet")
    
    conn.close()

def Cart():

    st.session_state.title = "Your Cart"
    title_placeholder.markdown(f'<h1 class="title">{st.session_state.title}</h1>', unsafe_allow_html=True)

    conn = connect_db()
    cur = conn.cursor()

    if 'cart' in st.session_state and st.session_state.cart:
        cols = st.columns(3) 
        for index, (product_id, img, name, price) in enumerate(st.session_state.cart):
            with cols[index % 3]:
                st.image(img, caption=f"{name} \n - Price: ${price}", use_container_width=True) 
                
                if st.button(f"Remove {name}", key=f"remove_{index}"):
                    st.session_state.cart.pop(index) 
                    st.rerun() 

    else:
        st.write("Your cart is empty.")
        conn.commit()
        conn.close()
        return

    if st.button("Buy"):
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        
        for (product_id, img, name, price) in st.session_state.cart:
            cur.execute("INSERT INTO Purchase (Id, Name, Time, Price) VALUES (?, ?, ?, ?)", (product_id, name, current_time, price))
        
        conn.commit()
        conn.close()
        
        st.success("You have successfully purchased the items in your cart!")
        
        st.session_state.cart = []

def display_all_products():
    conn = connect_db()
    cur = conn.cursor()

    st.session_state.title = "Products"
    title_placeholder.markdown(f'<h1 class="title">{st.session_state.title}</h1>', unsafe_allow_html=True)

    cur.execute("SELECT Name, Image, Price FROM Products")
    results = cur.fetchall()
    
    if results:

        images = [(name, Image.open(io.BytesIO(img_data)), price) for name, img_data, price in results]
        
        cols = st.columns(3)  
        
        for i, (name, img, price) in enumerate(images):
            with cols[i % 3]:  
                st.image(img, use_container_width=True)  
                st.markdown(f"<div style='text-align: center;'><h5>{name}</h5><p>Price: {price}</p></div>", unsafe_allow_html=True)
                
    else:
        st.write("No images found in the database.")
    
    conn.close()

with st.sidebar:
    if st.session_state.signed_in_M:
        st.session_state.selected = option_menu('Manager Menu', ['Show Employees', 'Add Employee', 'Add Product', 'Show Sales','Logout'])

    elif st.session_state.signed_in_E:
        st.session_state.selected = option_menu('Employee Menu', ['Show Customers', 'Show Products', 'Remove Customer','Logout'])

    elif st.session_state.signed_in_C:
        st.session_state.selected = option_menu('Customer Menu', ['Buy Products', 'Show Cart','Logout'])

    else:
        st.session_state.selected = option_menu('Dashboard', ['Sign-Up', 'Sign In'])


if st.session_state.selected == "Sign-Up":
    signup()
elif st.session_state.selected == "Sign In":
    signin()

elif st.session_state.selected == "Show Employees":
    show_employee()
elif st.session_state.selected == "Add Employee":
    add_employee()
elif st.session_state.selected == "Add Product":
    selectProduct()
elif st.session_state.selected == "Show Sales":
    show_profit()

elif st.session_state.selected == "Show Customers":
    show_customer()
elif st.session_state.selected == "Show Products":
    display_all_products()
elif st.session_state.selected == "Remove Customer":
    Remove_customer()

elif st.session_state.selected == "Buy Products":
    Buy_product() 
elif st.session_state.selected == "Show Cart":
    Cart()

elif st.session_state.selected == 'Logout':
    
    st.session_state.signed_in_C = False
    st.session_state.signed_in_E = False
    st.session_state.signed_in_M = False
    st.session_state.selected = "Sign-Up"  
    st.rerun()  

create_table()
