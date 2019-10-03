Author: Fabio Curi Paixao 

E-mail: fcuri91@gmail.com

Date: 27.09.2019

### Installations:

Note: Start your venv and unzip all folders into the root folder.

* pip3 install -r requirements.txt
* Install GNormPlus (both Perl and Java's version): https://www.ncbi.nlm.nih.gov/research/bionlp/Tools/gnormplus/
* Install GloVe: https://nlp.stanford.edu/projects/glove/
* Clone the Byte-pair encoding repository: https://github.com/rsennrich/subword-nmt
* Download data: https://drive.google.com/file/d/1bnNKFUwPY0rwh5mHIk40pCfoc9z30R5j/view?usp=sharing

### Train Triage and Relation Extractor

   * ./bash/triage.sh && ./bash/re.sh

### RNN Training results of 2-class text classification (10-fold averaged):

|Model |Precision|Recall|F1-score|
|-------------|-------------|-------------|-------------|
|triage_data_original|0.8498|0.8724|0.8583|
|triage_data_original_BPE|0.8493|0.8563|0.8499|
|*triage_data_preprocessed|0.8576|0.8925|0.8733|
|triage_data_preprocessed_BPE|0.8395|0.8878|0.8608|

### RF/SVM/RNN Training results of 4-class relation extraction classification (10-fold averaged):

|Model |Precision|Recall|F1-score|
|-------------|-------------|-------------|-------------|
|re_RF_predictions_original_TF-IDF||||
|re_RF_predictions_original_BoW||||
|re_RF_predictions_preprocessed_TF-IDF||||
|*re_RF_predictions_preprocessed_BoW||||
|re_SVM_predictions_original_TF-IDF||||
|re_SVM_predictions_original_BoW||||
|re_SVM_predictions_preprocessed_TF-IDF||||
|re_SVM_predictions_preprocessed_BoW||||
|re_RNN_predictions_RNN_500_100_original||||
|re_RNN_predictions_RNN_500_100_preprocessed||||

### Predict and score with best models. Reference: silver standard

   * ./bash/score.sh 
   
|Task |Precision|Recall|F1-score|Output file|
|-------------|-------------|-------------|-------------|-------------|
|Triage|0.8601|0.3323|0.4614|triage.output|
|RE|0.2976|0.0732|0.1032|re.output|

##### Comment: the low recall is likely to be due to lack of representative data. 

##### Idea: add more sentences to the training corpus.
