from matplotlib import pyplot as plt
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import os

def make_decision(material):
    decyzja = clf.predict(material)
    return 1 if decyzja[0] == 1 else 0

file_path = os.path.join(os.path.dirname(__file__), 'dane.csv')
with open(file_path, 'r') as plik:
    dane = []
    next(plik)
    for linia in plik:
        wartosci = [int(w) for w in linia.strip().split(';')]
        dane.append(wartosci)

file_path = os.path.join(os.path.dirname(__file__), 'decyzje.csv')
with open(file_path) as plik2:
    decyzje = []
    next(plik2)
    for linia in plik2:
        wartosci = [int(w) for w in linia.strip().split()]
        decyzje.extend(wartosci)

X_train, X_test, y_train, y_test = train_test_split(dane, decyzje, test_size=0.2, train_size=0.8)

clf = tree.DecisionTreeClassifier(criterion='entropy')
clf = clf.fit(X_train, y_train)
tree.plot_tree(clf, feature_names=["długość przebywania w magazynie", "waga", "materiał", "wysokość",
                                      "szerokość", "głębokość", "priorytet", "ostrożność"])
plt.savefig("./tree.svg")

predict = clf.predict(X_test)

accuracy = accuracy_score(y_test, predict)

nowy_material = [[1, 10, 1, 50, 50, 50, 2, 1]]
zly_material = [[1, 30, 2, 50, 3, 100, 1, 1]]
make_decision(nowy_material)
make_decision(zly_material)
    