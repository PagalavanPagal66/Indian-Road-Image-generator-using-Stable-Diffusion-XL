import random
import streamlit as st

prompts = [
    ["Highways", "city roads", "rural roads", "urban roads"],
    ["Straight roads", "Curvy roads", "Intersections", "Roundabouts", "Bridges and tunnels", "Road gradients"],
    ["Urban roads with buildings", "traffic signals", "streetlights", "Rural roads with fields", "farms", "Mountain",
     "trees", "Coastal roads with beaches", "oceans"],
    ["Sunny days", "Rainy days with wet roads", "Foggy conditions", "Snow-covered roads"],
    ["Cars", "trucks", "bicycles", "Traffic signs", "Herds of goats", "Road markings", "Emergency vehicles"],
    ["Daytime scenes with streetlights", "Daytime scenes without streetlights", "Nighttime scenes with streetlights",
     "Nighttime scenes without streetlights"],
    ["Spring", "Autumn", "summer fall", "winter scenes"],
    ["Parades or festivals on the road", "Construction sites with workers and machinery",
     "Accidents or emergency situations"],
    ["Driver's perspective from a car"],
    ["Roadside cafes or restaurants", "Gas stations", "Public transportation"],
    ["Paved roads", "Gravel roads", "Dirt roads", "Cobblestone streets"],
    ["Shops", "storefronts", "Houses", "residential buildings", "Office buildings", "Gas stations", "Advertisements"],
    ["Farmlands with crops", "barns", "Forests with trees"],
    ["Food stalls and markets", "Roadside cafes and restaurants", "Joggers and cyclists", "Children playing"],
    ["Construction sites with heavy machinery", "Road repairs", "workers", "Traffic diversions"],
    ["Police cars", "Ambulances and emergency vehicles", "Public transportation", "vans"],
    ["Street lamps", "decorative lighting", "Flower pots", "planters", "Sculptures", "monuments"],
    ["Sporting events", "marathons", "cycling races", "Festivals", "celebrations", "Political rallies", "gatherings"],
    ["Rivers", "bridges", "Lake"],
    ["Parking lots", "parked cars"],
    ["Stop signs", "Speed limit signs", "Directional signs", "Traffic lights"],
    ["Rain puddles on the road", "Snow-covered roads", "Stormy weather with lightning",
     "Mist", "fog", "sunset color", "sunrise color"],
    ["Birds flying or perched on road signs", "Squirrels or small animals crossing the road"],
    ["Car repair shops", "Hotels and motels", "Hospitals"],
    ["Historical buildings", "monuments", "Churches", "temples", "mosques"],
    ["Fallen trees or branches", "Construction debris", "Potholes", "road damage", "Wildfire smoke or haze"],
    ["Motorcycles", "scooters", "Public bicycles"],
    ["Street art and murals", "cultural festivals", "decorations"],
    ["Carnivals", "amusement parks", "Fireworks displays"],
    ["Autumn leaves covering the road", "Rainbows after a rain shower"],
    ["Elevated highways", "Train tracks"],
    ["Cultural processions and traditional dances", "Wedding processions with decorated cars"],
    ["Theaters and cinemas with movie posters"],
    ["Wildlife crossings and signs"]
]

PAT = '51fd09675a8e4b0684f8052bff6d7258'
USER_ID = 'stability-ai'
APP_ID = 'stable-diffusion-2'
MODEL_ID = 'stable-diffusion-xl'
MODEL_VERSION_ID = '0c919cc1edfc455dbc96207753f178d7'


from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import openai

api_key = "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"
openai.api_key = api_key
model_engine = "gpt-3.5-turbo-16k"


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

def generate_image(prompt,number):

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
    image_filename = f"Image_data_{number}.jpg"
    with open(image_filename, 'wb') as f:
        f.write(base64_image)

    print("Generated successfully")
    st.image(base64_image)
# text = input("Please enter some text to generate image")
#
# prompt = get_chatgpt_response(text)
#
# print("PROMPT" , prompt)
#
# generate_image(prompt)

import Test

print(len(prompts))

def random_generation(count):
    for i in range(count):
        current_sentence = "India road realistic images with the upcoming situations , "
        count = random.randint(3,8)
        prompt_sentence = []
        for j in range(0,count):
            row = random.randint(0,33)
            col = random.randint(0,len(prompts[row])-1)
            prompt_sentence.append(prompts[row][col])
        for iter in prompt_sentence:
            current_sentence = current_sentence + iter + " "
        print("IMAGE NUMBER ",i)
        print("SENTENCE ",current_sentence)
        prompt = get_chatgpt_response(current_sentence)
        print("PROMPT : ",prompt)
        generate_image(prompt,i)