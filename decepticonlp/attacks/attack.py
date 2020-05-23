from tqdm import tqdm
import torch

loss_type_list = [
    torch.nn.modules.loss.BCELoss,
    torch.nn.modules.loss.BCEWithLogitsLoss,
    torch.nn.modules.loss.CrossEntropyLoss,
    torch.nn.modules.loss.NLLLoss,
]


class CharAttackerWithHuggingFace:
    """
		Args:
		model: PyTorch model
			-Pretrained PyTorch model (trained on benign training set) for inference
		
		data_loader: torch.utils.data.Dataloader 
			-Dataloader object of the original test set
		
		adversarial_data_loader: torch.utils.data.Dataloader
			-Dataloader object of the adversarial test set
		
		input_format: list (of strings) (default: ['input_ids','labels'])
			-The input format as you would feed to your model.
			Eg:
				For BERTForSequenceClassification, the input_format will be ['input_ids','attention_masks','labels'] (if you are feeding only these three to the model).
		
		accuracy: boolean (default: True)
			-If True, logs and prints the accuracy
		
		logs_after_every: int (default: 50)
			-number of batch intervals after which loss (and accuracy) is/are logged.
		
		device: torch.device (default: torch.device('cpu'))
			-to push the inputs/model to CPU/GPU.
	"""

    def __init__(
        self,
        model,
        data_loader,
        adversarial_data_loader,
        input_format,
        accuracy=True,
        logs_after_every=50,
        device=torch.device("cpu"),
    ):

        # initialise parameters
        self.model = model.to(device)
        self.data_loader = data_loader
        self.adversarial_data_loader = adversarial_data_loader
        self.input_format = input_format
        self.accuracy = accuracy
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
                input_dict[i] = inputs[k].long().to(self.device)

            # Forward pass
            outputs = self.model(**input_dict)
            # Compute Loss and probabilities
            computed_loss = outputs[0]
            logits = outputs[1]
            probabilities = torch.nn.functional.log_softmax(logits, dim=1)

            running_loss += computed_loss.item()
            loss = running_loss / (counter * dataloader.batch_size)

            # Log the loss
            if counter % self.logs_after_every == 0:
                loss_logs.append(loss)

            tqdm_dataloader.set_description("Loss (%f)" % (loss))

            # Compute Accuracy
            if self.accuracy:
                _, computed_labels = torch.max(probabilities, dim=1)
                correct = (computed_labels == input_dict["labels"]).float().sum()

                correct_total += correct
                acc = correct_total / (counter * dataloader.batch_size)

                if counter % self.logs_after_every == 0:
                    accuracy_logs.append(acc)

                tqdm_dataloader.set_postfix(Accuracy=acc)

            # Increment counter
            counter += 1
        return loss_logs, accuracy_logs

    # Getter functions

    def get_criterion_logs(self):
        return self.loss_logs, self.accuracy_logs


class CharAttacker:
    """
		Args:
		model: PyTorch model
			-Pretrained PyTorch model (trained on benign training set) for inference
		
		data_loader: torch.utils.data.Dataloader 
			-Dataloader object of the original test set
		
		adversarial_data_loader: torch.utils.data.Dataloader
			-Dataloader object of the adversarial test set
		
		criterion: dict
			-Has the following format: 
			{'loss': Torch Loss Object, 'accuracy': True/False}
		
		input_format: list (of strings) (default: ['input_ids','labels'])
			-The input format as you would feed to your model
			Eg: "def forward(self, inputs, input_length)" will have ['inputs','input_length', 'labels'] as the input_format.
		
		threshold: float (range: 0 to 1) (default: 0.5) 
			-valid only if criterion['accuracy'] is True.
			-threshold for calculating accuracy .
		
		apply_activation: boolean (default: False) -- only for output_format = 'normal'
			-valid only if output_format = 'normal'
			-if True, apply sigmoid/softmax in the inference loop.
			-if False, sigmoid/softmax is a part of the model itself.
		
		logs_after_every: int (default: 50)
			-number of batch intervals after which loss (and accuracy) is/are logged.
		
		device: torch.device (default: torch.device('cpu'))
			-to push the inputs/model to CPU/GPU.
	"""

    def criterion_format_error_message(self):
        return "Criterion (loss/accuracy) should be dictionary"

    def loss_type_error_message(self):
        return "Loss should be one of " + str(loss_type_list)

    def criterion_loss_error_message(self):
        return "'loss' should be a key in criterion"

    def criterion_accuracy_error_message():
        return "'accuracy' should be a key in criterion"

    def __init__(
        self,
        model,
        data_loader,
        adversarial_data_loader,
        criterion,
        input_format,
        apply_activation=False,
        threshold=0.5,
        logs_after_every=50,
        device=torch.device("cpu"),
    ):
        # Assertion tests
        assert type(criterion) == dict, self.criterion_format_error_message()

        assert "loss" in criterion.keys(), self.criterion_loss_error_message()

        assert "accuracy" in criterion.keys(), self.criterion_accuracy_error_message()

        assert type(criterion["loss"]) in loss_type_list, self.loss_type_error_message()

        # initialise parameters
        self.model = model.to(device)
        self.data_loader = data_loader
        self.adversarial_data_loader = adversarial_data_loader
        self.criterion = criterion
        self.input_format = input_format
        self.apply_activation = apply_activation
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

            # Compute Loss
            if type(self.criterion["loss"]) == torch.nn.modules.loss.BCELoss:
                # Binary Classification with Sigmoid
                if self.apply_activation:
                    outputs = torch.sigmoid(outputs)
                computed_loss = self.criterion["loss"](outputs.float(), labels.float())

            elif (
                type(self.criterion["loss"]) == torch.nn.modules.loss.BCEWithLogitsLoss
            ):
                # Binary Classification, but BCEWithLogitsLoss computed sigmoid on its own, so it is assumed that the user does not have sigmoid in his model
                # apply_activation has no significance here
                computed_loss = self.criterion["loss"](
                    outputs.float().view(labels.shape), labels.float()
                )
                outputs = torch.sigmoid(outputs)

            elif type(self.criterion["loss"]) == torch.nn.modules.loss.NLLLoss:
                # Multiclass Classification, with Log_Softmax
                if self.apply_activation:
                    outputs = torch.log_softmax(outputs, dim=1)
                computed_loss = self.criterion["loss"](outputs, labels)

            elif type(self.criterion["loss"]) == torch.nn.modules.loss.CrossEntropyLoss:
                # Multiclass Classification, but since CrossEntropy computes log_softmax on its own, it is assumed that the user does not have a softmax/log_softmax in his model
                # apply_activation has no significance here
                computed_loss = self.criterion["loss"](outputs, labels)
                outputs = torch.log_softmax(outputs, dim=1)

            running_loss += computed_loss.item()
            loss = running_loss / (counter * dataloader.batch_size)

            # Log the loss
            if counter % self.logs_after_every == 0:
                loss_logs.append(loss)

            tqdm_dataloader.set_description("Loss (%f)" % (loss))

            # Compute Accuracy
            if self.criterion["accuracy"]:

                if (type(self.criterion["loss"]) == torch.nn.modules.loss.BCELoss) or (
                    type(self.criterion["loss"])
                    == torch.nn.modules.loss.BCEWithLogitsLoss
                ):
                    computed_labels = (outputs > self.threshold).float()

                elif (
                    type(self.criterion["loss"]) == torch.nn.modules.loss.NLLLoss
                ) or (
                    type(self.criterion["loss"])
                    == torch.nn.modules.loss.CrossEntropyLoss
                ):
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
