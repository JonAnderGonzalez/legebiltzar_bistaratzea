import datetime
import scattertext as st
import pandas as pd
from os import path
from collections import Counter
from calendar import monthrange
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse
from legebiltzar_bistaratzea.settings import BASE_DIR
from .models import Hizlaria, Testua, ParteHartzea

scatter_path = path.join(BASE_DIR, 'bis', 'templates', 'bis', 'scatter.html')

class IndexView(generic.ListView):
    """
    Informazioa bistaratzeko bista.

    Context beharrezkoa da html-ko select-etan aukerak ez hardcodetzeko.
    **Context**

    ``abizenak``
        abizenak field-eko instantzia guztien zerrenda :model:`bis.Hizlaria`.

    ``urteak``
        data field-eko instantzia guztien zerrenda :model:`bis.ParteHartzea`.

    **Template:**

    :template:`bis/index.html`

    """
    template_name = 'bis/index.html'
    model = Hizlaria
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hizlariak = Hizlaria.objects.all()
        parteHartzeak = ParteHartzea.objects.all()
        context["abizenak_zer"] = sorted(list([h.abizenak for h in hizlariak]))
        context["urteak"] = sorted(list(set([p.data.year for p in parteHartzeak])))
        return context

def titulua_egin(*aukerak):
    """Aukerekin egindako titulu bat bueltatu, zuriunekin konkatenatuta."""
    titulua = ""

    for aukera in aukerak:
        if aukera:
            titulua += aukera + " "

    if titulua:
        titulua = titulua[:-1]

    return titulua



def testuak_iragazi(bakarra=False, **aukerak):
    """
    Testuak iragazi formularioan aukeratutakoaren arabera.

    Parameters:
    bakarra: True scatter-text erabiltzen bada formulario bakarrarekin.
    aukerak: Kwargs formularioaren aukerekin.

    Returns:
    testuak: Iragazitako testuen zerrenda.

    """
    abizenak = aukerak["abizenak"]
    euskera = aukerak["euskera"]
    gaztelania = aukerak["gaztelania"]
    urtea_h = aukerak["urtea_h"]
    urtea_b = aukerak["urtea_b"]
    hilabetea_h = aukerak["hilabetea_h"]
    hilabetea_b = aukerak["hilabetea_b"]

    if abizenak:
        testuak = Testua.objects.filter(parteHartzea__hizlaria__abizenak=abizenak)
    else:
        gizon = aukerak["gizon"]
        emakume = aukerak["emakume"]
        alderdia = aukerak["alderdia"]

        if (gizon and not emakume):
            testuak = Testua.objects.filter(parteHartzea__hizlaria__generoa='G')
        elif (emakume and not gizon):
            testuak = Testua.objects.filter(parteHartzea__hizlaria__generoa='E')
        elif (emakume and gizon):
            testuak = Testua.objects.exclude(parteHartzea__hizlaria__generoa='N')
        else:
            testuak = Testua.objects.all()

        if alderdia:
            testuak = testuak.filter(parteHartzea__hizlaria__alderdia=alderdia)

    if (euskera and not gaztelania):
        testuak = testuak.filter(hizkuntza="eu")
    elif (gaztelania and not euskera):
        testuak = testuak.filter(hizkuntza="es")

    if bakarra:
        if urtea_h!='':
            if hilabetea_h!='':
                testuak = testuak.filter(parteHartzea__data__lt=datetime.date(int(urtea_h),
                                     int(hilabetea_h), 1))
            else:
                testuak = testuak.filter(parteHartzea__data__lt=datetime.date(int(urtea_h), 1, 1))
        else:
            testuak = testuak.filter(parteHartzea__data__year=1)

    else:
        if urtea_h!='':
            if hilabetea_h!='':
                testuak = testuak.filter(parteHartzea__data__gte=datetime.date(int(urtea_h),
                                               int(hilabetea_h), 1))
            else:
                testuak = testuak.filter(parteHartzea__data__year__gte=urtea_h)

        if urtea_b!='':
            if hilabetea_b!='':
                testuak = testuak.filter(parteHartzea__data__lte=datetime.date(int(urtea_b),
                                     int(hilabetea_b), monthrange(urtea_b,hilabetea_b)[1]))
            else:
                testuak = testuak.filter(parteHartzea__data__year__lte=urtea_b)

    return testuak

