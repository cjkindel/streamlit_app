import streamlit as st
import openapi_client
import os
import time

os.system("pip install openapi_client-1.0.0-py3-none-any.whl")

import openapi_client
from openapi_client.models.list_organizations_response_content import ListOrganizationsResponseContent
from openapi_client.rest import ApiException

st.title("E28 Service Manual Bot")

configuration = openapi_client.Configuration(
    access_token = st.secrets["GRIPTAPE_API_KEY"]
)

ORG_ID="336f3f9e-171b-4fdd-981f-eb3404b5634e"
ENV_ID="ae7bb6f3-624a-49d9-8498-b5d9875cd98f"
APP_ID="e9b9c088-0238-4ebe-8fad-fdac2fa1efe9"
DEP_ID="6c11a569-22ab-4363-a217-c6d9b9e4c5b7"
SES_ID="fea09900-1b12-4dea-8e03-4b04c7d8e50b"

def create_run(question):
    with openapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.RunsApi(api_client)
        create_run_request_content = openapi_client.CreateRunRequestContent.from_dict({"args": [question]})

        try:
            api_response = api_instance.create_run(APP_ID, create_run_request_content=create_run_request_content)
        except Exception as e:
            print("Exception: %s\n" % e)
        return api_response.run_id

def poll_run_status(run_id):
    with openapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.RunsApi(api_client)
        status=""
        print(run_id)
        while status != "SUCCEEDED":
            try:
                time.sleep(2)
                api_response = api_instance.get_run(run_id)
                print(api_response.status.value)
                status = api_response.status.value
            except Exception as e:
                print("Exception: %s\n" % e)
    return api_response.output.value

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you with your E28?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Create Run
    run_id = create_run(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = ""

        # Poll Run Status
        response = poll_run_status(run_id)

        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})