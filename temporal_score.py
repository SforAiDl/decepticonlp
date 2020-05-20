import torch.nn as nn
import torch.nn.functional as F
import torch
import string
import gensim.downloader as api
import temporal_metrics
model_gigaword = api.load("glove-wiki-gigaword-100")

def sentenceToTensor(text):
    op = torch.zeros((len(text.split(' ')),model_gigaword['i'].shape[0]))
    for i,word in enumerate(text.split(' ')):
        op[i] = torch.from_numpy(model_gigaword[word])
    return op


encoded = sentenceToTensor("i like dogs")
rc = temporal_metrics.RankCharacters()
print(rc.combined_score(encoded, 0.5))