def form_handler(request_, form_kopurua, mode="other"):
    """
    Bidalitako formularioak maneiatu.

    Parameters:
    request_ : formulario(eta)ko POST bidalketa.

    Returns:
    testu_parea: Tuple bat. Elementu bakoitza formularioko aukerekin
                iragazitako testuen zerrenda bat da. 
    titulo_parea: Tuple bat. Elementu bakoitza formularioen aukerekin kateatutako 
                    string bat da.

    """
    titulua1 = ""
    titulua2 = ""
    abizenak = request_.POST.get('abizenak1', False)
    gizon= request_.POST.get('generoa1_1', False)
    emakume = request_.POST.get('generoa2_1', False)
    alderdia = request_.POST.get('alderdia1', False)
    euskera = request_.POST.get('hizkuntza1_1', False)
    gaztelania = request_.POST.get('hizkuntza2_1', False)
    urtea_h = request_.POST.get('urtea_h1', False)
    urtea_b = request_.POST.get('urtea_b1', False)
    hilabetea_h = request_.POST.get('hilabetea_h1', False)
    hilabetea_b = request_.POST.get('hilabetea_b1', False)

    if mode!="scatter":
        titulua1 = titulua_egin(abizenak, gizon, emakume, alderdia, 
                            euskera, gaztelania, urtea_h, urtea_b,
                            hilabetea_h, hilabetea_b)

    testuak1 = testuak_iragazi(abizenak=abizenak, gizon=gizon, emakume=emakume, alderdia=alderdia,
                          euskera=euskera, gaztelania=gaztelania, urtea_h=urtea_h,
                          urtea_b=urtea_b, hilabetea_h=hilabetea_h, hilabetea_b=hilabetea_b)

    if form_kopurua=='2':
        abizenak = request_.POST.get('abizenak2', False)
        gizon = request_.POST.get('generoa1_2', False)
        emakume = request_.POST.get('generoa2_2', False)
        alderdia = request_.POST.get('alderdia2', False)
        euskera = request_.POST.get('hizkuntza1_2', False)
        gaztelania = request_.POST.get('hizkuntza2_2', False)
        urtea_h = request_.POST.get('urtea_h2', False)
        urtea_b = request_.POST.get('urtea_b2', False)
        hilabetea_h = request_.POST.get('hilabetea_h2', False)
        hilabetea_b = request_.POST.get('hilabetea_b2', False)

        if mode!="scatter":
            titulua2 = titulua_egin(abizenak, gizon, emakume, alderdia, euskera, gaztelania,
                               urtea_h, urtea_b, hilabetea_h, hilabetea_b)

        testuak2 = testuak_iragazi(abizenak=abizenak, gizon=gizon, emakume=emakume, alderdia=alderdia,
                              euskera=euskera, gaztelania=gaztelania,urtea_h=urtea_h,
                              urtea_b=urtea_b, hilabetea_h=hilabetea_h, hilabetea_b=hilabetea_b)
    elif mode!="scatter":
        testuak2 = []
    else:
        testuak2 = testuak_iragazi(unique=True, abizenak=abizenak, gizon=gizon, emakume=emakume,
                              alderdia=alderdia, euskera=euskera, gaztelania=gaztelania,urtea_h=urtea_h,
                              urtea_b=urtea_b, hilabetea_h=hilabetea_h, hilabetea_b=hilabetea_b)

    testuak_bikote = (testuak1, testuak2)
    titulua_bikote = (titulua1, titulua2)

    return testuak_bikote, titulua_bikote

def get_entitateak(testuak):
    """
    Izendun entitateak bueltatu.

    Parameters:
    testuak: Iragazitako testuen zerrenda.

    Returns:
    entitateak: testuetan agertzen diren entitate izendunen Counter.

    """
    entitateak_list = [t.entitateak for t in testuak if t.entitateak!='nan']

    entitateak = Counter([e for entitateak in entitateak_list
                        for e in entitateak.split("\n")])

    return entitateak

def get_entitateak_stp(testuak):
    """
    Izendun entitateak bueltatu.

    Parameters:
    testuak: Iragazitako testuen zerrenda.

    Returns:
    entitateak: testuetan agertzen diren entitate izendunen Counter.

    """
    entitateak_list = [t.entitateak_stopwords for t in testuak 
                        if t.entitateak_stopwords!='nan' and t.entitateak_stopwords!='[]']

    entitateak = Counter([e for entitateak in entitateak_list
                        for e in entitateak.split("\n")])

    return entitateak


