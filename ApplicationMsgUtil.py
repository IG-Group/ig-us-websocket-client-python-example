import FIXPMsgUtil
from typing import Dict
import Constant
from datetime import datetime

class ApplicationMsgUtil:

    @staticmethod
    def createApplicationMsg(msgType: str):
        msg = dict()
        msg["MsgType"] = msgType
        return msg

    @staticmethod
    def decorateApplicationMsg(msg: dict):
        msg["ApplVerID"] = Constant.APPL_VER_ID
        msg["SendingTime"] = datetime.now().isoformat()
        return msg

    @staticmethod
    def createSecurityListRequest(securityReqNumber:int):
        #{"MsgType":"SecurityListRequest","ApplVerID":"FIX50SP2","SendingTime":"2020-07-25T19:23:21.683","SecurityReqID":"security-list-1595701401683-1","SecurityListRequestType":"AllSecurities","SecAltIDGrp":[],"SubscriptionRequestType":"Snapshot"}
        msg: dict = ApplicationMsgUtil.createApplicationMsg("SecurityListRequest")
        msg = ApplicationMsgUtil.decorateApplicationMsg(msg)
        msg["SecurityReqID"] = "security-list-{0}".format(securityReqNumber)
        msg["SecurityListRequestType"] = "AllSecurities"
        msg["SecAltIDGrp"] = []
        msg["SubscriptionRequestType"] = "Snapshot"
        return msg

    @staticmethod
    def createQuoteRequest(quoteReqNumber:int, securityID:str):
        #{"MsgType":"QuoteRequest","ApplVerID":"FIX50SP2","SendingTime":"2020-07-25T19:23:21.845","QuoteReqID":"quote-1595701401845-1","SubscriptionRequestType":"SnapshotAndUpdates","QuotReqGrp":[{"SecurityID":"CS.D.GBPUSD.CZD.IP","SecurityIDSource":"MarketplaceAssignedIdentifier"}]}
        msg: dict = ApplicationMsgUtil.createApplicationMsg("QuoteRequest")
        msg = ApplicationMsgUtil.decorateApplicationMsg(msg)
        msg["QuoteReqID"] = "quote-request-{0}".format(quoteReqNumber)
        msg["SubscriptionRequestType"] = "SnapshotAndUpdates"
        qouteReqEntry={}
        qouteReqEntry["SecurityID"]=securityID
        qouteReqEntry["SecurityIDSource"] = "MarketplaceAssignedIdentifier"
        quoteReqGrp = [qouteReqEntry]
        msg["QuotReqGrp"] = quoteReqGrp
        return msg



