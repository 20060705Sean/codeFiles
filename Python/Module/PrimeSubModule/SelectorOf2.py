def operate2(array, status = "remove"):
	result = []
	if status == "remove":
		for _ in array:
			if _ % 2 != 0 or _ == 2:result.append(_)
	elif status == "select":
		for _ in array:
			if _ % 2 == 0 and _ != 2:result.append(_)
	return result