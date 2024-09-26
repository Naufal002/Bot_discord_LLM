from openai import OpenAI
from token_1 import *
client = OpenAI(api_key= TOKEN_OPENAI)

response = client.images.generate(
  model="dall-e-3",
  prompt="a white siamese cat",
  size="1024x1024",
  quality="standard",
  n=1,
)
image_url = response.data[0].url