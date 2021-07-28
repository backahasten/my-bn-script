#Prints the call stack from one function to another 
#backahasten
layer = 10			#搜索深度
start_address = 0x80855DC	#查找位置
end_function = 0x80077F0	#反向索引位置
class branch:

	def __init__(self,route,new_branch_function):
		self.route = route[:]
		self.route.append(new_branch_function)
		self.function = new_branch_function
	
	def get_next_branch(self):
		r = []
		#如果是结尾函数
		if self.function == bv.get_function_at(end_function):
			print("77f0")
			#返回空，不继续向下索引
			return r[:]
		else:
		#如果不是结尾函数
			for i in self.function.callers:
			#向下索引
				if i not in r:
				#已经再这个分支索引中，不添加，避免回环
					r.append(i)
			return r[:]

#初始化一些变量
#b用于暂存
b = []
#out用于输出
out = []
b.append(branch([],bv.get_function_at(start_address)))
#ii计数器用于搜索深度控制
ii=1
while(ii<layer):
	bb = []
	for i in range(len(b)):
	#上一次接索引头节点
		search_b = b.pop(0)
		#弹出一个
		new_find_b = search_b.get_next_branch()
		#拿到新的头节点
		if len(new_find_b)!=0:
		#如果新的头节点不是空
			for new_branch_function in new_find_b:
			#对每一个新的头节列表点遍历，并新增索引头节点
				#print(search_b.route)
				bb.append(branch(search_b.route,new_branch_function))
		else:
		#如果新的头节点是空，说明一个分支已经搜索结束了
			if bv.get_function_at(end_function) in search_b.route:
			#如果已经搜索结束的路径中有目标函数
				out.append(search_b)
				#添加到输出
	b = bb
	if bb==[]:
		break
	ii = ii+1
for i in out:
	print("---------------")
	print(i.route)
	print("---------------")




