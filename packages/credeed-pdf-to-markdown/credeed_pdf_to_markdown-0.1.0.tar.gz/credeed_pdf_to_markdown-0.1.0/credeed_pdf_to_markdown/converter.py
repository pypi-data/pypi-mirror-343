import os
import uuid
import boto3
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentContentFormat
from .utils import is_url, get_s3_url


class PDFToMarkdownConverter:
    def __init__(self, azure_endpoint, azure_key, s3_bucket, aws_access_key, aws_secret_key, s3_region="ap-southeast-1"):
        self.azure_endpoint = azure_endpoint
        self.azure_key = azure_key
        self.s3_bucket = s3_bucket
        self.s3_region = s3_region

        self.s3_client = boto3.client(
            "s3",
            region_name=s3_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )

        self.document_intelligence_client = DocumentIntelligenceClient(
            endpoint=azure_endpoint,
            credential=AzureKeyCredential(azure_key)
        )

    def convert(self, pdf_path_or_url: str) -> str:
        # Upload to S3 if local path
        if is_url(pdf_path_or_url):
            pdf_url = pdf_path_or_url
        else:
            pdf_url = self._upload_to_s3(pdf_path_or_url, file_type="pdf")

        # Analyze document from URL
        poller = self.document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            AnalyzeDocumentRequest(
                url_source=pdf_url
            ),
            output_content_format=DocumentContentFormat.MARKDOWN,
        )
        result = poller.result()
        markdown_content = result.content

        # Save to markdown and upload to S3
        md_filename = f"{uuid.uuid4().hex}.md"
        local_md_path = f"tmp_{md_filename}"

        with open(local_md_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        md_url = self._upload_to_s3(local_md_path, file_type="md")
        os.remove(local_md_path)
        return md_url

    def _upload_to_s3(self, local_path, file_type="pdf") -> str:
        ext = "pdf" if file_type == "pdf" else "md"
        key = f"uploads/{uuid.uuid4().hex}.{ext}"

        self.s3_client.upload_file(
            Filename=local_path,
            Bucket=self.s3_bucket,
            Key=key
        )

        return get_s3_url(self.s3_bucket, key, self.s3_region)
