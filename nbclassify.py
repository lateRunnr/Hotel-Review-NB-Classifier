import sys
from string import punctuation

def remove_punctuation(with_punctuation):
	return ''.join(letter for letter in with_punctuation if letter not in punctuation)

def createProbTable(length):
	keys=[]
	values=[]
	i=0
	while (i<length):
		key_value=model_file.readline()
		l=key_value.split()
		keys.append(l[0])
		values.append(float(l[1]))
		i=i+1
	return dict(zip(keys,values))

def check_probability(hotel_review,label):
	#print hotel_review
	if (label=="truthful"):
		conditional_prob=0
		for token in hotel_review:
			if(truthful_prob.get(token)!=None):
				#print truthful_prob.get(token)
				conditional_prob = float(conditional_prob) + truthful_prob.get(token)
		#print conditional_prob
		return conditional_prob
	if(label=="deceptive"):
		conditional_prob=0
		for token in hotel_review:
			if(deceptive_prob.get(token)!=None):
				#print deceptive_prob.get(token)
				conditional_prob = float(conditional_prob) + deceptive_prob.get(token)
		#print conditional_prob
		return conditional_prob

	if(label=="positive"):
		conditional_prob=0
		for token in hotel_review:
			if(positive_prob.get(token)!=None):
				#print positive_prob.get(token)
				conditional_prob=float(conditional_prob) + positive_prob.get(token)
		#print conditional_prob
		return conditional_prob
	if(label=="negative"):
		conditional_prob=0
		for token in hotel_review:
			if(negative_prob.get(token)!=None):
				#print negative_prob.get(token)
				conditional_prob=float(conditional_prob) + negative_prob.get(token)
		#print conditional_prob
		return conditional_prob

#Reading test file
s=sys.argv
test_file=open(s[1],"r")
model_file=open("nbmodel.txt","r")

## reading truthful
prior_t=model_file.readline()
label=model_file.readline()
length=model_file.readline()
truthful_prob=createProbTable(int(length))
#print truthful_prob

##reading deceptive
prior_d=model_file.readline()
label=model_file.readline()
length=model_file.readline()
deceptive_prob=createProbTable(int(length))
#print deceptive_prob

##reading positive
prior_p=model_file.readline()
label=model_file.readline()
length=model_file.readline()
positive_prob=createProbTable(int(length))

##reading negative
prior_n=model_file.readline()
label=model_file.readline()
length=model_file.readline()
negative_prob=createProbTable(int(length))

#Calculating priors
prior_t_list=prior_t.split()
prior_truthful=float(prior_t_list[1])
prior_d_list=prior_d.split()
prior_deceptive=float(prior_d_list[1])
prior_p_list=prior_p.split()
prior_positive=float(prior_p_list[1])
prior_n_list=prior_n.split()
prior_negative=float(prior_n_list[1])

#Reading test input for classification
out_file=open("nboutput.txt","w")
t_data={"test":None}
test_info={"id":None,"review":None}
t_data["test"]=[]
for line in test_file:
	test_info["id"]=line[0:20]
	test_info["review"]=remove_punctuation(line[21:]).lower().split()
	t_data["test"].append(test_info.copy())
for list_check in t_data["test"]:
	hotel_review=list_check["review"]
	##Calculating conditional probability
	truthful_calc_prob=check_probability(hotel_review,"truthful")
	deceptive_calc_prob=check_probability(hotel_review,"deceptive")
	positive_calc_prob=check_probability(hotel_review,"positive")
	#print "positive " + '%d' %positive_calc_prob
	negative_calc_prob=check_probability(hotel_review,"negative")
	#print "negative " + '%d' %negative_calc_prob

	##Calculating Posterier probability
	posterier_truthful=float(truthful_calc_prob)+prior_truthful
	posterier_deceptive=float(deceptive_calc_prob)+prior_deceptive
	posterier_positive=float(positive_calc_prob)+prior_positive
	posterier_negative=float(negative_calc_prob)+prior_negative
	if (posterier_truthful > posterier_deceptive):
		out_file.write(list_check["id"] + " truthful")
		out_file.write(" ")
	else:
		out_file.write(list_check["id"] + " deceptive")
		out_file.write(" ")
	if(posterier_positive > posterier_negative):
		out_file.write("positive")
		out_file.write('\n')
	else:
		out_file.write("negative")
		out_file.write('\n')






