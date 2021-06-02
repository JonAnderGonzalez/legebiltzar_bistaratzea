import os
from collections import Counter
from datetime import date
import pandas as pd

from django.core.management.base import BaseCommand

from ...models import Hizlaria

class Command(BaseCommand):
    def handle(self, *args, **options):
        dirname = os.path.dirname(__file__)
        transkripzioak = os.path.join(dirname, 'data', 'transkripzioak_clean.csv')
        testuak = os.path.join(dirname, 'data', 'testuak_guztia.csv')
        df_transkripzioak = pd.read_csv(transkripzioak, sep='\t')
        df_testuak = pd.read_csv(testuak, sep="\t")

        for abizenak in Counter(df_transkripzioak["Hizlaria"]):
            row = df_transkripzioak[df_transkripzioak["Hizlaria"]==abizenak].iloc[0]
            alderdia = row["Alderdia"]
            generoa = row["Generoa"]
            h = Hizlaria(abizenak=abizenak, alderdia=alderdia, generoa=generoa)
            h.save()

        for _, row in df_transkripzioak.iterrows():
            data = date.fromisoformat(row["Data"])
            p_ordena = int(row["Id"])
            hizlaria = row["Hizlaria"]
            h = Hizlaria.objects.get(abizenak=hizlaria)
            p = h.partehartzea_set.create(data=data, p_ordena=p_ordena)

            p_id = row["P_id"]
            for  _, row_testua in df_testuak[df_testuak["P_id"]==p_id].iterrows():
                t_ordena = int(row_testua["T_ordena"])
                testua = row_testua["Testua"]
                hizkuntza = row_testua["Hizkuntza"]
                entitateak = row_testua["NER"]
                entitateak_stopwords = row_testua["NER_stopwords"]
                lemma = row_testua["lemma_stopwords"]

                p.testua_set.create(t_ordena=t_ordena, testua=testua, hizkuntza=hizkuntza, 
                                    entitateak=entitateak, entitateak_stopwords=entitateak_stopwords,
                                    lemma=lemma)
