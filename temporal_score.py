import torch.nn as nn
import torch.nn.functional as F
import torch
import string
class RNN(nn.Module):
    def __init__(self):
        super(RNN, self).__init__()
        self.rnn = nn.RNN(57,1)

    def forward(self, x):
        output = self.rnn(x)
        return output
all_letters = string.ascii_letters + " .,;'"
n_letters = len(all_letters)
def letterToIndex(letter):
    return all_letters.find(letter)
def letterToTensor(letter):
    tensor = torch.zeros(1, n_letters)
    tensor[0][letterToIndex(letter)] = 1
    return tensor
def lineToTensor(line):
    tensor = torch.zeros(len(line), 1, n_letters)
    for li, letter in enumerate(line):
        tensor[li][0][letterToIndex(letter)] = 1
    return tensor

def replaceone(model, inputs):
    pred = model(inputs)
    losses = torch.zeros(inputs.size()[0],inputs.size()[2])
    with torch.no_grad():
        for i in range(inputs.size()[2]):
            tempinputs = inputs.clone()
            tempinputs[:,:,i].zero_()
            tempoutput = model(tempinputs)
            losses[:,i] = F.nll_loss(tempoutput, pred, reduce=False)
    return losses
rnn=RNN()
encoded = lineToTensor('Harshit')

print(replaceone(rnn,encoded))
