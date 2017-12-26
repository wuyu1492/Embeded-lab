import pygatt
import binascii
import time
import threading



# Many devices, e.g. Fitbit, use random addressing - this is required to connect.
ADDRESS_TYPE = pygatt.BLEAddressType.public
DEVICE_ADDRESS = "34:15:13:87:DD:D8"

#adapter = pygatt.GATTToolBackend()

class writeThread (threading.Thread):
	def __init__(self, threadID, name, device, uuid, buf):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.device = device
		self.uuid = uuid
		self.buf = buf
		print("Initialized successful!!!")
		#self.run

	def run(self):
		print "starting " + self.name
		write_pos()
		print "Exiting "+self.name

	def write_pos(self):
		self.device.char_write(self.uuid, self.buf[:20])
		self.device.char_write(self.uuid, self.buf[20:])

def write_pos(device, uuid, str):
	print "Start writing " + str
	in_buf = map(ord, str)
	device.char_write(uuid, in_buf[:20])
	device.char_write(uuid, in_buf[20:])


class myThread (threading.Thread):
	def __init__(self, threadID=0, name="thread0", address="34:15:13:87:DD:D8", addr_type=pygatt.BLEAddressType.public):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.address = address
		self.type = addr_type
		try:
			self.adapter = pygatt.GATTToolBackend()
			self.adapter.start()
			print "===== adapter.connect() ====="
			self.device = self.adapter.connect(address, address_type=addr_type)
			print "address: " + str(self.device._address)
		except:
			print "Cannot start adapter"
		print "myThread Initialized successful!!"

		def run(self):		
			print "====== device.discover_characteristics() ====="
	        for uuid in self.device.discover_characteristics().keys():
	            try:
	                print("Read UUID %s (handle %d): %s" %
	                      (uuid, self.device.get_handle(uuid), binascii.hexlify(self.device.char_read(uuid))))
	            except:
	                print("Read UUID %s (handle %d): %s" %
	                      (uuid, self.device.get_handle(uuid), "!deny!"))

	    #return device


def indication_callback(handle, value):
    print "indication, handle %d: %s " % (handle, value)

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print("Received data: %s" % hexlify(value))

def pytest(address=DEVICE_ADDRESS, type=pygatt.BLEAddressType.public):
    try:
        adapter.start()

        print "===== adapter.connect() ====="
        device = adapter.connect(address, address_type=type)
        print "address: " + str(device._address)
        #print "handle : " + str(device.get_handle)
        #print "rssi   : " + str(device.get_rssi())

        print "====== device.discover_characteristics() ====="
        for uuid in device.discover_characteristics().keys():
            try:
                print("Read UUID %s (handle %d): %s" %
                      (uuid, device.get_handle(uuid), binascii.hexlify(device.char_read(uuid))))
            except:
                print("Read UUID %s (handle %d): %s" %
                      (uuid, device.get_handle(uuid), "!deny!"))

        char_uuid = "0000ffe2-0000-1000-8000-00805f9b34fb"
        #device.subscribe(char_uuid,callback=indication_callback, indication=True)
        # device.receive_notification(8, "test")

        print "====== device.char_write_handle() ====="
        in_buf = map(ord, "hello!X1010Y2525!!!")
        # send via uuid & handle, maximum is 20 bytes
        #char_uuid = 0xFFE2
        device.char_write(char_uuid, in_buf[:20])
        #char_hnd = device.get_handle(char_uuid)
        #device.char_write_handle(char_hnd, in_buf[20:])

        while (True):
            time.sleep(0.1)
    finally:
        adapter.stop()


def main():
	write_uuid = "0000ffe2-0000-1000-8000-00805f9b34fb"
	thread = myThread()
	thread.start()
	device = thread.device
	print "====== device.char_write_handle() ====="
	write_str = "hello!X1010Y2525!!!"
	#in_buf = map(ord, write_str)
	#wt = writeThread(1, "writeThread", device, write_uuid, in_buf)
	#wt.start()
	if device != None:
		write_pos(device, write_uuid, write_str)
	else:
		print "Device is None!!!"
	for i in range(3):
		time.sleep(10)
		write_str = "smhX%d010Y%d525"%(i, i)
		write_pos(device, write_uuid, write_str)
	adapter.stop()


if __name__ == "__main__":
    main()