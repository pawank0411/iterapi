import requests

class Student(object):
	"""Student Object containing functions to retrieve various student details"""

	LOGIN_URL = "http://103.112.27.37:8282/CampusPortalSOA/login"
	STUDENTINFO_URL = "http://103.112.27.37:8282/CampusPortalSOA/studentinfo"
	STUDENTPHOTO_URL = "http://103.112.27.37:8282/CampusPortalSOA/image/studentPhoto"
	STUDENTRESULT_URL = "http://103.112.27.37:8282/CampusPortalSOA/stdrst"
	RESULTDETAIL_URL = "http://103.112.27.37:8282/CampusPortalSOA/rstdtl" # styno = int(1-8) semester number
	ATTENDANCE_URL = "http://103.112.27.37:8282/CampusPortalSOA/attendanceinfo"

	HEADERS = {"Content-Type" : "application/json"}

	def __init__(self, regdno, password):
		super(Student, self).__init__()
		self.regdno = regdno
		self.password = password
		self.cookies = self.login()
		self.details = None
		self.attendance = None
		self.img_path = None
		self.results = None
		self.resultDetail = dict()

	def login(self):
		"""
		Logs in the student portal to retrieve cookies
		
		self.cookies -> request.Response.cookies

		"""
		payload = str({"username":self.regdno, "password":self.password, "MemberType":"S"})

		response = requests.post(Student.LOGIN_URL, data=payload, headers=Student.HEADERS)
		if response.status_code == 200:
			return response.cookies
		else:
			print("Error: " ,response.status_code)
			return None

	def getInfo(self):
		"""
		Gets studentinfo

		self.details -> dict()

		"""
		response = requests.post(Student.STUDENTINFO_URL,data={},headers=Student.HEADERS, cookies=self.cookies)

		res = response.json()
		
		if response.status_code == 200:
			self.details = response.json()
			return self.details
		else:
			print("Error: " ,response.status_code)
			return None

	def getPhoto(self):
		""" 
		Downloads Student Profile Picture
		
		self.img_path -> str # Path to the image written

		"""
		response = requests.get(Student.STUDENTPHOTO_URL, data={}, headers=Student.HEADERS, cookies=self.cookies)
		res = response.content

		if response.content == None:
			print("Error: ", response.status_code)
			return None
		else:
			self.img_path = self.regdno+".jpg"
			with open(self.img_path, "wb+") as image:
				image.write(res)
				print("File written to {}".format(self.img_path))
				return self.img_path

	def getAttendance(self):
		"""
		Gets current Attendance 

		self.attendance -> dict()

		"""
		payload = str({"registerationid": "ITERRETD2001A0000001"})
		response = requests.post(Student.ATTENDANCE_URL, data=payload, headers=Student.HEADERS, cookies=self.cookies)

		if response.status_code == 200:
			self.attendance = response.json()
			return self.attendance
		else:
			print("Error: ", response.status_code)
			return None

	def getResult(self):
		"""
		Gets results

		self.result -> dict()

		"""

		payload = "{}"
		response = requests.post(Student.STUDENTRESULT_URL, data=payload, headers=Student.HEADERS, cookies=self.cookies)

		if response.status_code == 200:
			self.results = response.json()
			return self.results
		else:
			print("Cannot fetch results.", response.status_code)
			return None

	def getDetailedResult(self, sem):
		"""
		Gets result details of a semester

		Stored in self.resultDetail[sem] -> dict()

		"""

		payload = {"styno" : str(sem)}

		response = requests.post(Student.RESULTDETAIL_URL, data=str(payload), headers=Student.HEADERS, cookies=self.cookies)
		
		if response.status_code == 200:
			self.resultDetail[sem] = response.json()
			return self.resultDetail[sem]
		else:
			print("Cannot fetch results.", response.status_code)
			return None


