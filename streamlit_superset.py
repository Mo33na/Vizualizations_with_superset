import streamlit as st
import requests
import json

def fetch_guest_token_from_backend():
    url = 'http://localhost:8088/'
    username = 'admin'
    password = 'iamadmin'

    login_endpoint = f'{url}/api/v1/security/login'

    login_data = {
        'username': username,
        'password': password,
        'provider': "db"
    }

    session = requests.Session()
    response = session.post(login_endpoint, json=login_data)

    if response.status_code == 200:
        access_token = response.json().get('access_token')

        if access_token:
            #st.write("Access Token:", access_token)  # Display the access token in Streamlit (optional)

            guest_token_endpoint = f'{url}/api/v1/security/guest_token'
            headers = {'Authorization': f'Bearer {access_token}'}

            data = {
                "resources": [
                    {
                        "id": "8b2e8ee6-eda4-4477-a9ea-d0d97c991a2a",
                        "type": "dashboard"
                    }
                ],
                "rls": [],
                "user": {
                    "first_name": "Mona",
                    "last_name": "Pal",
                    "username": "admin"
                }
            }

            guest_token_response = session.post(guest_token_endpoint, json=data, headers=headers)
            if guest_token_response.status_code == 200:
                guest_token = guest_token_response.json().get('token')
                return guest_token  # Return the guest token

    return None  # Return None if unable to fetch the guest token

def main():
    # Fetch the guest token while loading the page
    guest_token = fetch_guest_token_from_backend()

    if guest_token:
        col1, col2 = st.columns([1,3])

        # Embedding the dashboard using HTML component
        with col2:
            st.header('Analytics using MPlad Dashboard')
            st.components.v1.html(
                f"""
                <div id="embed"></div>
                <script src="https://unpkg.com/@preset-sdk/embedded"></script>
                <script>
                    const mountPoint = document.getElementById("embed");
                    presetSdk.embedDashboard({{
                        id: "8b2e8ee6-eda4-4477-a9ea-d0d97c991a2a", 
                        supersetDomain: "http://localhost:8088/", 
                        mountPoint: mountPoint,
                        fetchGuestToken: () => "{guest_token}",
                        dashboardUiConfig: {{
                            filters: {{
                                expanded: false
                            }}
                        }}
                    }});
                    
                    document.getElementById("embed").children[0].width = "100%";
                    document.getElementById("embed").children[0].height = "1000px";
                </script>
                """,
                height=600
            )
    else:
        st.error("Failed to retrieve guest token.")

if __name__ == '__main__':
    main()