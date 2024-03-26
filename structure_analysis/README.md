use Baidu's `PP-Structure` for PDF structure analysis。

### PP-Structure

- website：[https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/ppstructure/README_ch.md](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/ppstructure/README_ch.md)
- command：

```bash
paddleocr --use_gpu=false --image_dir=./data/llama_split.pdf --type=structure --table=false --ocr=false
```