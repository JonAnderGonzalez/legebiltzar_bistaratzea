from collections import defaultdict
import numpy as np


from sklearn.feature_extraction.text import TfidfVectorizer
from django.core.management.base import BaseCommand
from django.db.models.functions import TruncMonth, TruncWeek
from ...models import ParteHartzea

class Command(BaseCommand):

    help = 'tf_idf terms filter.'

    def add_arguments(self, parser):

        parser.add_argument('type',
                            nargs='+',
                            choices=['hilabetero','astero'],   
                            help='Hilabeteetan edo asteetan banatzea tf_idf dokumentuak parekatzeko.')

        parser.add_argument('--top',
                            action='store_true',
                            help='Gehienez zenbat termino. 100 aurrezarrita')

    def handle(self, *args, **options):

        def identity_tokenizer(text):
            return text

        def monthly2(top):
            data_dict = defaultdict(list)
            query = ParteHartzea.objects.exclude(testua__lemma__isnull=True
                    ).exclude(testua__lemma="nan"
                    ).annotate(month=TruncMonth('data')
                    ).values('month', 'testua__lemma')
            for d in query:
                data_dict[d["month"]] += d["testua__lemma"].split("\n")

            tfidf = TfidfVectorizer(tokenizer=identity_tokenizer, lowercase=False)
            lemma = []
            tf_idf_hilabete = defaultdict(list)
            for key, value in data_dict.items():
                lemma.append(value)
                X = tfidf.fit_transform(lemma)
                feature_array = np.array(tfidf.get_feature_names())
                tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
                tf_idf_hilabete[key] = feature_array[tfidf_sorting]

            for key, value in tf_idf_hilabete.items():
                top_n = value[:top]
                query = ParteHartzea.objects.filter(data__year=key.year).filter(data__month=key.month)

                for p in query:
                    for t in p.testua_set.all():
                        tf_idf = "\n".join([ent for ent in t.lemma.split("\n") if ent in top_n])
                        t.tf_idf = tf_idf
                        t.save()
                print(key)

        def hilabetero(top):
            data_dict = defaultdict(list)
            query = ParteHartzea.objects.exclude(testua__lemma__isnull=True
                    ).exclude(testua__lemma="nan"
                    ).annotate(month=TruncMonth('data')
                    ).values('month', 'testua__lemma')
            for d in query:
                data_dict[d["month"]] += d["testua__lemma"].split("\n")

            lemma = list(data_dict.values())
            lemma = [" ".join(l) for l in lemma]
            tfidf = TfidfVectorizer(max_df=0.6)
            X = tfidf.fit_transform(lemma)
            feature_array = np.array(tfidf.get_feature_names())
            feature_array = set(feature_array)
            query = ParteHartzea.objects.all()
            for p in query:
                for t in p.testua_set.all():
                    t.tf_idf = " ".join([l for l in t.lemma.split() if l.lower() in feature_array])
                    t.save()
                    
        def astero(top):
            data_dict = defaultdict(list)
            query = ParteHartzea.objects.exclude(testua__lemma__isnull=True
                    ).exclude(testua__lemma="nan"
                    ).annotate(week=TruncWeek('data')
                    ).values('week', 'testua__lemma')
            for d in query:
                data_dict[d["week"]] += d["testua__lemma"].split()

            lemma = list(data_dict.values())
            lemma = [" ".join(ent) for ent in lemma]
            tfidf = TfidfVectorizer(max_df=0.5)
            X = tfidf.fit_transform(lemma)
            feature_array = np.array(tfidf.get_feature_names())
            feature_array = set(feature_array)
            query = ParteHartzea.objects.all()
            for p in query:
                for t in p.testua_set.all():

                    t.tf_idf = " ".join([ent for ent in t.lemma.split().lower() if ent in feature_array])
                    t.save()
               
        if options['top']:
            top = options['top']
        else:
            top = 200

        if options['type'][0]=="hilabetero":
            hilabetero(top)
        elif options['type'][0]=="astero":
            astero(top)