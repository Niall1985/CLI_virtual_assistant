# # import spacy
# # nlp = spacy.load("en_core_web_sm")
# # def extract_city(command):
# #     doc = nlp(command)
# #     for ent in doc.ents:
# #         if ent.label_ == "GPE": 
# #             return ent.text
# #     return None
# # extract_city('I love Mumbai')

# import spacy

# # Load the spaCy English model
# nlp = spacy.load("en_core_web_sm")

# def extract_city(command):
#     doc = nlp(command)
#     # Print recognized entities for debugging
#     for ent in doc.ents:
#         print(f"Entity: {ent.text}, Label: {ent.label_}")
# # # Test the function
# print(extract_city('Play Superstar by Jamelia on youtube music'))

n = int(input("Enter number:"))
