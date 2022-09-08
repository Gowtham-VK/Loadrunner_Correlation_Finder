import re
import linecache
import tkinter as tk
from tkinter import filedialog

#____________GlobalVariable_Start
snapshot="Snapshot=t"

ResponseEnd="$$ $\S$$ Response Body For Transaction with ld"

End_Value='''

	/*Actual value={}:*/
	
	/*Line No={}*/
	
	{}
'''

webregsave='web_reg_save_param("C_Corelation","LB={LB_Value}", "RB={RB_Value}", "Notfound=Warning", LAST);'
#___________________GlobalVariable End

#_________________RegularExp:Match either web_url or web_submit_data or web_custom_request
Regex_Web=re.compile("(?:web_url|web_submit_data|web_custom_request)")

def getCorelationValue():

	ActualValue=text_box1.get(1.0,"end-1c")#____________Userlnput
	
	CorrelationValue=""#______LocalVar
	CorrelationValue=ActualValue.replace("Select the Path of the Vugen file to find corelation","")
	if re.search("(?:\+|\*|\?)", ActualValue):#_______RegularExp:Match special charcters
		specialChar=re.findall("(?:\+1\/\?)", ActualValue)
		for i in specialChar:
			rep="\\{}".format(i)
			CorrelationValue=ActualValue.replace(i, rep)
	else:
		CorrelationValue=ActualValue
		
		
	#_______________________________RegularExp_Start______________________
	
	
	Regex_Search=re.compile("("+CorrelationValue+")")#__RegularExp:To match the corerelation Value_________________
	
	# Reg_Exp2=re.compile("A"+ResponseEnd+""}#________RegularExp:To match the ResponseEnd Value
	
	Regex_Snapshot=re.compile("\""+snapshot+"")#____________RegularExp:To match the snapshot Value
	
	# Regex_RightBound=re.compile(".+?("+CorrelationValue+")[\s\S]")#______________RegularExp:To match the Right Boundary Value
	
	# Regex_LeftBound=re.compile(".+?(?="+CorrelationValue+")")#_____________RegularExp:To match the Left Boundary Value
	
	Regex_split=re.compile("("+CorrelationValue+")(?!.*"+CorrelationValue+")")#____ RegularExp:To split the correlation Value_

	Regex_LeftBoundSplit=re.compile("[\w\W\d\D\s\s]{1,25}$")#_______________RegularExp:To match the Left Boundary Value upto 25 chars
	
	Regex_RightBoundSplit=re.compile("\[\w\W\d\D\S\s]{1,15}")#________RegularExp:To match the Right Boundary Value upto 15 chars
	
	#__________________________________________RegularExp_End_____________________________________
	
	FileLocation=text_box.get(1.0,"end-1c")#_________File-Location

	FileLocation=FileLocation.replace("Choose Path","")#_________File-Location
	
	CodegenerationLog=FileLocation+"/data/CodeGenerationLog.txt"#__________CodeGenerationLog File-Location
	
	CodeGenerationLog_filepath=r'%s' % CodegenerationLog#_______________CodeGenerationLog File-Location

	try:
		CodGen_File=open(CodeGenerationLog_filepath,"r")#_______________CodegenerationLog File Open
	except:
		text_box1.delete(1.0, 'end')#_________Delete the value in textbox
		text_box1.insert(1.0,"Choose The Correct Path")#_____Insert the value in textbox
		CodGen_File=CodGen_File.close()
		return 0

		
	#_____________Local Var Start
	WebFlag=False
	SnapFlag=False
	CorrelationLine=""
	Snapshot_value=""
	Left_Boundary=""
	Right_Boundary=""
	#__________________Local Var End
	
	#_____________loop throught the action.c file
	
	for number, line in enumerate(CodGen_File,0):
	
		if re.findall(Regex_Search,line):#____________If Condition to match the corerelation Value line
			CorrelationLine=line
			current='\\"'
			replace="\\{}".format('\"')
			CrBoundaries=re.split(Regex_split,line,maxsplit=2)
			try:
				Left_Boundary,Right_Boundary=re.findall(Regex_LeftBoundSplit,CrBoundaries[0]),re.findall(Regex_RightBoundSplit, CrBoundaries[2])
				Right_Boundary=Right_Boundary[0].replace(current, replace)
				Left_Boundary=Left_Boundary[0].replace(current, replace)
			except:
				text_box1.delete(1.0,'end')#_______Delete the value in textbox_
				text_box1.insert(1.0,"Please check the value")#__________Insert the value in textbox
			WebFlag=True
		elif re.findall(Regex_Web,line) and WebFlag: #____________Condition to match the web_url or web_submit_data or web_custom_request line
			WebFlag=False
			SnapFlag=True
		elif re.findall(Regex_Snapshot, line) and SnapFlag:#______________Condition to match the snapshot line
			Snapshot_value=re.sub("[(\t)|(\n))]","",line)
			SnapFlag=False
			Left_Boundary = Left_Boundary.lstrip()#__________Strip the extra spaces from left side of the line
			Right_Boundary=Right_Boundary.rstrip()#__________Strip the extra spaces from right side of the line
			webreg=webregsave.format(LB_Value=Left_Boundary,RB_Value=Right_Boundary) 
			getLineNumber(Snapshot_value,Filelocation,webreg,CorrelationLine)#___calling getLineNumber function_
			CodGen_File.close()#__________CodeGenerationLog File Close
			return 0
			
	if CorrelationLine=="":
		text_box1.delete(1.0,'end')#__________Delete the value in textbox
		text_box1.insert(1.0,"Not Found")#_________________Insert the value in textbox
		return 0
		
		
