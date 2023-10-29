# AI Wizards AI The Ultimate challenge

## Problem Statement

Generating Synthetic Dataset of Indian Roads

Develop an algorithm which produces photorealistic and context-informed synthetic images of Indian driving scenarios. The algorithm will need to be controlled by visual or textual prompts or any novel control method.

## Overview

This repository contains an AI model for generating text and images. It leverages a combination of GPT-3.5 Turbo for text generation and a custom model for image generation. The model was trained using both API data and a fine-tuning method, using a dataset of 2000 images. To enhance the quality of image generation, an inpainting method of masking was applied.

## Model Selection

The AI model for this project was chosen based on its stability and performance. The two primary contenders for this task were DELLE-2 and Midjourney. After careful evaluation, we determined that Stable diffusion exhibited better stability and performance for our specific use case.

## Getting Started

To use the AI model, follow these steps:

1. *Clone the Repository*:
  bash
git clone https://github.com/PagalavanPagal66/AIED-Wizards.git
  

2. *Dependencies*:
  Make sure you have the required dependencies installed. You can find them in the requirements.txt file.

3. *Run the Model*:
  You can use the model by running the provided scripts. For text generation, use the GPT-3.5 Turbo API, and for image generation, use the custom model with the inpainting method.

4. *Training Data*:
  If you want to fine-tune the model or train it on your own data, make sure to prepare a dataset with 2000 images and use the provided training scripts.
