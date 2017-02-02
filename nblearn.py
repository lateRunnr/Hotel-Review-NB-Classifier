import sys
import math
from string import punctuation

def remove_punctuation(with_punctuation):
	return ''.join(letter for letter in with_punctuation if letter not in punctuation)

def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist,wordfreq))

def wordListToZeroFreqDict(wordlist):
	wordfreq=[0 for p in wordlist]
	return dict(zip(wordlist,wordfreq))

def getOppositeLabel(labels):
	oppositeLabel=[]
	for label in labels:
		if label == "truthful":
			oppositeLabel.append("deceptive")
		if label == "deceptive":
			oppositeLabel.append("truthful")
		if label == "positive":
			oppositeLabel.append("negative")
		if label == "negative":
			oppositeLabel.append("positive")
	return oppositeLabel

def removeHighFreq(table):
	copy_d=table.copy()
	for key,val in table.iteritems():
		count=table.get(key)
		if count > 1500:
			copy_d.pop(key,val)
	return copy_d

def calculateProb(table,sum_of_values):
	for key,val in table.iteritems():
		count=table.get(key)
		if count == 0:
			deno=sum_of_values+len(table)
			table[key]=math.log(float(1)/deno)
		else:
			table[key]=math.log(float(count)/sum_of_values)
	return table

def writeModel(prob_table,label):
	out_file.write(label+'\n')
	out_file.write('%d' %len(prob_table))
	out_file.write('\n')
	for key,val in prob_table.iteritems():
		out_file.write(key+"")
		out_file.write('%14f' %val)
		out_file.write('\n')
	return

## I/O operations & Initialiations
s=sys.argv
text_file=open(s[1],"r")
label_file=open(s[2],"r")
c_data={"train":None,"test":None}
info={"id":None,"review":None,"label":None,"zeroCountReview":None,"oppositeLabel":None}
c_data["train"]=[]
line_count=0
truthful_count=0
deceptive_count=0
positive_count=0
negative_count=0

## Dictionary processes
for line in text_file:
	label_line=label_file.readline()
	labels=label_line[21:].split()
	#print labels

	## Increasing count of truthful,deceptive,positive,negative
	if labels[0]=="truthful":
		truthful_count=truthful_count+1
	else:
		deceptive_count=deceptive_count+1
	if labels[1] == "positive":
		positive_count=positive_count+1
	else:
		negative_count=negative_count+1
    
    ## Storing Input values in dictionary
	info["id"]=line[0:20]
	#print remove_punctuation(line[21:]).lower().split()
	review_freq=wordListToFreqDict(remove_punctuation(line[21:]).lower().split())
	info["review"]=review_freq
	info["label"]=labels
	zero_count_freq=wordListToZeroFreqDict(remove_punctuation(line[21:]).lower().split())
	info["zeroCountReview"]=zero_count_freq
	info["oppositeLabel"]=getOppositeLabel(labels)
	c_data["train"].append(info.copy())
	line_count=line_count+1

## Freqency table initialisation
truthful={}
deceptive={}
positive={}
negative={}
for list_dict in c_data["train"]:
	label_in_list=list_dict["label"]
	d=list_dict["review"]

	## Accessing Class 1 labels i.e. truthful/deceptive
	if label_in_list[0]=="truthful":
		for key,val in d.iteritems():
			if key in truthful:
				truth_count=truthful.get(key)
				truth_count=truth_count+val
				truthful[key]=truth_count
			else:
				truthful[key]=val
	else:
		for key,val in d.iteritems():
			if key in deceptive:
				decep_count=deceptive.get(key)
				decep_count=decep_count+val
				deceptive[key]=decep_count
			else:
				deceptive[key]=val
	## Adding zero counts for Class 1 labels
	oppositeLabel_in_List=list_dict["oppositeLabel"]
	zero_d=list_dict["zeroCountReview"]
	if oppositeLabel_in_List[0]=="truthful":
		for key,val in zero_d.iteritems():
			if key not in truthful:
				truthful[key]=0
	else:
		for key,val in zero_d.iteritems():
			if key not in deceptive:
				deceptive[key]=0

	##Accessing Class 2 labels i.e. Positive/negative
	if label_in_list[1] == "positive":
		for key,val in d.iteritems():
			if key in positive:
				positive_count=positive.get(key)
				positive_count=positive_count+val
				positive[key]=positive_count
			else:
				positive[key]=val
	else:
		for key,val in d.iteritems():
			if key in negative:
				negative_count=negative.get(key)
				negative_count=negative_count+val
				negative[key]=negative_count
			else:
				negative[key]=val
    ## Addiing Zero counts for class 2
	if oppositeLabel_in_List[1]=="positive":
		for key,val in zero_d.iteritems():
			if key not in positive:
				positive[key]=0
	else:
		for key,val in zero_d.iteritems():
			if key not in negative:
				negative[key]=0

###removing high frequency words
#truthful=removeHighFreq(truthful)
#deceptive=removeHighFreq(deceptive)

##Calculating probability with smoothing
truthful_prob=calculateProb(truthful,sum(truthful.values()))
deceptive_prob=calculateProb(deceptive,sum(deceptive.values()))
positive_prob=calculateProb(positive,sum(positive.values()))
negative_prob=calculateProb(negative,sum(negative.values()))

#### Writing model ####
out_file=open("nbmodel.txt","w")

##Priors
prob_truthful=math.log(float(truthful_count)/line_count)
prob_deceptive=math.log(float(deceptive_count)/line_count)
prob_positive=math.log(float(positive_count)/line_count)
prob_negative=math.log(float(negative_count)/line_count)

## writing to output file
out_file.write("P(truthful)" +'%10f' %prob_truthful)
out_file.write('\n')
writeModel(truthful_prob,"truthful")
out_file.write("P(deceptive)" +'%10f' %prob_deceptive)
out_file.write('\n')
writeModel(deceptive_prob,"deceptive")
#print "Writing positive "
out_file.write("P(positive)"+'%10f' %prob_positive)
out_file.write('\n')
writeModel(positive_prob,"positive")
out_file.write("P(negative)"+'%10f' %prob_negative)
out_file.write('\n')
writeModel(negative_prob,"negative")


    




    

