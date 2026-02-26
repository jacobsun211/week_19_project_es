import re


text = 'Smokers appear to be at higher risk from coronavirus - expert | The Times of Israel https://t.co/HgKQ8M7 qr'

cleaned_text = re.sub(r"[?!-//)|:.,$#%@`]",'', text)



print(cleaned_text)