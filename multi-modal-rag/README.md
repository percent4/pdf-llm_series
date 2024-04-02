Multi modal RAG for PDF file.


### demo

PDF file: LLaMA.pdf

qa based on tables or images:

- query: What is LLaMA-7B's zero-shot accuracy on RACE dataset?

answer: 
```commandline
LLaMA-7B's zero-shot accuracy on the RACE dataset is 61.1% for RACE-middle and 46.9% for RACE-high.
```

- query: What is LLaMA model's accuracy on MMLU dataset?

answer: 
```commandline
The LLaMA model's accuracy on the MMLU dataset for the 65B parameter version is 63.4%.
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

qa_based_on_pure_text:

- query: What are mathematical reasoning benchmarks in this paper?

answer: 
```commandline
The mathematical reasoning benchmarks mentioned in the text are MATH and GSM8k. The MATH dataset contains 12K middle school and high school mathematics problems, while the GSM8k is a set of middle school mathematical problems. The paper discusses evaluating models on these benchmarks and comparing model performance, specifically mentioning LLaMA model variants and their performance relative to other models such as PaLM and Minerva.
```

- query: what is the use of TruthfulQA?

```commandline
TruthfulQA is a benchmark designed to measure the truthfulness of a model's responses. Specifically, it evaluates the ability of a model to identify when a claim is true in the context of "literal truth about the real world" rather than claims that may only be considered true within a belief system or tradition. This means that TruthfulQA aims to help determine how effectively a model can distinguish valid information from misinformation or false claims, which can be indicative of the model's potential to generate reliable or misleading content. It is used to assess the risks of models in generating misinformation and to improve the design of models to mitigate these risks. The benchmark typically includes a set of questions that a language model must answer, and the model's responses are evaluated for both truthfulness and informativeness.
```