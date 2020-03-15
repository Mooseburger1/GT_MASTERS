# LunarLander-v2

The scripts in this module require
* python 3.7.x
* Tensorflow 2.0

Both Tensorflow CPU and GPU should work interchangeably as the main gridsearch was performed on GPU EC2 instance on AWS and all other scripts were tested locally on Xeon CPU with no changes to the scripts themselves (only Tensorflow GPU / CPU version)

### GRIDSEARCH
*********
The agent was trained across various hyperparameters. The script to rerun this gridsearch is **lunar_gridsearch.py**. 

Example Usage
```
python lunar_gridsearch.py
```

There are no CLI arguments. The script does rely on an output structure however that requires the folders (**data**, **image**, **models**)


```
Project 2
│   README.md
│   lunar_gridsearch.py
|   lunar_launch.py
|   train_with_best_params.py    
|   requirements.txt
│
└───data
│   │   *.pickle
│   │   *.pickle
│   │   ...
│   
│   
└───images
|   │
│   └───metrics
│   |   │   *.png
│   |   │   *.png
│   |   │   ...
|   |
|   └───scores
│       │   *.png
│       │   *.png
│       │   ...
│
└───models
    │   *.h5
    │   *.h5
    |   ...
```

The **images** folder houses some metric outputs in the form of graphs. These metrics range from Scores, and epsilon values, to iteration time per episode. The **data** folder houses the actual saved values of the metrics from training. Each training session saved the output of all metrics per episode in the form of a pickle file. 

Metrics

* scores - per episode
* avg_scores - average scores per 100 episodes (per episode)
* eps_history - epsilon value per episode
* iter_time - time per episode
* mem_full - memory capacity per episode

The **models** folder houses the saved NN weights for each training session. The naming convention for all outputs is gamma_memorySize_epsilonDecay.[png, h5, pickle]


### AGENT REPLAY
************
A user can load a saved model and launch the agent using the **lunar_launch.py** script. The only CLI arguments for this script is the full path to the model to be restored

args
\----
[-m, --model] - Path to model to be restored

Example Usage
```
python lunar_launch.py -m models/model__0.99_1000000_1.h5
```

### BEST PARAMS
******************
The script **train_with_best_params.py** is used to train an agent using only the best params as found in the gridsearch. The ouput of this script is all the aformentioned outputs, but under the naming convention *best_model*

Example Usage
```
python train_with_best_params.py
```



