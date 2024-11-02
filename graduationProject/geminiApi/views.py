from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from decouple import config
import google.generativeai as genai

import re

def response_cleaner(text):
    # 1. Headers (başlıklar) için `#` sembollerini kaldır
    text = re.sub(r'(^|\n)#{1,6}\s+', '', text)
    
    # 2. **Kalın** veya *İtalik* metin işaretlemelerini kaldır
    text = re.sub(r'(\*{1,2}|_{1,2})(.*?)\1', r'\2', text)
    
    # 3. [Linkler](https://örnek.com) için köşeli ve parantezleri kaldır
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    
    # 4. `inline code` işaretlemelerini kaldır
    text = re.sub(r'`(.*?)`', r'\1', text)
    
    # 5. Liste işaretçilerini (`-`, `*`, veya `+`) kaldır
    text = re.sub(r'^[\*\-\+] ', '', text)
    
    # 6. Blok kodları ve yatay çizgileri kaldır
    text = re.sub(r'(`{3,})(.*?)\1', r'\2', text)
    text = re.sub(r'(^|\n)(-{3,}|\*{3,})($|\n)', '', text)
    
    # 7. Resim işaretlemesini ![alt text](url) kaldır
    text = re.sub(r'!\[(.*?)\]\(.*?\)', r'\1', text)
    
    # 8. İç içe `>` sembolleriyle belirtilen blockquote'ları kaldır
    text = re.sub(r'(^|\n)>\s?', '', text)
    
    # 9. Satır başında sayı bulunan numaralı listeleri kaldır
    text = re.sub(r'^\d+\.\s+', '', text)
    
    # 10. Fazla boş satırları kaldır
    text = re.sub(r'\n{2,}', '\n', text)

    text = re.sub(r'\n', ' ', text)

    return text.strip()

class GeminiViewSet (viewsets.ViewSet):

    def list(self, request:Request, chemical=None):

        if chemical is not None:
            genai.configure(api_key=config('GEMINI_API_KEY'))
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"Can you give me information in Turkish about a chemical which is named \'{chemical}\'?")

            return Response({'AI_Response':response_cleaner(response.text)}, status=status.HTTP_200_OK)
        else:
            return Response({'Error':'Chemical not found. Please pass a chemical.'}, status=status.HTTP_404_NOT_FOUND)
