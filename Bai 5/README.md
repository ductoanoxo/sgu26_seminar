# Bai 5 - Chuoi Lab GenAI (Lab 6 den Lab 11)

Bai 5 tong hop cac bai thuc hanh ve Generative AI trong lap trinh, tap trung vao prompt engineering, workflow voi Copilot/OpenAI, xay dung API, va danh gia chat luong ket qua.

## Thong tin nhanh

- Mon hoc: Seminar chuyen nganh
- Truong: Dai hoc Sai Gon (SGU)
- Pham vi bai: Lab 6 -> Lab 11
- Thu muc chinh: `lab/`

## Cau truc thu muc

```text
Bai 5/
├── README.md
└── lab/
    ├── lab6/
    ├── lab7/
    ├── lab8/
    ├── lab9/
    ├── lab10/
    └── lab11/
```

## Tong quan noi dung tung lab

### Lab 6
- Tap trung vao xu ly du lieu van ban thong ke tu Reuters dataset.
- Trich xuat body text, tien xu ly, thong ke tan suat ky tu/n-grams.
- Tep tieu bieu:
  - `lab/lab6/lab6.ipynb`
  - `lab/lab6/letter_frequencies.csv`
  - `lab/lab6/reuters21578/`

### Lab 7
- Xay dung microservice Flask tinh Manhattan distance.
- Co Dockerfile, tests, va bo prompt ho tro explain/debug.
- Tep tieu bieu:
  - `lab/lab7/app.py`
  - `lab/lab7/src/manhattan.py`
  - `lab/lab7/tests/`
  - `lab/lab7/README.md`

### Lab 8
- Cac mau prompting patterns cho sinh code Python.
- Bao gom template-based, few-shot, iterative prompt va chain-of-thought workflow.
- Tep tieu bieu:
  - `lab/lab8/code_samples/`
  - `lab/lab8/README.md`

### Lab 9
- So sanh cac chien luoc prompt: baseline, CoT, naive chaining, selective chaining.
- Co script doi chieu ket qua giua cac phuong phap.
- Tep tieu bieu:
  - `lab/lab9/lab91_baseline.py`
  - `lab/lab9/lab93_cot.py`
  - `lab/lab9/lab96_comparison.py`
  - `lab/lab9/README.md`

### Lab 10
- Tiep tuc mo rong API Manhattan distance va workflow prompt cho refactor/performance.
- Co Dockerfile va cac script prompt trong `prompts/`.
- Tep tieu bieu:
  - `lab/lab10/app.py`
  - `lab/lab10/prompts/`
  - `lab/lab10/README.md`

### Lab 11
- Lam quen quy trinh fine-tuning va so sanh model base vs fine-tuned.
- Co du lieu train (`*.jsonl`) va script compare ket qua.
- Tep tieu bieu:
  - `lab/lab11/lab11_base.py`
  - `lab/lab11/lab11_fine-tuned.py`
  - `lab/lab11/lab11_compare_fine-tuned.py`
  - `lab/lab11/fine_tuning.jsonl`

## Huong dan chay nhanh

Tu thu muc `Bai 5`, co the thu nghiem nhanh nhu sau:

```powershell
# 1) Chay Flask API (Lab 7)
cd lab/lab7
pip install -r requirements.txt
python app.py

# 2) Chay test Lab 7
py -3 -m unittest discover -s tests -p "test_*.py" -v

# 3) Chay cac script chien luoc prompt (Lab 9)
cd ../lab9
python lab91_baseline.py
python lab93_cot.py
python lab96_comparison.py

# 4) Chay script fine-tuning workflow co ban (Lab 11)
cd ../lab11
python lab11_base.py
python lab11_compare_base.py
```

## Ghi chu moi truong

- Khuyen nghi Python 3.10+.
- Mot so script can API key neu goi OpenAI.
- Khong commit API key vao repository.

## De xuat mo rong

- Bo sung README rieng cho `lab6/` va `lab11/` de dong nhat tai lieu.
- Them `requirements.txt` rieng cho tung lab neu can tach moi truong.
- Chuan hoa output va them benchmark nho cho cac chien luoc prompt o Lab 9/11.
