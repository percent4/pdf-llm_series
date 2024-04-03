Multi modal RAG for PDF file.


### demo

#### LLaMA.pdf

##### qa based on tables or images

- query: What is LLaMA-7B's zero-shot accuracy on RACE dataset?

answer: 
```commandline
LLaMA-7B's zero-shot accuracy on the RACE dataset is 61.1% for RACE-middle and 46.9% for RACE-high.
```

- query: What is LLaMA model's average accuracy on MMLU dataset?

answer: 
```commandline
The LLaMA model's average accuracy on the Massive Multitask Language Understanding (MMLU) dataset is 63.4% as indicated in Table 9.

If you refer to the detailed results provided in Table 16, the average accuracy of the LLaMA 65B model specifically across all domains for the 5-shot setting is 63.4%.
```

- query: LLaMA 7B zero-shot performance on PIQA, SIQA, BoolQ dataset

answer:
```commandline
The zero-shot performance of the LLaMA 7B model on various Common Sense Reasoning tasks, including PIQA, SIQA, and BoolQ, is presented in the last image that contains multiple tables. This particular performance can be found in the "LLaMA 7B" row of the "0-shot" column across different datasets.

For PIQA, the zero-shot performance of LLaMA 7B is 76.5. For SIQA, it is 79.8. For BoolQ, the model scores 48.9.

These numbers indicate how well the LLaMA 7B model can perform on these specific tasks without any fine-tuning or additional shots, relying solely on its pre-existing training and capabilities to infer answers.
```

- query: pretraining data of LLaMA and their prop

answer:
```commandline
The pre-training data of LLaMA and their proportions from the various sources are as follows:

1. CommonCrawl: 67.0%
2. C4: 15.0%
3. Github: 4.5%
4. Wikipedia: 4.5%
5. Books: 4.5%
6. ArXiv: 2.5%
7. StackExchange: 2.0%

These sources were used for pre-training LLaMA models, with CommonCrawl being the largest proportion of the data used. The percentages indicate how much of each source was included in the mix of pre-training data.
```

##### qa based on pure text

- query: What are mathematical reasoning benchmarks in this paper?

answer: 
```commandline
The mathematical reasoning benchmarks mentioned in the text are MATH and GSM8k. The MATH dataset contains 12K middle school and high school mathematics problems, while the GSM8k is a set of middle school mathematical problems. The paper discusses evaluating models on these benchmarks and comparing model performance, specifically mentioning LLaMA model variants and their performance relative to other models such as PaLM and Minerva.
```

- query: what is the use of TruthfulQA?

```commandline
TruthfulQA is a benchmark designed to measure the truthfulness of a model's responses. Specifically, it evaluates the ability of a model to identify when a claim is true in the context of "literal truth about the real world" rather than claims that may only be considered true within a belief system or tradition. This means that TruthfulQA aims to help determine how effectively a model can distinguish valid information from misinformation or false claims, which can be indicative of the model's potential to generate reliable or misleading content. It is used to assess the risks of models in generating misinformation and to improve the design of models to mitigate these risks. The benchmark typically includes a set of questions that a language model must answer, and the model's responses are evaluated for both truthfulness and informativeness.
```

#### BLOOM.pdf

##### qa based on tables or images

- query: What's carbon emission of BLOOM?

answer:
```commandline
As shown in the first image, the CO2 equivalent emissions for BLOOM are listed as 25 tons. This is in the context of comparing it to similar large language models (LLMs) such as GPT-3, Gopher, and OPT. The table indicates the number of parameters, power consumption, and the resulting carbon emissions for each model.
```

- query: What's the number of data parallelism, tensor parallelism, pipeline parallelism in 3D-parallelism during the training of BLOOM?

answer:
```commandline
In the second image which illustrates the 3D-parallelism used during the training of BLOOM, it shows:

- Data Parallelism (DP): 8 copies of the model are trained in parallel.
- Tensor Parallelism (TP): Model parameters are divided across 4 GPUs.
- Pipeline Parallelism (PP): The layers of the model are spread across 12 groups of GPUs.

Therefore, the numbers for data parallelism, tensor parallelism, and pipeline parallelism are 8, 4, and 12, respectively.
```

- query: What is the training framework of BLOOM? What's the number of data parallelism, tensor parallelism, pipeline parallelism in 3D-parallelism during the training of BLOOM?

answer:
```commandline
The training framework of BLOOM is based on Megatron-DeepSpeed, which is a framework for large-scale distributed training. It utilized Megatron-LM for the Transformer implementation, tensor parallelism, and data loading primitives, while DeepSpeed provided the ZeRO optimizer, model pipelining, and general distributed training components.

In the context of 3D parallelism employed during the training of BLOOM, the process involves a combination of data parallelism (DP), tensor parallelism (TP), and pipeline parallelism (PP). According to the provided images, there are 8 copies of the model trained in parallel with data parallelism, each model replicated on a different GPU. The tensor parallelism is set to 4, which indicates that individual layers of the model are partitioned across 4 GPUs. The pipeline parallelism involves splitting up the model's layers across multiple GPUs, in this case, among 2 groups of GPUs.

Additionally, an image depicts a detailed illustration of the GPU setup for the training, showing the data batch being split across 8 data parallel (DP) nodes, with tensor parallelism splitting layers across 4 GPUs within each of these nodes, and pipeline parallelism splitting layers across 2 groups of GPUs. Thus, considering the entire setup, we can infer that the model employs 8-way data parallelism, 4-way tensor parallelism, and appears to utilize 2-way pipeline parallelism in the illustrated training configuration.
```
##### qa based on pure text

