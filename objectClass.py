class Attribute:

	def __init__(self, shape="", xpos=0, ypos=0, rx=0, ry=0, width=0, height=0, fill="", stroke="", strokeWidth=0):
		self.shape = shape
		self.xpos = 0
		self.ypos = 0
		self.rx = 0
		self.ry = 0
		self.width = 0
		self.height = 0
		self.fill = 0
		self.stroke = 0
		self.strokeWidth = 0

	def getShape(self):
		return self.shape

	def getXpos(self):
		return self.xpos

	def getYpos(self):
		return self.rx

	def getRx(self):
		return self.rx

	def getRy(self):
		return self.ry

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height

	def getFill(self):
		return self.fill

	def getStroke(self):
		return self.stroke

	def getStrokeWidth(self):
		return self.strokeWidth
