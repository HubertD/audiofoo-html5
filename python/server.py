import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.endpoints import serverFromString

from autobahn.wamp import router, types
from autobahn.twisted import wamp, websocket


if __name__ == '__main__':

   log.startLogging(sys.stdout)
   router_factory = router.RouterFactory()
   session_factory = wamp.RouterSessionFactory(router_factory)

   transport_factory = websocket.WampWebSocketServerFactory(session_factory, debug = False, debug_wamp = False)

   server = serverFromString(reactor, "tcp:8080")
   server.listen(transport_factory)

   reactor.run()

