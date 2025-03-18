from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from decouple import config
import google.generativeai as genai

#class GeminiViewSet (viewsets.ViewSet):
#    permission_classes = [IsAuthenticated]
#    
#    def list(self, request:Request, chemical=None):
#
#        if chemical is not None:
#
#            prompt = f"""
#                my app will turn the ingridients of a dermotologic product one by one as cards. 
#                I will give you 1 chemical to process. Then my app will show the chemicals as cards. 
#                can you turn the description of the chemical and make a list of its allergie risks and 
#                cancer risks of then detect which skin types are suitable this chemical give it as a 
#                list and all I need is answers like suitable/not suitable. is the chemical safe for 
#                roza, eczema, comedones disease and give short answers to me
#                {chemical}.
#            """
#
#            genai.configure(api_key=config('GEMINI_API_KEY'))
#            model = genai.GenerativeModel("gemini-1.5-flash")
#            response = model.generate_content(prompt)
#
#            return Response({'AI_Response':response.text}, status=status.HTTP_200_OK)
#        else:
#            return Response({'Error':'Chemical not found. Please pass a chemical.'}, status=status.HTTP_404_NOT_FOUND)

class GeminiViewSet (viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request:Request):
        try:
            data = request.data.get('ocr_text')
            user = request.user  # Authenticated user nesnesine erişim
            
            prompt = f"""
                I will send to you a OCR text results of a dermotologic product.
                You will analyse the list of ingredients with this user's information.
                Then, you will return to me your analyse.
                User Information:
                - User Skin Type(s): {user.skin_type}
                - User Skin Problem(s): {user.skin_problem}
                
                OCR Text:
                {data}
            """
            genai.configure(api_key=config('GEMINI_API_KEY'))
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return Response({response.text}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_BAD_REQUEST)


