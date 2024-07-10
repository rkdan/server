from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

#data handling
import json
import os

# ai
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

groq_api_key = os.getenv('GROQ_API')

@shared_task
def inference_ai():

    model = ChatGroq(
        model="llama3-70b-8192",
        api_key= groq_api_key
    )

    system_prompt = """ 
        You are an AI assistant that can help with a wide range of tasks.
        Always answer the human as a pirate.

        Human: {input}
    """
    prompt = PromptTemplate(
        template=system_prompt,
        input_variables=["input"]
        )

    new_input = "When was NASA created?"
    
    chain = prompt | model

    node_out = chain.invoke({"input": new_input})
    
    #Package message with AI response
    message = {
    "status": "AI Response", 
    "message": node_out.content,
    }

    # Use Channels layer to send the message
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'agent_tasks',
        {
            "type": 'agent_message',  # This corresponds to the consumer method to call
            "message": message
        }
    )
