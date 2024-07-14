# # import spacy

# # # Load the spaCy English model
# # load_english_model = spacy.load('en_core_web_sm')

# # def analyze_sentiment(review_to_be_analyzed):
# #     doc = load_english_model(review_to_be_analyzed)
# #     print(f"Text: {doc.text}")
# #     for ent in doc.ents:
# #         print(f"Entity: {ent.text}, Label: {ent.label_}")

# # # Analyze the sentiment and show named entities
# # analyze_sentiment('Weather in Mumbai.')
# from plyer import notification

# notification.notify(
#     title="Test Notification",
#     message="This is a test notification",
#     timeout=10
# )

from plyer import notification
import time

def send_notification():
    notification.notify(
        title="Test Notification",
        message="This is a test notification",
        timeout=10
    )

if __name__ == "__main__":
    while True:
        send_notification()
        time.sleep(10)