- query: what is the training framework of BLOOM?

answer:
```commandline
The training framework for BLOOM is Megatron-DeepSpeed, which utilizes large-scale distributed training. The Megatron-LM component provides the Transformer implementation, tensor parallelism, and data loading primitives, while DeepSpeed offers the ZeRO optimizer, model pipelining, and general distributed training components. This allows for efficient training with 3D parallelism, which is a combination of data parallelism (DP), tensor parallelism (TP), and pipeline parallelism (PP).
```

#### BERT.pdf

##### qa based on tables or images

- query: What's BERT large performance on QQP dataset in GLUE benchmark?

answer:
```commandline
Based on the given image, BERTLARGE's performance on the QQP (Quora Question Pairs) dataset in the GLUE (General Language Understanding Evaluation) benchmark is 72.1%.
```

- query: the input Embeddings of BERT, and what is the fist and last token of the input text?

answer:
```commandline
The image shows the input representation used by BERT (Bidirectional Encoder Representations from Transformers). The input embeddings for BERT are composed of the sum of three different types of embeddings:

1. Token Embeddings: These are embeddings at the word or sub-word level, given by WordPiece embeddings. In the example, the tokens are "[CLS]", "he", "likes", "play", "##ing", "[SEP]", "my", "dog", "is", "cute", and "[SEP]".

2. Segment Embeddings: These embeddings differentiate between pairs of sentences in the input. There are two types of segment embeddings, "E_A" for the first sentence and "E_B" for the second sentence. In the image, the segment embeddings switch from "E_A" to "E_B" after the first "[SEP]" token.

3. Position Embeddings: These capture the sequential nature of the tokens by providing unique embeddings according to the position of the token in the sequence. The example includes position embeddings from "E_0" to "E_10".

The first token of the input text is a special classification token "[CLS]" which is used for classification tasks, and the last tokens are special separator tokens "[SEP]" which are used for separating sentences or segments in the text.
```

##### qa based on pure text

- query: What stands for GLUE in the paper of BERT?


```commandline
In the paper of BERT (Bidirectional Encoder Representations from Transformers), "GLUE" stands for the General Language Understanding Evaluation. The GLUE benchmark is a collection of diverse natural language understanding tasks used to evaluate and compare the performance of machine learning models on a variety of linguistic challenges.
```

#### Attention.pdf

##### qa based on tables or images

- query: What is the per-layer complexity in self attention?


```commandline
The per-layer complexity for self-attention as mentioned in the text is O(n^2 · d), where n is the sequence length and d is the representation dimension.
```

- query: the architecture of Transformer Encoder


```commandline
The Transformer architecture consists of two main components: the encoder and the decoder. Each component is composed of a stack of N identical layers.

1. Encoder: The encoder includes the following sub-layers:
   - Input Embedding: The input sequence is converted into vectors of fixed dimensionality.
   - Positional Encoding: These are added to the input embeddings to provide information about the position of each word in the sequence.
   - Multi-Head Self-Attention: This mechanism allows the model to weigh the importance of different words within the same sentence for a given word.
   - Add & Norm: Each sub-layer output undergoes a residual connection followed by layer normalization.
   - Feed Forward: A fully connected feed-forward network is applied to each position separately and identically.

The encoder processes the input sequence and transforms it into a continuous representation that carries semantic information about each word in the context of the entire sequence.

2. Decoder: The decoder also consists of a stack of N identical layers with additional components compared to the encoder:
   - Output Embedding: The target sequence is also transformed into vectors of fixed dimensionality, and positional encodings are added similarly to the encoder's input embedding.
   - Masked Multi-Head Self-Attention: This mechanism prevents positions from attending to subsequent positions, ensuring that the prediction for a given position can only depend on known outputs at positions before it.
   - Multi-Head Attention: This layer allows the decoder to attend to the encoder's output.
   - Add & Norm: Similar to the encoder, each sub-layer output goes through a residual connection followed by layer normalization.
   - Feed Forward: Similar to the encoder's feed-forward network.

Both the encoder's and decoder's stacks use multi-head attention to allow the model to jointly attend to information from different representation subspaces at different positions.
```

##### qa based on pure text

- query: How many GPUs are used for training Transformer?


```commandline
The training details for the Transformer model as indicated in one of your images are as follows:

- The big Transformer model was trained on 8 P100 GPUs for 3.5 days for the English-to-German translation task, achieving a state-of-the-art BLEU score of 28.4.
- For the English-to-French translation task, the Transformer (big) model was also trained on 8 P100 GPUs but for only 3.5 days, achieving a BLEU score of 41.8.

These details suggest that the Transformer models used 8 P100 GPUs for training.
```