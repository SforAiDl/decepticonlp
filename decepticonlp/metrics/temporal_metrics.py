import torch
import torch.nn as nn


class RankCharacters:
    """
        Accepts a feature vector torch tensor and outputs a temporal ranking of characters
        inputs of shape (number of words,feature_vector_size)
    """

    def temporal_score(self, sentence):
        """ 
            Considering a input sequence x1,x2,...,xn
            we calculate T(xi) = F(x1,x2,...,xi) - F(x1,x2,...,xi-1)
            where F is one pass through a RNN cell 
        """
        inputs = sentence.reshape(len(sentence), 1, -1)
        model = nn.RNN(inputs.shape[2], 1)
        with torch.no_grad():
            _, pred = model(inputs)
            losses = torch.zeros(inputs.shape[0:2])
            for i in range(inputs.size()[0]):
                tempinputs = inputs.clone()
                tempinputs[i, :, :].zero_()
                _, tempoutput = model(tempinputs)
                losses[i] = torch.dist(
                    tempoutput.squeeze(1), pred.squeeze(1)
                )  # L2 Norm
        return losses

    def temportal_tail_score(self, sentence):
        """ 
            Considering a input sequence x1,x2,...,xn
            we calculate T(xi) = F(xi,xi+1,...,xn) - F(xi+1,xi+2...,xn)
            where F is one pass through a RNN cell
        """
        inputs = sentence.reshape(len(sentence), 1, -1)
        model = nn.RNN(inputs.shape[2], 1)
        losses = torch.zeros(inputs.shape[0:2])
        with torch.no_grad():
            for i in range(inputs.size()[0] - 1):
                _, pred = model(inputs[i:, :, :])
                tempinputs = inputs[i + 1 :, :,].clone()
                _, tempoutput = model(tempinputs)
                losses[i] = torch.dist(tempoutput, pred)  # L2 Norm
        return losses

    def combined_score(self, sentence, lambda_):
        """ 
            Computes combined temporal_score, temportal_tail_score
            Combined Score = temporal_score + λ(temportal_tail_score),
        """
        return self.temporal_score(sentence) + lambda_ * self.temportal_tail_score(
            sentence
        )