def getLineNumber(Snapshot_value, FileLocation, webreg, CorrelationLine): 
	LineCounter=0
	ActionFileloc=FileLocation+"\Action.c"#____________action file locatiom.
	ActionFilePath=r'%s' % ActionFileloc#____________action file locatiom
	Action_File=open(ActionFilePath,"r")#____________Open Action File
	Regex_SnapshotValue=re.compile(Snapshot_value)
	for number, line in enumerate(Action_File):#________________iterate through the globfile.
		if re.findall(Regex_SnapshotValue,line):#_____________If Condition to match the "Snapshot=t.inf" line
			LineCounter=number-1
			while LineCounter>(number-10):#_______________While Condition to match the web_url or web_submit_data or web_custom_request line in reverse
				ln=linecache.getline(ActionFilePath, LineCounter)
				LineCounter=LineCounter-1
				if re.findall(Regex_Web,ln):#______________If Condition to match the web_url or web_submit_data or web_custom_request line
					Action_File.close()#__________Close Action File.
					CorrelatedValue=End_Value.format(CorrelationLine, LineCounter,webreg)
					text_box1.delete(1.0,'end')#_____________Delete the value in textbox
					text_box1.insert(1.0, CorrelatedValue)#__________Insert the value in textbox_
					return 0

def open_file():
	browse_text.set("Browse")
	file=filedialog.askdirectory()
	# file=file.replace('/','\\')
	if file:
		text_box.delete(1.0, 'end')#_________Delete the value in textbox
		text_box.insert(1.0, file)
	else:
		return 0
		
# ____________________________________GUI___________________________________________

root=tk.Tk()
root.maxsize(720,400)

canvas=tk.Canvas(root,width=720,height=300)
canvas.grid(columnspan=4, rowspan=4)

Headings=tk.Label(root, text="Select the Path of the Vugen file to find corelation", font="Raleway")
Headings.grid(columnspan=4, column=0, row=0)


browse_text=tk.StringVar()
find_text=tk.StringVar()
browse_btn=tk.Button(root, textvariable=browse_text, command=lambda:open_file(), font='Raleway', bg="#20bebe", fg="white", height=2, width=10)
find_btn=tk.Button(root, textvariable=find_text, command=lambda:getCorelationValue(), font='Raleway', bg="#20bebe", fg="white", height=2, width=10)

browse_text.set("Browse")
find_text.set("Find")
browse_btn.grid(column=1,row=1)
find_btn.grid(column=1,row=2)


#textbox

text_box = tk.Text(root, height=1,width=50, padx=10, pady=10)
text_box.insert(1.0,"Choose Path")
text_box.tag_configure("center", justify="center")
text_box.tag_add("center", 1.0,"end")
text_box.grid( column=0,row=1)
 
Filelocation=text_box.get(1.0,"end-1c")


#textbox
text_box1 = tk.Text(root, height=10,width=50, padx=10, pady=10)
text_box1.insert(1.0,"Enter The Value To be corelated")
text_box1.tag_configure("center" ,justify="center")
text_box1.tag_add("center", 1.0,"end")
text_box1.grid(column=0,row=2)

canvas=tk.Canvas(root,width=720,height=300)
canvas.grid(columnspan=4, rowspan=4)

root.mainloop()







