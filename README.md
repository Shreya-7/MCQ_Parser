# MCQ_Parser

Takes a sample file containing MCQs (questions, answers, options, possible explanations).
Parses them into a uniform format.

Input formats currently accepted are same as the sample files.
Explanations are optional.

Usage:

1) Parse with explanations:

python3 qconvert.py -f file_name

2) Parse without explanations:

python3 qconvert.py file_name
