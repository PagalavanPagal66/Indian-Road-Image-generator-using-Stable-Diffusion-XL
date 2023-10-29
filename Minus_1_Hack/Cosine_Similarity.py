import numpy as np
import pandas as pd
import os
from collections import Counter

images_path = os.listdir('E:\\resize\\')
embedding_df = pd.read_csv(r'C:\Users\pagal\PycharmProjects\TEXT\Minus_1_Hack\Embeddings.csv')
from sklearn.metrics.pairwise import cosine_distances,pairwise_distances,cosine_similarity
cosine_similarity_df = pd.DataFrame(cosine_similarity(embedding_df.drop('image',axis=1)))

total_str = ""
with open(r"C:\Users\pagal\PycharmProjects\TEXT\Minus_1_Hack\Tags_File.txt","r")as f:
    total_str+=str(f.read())
string_split = total_str.split('*')
temp_list=[]
total_list=[]
search_term = "\n"
for iter in string_split:
    if(iter==''):
       continue
    index = iter.find(search_term)
    if index != -1:
        temp_list.append(iter[0:-1])
        total_list.append(temp_list)
        temp_list=[]
    else:
        temp_list.append(iter)
print(temp_list)
def fetch_most_similar_products(image_name,n_similar=5):
    curr_index = embedding_df[embedding_df['image']==image_name].index[0]
    closest_image = pd.DataFrame(cosine_similarity_df.iloc[curr_index].nlargest(n_similar+1)[1:])
    total_tags = dict()
    for index,imgs in closest_image.iterrows():
        similar_image_name = embedding_df.iloc[index]['image']
        similarity = np.round(imgs.iloc[0],3)
        current_tags = total_list[int(list(str(similar_image_name).split('_'))[-1])]
        print(current_tags)
        for iter in current_tags:
            if iter in total_tags:
                total_tags[str(iter)]+=1
            else:
                total_tags[str(iter)]=1
    value_counts = Counter(total_tags.values())
    total_tags = dict(sorted(total_tags.items(), key=lambda item: value_counts[item[1]], reverse=False))
    print(total_tags)
    return_value = ""
    for key, value in total_tags.items():
        return_value += str(key)+" "
    print(return_value)
    return return_value

image_name = "sample_image_10"
print(fetch_most_similar_products(image_name))

