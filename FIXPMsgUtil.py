from datetime import datetime
from typing import Dict

class FIXPMsgUtil:

    @staticmethod
    def createFIXPMsg(msgType: str):
        msg = dict()
        msg["MessageType"] = msgType
        return msg

    @staticmethod
    def decorateFIXPMsg(msg: dict, sessionId: str):
        msg["SessionId"] = sessionId
        msg["Timestamp"] = datetime.now().timestamp()
        return msg

    @staticmethod
    def createNegotiateMsg(sessionId:str, userName:str, password:str):
        # '{"MessageType":"Negotiate","ApplVerID":"FIX50SP2","SendingTime":"2020-07-24T17:16:20.000","Timestamp":1595610929414,"SessionId":"17b7f610-cc30-11ea-99b8-5fd27dae0d36","ClientFlow":"Unsequenced","Credentials":{"CredentialsType":"login","Token":"<user-name:password>"}}'
        msg: dict = FIXPMsgUtil.createFIXPMsg("Negotiate")
        msg = FIXPMsgUtil.decorateFIXPMsg(msg, sessionId)
        msg["ClientFlow"] = "Unsequenced"
        credentials: Dict[str, str] = {
            "CredentialsType": "login"
        }
        credentials["Token"] = userName + ':' + password
        msg["Credentials"] = credentials
        return msg

    @staticmethod
    def createEstablishMsg(sessionId:str, heartBeatIntervalSeconds:int):
        #'{"MessageType":"Establish","Timestamp":159543175368000000,"SessionId":"17b7f610-cc30-11ea-99b8-5fd27dae0d36","KeepaliveInterval":30000}'
        msg:dict = FIXPMsgUtil.createFIXPMsg("Establish")
        msg = FIXPMsgUtil.decorateFIXPMsg(msg, sessionId)
        msg["KeepaliveInterval"] = heartBeatIntervalSeconds*10000
        return msg

    @staticmethod
    def createHeartBeatMsg():
        return {"MessageType": "UnsequencedHeartbeat"}
