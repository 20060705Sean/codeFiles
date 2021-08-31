class xrange(object):
	def __init__(self,i):self.n=i if isinstance(i,int)and i>=0 else self.__rn(i,i>0)
	def __rn(self,i,m):raise AttributeError(f'Attribute integar must {"be class int"if m==False else"bigger than 0"}, not {i if m==True else str(type(i))[8:11]}')
	def __del__(self):del self
	def __iter__(self,i=0):
		while i<=self.n:yield i;i+=1