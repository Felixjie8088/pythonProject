from tkinter import Frame, BOTH

class managedframe(Frame):
	"""tkinter frame with built in content manager."""
	def __init__(self, master, nameList=['None'], initialIndex='None', **options):
		"""
		master is the parent widget of this frame
		nameList is a list of keys that you want to have empty subframes for.
		initialIndex is the first frame that will be displayed.
			if initialIndex is None, an empty frame will be displayed.
		options accepts kwargs identical to those of tkinter.Frame
		"""
		super().__init__(master)
		self.__master = master
		self.config(**options)	
		self.__frames = {str(n) : Frame(self) for n in nameList}
		if not initialIndex in self.__frames.keys() and not initialIndex in nameList:
			self.__frames[initialIndex] = Frame(self)
		else:
			self.__currentKey = initialIndex
				
	def getCurrentFrameKey(self):
		"""Gets the key value for the currently displayed subframe"""
		return self.__currentKey

	def getCurrentFrame(self):
		"""Gets the object reference to the current frame."""
		return self.__frames[self.__currentKey]

	def getFrameAtKey(self, key):
		"""
		gets the subframe that exists at key
		@raises KeyError if key is not a valid Key value.
		"""
		if not key in self.__frames.keys():
			raise KeyError
		else:
			return self.__frames[key]

	def addOption(self, inputFrame, key):
		"""
		adds a frame at the given index
		@raises KeyError if the key is already present.
			use updateOption to update an existing frame object
		"""
		if key in self.__frames.keys():
			raise KeyError
		else:
			self.__frames[key] = inputFrame
	
	def updateOption(self, inputFrame, key):
		"""
		updates the frame object at key.
		@raises KeyError if the key is not present.
			use addOption to add a new frame
		"""
		if not key in self.__frames.keys():
			raise KeyError
		else:
			self.__frames[key] = inputFrame

	def changeOption(self, key):
		"""
		changes the currently active frame to the one at key
		@raises KeyError if the key is not present
			use setOption to add and set as active a frame.
		"""
		if not key in self.__frames.keys():
			raise KeyError
		else:
			self.__frames[self.__currentKey].pack_forget()
			self.__currentKey = key
			self.__frames[key].pack(fill=BOTH, expand=True)

	def setOption(self, inputFrame, key):
		"""
		adds a frame to the manager, and sets that frame as active.
		@raises KeyError if the key is already present.
			use changeOption to change the current frame.
		"""
		try:
			self.addOption(inputFrame, key)
			self.changeOption(key)
		except KeyError:
			raise KeyError
	def removeOption(self, key, default=self.__frames.keys()[-1]):
		"""
		removes a frame from the manager.
		if key is the currently displayed key, change to a default.
		@raises KeyError if the key is not present.

		"""
		if not key in self.__frames.keys() or not default in self.__frames.keys():
			raise KeyError
		else:
			if key == self.__currentKey:
				self.changeOption(default)
			del self.__frames[key]
