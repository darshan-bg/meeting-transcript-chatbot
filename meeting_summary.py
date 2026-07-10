import boto3
import json
import os
from datetime import datetime
import anthropic

# Initialize the client outside the handler to reuse it across Lambda warm starts.
anthropic_client = anthropic.Anthropic()


def generate_dynamic_response(transcript: str, instruction: str) -> str:
    """
    Combines the user's custom instruction with the uploaded transcript 
    and sends it directly to Claude.
    """
    try:
        response = anthropic_client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4000,
            temperature=0.1,  # Low temperature keeps code generation/summaries stable
            messages=[
                {
                    "role": "user",
                    "content": f"Context Transcript:\n{transcript}\n\nUser Instruction: {instruction}"
                }
            ]
        )
        return response.content[0].text.strip()
    except Exception as e:
        print(f"Error generating response from Anthropic: {e}")
        return ""


def save_summary_to_s3_bucket(summary, s3_bucket, s3_key):
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=summary)
        print("Summary successfully logged to S3")
    except Exception as e:
        print(f"Error when saving to S3: {e}")


def lambda_handler(event, context):
    try:
        # 1. Parse the clean incoming JSON payload sent by the S3 static frontend
        body = json.loads(event['body'])
        user_instruction = body.get('instruction', 'Summarize the following meeting notes') # "Summarize the following meeting notes" is the default instruction when no instruction is passed from chatbot
        transcript_content = body.get('transcript', '')

        if not transcript_content:
            return {
                'statusCode': 400,
                'body': json.dumps({"response": "Error: No transcript text found in payload."})
            }

        # 2. Feed BOTH variables dynamically straight to Claude
        claude_output = generate_dynamic_response(transcript_content, user_instruction)

        if claude_output:
            # Maintain an automated log archive in S3
            current_time = datetime.now().strftime('%H%M%S') 
            s3_key = f'chat-output/{current_time}.txt'
            s3_bucket = 'bedrock-chatbot-frontend-2026'
            save_summary_to_s3_bucket(claude_output, s3_bucket, s3_key)
            
            # 3. CRITICAL: Return Claude's real live text response back to the browser.
            # (Note: API Gateway global CORS handles headers; keep this body clean)
            return {
                'statusCode': 200,
                'body': json.dumps({"response": claude_output})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({"response": "Error: Claude failed to generate a response."})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"response": f"Pipeline failure: {str(e)}"})
        }
