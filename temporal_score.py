import torch.nn as nn
import torch.nn.functional as F
import torch
import string

all_letters = string.ascii_letters + " .,;'"
n_letters = len(all_letters)

def lineToTensor(line):
    tensor = torch.zeros(len(line), 1, n_letters)
    for li, letter in enumerate(line):
        tensor[li][0][all_letters.find(letter)] = 1
    return tensor

def temporal_score(inputs):
    model = nn.RNN(inputs.shape[2],1)
    _,pred = model(inputs)
    losses = torch.zeros(inputs.shape[0:2])	
    with torch.no_grad():
        for i in range(inputs.size()[0]):
            tempinputs = inputs.clone()
            tempinputs[i,:,:].zero_()
            _,tempoutput = model(tempinputs)
            losses[i] = torch.dist(tempoutput.squeeze(1), pred.squeeze(1)) #L2 Norm
    return losses

def temportal_tail_score(inputs):
    model = nn.RNN(inputs.shape[2],1)
    losses = torch.zeros(inputs.shape[0:2]) 
    for i in range(inputs.size()[0]-1):
        _,pred = model(inputs[i:,:,:])
        tempinputs = inputs[i+1:,:,].clone()
        with torch.no_grad():
            _,tempoutput = model(tempinputs)
        losses[i] = torch.dist(tempoutput, pred) #L2 Norm
    return losses

def combined_score(inputs,lambda_):
    return temporal_score(inputs) + lambda_ * temportal_tail_score(inputs)


encoded = lineToTensor('Good')
print(combined_score(encoded,0.5))
