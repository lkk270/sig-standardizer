
# NoSIG - Medical Prescription Standardization System

NoSIG is a simple application for extracting and standardizing medical prescription information from images. It lets users upload an image of a typed prescription (not handwritten) that lacks SIG codes. The system uses Tesseract OCR to extract the text from the image and then leverages OpenAI to standardize the text and generate the appropriate SIG codes.

---

## Architecture

### Interface
- **Modern web application** built with Next.js 15
- Responsive UI using **Tailwind CSS** and **shadcn/ui** components
- Dark/Light mode support
- Client-side state management with **Zustand**
- Type-safe development with **TypeScript**

### Lambda Functions
- Two **AWS Lambda functions** for text extraction and standardization
- Infrastructure as Code using **Terraform**
- Custom Lambda layer for **Tesseract OCR**
- **OpenAI integration** for intelligent text processing

---

## Technologies

### Frontend
- **Next.js** 15.0.3
- **React** 19
- **TypeScript**
- **Tailwind CSS**
- **shadcn/ui** components
- **Zustand** for state management
- **Radix UI** primitives

### Backend
- **AWS Lambda**
- **Terraform** 1.5.7
- **Python** 3.9
- **PyTesseract** 0.3.10
- **Pillow** 10.2.0
- **OpenAI API (GPT-4)**

---

## Prerequisites

- **Node.js** 18.x or higher
- **Python** 3.9
- **AWS CLI** configured with appropriate credentials
- **Terraform** 1.5.7 or higher
- **OpenAI API key**
- **Docker** (for building Lambda layers)

---

## Installation

### Interface

1. Navigate to the interface directory:
   ```bash
   cd interface
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file with the following variables (store these in GitHub Actions secrets):
   ```env
   NEXT_PUBLIC_LAMBDA_URL=your_extract_lambda_url
   NEXT_PUBLIC_STANDARDIZE_LAMBDA_URL=your_standardize_lambda_url
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

### Lambda Functions

1. Navigate to the lambda directory:
   ```bash
   cd lambda
   ```

2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure AWS credentials:
   ```bash
   aws configure
   ```

5. Initialize Terraform:
   ```bash
   cd infrastructure
   terraform init
   ```

6. Create a `terraform.tfvars` file with the following content:
   ```hcl
   openai_api_key = "your_openai_api_key"
   allowed_origins = ["http://localhost:3000", "your_production_domain"]
   environment = "prod"
   project_name = "sig-standardizer"
   ```

7. Deploy the infrastructure:
   ```bash
   terraform apply
   ```

---

## Project Structure

```plaintext
.
├── interface/         # Next.js frontend application
│   ├── app/           # Next.js app directory
│   ├── components/    # React components
│   ├── hooks/         # Custom React hooks
│   └── public/        # Static assets
│
└── lambda/            # AWS Lambda functions
    ├── infrastructure/  # Terraform configuration
    ├── src/             # Lambda function source code
    └── requirements.txt # Python dependencies
```

## Technical Details

### Frontend Stack
- **Next.js** 15 with App Router
- **React** 19 with Server Components
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **shadcn/ui** component library
- **Zustand** for state management

### Backend Stack
- **AWS Lambda** for serverless computing
- **Terraform** for infrastructure management
- **Python** 3.9 runtime
- **PyTesseract** for OCR
- **OpenAI API** for text standardization
- Custom Tesseract Lambda layer

---