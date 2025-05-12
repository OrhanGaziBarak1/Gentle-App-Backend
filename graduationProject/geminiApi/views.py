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
                You are a skincare analysis assistant. You will receive OCR text results of a dermatological product.
                Based on the list of ingredients extracted from the OCR text, analyze each ingredient according to the user's information. Then, return the analysis in the following format:

                Result Format:

                [
                    {{
                        "Ingredient Name": "Alcohol Denat.",
                        "Ingredient Description": "Common solvent and preservative in skincare and cosmetics. Used for its ability to dissolve other substances and enhance product shelf life.",
                        "Ingredient Toxicity Status": "high risk",
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

                - High Risk: If an ingredient is known to cause significant skin reactions such as burning, cracking, peeling, or aggravation of existing conditions (e.g., eczema, dermatitis, rosacea). It may lead to visible damage, wounds, or prolonged inflammation on the skin.
                Example: Sodium Lauryl Sulfate is high risk because it can cause irritation and worsen eczema or dermatitis in sensitive users.

                - Low Risk: If an ingredient is generally safe but may lead to mild symptoms like itching, redness, dryness, pore clogging, or occasional breakouts. These effects are usually not permanent but can be bothersome for certain skin types or conditions.
                Example: Coconut Oil is low risk because it can clog pores and cause acne in oily or acne-prone skin.

                - Safe: If an ingredient is considered well-tolerated across most skin types, with a low chance of irritation or reaction. These ingredients are often soothing or neutral in nature.
                Example: Panthenol is safe because it supports skin hydration and barrier function, and rarely causes irritation.


                Few-Shot Examples:

               Example 1:  
                User Profile:  
                - Age: 29  
                - Skin Type: Sensitive  
                - Skin Conditions: Eczema, Allergy  

                Extracted Ingredients:  
                - Alcohol Denat.  
                - Aqua  
                - Parfum  
                - Aloe Barbadensis Leaf Juice  
                - Chamomilla Recutita Flower Water  
                - Panthenol  

                Output:

                [
                    {{
                        "Ingredient Name": "Alcohol Denat.",
                        "Ingredient Description": "A solvent and preservative used in skincare formulations. It improves product texture and shelf life.",
                        "Ingredient Toxicity Status": "high risk",
                        "Reasoning": "Alcohol Denat. can cause significant dryness and irritation, especially for users with eczema or allergic skin. It may worsen existing conditions and lead to discomfort."
                    }},
                    {{
                        "Ingredient Name": "Parfum",
                        "Ingredient Description": "Synthetic or natural fragrance used to scent cosmetic products.",
                        "Ingredient Toxicity Status": "low risk",
                        "Reasoning": "Fragrance can trigger allergic reactions or mild irritation in sensitive users. It doesn't typically cause long-term harm but requires caution for allergy-prone individuals."
                    }},
                    {{
                        "Ingredient Name": "Aloe Barbadensis Leaf Juice",
                        "Ingredient Description": "Moisturizing and soothing agent commonly used in skincare products.",
                        "Ingredient Toxicity Status": "safe",
                        "Reasoning": "Aloe Vera helps calm irritated skin and reduce inflammation. It is safe and well-tolerated by sensitive and eczema-prone skin types."
                    }},
                    {{
                        "Ingredient Name": "Panthenol",
                        "Ingredient Description": "Provitamin B5 used for hydration and skin barrier support.",
                        "Ingredient Toxicity Status": "safe",
                        "Reasoning": "Panthenol improves skin hydration and elasticity. It is non-irritating and widely used in products for sensitive skin."
                    }}
                ]


               Example 2:  
                User Profile:  
                - Age: 34  
                - Skin Type: Normal  
                - Skin Conditions: Psoriasis  

                Extracted Ingredients:  
                - Salicylic Acid  
                - Aloe Barbadensis Leaf Juice  

                Output:

                [
                    {{
                        "Ingredient Name": "Salicylic Acid",
                        "Ingredient Description": "A beta hydroxy acid (BHA) used for exfoliation and acne or psoriasis management.",
                        "Ingredient Toxicity Status": "safe",
                        "Reasoning": "Salicylic acid is safe and often recommended for psoriasis. It helps reduce scaling and clears excess skin cells. Overuse may cause dryness, so moderate use is advised."
                    }},
                    {{
                        "Ingredient Name": "Aloe Barbadensis Leaf Juice",
                        "Ingredient Description": "A natural extract that hydrates and calms the skin.",
                        "Ingredient Toxicity Status": "safe",
                        "Reasoning": "Aloe Vera supports skin recovery and soothes irritation. It is compatible with normal and sensitive skin, including conditions like psoriasis."
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


