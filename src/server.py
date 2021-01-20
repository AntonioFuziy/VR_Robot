import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as plt
from IP import IP_ADDRESS

server_socket = socket.socket()
server_socket.bind((IP_ADDRESS, 8000))
server_socket.listen(0)

connection = server_socket.accept()[0].makefile("rb")
try:
  img = None
  while True:
    image_len = struct.unpack("<L", connection.read(struct.calcsize("<L")))[0]
    if not image_len:
      break

    image_stream = io.BytesIO()
    image_stream.write(connection.read(image_len))

    image_stream.seek(0)
    image = Image.open(image_stream)

    if img is None:
      img = plt.imshow(image)
    else:
      img.set_data(image)
    
    plt.pause(0.01)
    plt.draw()
    
    print(f"Image is {image.size}")
    image.verify()
    print("Image is verified")
finally:
  connection.close()
  server_socket.close()