from pprint import pprint
import ssl
import easyocr


def recognize_number(destination: str) -> list:
    ssl._create_default_https_context = ssl._create_unverified_context

    reader = easyocr.Reader(['ru'], gpu=False)
    results = reader.readtext(destination, 
                             paragraph=False)
    filtered_results = [result for result in results if result[1].isdigit()]
    
    del reader, results
    return filtered_results

if __name__ == "__main__":
    pprint(recognize_number('images/2025-03-11 12.02.21 PM.jpg'))