# 💬 Serverless Meeting Transcript Assistant Chatbot

An end-to-end, production-grade serverless chatbot that allows users to upload meeting transcripts (.txt) and dynamically ask tailored questions (e.g., summarizing notes, extracting action items, or tracking specific timelines). 

## 🏗️ Architecture Overview
This application is built with a 100% serverless architecture on AWS, ensuring **zero idle maintenance costs** and instant scalability:
* **Frontend:** Static web interface hosted on **Amazon S3** utilizing vanilla HTML/CSS and asynchronous JavaScript (`fetch`).
* **API Layer:** **Amazon API Gateway (HTTP API)** acting as the secure routing interface with CORS fully configured.
* **Compute:** **AWS Lambda (Python)** parsing dynamic JSON payloads and managing execution workflows.
* **AI Engine:** **Anthropic Claude (Haiku 4.5)** via the official Anthropic Python SDK Layer.
* **Storage/Audit:** **Amazon S3** automatically archiving and timestamping generated responses.

## 🚀 Key Engineering Accomplishments
* **Cost Efficiency:** Designed a architecture that incurs a $0.00 base cost when idle.
* **Enterprise-Grade Privacy:** Routed traffic through the official Anthropic API to guarantee company transcript data is never used for LLM model training.
* **Cross-Origin Security:** Successfully configured and deployed global CORS preflight policies between decentralized AWS services.

## 📁 Repository Structure
* `index.html` - Static web frontend with integrated asynchronous API calls.
* `meeting_summary.py` - Cleaned JSON-native AWS Lambda handler function.
