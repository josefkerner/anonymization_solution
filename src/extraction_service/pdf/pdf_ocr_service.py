import os
import boto3
from langchain_community.document_loaders.pdf import AmazonTextractPDFLoader


class PdfOcrService:
    def __init__(self):
        self.s3_bucket_name = os.environ["S3_BUCKET_NAME"]

        self.client = boto3.client(
            'textract',
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            region_name="us-east-1"
        )

    def extract_text(self, filename):
        file_path = f"s3://{self.s3_bucket_name}/{filename}"

        loader = AmazonTextractPDFLoader(file_path, client=self.client)

        documents = loader.load()

        extracted_text = "\n".join(document.page_content for document in documents)
        return extracted_text