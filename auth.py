import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

def auth():
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
    )

    tab1, tab2, tab3, tab4= st.tabs(["登陆", "注册", "忘记密码", "修改密码"])
    with tab1:
        authenticator.login(fields={'Form name':'登陆', 'Username':'用户名', 'Password':'密码', 'Login':'登陆'})
        if st.session_state["authentication_status"]:
            authenticator.logout(location='sidebar')
        
        elif st.session_state["authentication_status"] is False:
            st.error('密码错误🤔️')
    #elif st.session_state["authentication_status"] is None:
        #st.warning('')
    with tab3:
        try:
            if st.session_state["authentication_status"]:
                st.success('您还记得自己的密码, Congrats!🎉')
                
            
            

            else:
                username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password(fields={'Form name':'忘记密码😭', 'Username':'用户名', 'Submit':'提交'})
                if username_of_forgotten_password:
                    st.success(f'临时密码是: {new_random_password}, 请登录后更改')
                    with open('config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
        
                elif username_of_forgotten_password == False:
                    st.error('Username not found')
        
        except Exception as e:
            st.error(e)
    with tab2:
            if st.session_state["authentication_status"]:
                st.success('请不要帮别人注册哦😊')
            else:
                try:
                    email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(preauthorization=False,
                fields={'Form name':'用户注册👶', 'Email':'邮箱(请用公司邮箱注册)', 'Username':'用户名', 'Password':'密码', 'Repeat password':'重复密码', 'Register':'注册','Name':'姓名'},
                location='main',domains=['icekredit.com'])
                    if email_of_registered_user:
                        st.success('User registered successfully')
                        with open('config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                except Exception as e:
                    st.error(e)
    with tab4: 
        if st.session_state["authentication_status"]:
            try:
                if authenticator.reset_password(st.session_state["username"],fields={'Form name':'重置密码😄', 
             'Current password': '当前密码', 'New password':'新密码', 'Repeat password': '重复新密码', 'Reset':'重置'}):
                    st.success('修改成功🎉')
                    with open('config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
            except Exception as e:
                st.error(e)
        else:
            st.warning('请先登录哦😊')



