class UnknownTestException(Exception):
	def __init__(self, message=""):
		self.message = message

	def __str__(self):
		return f"Test exception. Invalid link or unknown test!\n{self.message}"


class AuthException(Exception):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return f"Login error. Login or password is incorrect!\n{self.message}"
