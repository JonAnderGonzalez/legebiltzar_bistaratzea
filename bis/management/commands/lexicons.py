from os import path
import pandas as pd
from django.core.management.base import BaseCommand
from ...models import Testua
import json

from legebiltzar_bistaratzea.settings import BASE_DIR
with open(path.join(BASE_DIR, 'bis', 'management', 'commands', 'data', 'stopwords.json'), encoding='utf-8') as f:
    stopwords = json.load(f)

class Command(BaseCommand):

    def handle(self, *args, **options):
        dirname = path.dirname(__file__)
        eu_lexicons_path = path.join(dirname, 'data', 'eu_lexicon.csv')
        es_lexicons_path = path.join(dirname, 'data', 'es_lexicon.csv')

        eu_lexicons = pd.read_csv(eu_lexicons_path, sep='\t')
        es_lexicons = pd.read_csv(es_lexicons_path, sep='\t')

        t_zerrenda = Testua.objects.all()

        for t in t_zerrenda:
            sentimenduak = {'Positive':0, 'Negative':0, 'Anger':0, 
                                'Anticipation':0, 'Disgust':0, 'Fear':0, 
                                'Joy':0, 'Sadness':0, 'Surprise':0, 'Trust':0}
 
            c = 0
            if t.hizkuntza=="eu":
                for h in t.testua.split(" "):
                    if not h in stopwords:
                        row = eu_lexicons[eu_lexicons["Basque (eu)"]==h]
                        if not(row.empty):
                            sentimenduak = {mota: (portzentaia + row[mota].values[0]) for mota, portzentaia 
                                            in sentimenduak.items()}
                            c +=1

                if c!=0:
                    sentimenduak = {mota: portzentaia / c for mota, portzentaia 
                                    in sentimenduak.items()}

                for mota, portzentaia in sentimenduak.items():
                    t.sentimendua_set.create(mota=mota, portzentaia=portzentaia)

            if t.hizkuntza=="es":
                for h in t.testua.split(" "):
                    if not h in stopwords:
                        row = es_lexicons[es_lexicons["Spanish (es)"]==h]
                        if not(row.empty):
                            sentimenduak = {mota: portzentaia + row[mota].values[0] for mota, portzentaia 
                                            in sentimenduak.items()}
                            c +=1

                if c!=0:
                    sentimenduak = {mota: portzentaia / c for mota, portzentaia 
                                    in sentimenduak.items()}

                for mota, portzentaia in sentimenduak.items():
                    t.sentimendua_set.create(mota=mota, portzentaia=portzentaia)
