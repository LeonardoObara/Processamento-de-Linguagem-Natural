# -*- coding: utf-8 -*-
"""Criando um classificador de textos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vuY2KKKagBCfrhRWsoyNe-yBm-gsYRPb

# **Criando um classificador de textos**

---


***Para isso vamos importar algumas bibliotecas.*** 

*CountVectorizer*: para transformar um texto em vetor.  
*TfidfTransformer*: para fazer a normalização dos dados.  
*MultinomialNB*: para assumir a independência total das features do modelo.  
*Pipeline*: para trabalhar com uma seguência de tarefas.  
*SnowballStemmer*: para reduzir uma palavra para a sua forma base.  
*SGDClassifier*: para as previsões finais do pipeline.  
*GridSearchCV*: para automatizar o ajuste dos processos.  
*f1_score*: para a visualização a precisão e recall juntas.  
*accuracy_score*: para caulo (todos os acertos / total).  
*confusion_matrix*: tabela para auxiliar a avaliação do modelo.  
*classification_report*: retornar um relatório.  
*ConfusionMatrixDisplay*: exibe em forma de imagem.
"""

from sklearn.datasets import fetch_20newsgroups 
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer 
from sklearn.naive_bayes import MultinomialNB 
from sklearn.pipeline import Pipeline 
from nltk.stem.snowball import SnowballStemmer 
import numpy as np
from sklearn.linear_model import SGDClassifier 
from sklearn.model_selection import GridSearchCV
import nltk 
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay
import warnings
import matplotlib.pyplot as plt 
warnings.simplefilter('ignore')

"""# **Carregando o Dataset**




Vamos usar o dataset fetch 20 new groups pois ele retorna uma lista de textos divididos em 20 grupos para serem alimentados por extratores de textos.
"""

newsgroups = fetch_20newsgroups(subset='train')

"""**Mostrando os grupos dentro do dataset.**"""

list(newsgroups.target_names)

"""Escolhendo 10 grupos e fazendo o treino e teste."""

categories = ['alt.atheism', 'soc.religion.christian','rec.motorcycles','rec.autos','comp.graphics','comp.os.ms-windows.misc','comp.sys.ibm.pc.hardware','sci.electronics','talk.politics.guns','sci.space',] 
df_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)
df_test = fetch_20newsgroups(subset='test', categories=categories, shuffle=True)

"""# **Apresentando as classes (grupos)**"""

df_train.target_names

"""convertendo para matriz uma coleção de texto, produzindo uma representação das contagens instanciando o algoritimo do count vectorizer."""

count_vect = CountVectorizer() 
X_train_counts = count_vect.fit_transform(df_train.data)
X_train_counts.shape

tfidf_transformer = TfidfTransformer() 
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

"""# ***Abordagem I***

**Treinando um modelo**

Utilizando o pipeline para as tarefaz serem execultadas em seguência.
"""

clf = MultinomialNB() 
clf.fit(X_train_tfidf, df_train.target)

"""# `OBS`
 Em um ambiente Jupyter, execute novamente esta célula para mostrar a representação HTML ou confiar no notebook.
No GitHub, a representação HTML não pode ser renderizada, tente carregar esta página com nbviewer.org.

# *Pipeline*
Passo 1, aplicar o count vectorizer nos textos  
Passo 2, aplicar o TFIDF nos textos  
Passo 3, aplicar o algoritmo Naive Bayes
"""

clf_1 = Pipeline([
    ('vect', CountVectorizer()),    
    ('tfidf', TfidfTransformer()), 
    ('clf', MultinomialNB())])

"""Treinando o modelo no pipeline."""

clf_trained = clf_1.fit(df_train.data, df_train.target)

"""Fazendo predição no dados de teste."""

pred = clf_trained.predict(df_test.data)

acc = np.mean(pred == df_test.target)
print('>>>> Acurácia: ', acc)

"""**Gerando as métricas de acerto do modelo.**"""

creport = classification_report(df_test.target, pred, target_names=df_test.target_names)
print(creport)

"""*Nesse modelo utilizando 10 classes (grupos) conseguimos um recall baixo para a metade, vamos tentar da uma melhorada com o tuning.*

# **Abordagem II**

***Tuning***  
*Tuning é uma forma de otimizar os dados para retornar valores mais autos.  
Criando uma lista de parâmetros para ajuste.*
"""

parameters = {'vect__ngram_range': [(1, 1), (1, 2)], 'tfidf__use_idf': (True, False), 'clf__alpha': (1e-2, 1e-3)}

"""Buscando os melhores parâmetros e treinando o modelo."""

gs_clf = GridSearchCV(clf_trained, parameters, n_jobs=-1)  
gs_clf = gs_clf.fit(df_train.data, df_train.target)

"""Mostrando a melhor pontuação."""

print(gs_clf.best_score_)
gs_clf.best_params_

"""depois do tuning temos um valor aceitavel.

---
---

*Prediçao no dado de teste.*
"""

pred = gs_clf.predict(df_test.data)

acc = np.mean(pred == df_test.target)
print('>>>> Acurácia: ', acc)

"""# ***A ideia era ele apresentar um valor mais alto, para isso é so mudar o modelo.***"""

creport = classification_report(df_test.target, pred, target_names=df_test.target_names)
print(creport)

"""# **Abordagem III**  
Vamos treinar um segundo modelo.  

***Treinando um segundo modelo***
"""

clf_2 = Pipeline([
    ('vect', CountVectorizer()), 
    ('tfidf', TfidfTransformer()), 
    ('clf-svm', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, max_iter=25, random_state=42))])

svm_trained = clf_2.fit(df_train.data, df_train.target)

pred_1 = svm_trained.predict(df_test.data)

acc_2 = np.mean(pred_1 == df_test.target)
print('>>>> Acurácia: ', acc_2)

creport_2 = classification_report(df_test.target, pred_1, target_names=df_test.target_names)
print(creport_2)

"""# ***Abordagem IV***
***Tuning***
"""

parameters_svm = {'vect__ngram_range': [(1, 1), (1, 2)], 'tfidf__use_idf': (True, False),'clf-svm__alpha': (1e-2, 1e-3)}

gs_clf_svm = GridSearchCV(svm_trained, parameters_svm, n_jobs=-1)
gs_clf_svm = gs_clf_svm.fit(df_train.data, df_train.target)

print(gs_clf_svm.best_score_)
gs_clf_svm.best_params_

pred = gs_clf_svm.predict(df_test.data)

acc = np.mean(pred == df_test.target)
print('>>>> Acurácia: ', acc)

creport = classification_report(df_test.target, pred, target_names=df_test.target_names)
print(creport)