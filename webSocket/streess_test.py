#!/usr/bin/env python

# -*- coding: utf-8 -*-

from ws4py.client.threadedclient import WebSocketClient

class EchoClient(WebSocketClient):
    def opened(self):
        def data_provider():
            for i in range(1, 200, 25):
                yield "#" * i

        self.send(data_provider())

        for i in range(0, 200, 25):
            print(i)
            self.send("*" * i)

    def closed(self, code, reason):
        print(("Closed down", code, reason))

    def received_message(self, m):
        print("=> %d %s" % (len(m), str(m)))
        if len(m) == 175:
            self.close(reason='Bye bye')

if __name__ == '__main__':
    try:
        ws = EchoClient('ws://10.155.103.11:7000/new-msg/socket', protocols=['http-only', 'chat'])
        ws.daemon = False
        #ws.daemon = True 
        ws.connect()
    except KeyboardInterrupt:
        ws.close()