def get_tf_idfs(testuak):
    """
    tf_idf metodoarekin iragazitako hitz maiztasuna bueltatu.

    Parameters:
    testuak: Iragazitako testuen zerrenda.

    Returns:
    tf_idfs: testuetan agertzen diren tf_idf metodoarekin garbitutako hitzak.

    """
    tf_idfs_zerrenda = [t.tf_idf for t in testuak if t.tf_idf!='nan' ]

    tf_idfs = Counter([t for tf_idfs in tf_idfs_zerrenda
                        for t in tf_idfs.split()])

    return tf_idfs

def taulak(request):
    """
    NER edo tf-idf erabilitako entitateak erakutsi taula batean.

    **Context**

    ``taula_err1``
        1. taulako errenkaden zerrenda, NER edo tf-idf duten entitateekin.
        entitateak eta tf_idf field-ak.
        :model:`bis.Testua`.

    ``taula_err2``
        2. taulako errenkaden zerrenda, NER edo tf-idf duten entitateekin.
        entitateak eta tf_idf field-ak.
        :model:`bis.Testua`.

    ``titulua1``
        1. taulako titulua. Iragazketan erabilitako aukerak kateatzen ditu zuriunekin.

    ``titulua2``
        2. taulako titulua. Iragazketan erabilitako aukerak kateatzen ditu zuriunekin.

    ``warn``
        Warning-a filtroak 0 testu bueltatzen duenean.

    **Template:**

    Ajax dei bati erantzuten dio Json formatuan. Beraz, ez dago templaterik.
    zeharka eguneratu
    :template:`bis/taulak.html`

    """
    taula_err1 = []
    taula_err2 = []
    form_kopurua = request.POST['form_kopurua'] #bidalitako formulario kopurua
    testuak_bikote, tituluak_bikote = form_handler(request, form_kopurua)
    testuak1 = testuak_bikote[0]
    testuak2 = testuak_bikote[1]

    if not (testuak1 or testuak2):
        warn = "Iragazketak 0 testu bueltatu ditu."
    elif not testuak1:
        warn = "1. formularioko iragazketak 0 testu bueltatu ditu."
    elif form_kopurua=='2' and not testuak2:
        warn = "2. formularioko iragazketak 0 testu bueltatu ditu."
    else:
        warn = ""

    if testuak1:
        entitateak1 = get_entitateak(testuak1)
        entitateak_stp1 = get_entitateak_stp(testuak1)
        tf_idfs1 = get_tf_idfs(testuak1)
        taula_err1 = [e + es + t for e, es, t in zip(entitateak1.most_common()[:25],
                     entitateak_stp1.most_common()[:25], tf_idfs1.most_common()[:25])]
    if testuak2:
        entitateak2 = get_entitateak(testuak2)
        entitateak_stp2 = get_entitateak_stp(testuak2)
        tf_idfs2 = get_tf_idfs(testuak2)
        taula_err2 = [e + es + t for e, es, t in zip(entitateak2.most_common()[:25],
                     entitateak_stp2.most_common()[:25], tf_idfs2.most_common()[:25])]

    return JsonResponse({'taula_err1':taula_err1, 'taula_err2':taula_err2,
                        'titulua1':tituluak_bikote[0], 'titulua2':tituluak_bikote[1], 'warn':warn})

def parteHartzeak(request):
    """
    Parte-hartzeak erakutsi.

    **Context**

    ``parteHartze_err1``
        1. taulako errenkaden zerrenda, entitateekin.
        Iragazitako entitateak eta tf_idf field-ak
        :model:`bis.Testua`.

    ``parteHartze_err2``
         2. taulako errenkaden zerrenda, entitateekin.
        Iragazitako entitateak eta tf_idf field-ak.
        :model:`bis.Testua`.

    ``titulua1``

    ``titulua2``

    ``warn``
        Filtroak 0 testu bueltatzen dituen kasuan.

    **Template:**

    Zeharka eguneratu
    :template:`bis/parteHartzeak.html`

    """
    parteHartze_err1 = []
    parteHartze_err2 = []
    form_kopurua = request.POST['form_kopurua']
    testuak_bikotea, titulua_bikotea = form_handler(request, form_kopurua)
    testuak1 = testuak_bikotea[0]
    testuak2 = testuak_bikotea[1]

    if not (testuak1 or testuak2):
        warn = "Iragazketak 0 testu bueltatu ditu."
    elif not testuak1:
        warn = "1. formularioko iragazketak 0 testu bueltatu ditu."
    elif form_kopurua=='2' and not testuak2:
        warn = "2. formularioko iragazketak 0 testu bueltatu ditu."
    else:
        warn = ""

    if testuak1:
        parteHartze_err1 = [t.testua for t in testuak1][:100]
    if testuak2:
        parteHartze_err2 = [t.testua for t in testuak2][:100]

    return JsonResponse({'parteHartze_err1':parteHartze_err1, 'parteHartze_err2':parteHartze_err2,
                        'titulua1':titulua_bikotea[0], 'titulua2':titulua_bikotea[1], 'warn':warn})


