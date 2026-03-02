from groq import Groq

import streamlit as st
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

print("مرحبًا, أنا مساعد جامعة العقبة للتكنولوجيا!")
print("اكتب سؤالك واضغط Enter — اكتب 'خروج' للإنهاء")
print("-" * 40)

while True:
    سؤال = input("أنت: ")
    
    if سؤال == "خروج":
        print("إلى اللقاء!")
        break
    
    رد = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "أنت مساعد أكاديمي لجامعة العقبة للتكنولوجيا. أجب دائماً بالعربية بشكل مختصر ومفيد."},
            {"role": "user", "content": سؤال}
        ]
    )
    
    print(f"المساعد: {رد.choices[0].message.content}")
    print("-" * 40)
