# credeed-pdf-to-markdown

Convert PDF files into Markdown format using Azure AI Document Intelligence and store results in AWS S3.

Supports both online PDF URLs and local PDF files. Output Markdown file will be publicly accessible via a generated S3 URL.

Provided by the Credeed AI team, it can be used for AI Agent to understand PDF documents.

---

# About Credeed

[Credeed](https://www.credeed.com) is an AI-powered platform that helps SMEs build strong credit profiles, making it easier to access funding and grow their business. Tailored for SMEs, Credeed offers an AI-augmented, hyper-personalised experience in your [credit-building](https://www.credeed.com/score) journey.

*Keywords: KYC Report, Financial Health, Financial Risk, Credit Profile, Risk Assessment, Risk Management, Sanctions Compliance, Intelligence Platform, Company Risk, Identity Verification*

---

## Features

- Extract text and layout from PDF using Azure AI Document Intelligence
- Auto-convert to clean Markdown format
- Upload Markdown to Amazon S3 with public access
- Supports both PDF URLs and local file uploads
- Usable as a Python library, CLI tool, or Flask API

---

## Installation

```bash
pip install credeed-pdf-to-markdown
```

---

### Example Usage

```bash
from credeed_pdf_to_markdown import PdfToMarkdownConverter

converter = PdfToMarkdownConverter(
    azure_endpoint="https://<your-endpoint>.cognitiveservices.azure.com/",
    azure_key="<your-azure-key>",
    aws_access_key="<aws-access-key>",
    aws_secret_key="<aws-secret-key>",
    s3_bucket="<your-s3-bucket>",
    s3_region="ap-southeast-1"
)

# From PDF URL
markdown_url = converter.convert_from_url("https://example.com/sample.pdf")
print("Markdown URL:", markdown_url)

# From local file
markdown_url = converter.convert_from_file("sample.pdf")
print("Markdown URL:", markdown_url)
```

---

### As a CLI Tool

```bash
# From PDF URL
credeed-pdf-to-markdown --url https://example.com/sample.pdf

# From local PDF file
credeed-pdf-to-markdown --file /path/to/your.pdf
```

---

### As a Flask API

```bash
# Start the API:
python app.py

# POST request to:
http://127.0.0.1:5000/convert

# With File Upload:
curl -X POST http://127.0.0.1:5000/convert \
     -F "pdf_file=@your.pdf"

# With PDF URL:
curl -X POST http://127.0.0.1:5000/convert \
     -F "pdf_url=https://example.com/your.pdf"
```

---

### Required AWS S3 Bucket Permissions
This tool uploads Markdown files and local PDFs to S3 with public read access. Ensure your bucket has a policy like this:
```bash
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}

```

---

### License

MIT © 2025 Credeed
