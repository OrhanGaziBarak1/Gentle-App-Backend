from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from decouple import config
import google.generativeai as genai
import json

class GeminiViewSet (viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request:Request):
        try:
            data = request.data.get('ocr_text')
            user = request.user

            prompt = f"""
                You are a skincare analysis assistant. You will receive OCR text results of a dermatological product. Based on the list of ingredients extracted from the OCR text, analyze each ingredient according to the user's information. Then, return the analysis in the following format:

                Result Format:

                [
                    {{
                        "Ingredient Name": "Alcohol Denat.",
                        "Ingredient Description": "Common solvent and preservative in skincare and cosmetics. Used for its ability to dissolve other substances and enhance product shelf life.",
                        "Ingredient Toxicity Status": "risky",
                        "Reasoning": "This ingredient can cause skin dryness and irritation, particularly on sensitive skin. It's best to avoid using it regularly if you have sensitive or dry skin."
                    }},
                    {{
                        "Ingredient Name": "Salicylic Acid",
                        "Ingredient Description": "Exfoliant used in acne treatment and psoriasis management. It helps to unclog pores and reduce skin inflammation.",
                        "Ingredient Toxicity Status": "safe",
                        "Reasoning": "Generally considered safe, but overuse can lead to skin dryness or peeling. Use in moderation for best results, especially if you have sensitive skin."
                    }}
                ]

                User Information:

                -  User Skin Type(s): {user.skin_type}
                -  User Skin Problem(s): {user.skin_problem}
                -  User Birth Year: {user.birth_year}

                OCR Text:  
                {data}

                Definitions:

                -  Toxic: If an ingredient is known to cause significant harm, either from long-term exposure or acute reactions. It may damage skin, organs, or pose other serious health risks.
                Example: Formaldehyde is toxic because it is a known carcinogen and can cause severe allergic reactions.

                -  Risky: If an ingredient is generally safe but may cause irritation, allergic reactions, or other issues for certain skin types or conditions. It may be harmful when overused or misused.
                Example: Fragrance (Parfum) is risky because it can cause allergic reactions or irritation, especially for sensitive skin types.

                -  Safe: If an ingredient is considered safe for most users and provides benefits with minimal risk of irritation or harm.
                Example: Aloe Vera is safe because it is soothing, moisturizing, and generally beneficial for all skin types.

                Few-Shot Examples:

                Example 1:  
                User Profile:  
                -  Age: 29  
                -  Skin Type: Sensitive  
                -  Skin Conditions: Eczema, Allergy  

                Extracted Ingredients:  
                -  Alcohol Denat.  
                -  Aqua  
                -  Parfum  
                -  Aloe Barbadensis Leaf Juice  
                -  Chamomilla Recutita Flower Water  
                -  Panthenol  

                Output:

                [
                    {{
                        "Ingredient Name": "Alcohol Denat.",
                        "Ingredient Description": "Common solvent and preservative in skincare and cosmetics. Used for its ability to dissolve other substances and enhance product shelf life.",
                        "Ingredient Toxicity Status": "risky",
                        "Reasoning": "This ingredient can cause skin dryness and irritation, especially on sensitive skin or in individuals with eczema or allergies. It's recommended to avoid it if you have sensitive skin."
                    }},
                    {{
                        "Ingredient Name": "Aloe Barbadensis Leaf Juice",
                        "Ingredient Description": "Used for its soothing and moisturizing properties in skincare products. Helps to hydrate and calm irritated skin.",
                        "Ingredient Toxicity Status": "safe",
                        "Reasoning": "Aloe Vera is soothing and moisturizing, and it's generally safe for sensitive skin. It can help calm irritation and reduce inflammation."
                    }}
                ]

                Example 2:  
                User Profile:  
                -  Age: 34  
                -  Skin Type: Normal  
                -  Skin Conditions: Psoriasis  

                Extracted Ingredients:  
                -  Salicylic Acid  
                -  Aloe Barbadensis Leaf Juice  

                Output:

                [
                    {{
                        "Ingredient Name": "Salicylic Acid",
                        "Ingredient Description": "Exfoliant used in acne treatment and psoriasis management. It helps to unclog pores and reduce skin inflammation.",
                        "Ingredient Toxicity Status": "safe",
                        "Reasoning": "Salicylic acid is safe for most people and is especially helpful for psoriasis, as it helps reduce scaling and inflammation. Just be cautious not to overuse, as it may cause dryness."
                    }},
                    {{
                        "Ingredient Name": "Aloe Barbadensis Leaf Juice",
                        "Ingredient Description": "Used for its soothing and moisturizing properties in skincare products. Helps to hydrate and calm irritated skin.",
                        "Ingredient Toxicity Status": "safe",
                        "Reasoning": "Aloe Vera is beneficial for soothing irritated skin and providing moisture, making it a great option for maintaining skin hydration without the risk of irritation."
                    }}
                ]

                You will only return the result in the above format and avoid any additional comments or variables.
            """


            
            genai.configure(api_key=config('GEMINI_API_KEY'))
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            
            return Response({response.text}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


