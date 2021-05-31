from django.db import models

class Hizlaria(models.Model):
    ALDERDIA_CHOICES = [('ARARTEKO','Arartekoa'),('EAJ','EAJ'),
                        ('EB','Ezker Batua'),('EH Bildu','Bildu'), ('EP','Elkarrekin Podemos'),
                        ('N','Ezezaguna'),('PP','PP'),('PSE-EE','PSE'),('UPyD','UPyD')]

    GENEROA_CHOICES = [('E', 'Emakume'),('G','Gizon'),('N','Ezezagun')]
    h_id = models.AutoField(primary_key=True)

    abizenak = models.CharField(max_length=100, unique=True)
    alderdia = models.CharField(max_length=100, choices=ALDERDIA_CHOICES)
    generoa = models.CharField(max_length=100, choices=GENEROA_CHOICES)
    informazioa = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Hizlariak"

    def __str__(self):
        return self.abizenak

class ParteHartzea(models.Model):
    p_id = models.AutoField(primary_key=True)

    hizlaria = models.ForeignKey(Hizlaria, on_delete=models.CASCADE)
    data = models.DateField('parte-hartzearen data')
    p_ordena = models.IntegerField(default=0)
    class Meta:
        unique_together = ["data", "p_ordena"]
        verbose_name_plural = "ParteHartzeak"

    def __str__(self):
        return str(self.data) + "-" + str(self.p_ordena)

class Testua(models.Model):
    t_id = models.AutoField(primary_key=True)

    parteHartzea = models.ForeignKey(ParteHartzea, on_delete=models.CASCADE)
    t_ordena = models.IntegerField(default=0)
    testua = models.TextField()
    hizkuntza = models.CharField(max_length=10)
    entitateak = models.TextField()
    #entitateak_stopwords = models.TextField()
    #lemma = models.TextField()
    #tf_idf = models.TextField()

    class Meta:
        unique_together = ["parteHartzea", "t_ordena"]
        verbose_name_plural = "Testuak"

    def entitateak_ditu(self):
        return self.entitateak!= "nan"

    entitateak_ditu.boolean = True
    entitateak_ditu.short_description = 'Entitaterik du?'

    # def entitateak_stopwords_ditu(self):
    #     return self.entitateak!= "nan"

    # entitateak_stopwords_ditu.boolean = True
    # entitateak_stopwords_ditu.short_description = 'Entitaterik du?'

    # def tf_idf_ditu(self):
    #     return self.tf_idf!= ""
    
    # tf_idf_ditu.boolean = True
    # tf_idf_ditu.short_description = 'Entitaterik du?'

    def __str__(self):
        return str(self.parteHartzea.data) + "-" + str(self.parteHartzea.p_ordena) + "/" + str(self.t_ordena)

# class Sentimendua(models.Model):

#     s_id = models.AutoField(primary_key=True)
    
#     testua = models.ForeignKey(Testua, on_delete=models.CASCADE)
#     mota = models.CharField(max_length=100)
#     portzentaia = models.FloatField(default=0)

#     class Meta:
#         verbose_name_plural = "Sentimenduak"
