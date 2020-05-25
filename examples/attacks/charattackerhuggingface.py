__author__ = "Abheesht Sharma"

# Example Code on the use of CharAttacker using a HuggingFace ForSequenceClassification Model

# Import the important libraries
import sys

sys.path.append("./")

import warnings

warnings.filterwarnings("ignore")

import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler

from transformers import BertTokenizer, BertConfig
from transformers import BertForSequenceClassification
from transformers import AdamW, get_linear_schedule_with_warmup
from decepticonlp.attacks import attack
from decepticonlp.transforms import transforms

from sklearn.model_selection import train_test_split

import io

import pandas as pd
import numpy as np


# Define the Batch Size
BATCH_SIZE = 1
# Define number of test samples you want (should be between 1 and 10,000)
NUM_TEST = 15

# Define whether you want to infer on GPU/CPU
if torch.cuda.is_available():
    device = torch.device("cuda")
    devicename = "[" + torch.cuda.get_device_name(0) + "]"
else:
    device = torch.device("cpu")
    devicename = ""

# Here, we use CPU regardless
device = torch.device("cpu")
devicename = ""

print("Using PyTorch version:", torch.__version__, "Device:", device, devicename)

# Define the tokenizer
BERTMODEL = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(BERTMODEL, do_lower_case=True)

# Load the dataset
dataset = pd.read_csv("examples/attacks/datasets/IMDB Dataset.csv")

# Assign numerical class labels
dataset.loc[dataset.polarity == "positive", "polarity"] = int(1)
dataset.loc[dataset.polarity == "negative", "polarity"] = int(0)
print(dataset.head())

###############################################################################
# Define the function


def prepare_dataset(test_df):
    # Add important tokens
    sentences_test = test_df.sentence.values
    sentences_test = ["[CLS] " + s for s in sentences_test]

    labels_test = test_df.polarity.values

    tokenized_test = [tokenizer.tokenize(s) for s in sentences_test]

    # print ("The full tokenized first training sentence:")
    # print (tokenized_test[0])

    MAX_LEN_TRAIN, MAX_LEN_TEST = 128, 512

    tokenized_test = [t[: (MAX_LEN_TEST - 1)] + ["SEP"] for t in tokenized_test]

    # print ("The truncated tokenized first training sentence:")
    # print (tokenized_test[0])

    ids_test = [tokenizer.convert_tokens_to_ids(t) for t in tokenized_test]
    ids_test = np.array(
        [np.pad(i, (0, MAX_LEN_TEST - len(i)), mode="constant") for i in ids_test]
    )

    # Define the attention masks
    amasks_test = []

    for seq in ids_test:
        seq_mask = [float(i > 0) for i in seq]
        amasks_test.append(seq_mask)

    test_inputs = torch.tensor(ids_test.astype(np.int_)).long()
    test_labels = torch.tensor(labels_test.astype(np.int_)).long()
    test_masks = torch.tensor(amasks_test).long()

    print("Test: ", end="")
    test_data = TensorDataset(test_inputs, test_masks, test_labels)
    test_sampler = SequentialSampler(test_data)
    test_data_loader = DataLoader(
        test_data, sampler=test_sampler, batch_size=BATCH_SIZE
    )
    return test_data_loader


###############################################################################

# Prepare the original test dataset
test_df = dataset[40000:]

# possibly reduce the amount of training data:
test_df = test_df[:NUM_TEST]
print("Original IMDB data loaded:")
print("test:", test_df.shape)

test_dataloader = prepare_dataset(test_df)
print(len(test_dataloader), "adversarial reviews")

###############################################################################
# Do the same as above for the adversarial dataset
adv_test_df = test_df


print("Adversarial IMDB data loaded:")
print("test:", adv_test_df.shape)

# Apply transforms to the dataset
tfms = transforms.Compose(
    [
        transforms.AddChar(char_perturb=True),
        transforms.ShuffleChar(mid=True),
        transforms.TypoChar(probability=0.6),
        transforms.VisuallySimilarChar(),
        transforms.DeleteChar(),
    ]
)


for i, rows in test_df.iterrows():
    adv_test_df.at[i, "sentence"] = tfms(adv_test_df.at[i, "sentence"])

adv_test_dataloader = prepare_dataset(adv_test_df)


print(len(adv_test_dataloader), "adversarial reviews")


###############################################################################

# Load the saved model, we map it to cpu here. Feel free to remove map_location='cpu'
model = torch.load(
    "examples/attacks/pretrained models/BertForSequenceClassification.pth",
    map_location="cpu",
).to(device)

attacker = attack.CharAttacker(
    model,
    test_dataloader,
    adv_test_dataloader,
    input_format=["input_ids", "attention_mask", "labels"],
    huggingface=True,
    criterion=torch.nn.CrossEntropyLoss(),
    accuracy=True,
    logs_after_every=50,
    device=device,
)

attacker.attack()

loss_logs, accuracy_logs = attacker.get_criterion_logs()

####################################################################################################################################################################################################################
