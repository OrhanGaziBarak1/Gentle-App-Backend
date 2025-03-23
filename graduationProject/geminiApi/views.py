from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from decouple import config
import google.generativeai as genai

class GeminiViewSet (viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request:Request):
        try:
            data = request.data.get('ocr_text')
            user = request.user
            
            prompt = f"""
                I will send to you a OCR text results of a dermotologic product.
                You will analyse the list of ingredients with this user's information.
                Then, you will return to me your analysis with this result format.
                Remember that you will return to me only the result format. Dont say anything else.
                You dont write our variables like ingredient name, cancer possibility, allergie possibility.
                You write your result with markdown format.

                Result format:
                <Ingredient Name>:
                <Ingredient Description>:
                <Ingredient Toxicity Status>: toxic or risky or safe
                <Cancer Possibility>: low or modarate or high
                <Allergie Possibility>: low or modarate or high

                User Information:
                - User Skin Type(s): {user.skin_type}
                - User Skin Problem(s): {user.skin_problem}
                - User Age: {user.age}
                
                OCR Text:
                {data}
            """
            genai.configure(api_key=config('GEMINI_API_KEY'))
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return Response({response.text}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_400_BAD_REQUEST)


