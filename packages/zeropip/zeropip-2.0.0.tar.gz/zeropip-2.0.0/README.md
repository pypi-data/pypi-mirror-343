# zeropip v2.0

# zeropip

`zeropip 2.0`은 HuggingFace 및 기타 AI 모델을 pip 없이 복원하거나 저장할 수 있는 zip 기반 도구입니다.

## 사용법
```python
from zeropip import install, save
install("model_rip.zip", "~/.cache/huggingface/hub")
...
save("~/.cache/huggingface/hub", "model_rip.zip")
```

## Author
blueradiance
