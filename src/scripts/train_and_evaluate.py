import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report
)
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

def evaluate_model(name, model, X_train, y_train, X_test, y_test, report_lines):
    preds = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    roc_auc = roc_auc_score(y_test, proba) if proba is not None else "N/A"
    conf_matrix = confusion_matrix(y_test, preds)
    class_report = classification_report(y_test, preds)

    # Cross-validation (5-fold)
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')

    print(f"\n📊 {name}")
    print(f"Accuracy: {acc:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"ROC-AUC: {roc_auc}")
    print("Cross-Validation Accuracy:", np.round(cv_scores, 4))
    print("Classification Report:")
    print(class_report)
    print("Confusion Matrix:\n", conf_matrix)

    # Record to report
    report_lines.append(f"## {name}")
    report_lines.append(f"- Accuracy: `{acc:.4f}`")
    report_lines.append(f"- F1 Score: `{f1:.4f}`")
    report_lines.append(f"- ROC-AUC: `{roc_auc}`")
    report_lines.append(f"- Cross-Validation Accuracy: `{cv_scores.mean():.4f}` ± {cv_scores.std():.4f}")
    report_lines.append("\n**Classification Report:**\n")
    report_lines.append("```text\n" + class_report + "\n```")
    report_lines.append("\n**Confusion Matrix:**\n")
    report_lines.append("```text\n" + str(conf_matrix) + "\n```\n")

def main():
    X = pd.read_csv('../data/X.csv')
    y = pd.read_csv('../data/y.csv').squeeze()

    # Optional: scale features
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42)
    }

    report_lines = ["# 🧠 Model Evaluation Report\n"]

    for name, model in models.items():
        model.fit(X_train, y_train)
        evaluate_model(name, model, X_train, y_train, X_test, y_test, report_lines)

    # Export report
    with open('../data/evaluation_report.md', 'w') as f:
        f.write("\n".join(report_lines))

    print("\n✅ Evaluation complete. Report saved to '../data/evaluation_report.md'")

if __name__ == "__main__":
    main()
