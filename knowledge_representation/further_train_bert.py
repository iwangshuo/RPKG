# !pip install -q transformers
# !pip install -q datasets

import multiprocessing
import pandas as pd
import numpy as np
import torch
import matplotlib.pyplot as plt
import transformers

from sklearn.model_selection import train_test_split
from datasets import Dataset
from transformers import AutoModelForMaskedLM
from transformers import AutoTokenizer, AutoConfig
from transformers import BertForMaskedLM, DistilBertForMaskedLM
from transformers import BertTokenizer, DistilBertTokenizer
from transformers import RobertaTokenizer, RobertaForMaskedLM
from transformers import Trainer, TrainingArguments
from transformers import DataCollatorForLanguageModeling
from tokenizers import BertWordPieceTokenizer

# HYPERPARAMS
SEED_SPLIT = 0
SEED_TRAIN = 0

MAX_SEQ_LEN = 128
TRAIN_BATCH_SIZE = 64
EVAL_BATCH_SIZE = 64
LEARNING_RATE = 2e-5
LR_WARMUP_STEPS = 100
WEIGHT_DECAY = 0.01

# load data
dtf_mlm = pd.read_csv('../data/corpus_data.csv', encoding='utf-8')

# Train/Valid Split
df_train, df_valid = train_test_split(
    dtf_mlm, test_size=0.15, random_state=SEED_SPLIT
)
print(len(df_train), len(df_valid))

# Convert to Dataset object
train_dataset = Dataset.from_pandas(df_train[['text']].dropna())
valid_dataset = Dataset.from_pandas(df_valid[['text']].dropna())

'''
bert-base-uncased  # 12-layer, 768-hidden, 12-heads, 109M parameters
distilbert-base-uncased  # 6-layer, 768-hidden, 12-heads, 65M parameters
'''

MODEL = 'bert'
bert_type = 'bert-base-uncased'

if MODEL == 'distilbert':
    TokenizerClass = DistilBertTokenizer
    ModelClass = DistilBertForMaskedLM
elif MODEL == 'bert':
    TokenizerClass = BertTokenizer
    ModelClass = BertForMaskedLM
elif MODEL == 'roberta':
    TokenizerClass = RobertaTokenizer
    ModelClass = RobertaForMaskedLM
elif MODEL == 'scibert':
    TokenizerClass = AutoTokenizer
    ModelClass = AutoModelForMaskedLM

# bert_type = '/home/wshuo/dukto/uncased_L-12_H-768_A-12'
# TokenizerClass = BertTokenizer
# ModelClass = BertForMaskedLM

tokenizer = TokenizerClass.from_pretrained(
            bert_type, use_fast=True, do_lower_case=False, max_len=MAX_SEQ_LEN
            )
model = ModelClass.from_pretrained(bert_type)

# creating new tokenizer
tokenizer = TokenizerClass.from_pretrained(
            bert_type, use_fast=True, do_lower_case=False, max_len=MAX_SEQ_LEN
            )
print(tokenizer.tokenize('ros'))
print(tokenizer.tokenize('rplidar'))

new_tokens = []
df_region_word_example = pd.read_csv('../data/test_region_word_in_examples.csv', encoding='utf-8')
example_wds = df_region_word_example['word'].dropna().tolist()
new_tokens.extend(example_wds)
df_region_word_final = pd.read_csv('../data/region_word_frequency_final.csv', encoding='utf-8')
final_wds = df_region_word_final['word'].dropna().tolist()
for wd in final_wds:
    if wd not in new_tokens:
        new_tokens.append(wd)
print(len(new_tokens))

# update tokenizer
tokenizer.add_tokens(new_tokens[:850])
model.resize_token_embeddings(len(tokenizer))

print(tokenizer.tokenize('ros'))
print(tokenizer.tokenize('rplidar'))

# save new tokenizer
tokenizer.save_pretrained("./new_tokenizer")

# phrase = "ros stands for robot operating system, which is an open-source framework for building robotic software."
# print(phrase)
# tokens = tokenizer.encode_plus(phrase, add_special_tokens=True, return_tensors='pt')
# ids = tokens['input_ids'].numpy().tolist()
# print(ids)

def tokenize_function(row):
    return tokenizer(
        row['text'],
        padding='max_length',
        truncation=True,
        max_length=MAX_SEQ_LEN,
        return_special_tokens_mask=True)

column_names = train_dataset.column_names

train_dataset = train_dataset.map(
    tokenize_function,
    batched=True,
    num_proc=multiprocessing.cpu_count(),
    remove_columns=column_names,
)

valid_dataset = valid_dataset.map(
    tokenize_function,
    batched=True,
    num_proc=multiprocessing.cpu_count(),
    remove_columns=column_names,
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)

steps_per_epoch = int(len(train_dataset) / TRAIN_BATCH_SIZE)

# logging_steps=1,
training_args = TrainingArguments(
    output_dir='./bert-news',
    logging_dir='./LMlogs',
    num_train_epochs=100,
    do_train=True,
    do_eval=True,
    per_device_train_batch_size=TRAIN_BATCH_SIZE,
    per_device_eval_batch_size=EVAL_BATCH_SIZE,
    warmup_steps=LR_WARMUP_STEPS,
    save_steps=steps_per_epoch,
    save_total_limit=3,
    weight_decay=WEIGHT_DECAY,
    learning_rate=LEARNING_RATE,
    evaluation_strategy='epoch',
    save_strategy='epoch',
    load_best_model_at_end=True,
    metric_for_best_model='loss',
    greater_is_better=False,
    seed=SEED_TRAIN,
    logging_steps=1,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=valid_dataset,
    tokenizer=tokenizer,
)

trainer.train()
trainer.save_model("./model")