def get_scatter(tf_idfs1, tf_idfs2, testuak1, testuak2):
    """
    scatter.html datu berriekin gainidatzi.

    Parameters:
    tf_idfs1: 1. formularioko entitateen maiztasuna duen Counter-a.
    tf_idfs2: 2. formularioko entitateen maiztasuna duen Counter-a.
    testuak1: 1. formularioko entitateak dituzten testuen zerrenda.
    testuak2: 2. formularioko entitateak dituzten testuen zerrenda.

    Returns:
    None

    """
    tf_idfs1 = dict(tf_idfs1.most_common()[:1000])
    tf_idfs2 = dict(tf_idfs2.most_common()[:1000])
    entitateak = list(set(tf_idfs1) | set(tf_idfs2))
    frek1 = []
    frek2 = []
    for t in entitateak:
        if t in tf_idfs1:
            frek1.append(tf_idfs1[t])

        else:
            frek1.append(0)

    for t in entitateak:
        if t in tf_idfs2:
            frek2.append(tf_idfs2[t])
        else:
            frek2.append(0)
 
    data = {'1.':frek1,'2.':frek2}
    frek_df = pd.DataFrame(data, index=entitateak)
    # document_df = pd.DataFrame([{'text': t,
    #                             'category': '1.'} for t in testuak1] +[{'text': t,
    #                             'category': '2.'} for t in testuak2])

    doc_term_cat_freq = st.TermCategoryFrequencies(frek_df)#, document_category_df=document_df)
    html = st.produce_scattertext_explorer(doc_term_cat_freq, category='1.',
                                           category_name='1.', not_category_name='2.')

    open(scatter_path, 'wb').write(html.encode('utf-8'))

def scatter(request):
    """
    scatter_text plot batean erakutsi entitateak.

    **Context**

    ``warn``
        Iragazketak 0 testu bueltatzen baditu.

    **Template:**

    In case of warning returns a reponse to an Ajax request in Json format.
    Thus, there is no template.
    Indirectly updates
    :template:`bis/index.html`

    abisurik ez badago templatea gainidazten du.
    :template:`bis/scatter.html`

    """
    form_kopurua = request.POST['form_kopurua']
    testuak_bikote, _ = form_handler(request, form_kopurua, mode="scatter")
    testuak1 = testuak_bikote[0]
    testuak2 = testuak_bikote[1]
    warn = ""
    if not (testuak1 or testuak2):
        warn = "Iragazketak 0 testu bueltatu ditu."
    elif not testuak1:
        warn = "1. formularioko iragazketak 0 testu bueltatu ditu."
    elif not (testuak2 and form_kopurua=='2'):
        warn = "2. formularioko iragazketak 0 testu bueltatu ditu."

    if not warn:
        tf_idfs1 = get_tf_idfs(testuak1)
        testuak1 = [t.testua for t in testuak1 if t.tf_idf!='']
        if testuak2:
            tf_idfs2 = get_tf_idfs(testuak2)
            testuak2 = [t.testua for t in testuak2 if t.tf_idf!='']

        if form_kopurua=='2':
            get_scatter(tf_idfs1, tf_idfs2, testuak1, testuak2)
        else:
            # if testuak2:
            get_scatter(tf_idfs1, tf_idfs2, testuak1, testuak2)
            # else:
            #     #may change
            #     open(scatter_path, 'wb').write("")

    return JsonResponse({'warn':warn})

def hilabete_handler(request):
    """
    Urte bat hautatzen denean, urte horretan eskuragarri dauden hilabeteak erakutsi.
    **Context**

    ``hilabeteak``
        aukeratutako urtean eskuragarri dauden hilabeteak.

    **Template:**
    Ajax dei bati erantzuten dio Json formatuan. Beraz, ez dago templaterik.
    zeharka eguneratu
    :template:`bis/index.html`

    """
    urtea = request.GET['urtea']
    if urtea:
        parteHartzeak = ParteHartzea.objects.filter(data__year=urtea)
        hilabeteak = list(set([p.data.month for p in parteHartzeak]))
    else:
        hilabeteak = False
    return JsonResponse({'hilabeteak':hilabeteak})

