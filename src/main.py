from src.anonymization.anonymizer import Anonymizer
from src.extraction_service.extraction_service_factory import ExtractionServiceFactory
from data_models.file_input import Input
import glob, base64, os

an = Anonymizer()
ex = ExtractionServiceFactory()

def analyze_doc(doc_name: str, encoded: bytes):
    '''

    :param doc_name:
    :param encoded:
    :return:
    '''
    file_type = doc_name.split('.')[-1]
    if os.name == 'nt':
        base_name = doc_name.split('\\')[-1]
    else:
        base_name = doc_name.split('/')[-1]
    base_name = base_name.split('.')[0]

    input = Input(
        type=file_type,
        payload=encoded.decode('ascii')
    )
    service = ex.get_extraction_service(input)
    text = service.extract_text(encoded.decode('ascii'))
    anonymized_text = an.anonymize(text)
    txt_file = base_name.split('.')[0] + '.txt'
    with open(f'results/{txt_file}', 'w', encoding='utf-8') as f:
        f.write(anonymized_text)



docs = glob.glob("data/*")
for doc_name in docs:

    #open as binary
    with open(doc_name, 'rb') as f:
        content = f.read()
        #base64 encode
        encoded = base64.b64encode(content)
        #file type
        try:
            analyze_doc(
                doc_name=doc_name,
                encoded=encoded
            )
        except Exception as e:
            print(f"Error processing {doc_name}: {e}")
            continue





