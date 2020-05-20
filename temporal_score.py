import torch.nn as nn
import torch.nn.functional as F
import torch
import string
import gensim.downloader as api
model_gigaword = api.load("glove-wiki-gigaword-100")

def sentenceToTensor(sent):
    op = torch.tensor((len(sent.split(' ')),model_gigaword['i'].shape[0]))
    for i,word in enumerate(sent.split(' ')):
        op[i] = torch.from_numpy(model_gigaword[word])
    return op
class RankCharacters:
    """
        Accepts a feature vector tensor and outputs a temporal ranking of characters
    """

    def temporal_score(self, inputs):
        """ 
            Considering a input sequence x1,x2,...,xn
            we calculate T(xi) = F(x1,x2,...,xi) - F(x1,x2,...,xi-1)
            where F is one pass through a RNN cell
        """
        model = nn.RNN(inputs.shape[2], 1)
        _, pred = model(inputs)
        losses = torch.zeros(inputs.shape[0:2])
        with torch.no_grad():
            for i in range(inputs.size()[0]):
                tempinputs = inputs.clone()
                tempinputs[i, :, :].zero_()
                _, tempoutput = model(tempinputs)
                losses[i] = torch.dist(
                    tempoutput.squeeze(1), pred.squeeze(1)
                )  # L2 Norm
        return losses

    def temportal_tail_score(self, inputs):
        """ 
            Considering a input sequence x1,x2,...,xn
            we calculate T(xi) = F(xi,xi+1,...,xn) - F(xi+1,xi+2...,xn)
            where F is one pass through a RNN cell
        """
        model = nn.RNN(inputs.shape[2], 1)
        losses = torch.zeros(inputs.shape[0:2])
        for i in range(inputs.size()[0] - 1):
            _, pred = model(inputs[i:, :, :])
            tempinputs = inputs[i + 1 :, :,].clone()
            with torch.no_grad():
                _, tempoutput = model(tempinputs)
            losses[i] = torch.dist(tempoutput, pred)  # L2 Norm
        return losses

    def combined_score(self, inputs, lambda_):
        """ 
            Computes combined temporal_score, temportal_tail_score
            Combined Score = temporal_score + λ(temportal_tail_score),
        """
        return self.temporal_score(inputs) + lambda_ * self.temportal_tail_score(inputs)


encoded = sentenceToTensor("i love dogs")
print(encoded,encoded.shape)
# rc = RankCharacters()
# print(rc.combined_score(encoded, 0.5))
