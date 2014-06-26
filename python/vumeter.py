import alsaaudio
import audioop
import sys
import math
 
input = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
input.setchannels(1)                          # Mono
input.setrate(8000)                           # 8000 Hz
input.setformat(alsaaudio.PCM_FORMAT_S16_LE)  # 16 bit little endian
input.setperiodsize(320)
 
lo  = 2000
hi = 32000
 
log_lo = math.log(lo)
log_hi = math.log(hi)

i = 0
while True:
    len, data = input.read()
    if len > 0:
        vu = (math.log(float(max(audioop.max(data, 2),1)))-log_lo)/(log_hi-log_lo)
        
        print min(max(int(vu*100),0),99)
        
        i += 1
        if (i>100): break

