import streamlit as st
from MotionAPI_UserClass import User
from Buttons import *
import pandas as pd

from math import ceil

st.set_page_config(layout="wide")

def setup():
    st.session_state["all_posts_url"] = "https://motion.propulsion-home.ch/backend/api/social/posts/"
    st.session_state["all_friend_posts_url"] = "https://motion.propulsion-home.ch/backend/api/social/posts/friends/"
    st.session_state["all_buttons"] = []
    st.session_state["buttons"] = {}
    st.session_state.post_page = 1
    st.session_state.friend_page = 1
    st.session_state.setup = True

if "setup" not in st.session_state:
    setup()

# GUI
if "user" in st.session_state: # user is logged in

    user = st.session_state.user
    
    top_menu = st.columns(6)

    create_button("Home", container=top_menu[0], icon= ":material/home:")
    create_button("Post",container = top_menu[1], icon=":material/post_add:")
    create_button("Friend Area", container=top_menu[2], icon=":material/text_snippet:")
    create_button("User", container=top_menu[3],icon=":material/person:")
    create_button("Log out", container = top_menu[4], icon = ":material/logout:")
    create_button("Refresh Posts", container = top_menu[5], icon = ":material/refresh:", 
                    callback=delete_cache_and_session_state, 
                    args=[
                        user.get_all_posts,
                        ["all_posts_url","all_friend_posts_url","post_page","friend_page"],
                        ["https://motion.propulsion-home.ch/backend/api/social/posts/",
                         "https://motion.propulsion-home.ch/backend/api/social/posts/friends/",
                         1,1]
                         ],
                    track=False
                    )

    # Functionalitys of buttons

    # Home button - just unclick everything and rerun
    if is_clicked("Home"):
        unclick()
        st.rerun()

    # Post button - create a form with a text input field and post whatever the user inputs
    if is_clicked("Post"):
        with st.form("Post something"):
            text_to_post = st.text_input("Post")
            left, right = st.columns([1,1])
            submitted = left.form_submit_button("Post")

            if right.form_submit_button("Cancel"):
                unclick()
                st.rerun()

            if submitted:
                if text_to_post:
                    user.post_message(text_to_post)
                    st.success("Posted successfully")
                    unclick()
                else:
                    st.error("Empty Field")

    if is_clicked("Friend Area"):
        with st.spinner("Checking out friend requests"):
            sent_friend_requests, received_friend_requests = user.get_friend_requests()
        left, middle, right = st.columns([2,2,1])

        create_button("Sent Requests", container = left, 
                      icon = ":material/refresh:", callback=toggle_click, 
                      args = ["Sent Requests",["Received Requests"]]
                      )
        
        create_button("Received Requests", container = middle, 
                      icon = ":material/refresh:", callback=toggle_click, 
                      args = ["Received Requests",["Sent Requests"]]
                      )
        
        create_button("Refresh", container=right, 
                      icon = ":material/refresh:", callback=delete_cache, 
                      args = [user.get_friend_requests], track = False
                      )
        
        if is_clicked("Sent Requests"):
            if sent_friend_requests:
                for fr in sent_friend_requests:
                    with st.container(key = f"fr_to_{fr['receiver']['id']}"):
                        left,_,_ = st.columns([8,1,1])
                        left.write(f"{fr['receiver']['first_name']} {fr['receiver']['last_name']}")
            else:
                st.write("You have no sent out Friend Requests right now")

        if is_clicked("Received Requests"):
            if received_friend_requests:
                st.write(received_friend_requests)
                for fr in sent_friend_requests:
                    with st.container(key = f"fr_from_{fr['requester']['id']}"):
                        left,middle,right = st.columns([8,1,1])
                        left.write(f"{fr['requester']['first_name']} {fr['requester']['last_name']}")
                        create_button(" ", container =middle, 
                                      callback=User.handle_friend_request, args = [user, fr, "A"],
                                      icon = ":material/refresh:", key = f"accept_button_{fr['requester']['id']}", track = False
                                      )
            else:
                st.write("You have no received Friend Requests right now")
            
        with st.spinner("Loading Posts"):
            friend_posts, next, previous, count = user.get_all_posts(st.session_state["all_friend_posts_url"])
        for name, post in friend_posts:
            left, right = st.columns([1,3])
            left.write(name)
            right.write(post)
        _,left,middle,right,_ = st.columns([2,3,1,3,2])
        if previous:
            create_button("Previous", container = left, icon = ":material/arrow_back:",
                        callback= update_session_state, args = [["all_friend_posts_url","friend_page"],[previous,st.session_state.friend_page-1]], track = False
                        )
        nr_of_pages = ceil(count/25)
        middle.write(f"{st.session_state.friend_page} / {nr_of_pages}")
        if next:
            create_button("Next", container = right, icon = ":material/arrow_forward:",
                        callback= update_session_state, args = [["all_friend_posts_url","friend_page"],[next,st.session_state.friend_page+1]], track= False
                        )
        

    if is_clicked("User"):
        user_menu = st.columns([4,1])
        create_button("User Settings", container=user_menu[1], icon = ":material/settings:")
        if is_clicked("User Settings"):
            pass
        else:
            user_menu[0].dataframe(user.get_current_user(), width = 1000)

    # Log out button - del user from session_state and rerun
    if is_clicked("Log out"):
        del st.session_state.user
        unclick()
        st.rerun()

    # Default: Show Posts
    if not any_button_clicked():
        with st.spinner("Loading"):
            posts, next, previous, count = user.get_all_posts(st.session_state["all_posts_url"])
        for name, post in posts:
            left, right = st.columns([1,3])
            left.write(name)
            right.write(post)
        _,left,middle,right,_ = st.columns([2,3,1,3,2])
        if previous:
            create_button("Previous", container = left, icon = ":material/arrow_back:",
                          callback= update_session_state, args = [["all_posts_url","post_page"],[previous,st.session_state.post_page-1]], track = False
                          )
        nr_of_pages = ceil(count/25)
        middle.write(f"{st.session_state.post_page} / {nr_of_pages}")
        if next:
            create_button("Next", container = right, icon = ":material/arrow_forward:",
                          callback= update_session_state, args = [["all_posts_url","post_page"],[next,st.session_state.post_page+1]], track = False
                          )
            
    if st.checkbox("Debug Session state"):
        st.session_state

        
else: # Log in form
    _,middle,_ = st.columns([1,2,1])
    with middle.form(key = "login-form", enter_to_submit=True):
        email = st.text_input("email")
        password = st.text_input("password", type = "password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if email and password:
                user = User(email, password)
                if user.login_data:
                    st.success("Login successful")
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid Name / Password")
            else:
                st.error("Please enter something")