def operate5(array, status = "remove"):
	result = []
	if status == "remove":
		for _ in array:
			if str(_)[-1] != "0" and str(_)[-1] != "5":result.append(_)
	elif status == "select":
		for _ in array:
			if str(_)[-1] == "0" or str(_)[-1] == "5":result.append(_)
	return result