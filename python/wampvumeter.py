from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep

import alsaaudio
import audioop
import sys
import math
 
input = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
input.setchannels(1)                          # Mono
input.setrate(8000)                           # 8000 Hz
input.setformat(alsaaudio.PCM_FORMAT_S16_LE)  # 16 bit little endian
input.setperiodsize(320)
 
lo  = 500
hi = 32000
 
log_lo = math.log(lo)
log_hi = math.log(hi)


class Component(ApplicationSession):

	@inlineCallbacks
	def onJoin(self, details):
		print("session attached")
		
		while True:
			len, data = input.read()
			if len > 0:
				vu = (math.log(float(max(audioop.max(data, 2),1)))-log_lo)/(log_hi-log_lo)
				yield self.publish(u'audiofoo.vumeter', vu=vu);
		
			yield sleep(0.01)


	def onDisconnect(self):
		print("disconnected")
		reactor.stop()



if __name__ == '__main__':
   from autobahn.twisted.wamp import ApplicationRunner
   runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "mixer")
   runner.run(Component)
