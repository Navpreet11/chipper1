import streamlit as st
import sqlite3
from PIL import Image
from datetime import datetime,timedelta
import uuid

logot=Image.open("logo.png")

st.set_page_config(page_title="Chipper",page_icon=logot)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



st.markdown("<center><img src=https://img.icons8.com/fluency/500/soulseek.png; alt=centered image; height=200; width=200> </center>",unsafe_allow_html=True)

textcolor= """
    <style>
    .gradient-text{
        background: linear-gradient(to left,#3CCBF4,#2DB4EC,#20A2E6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family:serif;font-weight: 800;font-style:italic;color:#1A6DFF;text-align:center;font-size:40px;
    }
    </style>
    """
st.markdown(textcolor,unsafe_allow_html=True)

st.markdown('<p class="gradient-text">Chipper</p>', unsafe_allow_html=True)

st.divider()


db = sqlite3.connect('chipperdata.db')
c= db.cursor()


c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        email TEXT)
""")

c.execute('''CREATE TABLE IF NOT EXISTS sessions
             (user_id TEXT, last_active DATETIME)''')


db.commit()



button_style = '''
    <style>
        .stButton button {
            background: linear-gradient(to left,#3CCBF4,#2DB4EC,#20A2E6);
            color: #FFFFFF; 
            border-color:#2DB4EC; 
        }
    </style>
'''


st.markdown(button_style, unsafe_allow_html=True)
st.markdown('<style>.stButton>button { margin-left: auto; margin-right: auto; display: block; }</style>', unsafe_allow_html=True)




textcolor= """
    <style>
    .textlogin{
        background: linear-gradient(to left,#3CCBF4,#2DB4EC,#20A2E6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family:serif;font-style:italic;color:#1A6DFF;text-align:left;font-size:30px;
    }
    </style>
    """
st.markdown(textcolor,unsafe_allow_html=True)


textcolor= """
    <style>
    .text{
        background: linear-gradient(to left,#3CCBF4,#2DB4EC,#20A2E6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family:serif;font-style:italic;color:#1A6DFF;text-align:center;font-size:30px;
    }
    </style>
    """
st.markdown(textcolor,unsafe_allow_html=True)




        
def main():
    user_id = get_cookie()
   
    if user_id:
        app()
    else:
        login()
#def is_user_logged_in():
    #return st.session_state.get('username') is not None


def generate_unique_id():
    # Generate a unique identifier for the user
    return str(uuid.uuid4())


def set_cookie(user_id):
    expiry_date = datetime.now() + timedelta(days=30)
    expiry_str = expiry_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
    cookie_value = f"user_id={user_id}; expires={expiry_str};"
    st.experimental_set_query_params(cookie=cookie_value)
    

def get_cookie():
    params = st.experimental_get_query_params()
    return params.get("cookie", "")



def login():
    st.markdown("<p class='textlogin'>Login</p>", unsafe_allow_html=True)
    

    username = st.text_input("",placeholder="Username", key="login_username")
    password = st.text_input("",placeholder="Password", type="password", key="login_password")

    if st.button("Double tap to Login"):
        if not username  or not password :
            st.error("Please enter your full credentials!")
        else:
            
            c.execute("SELECT *FROM users WHERE username=? AND password=?" ,(username,password))
            resu=c.fetchone()
            if resu:
                 
                 user_id = generate_unique_id()  
                 set_cookie(user_id)
                 #set_user_logged_in(username)
            else:
                st.error("Invalid username or password !")
    st.write("___")
  
   
    st.markdown("<p class='text'>Don't have an account </p>", unsafe_allow_html=True)
    
    if st.button("Register"):
        st.session_state.show_signup_form = True

    if st.session_state.get('show_signup_form'):
        signup()


def signup():
    textcolor= """
    <style>
    .textsignup{
        background: linear-gradient(to left,#3CCBF4,#2DB4EC,#20A2E6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family:serif;font-style:italic;color:#1A6DFF;text-align:left;font-size:30px;
    }
    </style>
    """
    st.markdown(textcolor,unsafe_allow_html=True)
    st.markdown("<p class='textsignup'>Registration</p>", unsafe_allow_html=True)
    
    new_username = st.text_input("",placeholder="Please enter your new username", key="signup_username")
    new_password = st.text_input("",placeholder="Please enter your new password", type="password", key="signup_password")
    #new_email= st.text_input("",placeholder="Please enter email", key="signup_email")
    if st.button("Register now!"):
        if not new_username or not new_password :
            st.error("Please enter full credentials!")
        else:
             c.execute("SELECT * FROM users WHERE username=? AND password=?", (new_username,new_password))
             exiuser= c.fetchone()
             if exiuser:
                 st.error("Username already taken !")
             else :
                query = "INSERT INTO users (username, password) VALUES (?, ?)"
                c.execute(query, (new_username,new_password))
                db.commit()
                st.success("Account created you may Login now")
            






#def set_user_logged_in(username):
    #st.session_state.username = username




def app():
    st.success("hello")







if __name__=="__main__":
    main()
    c.close()
    db.close()
