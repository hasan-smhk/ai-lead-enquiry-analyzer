# ai-lead-enquiry-analyzer

## Setup & Installation

You can run this project in two ways: **locally with Python**, or **with Docker** (recommended for a clean, dependency-free setup).

---

### Option 1: Run Locally (Python)

**Prerequisites:**
- Python 3.10+
- pip

**1. Clone the repository**
```bash
git clone: (https://github.com/hasan-smhk/ai-lead-enquiry-analyzer.git)
cd ai-lead-enquiry-analyzer

2. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

3. Configure environment variables
copy .env.example .env

4.Prepare the dataset and train ML models
python ml/data/prepare_dataset.py
cd ml
python train.py
cd ..

5. Run the application
uvicorn backend.app.main:app --reload

Option 2: Run With Docker 

1. Clone the repository
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

2. Build and start the container
docker compose up --build
