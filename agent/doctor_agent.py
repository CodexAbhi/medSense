from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_mistralai import ChatMistralAI
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import uuid

from .prompts import DOCTOR_SYSTEM_PROMPT, REPORT_TEMPLATE

load_dotenv()

class DoctorAgent:
    def __init__(self):
        """Initialize the doctor agent with LLM and conversation memory."""
        self.llm = ChatMistralAI(
            api_key=os.getenv("MISTRAL_API_KEY"),
            model="mistral-medium",
            temperature=0.2
        )
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # Create the conversation chain
        system_message_prompt = SystemMessagePromptTemplate.from_template(DOCTOR_SYSTEM_PROMPT)
        human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")
        
        chat_prompt = ChatPromptTemplate.from_messages([
            system_message_prompt,
            human_message_prompt
        ])
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=chat_prompt,
            verbose=True
        )
        
        # Consultation tracking
        self.consultation_id = str(uuid.uuid4())
        self.consultation_started = False
        self.symptoms_collected = []
        self.possible_conditions = []
        self.recommendations = []

        
    def process_message(self, user_message):
        """Process a user message and return the doctor's response."""
        # If this is the first message, we're starting a consultation
        if not self.consultation_started:
            self.consultation_started = True
            # Store initial symptoms from first message
            self.symptoms_collected.append(user_message)
        
        # Process the message through the LLM
        response = self.chain.run(input=user_message)
        
        # Update the memory
        self.memory.chat_memory.add_user_message(user_message)
        self.memory.chat_memory.add_ai_message(response)
        
        return response
    
    def extract_medical_information(self):
        """Extract structured medical information from the conversation.
        This would normally use a more sophisticated approach, but this simplified
        version works for the demo."""
        messages = self.memory.chat_memory.messages
        
        # Get the full conversation history as a string
        conversation = "\n".join([f"{msg.type}: {msg.content}" for msg in messages])
        
        # Use the LLM to extract structured information
        extraction_prompt = f"""
        Based on the following conversation, extract:
        1. The main symptoms reported
        2. Possible conditions mentioned
        3. Recommendations provided
        
        Format your response as JSON with keys: "symptoms", "possible_conditions", "recommendations".
        
        Conversation:
        {conversation}
        """
        
        # Use a direct call to avoid adding to conversation memory
        extraction_response = self.llm.invoke(extraction_prompt)
        
        try:
            # Parse the JSON response - normally we'd use a better parsing method
            # but this is simplified for the demo
            response_content = extraction_response.content
            
            # Find JSON in the response
            start_idx = response_content.find('{')
            end_idx = response_content.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_content[start_idx:end_idx]
                data = json.loads(json_str)
                
                self.symptoms_collected = data.get("symptoms", [])
                self.possible_conditions = data.get("possible_conditions", [])
                self.recommendations = data.get("recommendations", [])
                
                return data
            else:
                return {
                    "symptoms": ["Error extracting symptoms"],
                    "possible_conditions": ["Error extracting conditions"],
                    "recommendations": ["Please consult a healthcare professional"]
                }
        except Exception as e:
            print(f"Error parsing extraction response: {e}")
            return {
                "symptoms": ["Error extracting symptoms"],
                "possible_conditions": ["Error extracting conditions"],
                "recommendations": ["Please consult a healthcare professional"]
            }
    
    def generate_report(self):
        """Generate a consultation report."""
        # Extract structured information from the conversation
        self.extract_medical_information()
        
        # Format the report
        report = REPORT_TEMPLATE.format(
            date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            user_id=self.consultation_id,
            symptoms="\n".join([f"- {s}" for s in self.symptoms_collected]),
            possible_conditions="\n".join([f"- {c}" for c in self.possible_conditions]),
            recommendations="\n".join([f"- {r}" for r in self.recommendations])
        )
        
        return report