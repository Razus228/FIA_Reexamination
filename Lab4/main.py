import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

# Load dataset
df = pd.read_csv("wine-quality-white-and-red.csv")

df['type'] = LabelEncoder().fit_transform(df['type'])
X = df.drop(columns=['quality'])
y = df['quality']

# Scale data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Initialize classifiers
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
svm_clf = SVC(kernel='rbf', random_state=42, probability=True)
knn_clf = KNeighborsClassifier(n_neighbors=5)

# Train models on entire dataset based on actual quality
rf_clf.fit(X_scaled, y)
svm_clf.fit(X_scaled, y)
knn_clf.fit(X_scaled, y)

# Predict based on actual quality for entire dataset
rf_pred = rf_clf.predict(X_scaled)
svm_pred = svm_clf.predict(X_scaled)
knn_pred = knn_clf.predict(X_scaled)

# Create DataFrames for results
rf_results = pd.DataFrame({"Wine": df.index, "Actual Quality": y, "Predicted Quality": rf_pred}).sort_values(by="Predicted Quality")
svm_results = pd.DataFrame({"Wine": df.index, "Actual Quality": y, "Predicted Quality": svm_pred}).sort_values(by="Predicted Quality")
knn_results = pd.DataFrame({"Wine": df.index, "Actual Quality": y, "Predicted Quality": knn_pred}).sort_values(by="Predicted Quality")

# Export results to CSV
rf_results.to_csv("rf_predictions.csv", index=False)
svm_results.to_csv("svm_predictions.csv", index=False)
knn_results.to_csv("knn_predictions.csv", index=False)

# Generate and save performance graphs
def plot_confusion_matrix(model, predictions, title):
    cm = confusion_matrix(y, predictions)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap='Blues')
    plt.title(title)
    plt.savefig(f"{title.lower().replace(' ', '_')}.png")
    plt.show()

plot_confusion_matrix(rf_clf, rf_pred, "Random Forest Confusion Matrix")
plot_confusion_matrix(svm_clf, svm_pred, "SVM Confusion Matrix")
plot_confusion_matrix(knn_clf, knn_pred, "KNN Confusion Matrix")

# Output a few results
print("\nRandom Forest Predictions:")
print(rf_results.head())

print("\nSVM Predictions:")
print(svm_results.head())

print("\nKNN Predictions:")
print(knn_results.head())
