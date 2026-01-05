from google import genai
import os
from dotenv import load_dotenv

# Load environment variables just in case
load_dotenv()

# Initialize new client (v2 SDK)
# It will automatically read GOOGLE_API_KEY from environment, but we force it to ensure
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

async def analyze_logs(question: str, logs: list[dict]) -> str:
    """
    Analiza logs usando Gemini 2.5 Flash con el nuevo SDK de Google Gen AI.
    """
    try:
        # Convert logs to text for AI consumption
        logs_str = str(logs)
        
        prompt = f"""You are a DevOps expert. Analyze these logs and answer the question.
        
        Logs:
        {logs_str}
        
        Question: {question}
        """

        # Async call with new SDK
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        return response.text

    except Exception as e:
        print(f"❌ Error conectando con Gemini 2.5: {e}")
        return "Lo siento, hubo un error de conexión con la IA. Verifica los logs del servidor."