#Print call tree
#backahasten
new_find_callers_list = []
graph = FlowGraph()
node_list = []
node_dict = {}

n = FlowGraphNode(graph)
bass_function = bv.get_function_at(0x046a8f4)#write function address here
callers = list(set(bass_function.callers))
n.lines = bass_function.name
graph.append(n)
node_dict[bass_function] = n
#print(callers)
len_node_dict_old = len(node_dict)
while(1):
	new_find_callers_list = []
	if callers == []:
		break
	for i in callers:
		if i.symbol.type == SymbolType.ImportedFunctionSymbol:
			token_type = InstructionTextTokenType.ImportToken
		else:
			token_type = InstructionTextTokenType.CodeSymbolToken
		n = FlowGraphNode(graph)
		n.lines = [
			   DisassemblyTextLine(
					[InstructionTextToken(token_type, i.name, i.start)],
					i.start,)]
		node_dict[i] = n
		new_find_callers_list = new_find_callers_list + list(set(i.callers))
	if len(node_dict)>len_node_dict_old:
		len_node_dict_old = len(node_dict)
	else:
		print(len_node_dict_old)
		break
	callers =  new_find_callers_list

node_list = node_dict.keys()
print(node_list)
for i in node_list:
	graph.append(node_dict[i])

for i in node_list:
	l = list(set(i.callers))
	for p in l:
		node_dict[p].add_outgoing_edge(BranchType.UnconditionalBranch,node_dict[i])

show_graph_report("CALL Graph", graph)

