import json, boto3
from typing import Dict
from core.error_handling.messages import (ERROR_QUEUE_NOT_FOUND, ERROR_TOPIC_NOT_FOUND,
                                          INFO_MESSAGE_CODE_MATCH, INFO_RESTARTING_CONSUMER,
                                          ERROR_CONSUME_FAILED) 
from core.event_manager.enums import ExpectedServices 
from mypy_boto3_sns.client import SNSClient
from mypy_boto3_sqs.client import SQSClient
from loguru import logger

from core.event_manager.models import EventDispatcher, GeneratedEvent

def default_consumer(settings: Dict):
    return Consumer(req_url=settings["req_url"],
                    res_url=settings["res_url"],
                    res_arn=settings["res_arn"])

class Consumer:
    def __init__(self,
                 req_url: str,
                 res_url: str,
                 res_arn: str):
        
        if req_url is None:
            raise ValueError(ERROR_QUEUE_NOT_FOUND % "REQ_URL")
        if res_url is None:
            raise ValueError(ERROR_QUEUE_NOT_FOUND % "RES_URL")
        if res_arn is None:
            raise ValueError(ERROR_TOPIC_NOT_FOUND % "RES_ARN")
        
        self.req_url = req_url
        self.res_url = res_url
        self.res_arn = res_arn
        
        self.MAX_NUMBER_MESSAGES = 10 
        self.POLLING_TIME = 5 
        
        self.sns: SNSClient = boto3.client('sns', region_name="sa-east-1")
        self.sqs: SQSClient = boto3.client('sqs', region_name="sa-east-1")
        
    
    def delete_message(self, message):
        self.sqs.delete_message(QueueUrl=self.req_url,
                                        ReceiptHandle=message["ReceiptHandle"])
    
    
    async def on_event(self, consumer: ExpectedServices, event: GeneratedEvent, event_dispatcher: EventDispatcher):
        callable_event = event_dispatcher.events.get(event.event_code, None)
        
        if callable_event:
            logger.info(INFO_MESSAGE_CODE_MATCH % (event.correlation_uuid, event.event_code.value))
            
            response = await callable_event(event.message)
            
            response_event = event.model_copy()
            
            response_event.message = json.dumps(response.response)
            response_event.response_service = consumer
            
            response_event_json = response_event.model_dump_json()
            response_event_json = json.loads(response_event_json)
            response_event_json["status"] = response.status.value
            
            if "_RPC" in event.event_code.value:
                self.sns.publish(TopicArn=self.res_arn,
                                 Message=json.dumps(response_event_json))
    
    
    async def consume(self, consumer: ExpectedServices, event_dispatcher: EventDispatcher):
        try:
            result = self.sqs.receive_message(QueueUrl=self.req_url,
                                                MaxNumberOfMessages=self.MAX_NUMBER_MESSAGES,
                                                WaitTimeSeconds=self.POLLING_TIME)

            for message in result.get("Messages", []):
                body = json.loads(message["Body"])
                inner_body = body["Message"]
                
                
                event = GeneratedEvent(**json.loads(inner_body))
                
                await self.on_event(consumer, event, event_dispatcher)
                
                self.delete_message(message)
        except Exception as ex:
            import traceback
            
            logger.error(ERROR_CONSUME_FAILED % traceback.print_exc())
            self.delete_message(message)