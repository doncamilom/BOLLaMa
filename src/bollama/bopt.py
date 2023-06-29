import ast
import numpy as np
from chaos.bo.module import BoModule
from chaos.data.module import BOAdditivesDataModule
from chaos.surrogate_models.gp import GP
from chaos.gprotorch.kernels.fingerprint_kernels.tanimoto_kernel import TanimotoKernel
#from chaos.data_init_selection.clustering import BOInitDataSelection
from chaos.initialization.initializers import BOInitializer
import ast
import torch
from pytorch_lightning.loggers import WandbLogger
from pytorch_lightning import Trainer
from pytorch_lightning import seed_everything

seed_everything(1, workers=True)


class LLMInterface:
    def __init__(self):
        self.design_space = ["a","v", "c","d","E","f","G","h","Z"]
        self.data_list = {}

    def initialize(self, n):

        initialization = BOInitializer(
            method="kmedoids",
            metric='euclidean',
            n_clusters=int(n),
        )

        self.data = BOAdditivesDataModule(
            'data/additives_reactions.csv',
            representation='fragprints',
            featurize_column='Additive_Smiles',
            init_sample_size=n,
            init_selection_method=initialization
        )

        return self.data.additives_reactions['Additive_Smiles'].values[self.data.train_indexes].tolist()
        # except:
        #     return "Error. Please check your input, it should be a single number."

    def optimization_step(self, d: dict):
        results_dict = ast.literal_eval(d)
        inputs, _ = zip(*results_dict.items())

        self.data.additives_reactions.loc[
            self.data.additives_reactions['Additive_Smiles'].isin(inputs),
            'UV210_Prod AreaAbs'
        ] = self.data.additives_reactions.loc[
            self.data.additives_reactions['Additive_Smiles'].isin(inputs),
            'Additive_Smiles'
        ].map(results_dict)

        train_x = self.data.x
        train_y = self.data.y

        surrogate_model = GP(train_x, train_y, kernel=TanimotoKernel())
        bo = BoModule(data=self.data, model=surrogate_model)

        trainer_config = {
            "logger": WandbLogger(project="additives-report"),
            "log_every_n_steps": 1,
            # "min_epochs": 0,
            # "max_steps": -1,
            "accelerator": "cpu",
            "devices": 1,
            "num_sanity_val_steps": 0,
            "max_epochs": 1,
            "deterministic": True
        }

        trainer =  Trainer(**trainer_config)
        trainer.fit(bo)

        trained_model = trainer.model

        # Get next experiment
        acq_repr, acq_val, acq_idx = trained_model.optimize_acqf_and_get_observation(
            self.data.heldout_x,
            self.data.heldout_y
        )
        next_smiles = self.data.additives_reactions.loc[
            acq_idx.item(),
            'Additive_Smiles'
        ]

        return f"Next experiment: {next_smiles}"


# if __name__=='__main__':
#     llm = LLMInterface()
#     llm.initialize(10)
#     llm.optimization_step(d="{'c1nnc2n1CCCC2C(=O)O': 0}")
