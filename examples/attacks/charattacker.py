__author__ = "Abheesht Sharma"

import sys

sys.path.append("./")

import warnings

warnings.filterwarnings("ignore")

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

import pandas as pd
import numpy as np

import re
import spacy
from collections import Counter
import string


from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


from decepticonlp.attacks import attack
from decepticonlp.transforms import transforms


batch_size = 8


class LSTM1(torch.nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super().__init__()
        self.embeddings = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.linear = nn.Linear(hidden_dim, 5)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x, l):
        x = self.embeddings(x)
        x = self.dropout(x)
        lstm_out, (ht, ct) = self.lstm(x)
        return self.linear(ht[-1])


model = LSTM1(8265, 50, 50)
model.load_state_dict(torch.load("examples/attacks/pretrained models/lstm.pth"))
# print(model)

tok = spacy.load("en")


def tokenize(text):
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    regex = re.compile("[" + re.escape(string.punctuation) + "0-9\\r\\t\\n]")
    nopunct = regex.sub(" ", text.lower())
    return [token.text for token in tok.tokenizer(nopunct)]


def encode_sentence(text, vocab2index, N=70):
    tokenized = tokenize(text)
    encoded = np.zeros(N, dtype=int)
    enc1 = np.array([vocab2index.get(word, vocab2index["UNK"]) for word in tokenized])
    length = min(N, len(enc1))
    encoded[:length] = enc1[:length]
    return encoded, length


reviews = pd.read_csv("examples/attacks/datasets/reviews.csv")
print(reviews.shape)
adv_reviews = reviews


def prepare_data(reviews):
    reviews["Title"] = reviews["Title"].fillna("")
    reviews["Review Text"] = reviews["Review Text"].fillna("")
    reviews["review"] = reviews["Title"] + " " + reviews["Review Text"]

    reviews = reviews[["review", "Rating"]]
    reviews.columns = ["review", "rating"]
    reviews["review_length"] = reviews["review"].apply(lambda x: len(x.split()))

    zero_numbering = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4}
    reviews["rating"] = reviews["rating"].apply(lambda x: zero_numbering[x])

    counts = Counter()
    for index, row in reviews.iterrows():
        counts.update(tokenize(row["review"]))

    # print("num_words before:",len(counts.keys()))

    for word in list(counts):
        if counts[word] < 2:
            del counts[word]

    # print("num_words after:",len(counts.keys()))

    vocab2index = {"": 0, "UNK": 1}
    words = ["", "UNK"]
    for word in counts:
        vocab2index[word] = len(words)
        words.append(word)

    reviews["encoded"] = reviews["review"].apply(
        lambda x: np.array(encode_sentence(x, vocab2index))
    )

    reviews.head()

    Counter(reviews["rating"])

    X = list(reviews["encoded"])
    y = list(reviews["rating"])
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2)

    return X_train, X_valid, y_train, y_valid


class ReviewsDataset(Dataset):
    def __init__(self, X, Y):
        self.X = X
        self.y = Y

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        """if(self.y[idx]>1):
            self.y[idx]=1"""
        return (
            torch.from_numpy(self.X[idx][0].astype(np.int_)),
            self.y[idx],
            self.X[idx][1],
        )


X_train_original, X_valid_original, y_train_original, y_valid_original = prepare_data(
    reviews
)
validation_loader = ReviewsDataset(X_valid_original, y_valid_original)

val_dl_original = DataLoader(validation_loader, batch_size=batch_size)


# Apply transforms to the dataset
tfms = transforms.Compose(
    [
        transforms.AddChar(char_perturb=True),
        transforms.ShuffleChar(mid=True),
        transforms.TypoChar(probability=0.6),
        transforms.DeleteChar(),
    ]
)

for i, rows in adv_reviews.iterrows():
    adv_reviews.at[i, "review"] = tfms(adv_reviews.at[i, "review"])

X_train_adv, X_valid_adv, y_train_adv, y_valid_adv = prepare_data(adv_reviews)
adv_validation_loader = ReviewsDataset(X_valid_adv, y_valid_adv)

val_dl_adv = DataLoader(adv_validation_loader, batch_size=batch_size)


attacker = attack.CharAttacker(
    model,
    val_dl_original,
    val_dl_adv,
    input_format=["x", "labels", "l"],
    huggingface=False,
    criterion=torch.nn.CrossEntropyLoss(),
    accuracy=True,
    logs_after_every=50,
    device=torch.device("cpu"),
)

attacker.attack()

loss_logs, accuracy_logs = attacker.get_criterion_logs()
