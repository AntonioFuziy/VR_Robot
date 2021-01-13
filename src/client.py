import io
import socket
import struct
import time
import picamera
from IP import IP_ADDRESS

client_socket = socket.socket()
client_socket.connect((IP_ADDRESS, 8000))

connection = client_socket.makefile("wb")

try:
  camera = picamera.PiCamera()
  camera.vflip = True
  camera.resolution = (500,480)
  camera.start_preview()
  time.sleep(2)

  start = time.time()
  stream = io.BytesIO()
  for foo in camera.capture_continuous(stream, "jpeg"):
    connection.write(struct.pack("<L", stream.tell()))
    connection.flush()

    stream.seek(0)
    connection.write(stream.read())
    
    #========================================
    #Limita o tempo de stream
    # if time.time() - start > 60:
    #   break
    #========================================

    stream.seek(0)
    stream.truncate()

  connection.write(struct.pack("<L", 0))

finally:
  connection.close()
  client_socket.close()