from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=key)

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )
#
# print(completion.choices[0].message)

response = client.images.generate(
  model="dall-e-3",
  prompt="One of the most fascinating planets I have visited is called Lyra IV. It exists in a distant star system, far beyond our own solar system. Lyra IV is a terrestrial planet with a breathtakingly diverse landscape and an extraordinary mix of natural wonders. "+
         "As I landed on Lyra IV, I was immediately struck by its vibrant colors and surreal atmosphere. The sky above was adorned with swirling ribbons of deep purples and electric blues, casting an ethereal glow upon the planet's surface. "+
         "The terrain of Lyra IV is a captivating blend of towering mountains and lush, dense forests. The mountains, with their jagged peaks and sheer cliffs, reach towards the sky like ancient guardians of the planet. Cascading waterfalls, fed by crystal-clear rivers, punctuate the mountain ranges, creating a mesmerizing symphony of sight and sound."+
         "Moving beyond the mountains, I discovered vast stretches of prairies dotted with vibrant wildflowers that seemed to shimmer under the alien sun. These prairies were home to a myriad of unique creatures, each adapted to the planet's distinct environment. I encountered creatures with vibrant, bioluminescent patterns, moving gracefully across the grasslands, their otherworldly beauty a testament to the evolution on this extraordinary planet.",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
print(image_url)