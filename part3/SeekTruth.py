# SeekTruth.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDs HERE
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import math

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):
    # This is just dummy code -- put yours here! - added my code below
    truthful_dict={} #dictionary to store count of all unique words of objects under truthful label
    deceptive_dict={} #dictionary to store count of all unique words of objects under deceptive label
    truthful_count=0 #to maintain total number of words under truthful label
    deceptive_count=0 #to maintain total number of words under deceptive label
    for index,sentence in enumerate(train_data["objects"]):
        if train_data["labels"][index] == "truthful" :
            words=sentence.split(" ") #get all words in sentence
            for word in words: 
                truthful_count=truthful_count+1
                if word in truthful_dict.keys() :
                    truthful_dict[word]+=1 #update into dictionary
                else:
                    truthful_dict[word]=1 #word is seen for first time, create new key and then update dictionary
        elif train_data["labels"][index] == "deceptive" : #same for this label
            words=sentence.split(" ")
            for word in words:
                deceptive_count= deceptive_count+1
                if word in deceptive_dict.keys() :
                    deceptive_dict[word]+=1
                else:
                    deceptive_dict[word]=1 
    for each in truthful_dict:
        truthful_dict[each]=(truthful_dict[each]/truthful_count) #calculating probability = (number of occurences of one word / total number of words)
    for each in deceptive_dict:
        deceptive_dict[each]=deceptive_dict[each]/deceptive_count
        
        #test data traversal
    test_labels=[]
    truth_prob=1
    decep_prob=1

    for sentence in test_data["objects"]:
        words=sentence.split(" ")
        for word in words:                 
            if word in truthful_dict.keys(): #used negative log to avoid the value from becoming too small to track
                truth_prob=(truth_prob)-math.log(truthful_dict[word]) #multiplying all stored parameters according to every word in the sentence
            else:
                truth_prob+=-math.log(1/truthful_count) #if it is a word never seen before then we are multiplying with its probability as (1/total number of words)
            if word in deceptive_dict.keys():
                decep_prob=(decep_prob)-math.log(deceptive_dict[word] )
            else:
                decep_prob+=-math.log(1/deceptive_count)

        if truth_prob<=decep_prob: #classifying based on which has higher probability
            test_labels.append("truthful")
        else:
            test_labels.append("deceptive")

    return test_labels


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}
    # print("train-----------------\n",train_data["labels"])
    # print("test------------------------\n",test_data_sanitized)
    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
