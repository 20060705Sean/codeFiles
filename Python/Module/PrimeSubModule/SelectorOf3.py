__added = lambda n:sum(list(map(int, [s for s in str(n)])))
def operate3(array, status = "remove"):
	result = []
	if status == "remove":
		for _ in array:
			if __added(_) % 3 != 0 or _ == 3:result.append(_)
	elif status == "select":
		for _ in array:
			if __added(_) % 3 == 0 and _ != 3:result.append(_)
	return result