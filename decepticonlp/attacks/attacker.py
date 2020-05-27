__author__ = "Abheesht Sharma"

from tqdm import tqdm
import torch

loss_type_tuple = (
    # torch.nn.modules.loss.BCELoss,
    torch.nn.modules.loss.BCEWithLogitsLoss,
    torch.nn.modules.loss.CrossEntropyLoss,
    # torch.nn.modules.loss.NLLLoss,
)


class Attacker(object):
    """
        Performs inference on original dataset and adversarial dataset and compares their performance. This class is for models which return the logits (the output before activation).
        Args:
        model: PyTorch model
            -Pretrained PyTorch model (trained on benign training set) for inference
        
        data_loader: torch.utils.data.Dataloader 
            -Dataloader object of the original test set
        
        adversarial_data_loader: torch.utils.data.Dataloader
            -Dataloader object of the adversarial test set
        
        input_format: list (of strings) (default: ['input_ids','labels'])
            -The input format as you would feed to your model (in the same sequence as in your dataloader)
            -labels' necessary.
            Eg:
                For BertForSequenceClassification, the input_format will be ['input_ids','attention_masks','labels'] (if you are feeding only these three to the model).

        criterion: PyTorch Loss (default: torch.nn.CrossEntropyLoss())
            -should be one of torch.nn.modules.loss.BCEWithLogitsLoss, torch.nn.modules.loss.CrossEntropyLoss
        
        accuracy: boolean (default: True)
            -If True, logs and prints the accuracy
        
        logs_after_every: int (default: 50)
            -number of batch intervals after which loss (and accuracy) is/are logged.
        
        device: torch.device (default: torch.device('cpu'))
            -to push the inputs/model to CPU/GPU.
    """

    def input_format_labels_error_message(self):
        return "'labels' should be in input_format list"

    def loss_type_error_message(self):
        return "Loss should be one of " + str(loss_type_tuple)

    def __init__(
        self,
        model,
        data_loader,
        adversarial_data_loader,
        input_format=["input_ids", "labels"],
        criterion=torch.nn.CrossEntropyLoss(),
        accuracy=True,
        threshold=0.5,
        logs_after_every=50,
        device=torch.device("cpu"),
    ):

        # Assertion Tests
        assert "labels" in input_format, self.input_format_labels_error_message()
        assert isinstance(criterion, loss_type_tuple), self.loss_type_error_message()

        # initialise parameters
        self.model = model.to(device)
        self.data_loader = data_loader
        self.adversarial_data_loader = adversarial_data_loader
        self.input_format = input_format
        self.criterion = criterion
        self.accuracy = accuracy
        self.threshold = threshold
        self.logs_after_every = logs_after_every
        self.device = device

        self.loss_logs = {}
        self.accuracy_logs = {}

    def attack(self):

        # set model to eval mode
        self.model.eval()

        print("Running inference on original dataset")

        (
            self.loss_logs["original"],
            self.accuracy_logs["original"],
        ) = self.inference_loop(self.data_loader)

        print("Running inference on adversarial dataset")

        (
            self.loss_logs["adversarial"],
            self.accuracy_logs["adversarial"],
        ) = self.inference_loop(self.adversarial_data_loader)

    def inference_loop(self, dataloader):
        # Define inference loop for dataloader
        running_loss = 0.0
        correct_total = 0
        counter = 1

        loss_logs = []
        accuracy_logs = []

        tqdm_dataloader = tqdm(dataloader)

        for batch in tqdm_dataloader:
            inputs = batch
            input_dict = {}
            for k, i in enumerate(self.input_format):
                if i != "labels":
                    input_dict[i] = inputs[k].long().to(self.device)
                else:
                    labels = inputs[k].long().to(self.device)

            # Forward pass
            outputs = self.model(**input_dict)
            if isinstance(outputs, (tuple, list)):
                outputs = outputs[0]

            # Compute Loss

            if isinstance(self.criterion, torch.nn.modules.loss.BCEWithLogitsLoss):
                # Binary Classification, but BCEWithLogitsLoss computed sigmoid on its own, so it is assumed that the user does not have sigmoid in his model
                # apply_activation has no significance here
                computed_loss = self.criterion(
                    outputs.float().view(labels.shape), labels.float()
                )
                outputs = torch.sigmoid(outputs)

            elif isinstance(self.criterion, torch.nn.modules.loss.CrossEntropyLoss):
                # Multiclass Classification, but since CrossEntropy computes log_softmax on its own, it is assumed that the user does not have a softmax/log_softmax in his model
                # apply_activation has no significance here
                computed_loss = self.criterion(outputs, labels)
                outputs = torch.log_softmax(outputs, dim=1)

            running_loss += computed_loss.item()
            loss = running_loss / (counter * dataloader.batch_size)

            # Log the loss
            if counter % self.logs_after_every == 0:
                loss_logs.append(loss)

            tqdm_dataloader.set_description("Loss (%f)" % (loss))

            # Compute Accuracy
            if self.accuracy:

                if isinstance(self.criterion, torch.nn.modules.loss.BCEWithLogitsLoss):
                    computed_labels = (outputs > self.threshold).float()

                elif isinstance(self.criterion, torch.nn.modules.loss.CrossEntropyLoss):
                    _, computed_labels = torch.max(outputs, dim=1)

                correct = (computed_labels.view(labels.shape) == labels).float().sum()
                correct_total += correct
                acc = correct_total / (counter * dataloader.batch_size)

                # Log the accuracy
                if counter % self.logs_after_every == 0:
                    accuracy_logs.append(acc)

                tqdm_dataloader.set_postfix(Accuracy=acc)

            # Increment counter
            counter += 1

        return loss_logs, accuracy_logs

    # Getter functions

    def get_criterion_logs(self):
        return self.loss_logs, self.accuracy_logs
