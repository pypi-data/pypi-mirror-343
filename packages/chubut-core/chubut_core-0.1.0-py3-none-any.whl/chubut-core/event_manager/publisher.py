import json, time, boto3
from loguru import logger
from typing import Dict, Optional
from mypy_boto3_sns.client import SNSClient
from mypy_boto3_sqs.client import SQSClient
from core.event_manager.enums.enums import ResponseStatus
from core.event_manager.models import GeneratedEvent
from core.error_handling.messages import (ERROR_PUBLISH_FAILED, ERROR_WAITING_TIMEDOUT,
                                          INFO_MESSAGE_RECEIVED, INFO_WAITING_FOR_RESPONSES, SUCCESS_MESSAGE_PUBLISHED,
                                          ERROR_TOPIC_NOT_FOUND, ERROR_QUEUE_NOT_FOUND)
from core.responses import ErrorResponse, SuccessPublish, SuccessRpcCall


def default_publisher(settings: Dict):
    
    return Publisher(req_arn=settings["req_arn"], res_arn=settings["res_arn"],
                     req_url=settings["req_url"], res_url=settings["res_url"])

class Publisher:
    def __init__(self,
                 req_arn: str,
                 res_arn: str,
                 req_url: str,
                 res_url: str):
        
        if req_arn is None:
            logger.error(ERROR_TOPIC_NOT_FOUND % "REQ_ARN")
            raise ValueError(ERROR_TOPIC_NOT_FOUND)
        if res_arn is None:
            logger.error(ERROR_TOPIC_NOT_FOUND % "RES_ARN")
            raise ValueError(ERROR_TOPIC_NOT_FOUND)
        
        if req_url is None:
            logger.error(ERROR_QUEUE_NOT_FOUND % "REQ_URL")
            raise ValueError(ERROR_QUEUE_NOT_FOUND)
        if res_url is None:
            logger.error(ERROR_QUEUE_NOT_FOUND % "RES_URL")
            raise ValueError(ERROR_QUEUE_NOT_FOUND)
    
        self.sns: SNSClient = boto3.client('sns', region_name="sa-east-1")
        self.sqs: SQSClient = boto3.client('sqs', region_name="sa-east-1")
        
        self.POLLING_TIME = 5 # Long polling
        self.TIMEOUT = 30
        self.WAIT_FOR_RESPONSES = "WAIT_FOR_RESPONSES"
        
        self.req_arn = req_arn
        self.res_arn = res_arn
        self.req_url = req_url
        self.res_url = res_url
        
        
    def publish(self, event: GeneratedEvent):
        try:
            logger.info(INFO_MESSAGE_RECEIVED % event.uuid)
            
            response = self.sns.publish(Message=event.model_dump_json(),
                                        TopicArn=self.req_arn)
            
            logger.success(SUCCESS_MESSAGE_PUBLISHED % (event.uuid,
                                                        self.req_arn.split(":")[5],
                                                        event.event_code.value))
            
            return {"success": True,
                    "event": response["MessageId"]}
        except Exception as ex:
            logger.error(ERROR_PUBLISH_FAILED % (event.uuid, str(ex)))
            return ErrorResponse(errors=str(ex))
            
            
    async def call_rpc(self, event: GeneratedEvent, on_success: Optional[callable]):
        try:
            self.publish(event=event)

            logger.info(INFO_WAITING_FOR_RESPONSES % (event.uuid, str([exp.value for exp in event.expected_services])))

            responses, errors = self._wait_for_responses(event)

            if on_success:
                responses = await on_success(responses)
        except Exception as ex:
            logger.error(ERROR_PUBLISH_FAILED % (event.uuid, str(ex)))
            responses = None
            errors = str(ex)

        return responses, errors
    
    
    def _wait_for_responses(self, event: GeneratedEvent):
        try:
            responses = {}
            errors = {}
            target = None
            
            everyone_answered = False
            start_time = time.time()
            
            while not everyone_answered and time.time() - start_time < self.TIMEOUT:
                response = self.sqs.receive_message(QueueUrl=self.res_url,
                                                     MaxNumberOfMessages=len(event.expected_services),
                                                     WaitTimeSeconds=self.POLLING_TIME)
            
                for message in response.get("Messages", []):
                    body = json.loads(message["Body"])
                    inner_body = json.loads(body["Message"])
                    
                    status = inner_body["status"]
                    corr_uuid = inner_body["correlation_uuid"]
                    
                    if corr_uuid == event.correlation_uuid:
                        self.sqs.delete_message(QueueUrl=self.res_url,
                                                ReceiptHandle=message["ReceiptHandle"])
                        
                        if status == ResponseStatus.ERROR.value:
                            target = errors
                        else:
                            target = responses
                            
                        target[inner_body["response_service"]] = json.loads(inner_body["message"])
                
                everyone_answered = (len(responses) + len(errors)) == len(event.expected_services)
            if not everyone_answered:
                raise TimeoutError(ERROR_WAITING_TIMEDOUT % self.TIMEOUT)
                
        except Exception as ex:
            import traceback
            
            logger.error(traceback.print_exc())
            errors[self.WAIT_FOR_RESPONSES] = (str(ex))
        
        return responses, errors