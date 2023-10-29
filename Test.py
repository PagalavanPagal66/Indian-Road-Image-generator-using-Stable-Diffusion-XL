PAT = '51fd09675a8e4b0684f8052bff6d7258'
USER_ID = 'stability-ai'
APP_ID = 'stable-diffusion-2'
MODEL_ID = 'stable-diffusion-xl'
MODEL_VERSION_ID = '0c919cc1edfc455dbc96207753f178d7'
USER_ID_2 = 'clarifai'
APP_ID_2 = 'main'
MODEL_ID_2 = 'general-image-recognition'
MODEL_VERSION_ID_2 = 'aa7f35c01e0642fda5cf400f543e7c40'

import WorkflowTest as wft

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

def get_chatgpt_response(content):
    messages = [
        {"role": "system",
         "content": """ You are now the prompt giver for my text inputs. 
                        Please give the correct prompt which should given to image generation models.
                        The image generated should be used for dataset creation for AI - self driving car from a drivers view, give very realistic image according to that.
                        Sample prompt : A highly photorealistic image of a off road race track , complete with precise replicas of the world’s most iconic heavy noun, captured at the moment of a sharp turn, with smoke and sparks flying from under the wheels and the noun drifting around the bend. The image captures the excitement of the moment, with happy and noisy fans cheering and waving in the background. (The image is depicted at dusk, with the headlights.
                        """  },
        {"role": "user", "content": content},
        {"role": "assistant", "content": "Consider the system content and give the results" }
    ]
    response = openai.ChatCompletion.create(
    model=model_engine,
    messages=messages
    )
    generated_text = response['choices'][0]['message']['content']
    st.write(generated_text)
    return  generated_text

def generate_image(prompt):

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=prompt
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    output = post_model_outputs_response.outputs[0]

    base64_image = output.data.image.base64
    image_filename = f"Output_image.jpg"
    with open(image_filename, 'wb') as f:
        f.write(base64_image)

    print("Generated successfully")
    st.image(base64_image)

def image_to_text(path):
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', 'Key ' + PAT),)
    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID_2, app_id=APP_ID_2)
    IMAGE_FILE_LOCATION = path
    with open(IMAGE_FILE_LOCATION, "rb") as f:
        file_bytes = f.read()
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            model_id=MODEL_ID_2,
            version_id=MODEL_VERSION_ID_2,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=file_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)
    output = post_model_outputs_response.outputs[0]

    print("Predicted concepts:")
    for concept in output.data.concepts:
        print("%s %.2f" % (concept.name, concept.value))
    print(output.data.concepts)
    return output.data.concepts


import openai
import api_key

openai.api_key = api_key.API_KEY
model_engine = "gpt-3.5-turbo-16k"

import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

@st.cache_data
def load_image(image_file):
    img= Image.open(image_file)
    return img

page_by_img ="""
<style>
#Mainmenu {visibility : hidden;}
footer {visibility : hidden;}
header {visibility :hidden;}
}
</style>
"""
st.markdown(page_by_img,unsafe_allow_html=True)

st.title("Hello USERS !!!")


value = st.selectbox("OPERATION : " , ("TEXT",'IMAGE',"MULTIPLE GENERATION"),key="YES")


if(value == "TEXT"):
    text = st.text_input("Please enter some text to generate image")
    if (st.button("SUBMIT")):
        prompt = get_chatgpt_response(text)
        print("PROMPT" , prompt)
        st.write(prompt)
        generate_image(prompt)
        st.success("GENERATED")

if(value == 'MULTIPLE GENERATION'):
  on = st.radio(
    "What type of generation",
    ["Random", "Selection"])
  if(on=="Random"):
    count = st.slider('How many images do you want?', 0, 25, 2)
    if(st.button("SUBMIT")):
        wft.random_generation(count)


  else:
    options = st.multiselect('Choose the climate : ',["Sunny days", "Rainy days with wet roads", "Foggy conditions", "Snow-covered roads","Spring", "Autumn", "summer fall", "winter scenes","Autumn leaves covering the road", "Rainbows after a rain shower"])
    options2 = st.multiselect('Choose the vehicles : ',["Cars", "trucks", "bicycles","Police cars", "Ambulances and emergency vehicles", "Public transportation", "vans"])
    options3 = st.multiselect('Choose the environment : ',["Urban roads with buildings", "traffic signals", "streetlights", "Rural roads with fields", "farms", "Mountain",
     "trees", "Coastal roads with beaches", "oceans","Highways", "city roads", "rural roads", "urban roads","Straight roads", "Curvy roads", "Intersections", "Roundabouts", "Bridges and tunnels", "Road gradients"])
    options4 =  st.multiselect('Choose the other things : ',["Traffic signs", "Herds of goats", "Road markings","Stop signs", "Speed limit signs", "Directional signs", "Traffic lights","Birds flying or perched on road signs", "Squirrels or small animals crossing the road","Historical buildings", "monuments", "Churches", "temples", "mosques","Fallen trees or branches", "Construction debris", "Potholes", "road damage", "Wildfire smoke or haze","Sporting events", "marathons", "cycling races", "Festivals", "celebrations", "Political rallies", "gatherings"])
    if(st.button("SUBMIT")):
         st.write(options + options2 + options3 + options4)
         data_str = "Indian roadside realistic image with "
         for iter in options:
             data_str+=str(iter)+" "
         for iter in options2:
             data_str+=str(iter)+" "
         for iter in options3:
             data_str+=str(iter)+" "
         for iter in options4:
             data_str+=str(iter)+" "
         prompt = get_chatgpt_response(data_str)
         st.write(prompt)
         generate_image(prompt)


if(value=="IMAGE"):
    image_file = st.file_uploader("Choose a IMAGE file",type=['png','jpeg','jpg'],key="IMAGE_UPLOAD")
    if image_file is not None:
        file_details = {"Filename":image_file.name,"FileType":image_file.type}
        st.write(file_details)
        img = load_image(image_file)
        st.image(img)
        with open("C:\\Users\\pagal\\PycharmProjects\\TEXT\\Minus_1_Hack\\TEST_IMAGE.jpg","wb")as f:
            f.write(image_file.getbuffer())
        st.success("IMAGE SAVED")
        dict =image_to_text("C:\\Users\\pagal\\PycharmProjects\\TEXT\\Minus_1_Hack\\TEST_IMAGE.jpg")
        data_str = "Indian roadside realistic image with "
        for iter in dict:
            data_str = data_str+" "+str(iter.name)
        st.write(data_str)
        prompt = get_chatgpt_response(data_str)
        print(prompt)
        st.write(prompt)
        generate_image(prompt)
