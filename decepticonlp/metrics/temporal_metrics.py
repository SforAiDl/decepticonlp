import torch
import torch.nn as nn


class RankWords:
    """
        Accepts a feature vector torch tensor and outputs a temporal ranking of each word
        inputs of shape (number of words,feature_vector_size)
        Methods
        --------
        temporal_score(self, model, sentence)
            - calculates the temporal score each word in a sentence(considering the first i words) 
        temportal_tail_score(self, model, sentence)
            - calculates the temporal score each word in a sentence(considering n-i words)
        combined_score(self, model, sentence, lambda_)
            - calculates the combined score taking into consideration temporal score and tailed temporal score with lambda as the weight
    """

    def temporal_score(self, model, sentence):
        """ 
            Considering a input sequence x1,x2,...,xn
            we calculate T(xi) = F(x1,x2,...,xi) - F(x1,x2,...,xi-1)
            where F is one pass through a RNN cell 
            
            Example:

            >> import temporal_metrics
            >> rw = temporal_metrics.RankWords()
            >> embedded_word = embed("i like dogs") #embed should convert the sentence to a (sent_length * embedding_dim) shape tensor
            >> print(rw.temporal_score(model,embedded_word))  #seed = 99 
            tensor([[1.1921e-07],[2.2054e-05],[8.4886e-01]])

            :params
            :model : The model must output torch tensor of dimension (1,1,1) as its output
            :sentence : An tensor of shape (sent_length * embedding_dim) where each word has been embedded 

            returns temporal score of each word
            :return type: torch.Tensor
        """
        inputs = sentence.reshape(len(sentence), 1, -1)
        with torch.no_grad():
            pred = model(inputs)
            losses = torch.zeros(inputs.shape[0:2])
            for i in range(inputs.size()[0]):
                tempinputs = inputs.clone()
                tempinputs[i, :, :].zero_()
                tempoutput = model(tempinputs)
                losses[i] = torch.dist(
                    tempoutput.squeeze(1), pred.squeeze(1)
                )  # L2 Norm
        return losses

    def temportal_tail_score(self, model, sentence):
        """ 
            Considering a input sequence x1,x2,...,xn
            we calculate T(xi) = F(xi,xi+1,...,xn) - F(xi+1,xi+2...,xn)
            where F is one pass through a RNN cell

            Example:

            >> import temporal_metrics
            >> rw = temporal_metrics.RankWords()
            >> embedded_word = embed("i like dogs") #embed should convert the sentence to a (sent_length * embedding_dim) shape tensor
            >> print(rw.temportal_tail_score(model,embedded_word)) #seed = 99

            tensor([[5.9605e-08],[1.9789e-05],[0.0000e+00]])

            :params
            :model : The model must output torch tensor of dimension (1,1,1) as its output
            :sentence : An tensor of shape (sent_length * embedding_dim) where each word has been embedded 

            returns temporal score of each word
            :return type: torch.Tensor
        """
        inputs = sentence.reshape(len(sentence), 1, -1)
        losses = torch.zeros(inputs.shape[0:2])
        with torch.no_grad():
            for i in range(inputs.size()[0] - 1):
                pred = model(inputs[i:, :, :])
                tempinputs = inputs[i + 1 :, :,].clone()
                tempoutput = model(tempinputs)
                losses[i] = torch.dist(tempoutput, pred)  # L2 Norm
        return losses

    def combined_score(self, model, sentence, lambda_):
        """ 
            Computes combined temporal_score, temportal_tail_score
            Combined Score = temporal_score + λ(temportal_tail_score)

            Example:

            >> import temporal_metrics
            >> rw = temporal_metrics.RankWords()
            >> embedded_word = embed("i like dogs") #embed should convert the sentence to a (sent_length * embedding_dim) shape tensor
            >> print(rw.combined_score(model,embedded_word,0.5)) #seed = 99

            tensor([[6.8545e-07], [3.8507e-03], [8.4886e-01]])

            :params
            :model : The model must output torch tensor of dimension (1,1,1) as its output
            :sentence : An tensor of shape (sent_length * embedding_dim) where each word has been embedded 
            :lambda_ : (float) , 0 <= lambda_ <= 1 

            returns temporal score of each word
            :return type: torch.Tensor
        """
        return self.temporal_score(
            model, sentence
        ) + lambda_ * self.temportal_tail_score(model, sentence)
