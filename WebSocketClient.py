import json
import uuid

import argparse
from argparse import Namespace

from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory, connectWS

from twisted.internet import reactor, ssl, defer

from FIXPMsgUtil import FIXPMsgUtil
from ApplicationMsgUtil import ApplicationMsgUtil

#Protocol class extending WebSocketClientProtocol
class IGUSPreTradeWebSocketClientProtocol(WebSocketClientProtocol):

    quoteRequestCounter: int = 0
    securityListRequestCounter: int = 0

    receivedQuoteCounter: int = 0
    heartBeatInterval: int = 3
    sessionId: str = None

    # override
    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))
        self.sessionId=str(uuid.uuid1())
        print("Session ID generated: {0}".format(self.sessionId))

    # override
    def onConnecting(self, transport_details):
        print("Connecting")
        return None  # ask for defaults

    # override
    def onOpen(self):
        print("WebSocket connection open.")
        # send Negotiate message
        self.sendNegotiateMsg()

    # override
    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            decodedPayload = payload.decode('utf8')
            print("Text message received: {0}".format(decodedPayload));
            msg = json.loads(decodedPayload)
            # Type is defined in FIXP messages by "MsgType", in Application Messages by "MessageType"
            if "MessageType" in msg:
                msgType = msg["MessageType"]
            elif "MsgType" in msg:
                msgType = msg["MsgType"]

            if msgType == "Quote":
                self.receivedQuoteCounter += 1
                # TODO optimise if possible by setting quoteLimit at construct or post-construct time
                limit:int = self.factory.params["quoteLimit"]
                # stop when limit of messages is exceeded
                if self.receivedQuoteCounter > limit:
                    print("Quote Limit of {0} exceeded, stopping".format(limit))
                    reactor.stop()
            elif msgType == "SecurityList":
                if msg["SecurityRequestResult"] == "ValidRequest" and msg["TotNoRelatedSym"] > 0:
                    # get the security ID from the first entry in the received SecListGrp
                    security = msg["SecListGrp"][0]
                    securityID = security["SecurityID"]
                    self.sendQuoteRequest(securityID) # request a (stream of) Quote
            # FIXP message types follow
            elif msgType == "UnsequencedHeartbeat":
                self.sendHeartbeat()
            elif msgType == "NegotiationResponse":
                # Negotiation successful so send FIXP msg to establish session
                self.sendEstablishMsg()
            elif msgType == "EstablishmentAck":
                # Session established, get list of securities
                self.factory.reactor.callLater(self.heartBeatInterval, self.sendHeartbeat)
                self.sendSecurityListRequest()
            elif msgType == "EstablishmentReject":
                print("EstablishmentReject message received : Stopping")
                # TODO close WebSocket "cleanly"
                reactor.stop()

    # override
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    # dispatch msg via WebSocket
    def dispatch(self,msg:dict):
        msgString: str = json.dumps(msg)
        print("Text message sent    : {0}".format(msgString))
        self.sendMessage(msgString.encode('utf8'))

    def sendHeartbeat(self):
        self.dispatch( FIXPMsgUtil.createHeartBeatMsg() )

    def sendNegotiateMsg(self):
        self.dispatch( FIXPMsgUtil.createNegotiateMsg(self.sessionId, self.factory.params["userName"], self.factory.params["password"]) )

    def sendEstablishMsg(self):
        self.dispatch(FIXPMsgUtil.createEstablishMsg(self.sessionId, self.heartBeatInterval))

    def sendSecurityListRequest(self):
        self.securityListRequestCounter += 1
        self.dispatch(ApplicationMsgUtil.createSecurityListRequest(self.securityListRequestCounter))

    def sendQuoteRequest(self, securityID:str):
        self.quoteRequestCounter += 1
        self.dispatch(ApplicationMsgUtil.createQuoteRequest(self.quoteRequestCounter, securityID))

if __name__ == '__main__':
    import sys

    from twisted.python import log
    from twisted.internet import reactor

    parser = argparse.ArgumentParser(description='Demonstrate PreTrade WebSocket API.')
    parser.add_argument('--URL',
                        metavar='wss://....',
                        type=str,
                        help="URL for the WebSocket endpoint",
                        default="wss://demo-iguspretrade.ig.com/pretrade")
    parser.add_argument('--quoteLimit',
                        metavar='N',
                        type=int,
                        help="Limit for received quotes after which the process will stop",
                        default="1")
    parser.add_argument('--userName',
                        metavar='<user-name>',
                        type=str,
                        help="User Name",
                        required=True)
    parser.add_argument('--password',
                        metavar="<password>",
                        type=str,
                        help="Password",
                        required=True)

    args: Namespace = parser.parse_args()
    print("args : {0} ".format(args))

    log.startLogging(sys.stdout)
    factory = WebSocketClientFactory(args.URL)
    factory.params={}
    factory.params["quoteLimit"] = args.quoteLimit
    factory.params["userName"] = args.userName
    factory.params["password"] = args.password
    print(factory.params)
    factory.protocol = IGUSPreTradeWebSocketClientProtocol
    contextFactory = ssl.ClientContextFactory()

    print("Ready to connect WebSocket")
    connectWS(factory, contextFactory)
    reactor.run()
    print("Returned from reactor.run()")