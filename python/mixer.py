from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep

class Component(ApplicationSession):

	@inlineCallbacks
	def onJoin(self, details):
		print("session attached")

		self.sliderValues = dict()

		def on_slider(id, value):
			self.sliderValues[id] = value

		def on_sliders_request():
			if len(self.sliderValues)>0:
				self.publish(u'audiofoo.sliders', data=self.sliderValues)

		yield self.subscribe(on_slider, u'audiofoo.slider')
		yield self.subscribe(on_sliders_request, u'audiofoo.sliders.request')
      
		while True:
			yield sleep(1)
			if len(self.sliderValues)>0:
				yield self.publish(u'audiofoo.sliders', data=self.sliderValues);


	def onDisconnect(self):
		print("disconnected")
		reactor.stop()



if __name__ == '__main__':
   from autobahn.twisted.wamp import ApplicationRunner
   runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "mixer")
   runner.run(Component)
