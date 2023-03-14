import openai

openai.api_key = "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" 

prompt = "如何理解量子计算？"
response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                # {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
                # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                # {"role": "user", "content": "Where was it played?"}
            ]
        )
# print(response)
answer = response.choices[0].message.content.strip()
print("答：", answer)