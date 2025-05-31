from together import Together
client = Together()
response = client.chat.completions.create(
    model="google/gemma-3-27b-it",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": "https://huggingface.co/datasets/patrickvonplaten/random_img/resolve/main/yosemite.png"}
                },
                {
                    "type": "text",
                    "text": "Describe this image."
                }
            ]
        }
    ]
)
print(response.choices[0].message.content)