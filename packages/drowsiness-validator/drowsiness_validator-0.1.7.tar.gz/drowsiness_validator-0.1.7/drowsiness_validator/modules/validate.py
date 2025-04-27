import ollama
res = ollama.chat(
    model='llava-phi3:latest',
    messages=[{
        'role': 'user',
        'content': 'Describe the drowsiness visual clues in this image. forget about his appearance, his short color hair, and his clothes. Just focus on the drowsiness visual clues on his face and eyes and posture',
        'images': ['./download.jpeg'] 
    }]
)
print(res['message']['content'])