# def sentiments(request):
    # """
    # Display the entitateak in a scatter_text plot.

    # **Context**

    # ``warn``
    #     Warning in case any of the filters returned 0 texts.

    # **Template:**

    # In case of warning returns a reponse to an Ajax request in Json format.
    # Thus, there is no template.
    # Indirectly updates
    # :template:`vis/index.html`

    # If there is no warning overwrites template.
    # :template:`vis/scatter.html`

    # """
    # form_kopurua = request.POST['form_kopurua'] #The number of forms submitted
    # testuak_bikote, title_pair = form_handler(request, form_kopurua)
    # testuak1 = testuak_bikote[0]
    # testuak2 = testuak_bikote[1]

    # if not (testuak1 or testuak2):
    #     warn = "Iragazketak 0 testu bueltatu ditu."
    # elif not testuak1:
    #     warn = "1. formularioko iragazketak 0 testu bueltatu ditu."
    # elif not (testuak2 and form_kopurua=='2'):
    #     warn = "2. formularioko iragazketak 0 testu bueltatu ditu."
    # else:
    #     warn = ""

    # if testuak1:
    #     entitateak1 = get_entitateak(testuak1)
    #     tf_idfs1 = get_tf_idfs(testuak1)
    #     table_rows1 = [e + t for e, t in zip(entitateak1.most_common()[:25],
    #                    tf_idfs1.most_common()[:25])]
    # if testuak2:
    #     entitateak2 = get_entitateak(testuak2)
    #     tf_idfs2 = get_tf_idfs(testuak2)
    #     table_rows2 = [e + t for e, t in zip(entitateak2.most_common()[:25],
    #                    tf_idfs2.most_common()[:25])]

    # return JsonResponse({'table_rows1':table_rows1, 'table_rows2':table_rows2,
    #                     'title1':title_pair[0], 'title2':title_pair[1], 'warn':warn})

    # categories= ['Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust']
    # values = []
    # for cat in categories:
    #     mota = t_zerrenda.filter(sentimendua__mota=cat)
    #     for t in mota:
    #         portzentaia = 0
    #         c = 0
    #         sentimenduak = t.sentimendua_set.all()
    #         for s in sentimenduak:
    #             portzentaia += s.portzentaia
    #             c +=1
    #         values.append(portzentaia*100 / c )

    # N = len(categories)
    # values += values[:1]
    
    # angles = [n / float(N) * 2 * pi for n in range(N)]
    # angles += angles[:1]
    
    # # Initialise the spider plot
    # if kopurua=='1':
    #     ax = plt.subplot(111, polar=True)
    # else:
    #     ax = plt.subplot(121, polar=True)

    # # Draw one axe per variable + add labels labels yet
    # plt.xticks(angles[:-1], categories, color='grey', size=8)

    # # Draw ylabels
    # ax.set_rlabel_position(0)
    # plt.yticks([25,50,75], ["25","50","75"], color="grey", size=7)
    # plt.ylim(0,100)

    # # Plot data
    # ax.plot(angles, values, linewidth=1, linestyle='solid')

    # # Fill area
    # ax.fill(angles, values, 'b', alpha=0.1)
    # ax.title.set_text(titulua1)
    # if kopurua=='2':
    #     values = []
    #     for cat in categories:
    #         mota = t_zerrenda2.filter(sentimendua__mota=cat)
    #         for t in mota:
    #             portzentaia = 0
    #             c = 0
    #             sentimenduak = t.sentimendua_set.all()
    #             for s in sentimenduak:
    #                 portzentaia += s.portzentaia
    #                 c +=1
    #             values.append(portzentaia*100 / c )
    #     values += values[:1]

    #     ax2 = plt.subplot(122, polar=True)
        
    #     # Draw one axe per variable + add labels labels yet
    #     plt.xticks(angles[:-1], categories, color='grey', size=8)
        
    #     # Draw ylabels
    #     ax2.set_rlabel_position(0)
    #     plt.yticks([25,50,75], ["25","50","75"], color="grey", size=7)
    #     plt.ylim(0,100)

    #     # Plot data
    #     ax2.plot(angles, values, linewidth=1, linestyle='solid')
        
    #     # Fill area
    #     ax2.fill(angles, values, 'b', alpha=0.1)
        
    #     ax2.title.set_text(titulua2)
    
    # tmpfile = BytesIO()
    # plt.savefig(tmpfile, format='png')
    # encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    # html = '<img src=\'data:image/png;base64,{}\'>'.format(encoded)
    # return JsonResponse({'html':html})
