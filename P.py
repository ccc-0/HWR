from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
from time import ctime
from MainWindow import Main

class HWServer(Protocol):
    def connectionMade(self):# 当客户端连接时，自动调用
        print("GET connection from", self.transport.client)

    def connectionLost(self, reason): # 当客户端断开时，自动调用
        print(self.transport.client, 'disconnected')

    def dataReceived(self, data): # 接收数据时，会自动调用
        print(data)
        # data = data.decode('gb2312')
        # self.transport.write(('[%s] %s'%(ctime(),data)).encode('gb2312'))


if __name__=="__main__":
    factory = Factory()
    factory.protocol = HWServer
    port = 20000
    reactor.listenTCP(port, factory)
    reactor.run()
