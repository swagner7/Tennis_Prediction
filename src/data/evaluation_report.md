# 🧠 Model Evaluation Report

## Logistic Regression
- Accuracy: `0.8766`
- F1 Score: `0.8792`
- ROC-AUC: `0.9459917263699122`
- Cross-Validation Accuracy: `0.8646` ± 0.0073

**Classification Report:**

```text
              precision    recall  f1-score   support

           0       0.88      0.87      0.87       861
           1       0.88      0.88      0.88       890

    accuracy                           0.88      1751
   macro avg       0.88      0.88      0.88      1751
weighted avg       0.88      0.88      0.88      1751

```

**Confusion Matrix:**

```text
[[749 112]
 [104 786]]
```

## Random Forest
- Accuracy: `0.8846`
- F1 Score: `0.8870`
- ROC-AUC: `0.9495915384515001`
- Cross-Validation Accuracy: `0.8750` ± 0.0138

**Classification Report:**

```text
              precision    recall  f1-score   support

           0       0.89      0.88      0.88       861
           1       0.88      0.89      0.89       890

    accuracy                           0.88      1751
   macro avg       0.88      0.88      0.88      1751
weighted avg       0.88      0.88      0.88      1751

```

**Confusion Matrix:**

```text
[[756 105]
 [ 97 793]]
```

## Gradient Boosting
- Accuracy: `0.8829`
- F1 Score: `0.8858`
- ROC-AUC: `0.9564844902060579`
- Cross-Validation Accuracy: `0.8805` ± 0.0113

**Classification Report:**

```text
              precision    recall  f1-score   support

           0       0.89      0.87      0.88       861
           1       0.88      0.89      0.89       890

    accuracy                           0.88      1751
   macro avg       0.88      0.88      0.88      1751
weighted avg       0.88      0.88      0.88      1751

```

**Confusion Matrix:**

```text
[[751 110]
 [ 95 795]]
```
