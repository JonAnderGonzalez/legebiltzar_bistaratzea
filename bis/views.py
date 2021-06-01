import datetime
from calendar import monthrange
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse

from .models import Hizlaria, Testua, ParteHartzea

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
        testuak = Testua.objects.filter(parteHartzeak__hizlaria__abizenak=abizenak)
    else:
        gizon = aukerak["gizon"]
        emakume = aukerak["emakume"]
        alderdia = aukerak["alderdia"]

        if (gizon and not emakume):
            testuak = Testua.objects.filter(parteHartzeak__hizlaria__generoa='G')
        elif (emakume and not gizon):
            testuak = Testua.objects.filter(parteHartzeak__hizlaria__generoa='E')
        elif (emakume and gizon):
            testuak = Testua.objects.exclude(parteHartzeak__hizlaria__generoa='N')
        else:
            testuak = Testua.objects.all()

        if alderdia:
            testuak = testuak.filter(parteHartzeak__hizlaria__alderdia=alderdia)

    if (euskera and not gaztelania):
        testuak = testuak.filter(hizkuntza="eu")
    elif (gaztelania and not euskera):
        testuak = testuak.filter(hizkuntza="es")

    if bakarra:
        if urtea_h!='':
            if hilabetea_h!='':
                testuak = testuak.filter(parteHartzeak__data__lt=datetime.date(int(urtea_h),
                                     int(hilabetea_h), 1))
            else:
                testuak = testuak.filter(parteHartzeak__data__lt=datetime.date(int(urtea_h), 1, 1))
        else:
            testuak = testuak.filter(parteHartzeak__data__year=1)

    else:
        if urtea_h!='':
            if hilabetea_h!='':
                testuak = testuak.filter(parteHartzeak__data__gte=datetime.date(int(urtea_h),
                                               int(hilabetea_h), 1))
            else:
                testuak = testuak.filter(parteHartzeak__data__year__gte=urtea_h)

        if urtea_b!='':
            if hilabetea_b!='':
                testuak = testuak.filter(parteHartzeak__data__lte=datetime.date(int(urtea_b),
                                     int(hilabetea_b), monthrange(urtea_b,hilabetea_b)[1]))
            else:
                testuak = testuak.filter(parteHartzeak__data__year__lte=urtea_b)

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
    titulua1, titulua2 = ""
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
            title2 = titulua_egin(abizenak, gizon, emakume, alderdia, euskera, gaztelania,
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


def taulak(request):
    """
    NER edo tf-idf erabilitako entitateak erakutsi taula batean.

    **Context**

    ``taula_err1``
        1. taulako errenkaden zerrenda, NER edo tf-idf duten entitateekin.
        entitateak eta tf_idf field-ak.
        :model:`vis.Testua`.

    ``taula_err2``
        2. taulako errenkaden zerrenda, NER edo tf-idf duten entitateekin.
        entitateak eta tf_idf field-ak.
        :model:`vis.Testua`.

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
    testuak_bi, tituluak_bi = form_handler(request, form_kopurua)
    testuak1 = testuak_bi[0]
    testuak2 = testuak_bi[1]

    if not (testuak1 or testuak2):
        warn = "Iragazketak 0 testu bueltatu ditu."
    elif not testuak1:
        warn = "1. formularioko iragazketak 0 testu bueltatu ditu."
    elif not (testuak2 and form_kopurua=='2'):
        warn = "2. formularioko iragazketak 0 testu bueltatu ditu."
    else:
        warn = ""

    if testuak1:
        entitateak1 = get_entitateak(testuak1)
        #tf_idfs1 = get_tf_idfs(testuak1)
        taula_err1 = [e + t for e, t in entitateak1.most_common()[:25]]#zip(entities1.most_common()[:25],
                       #tf_idfs1.most_common()[:25])]
    if testuak2:
        entitateak2 = get_entitateak(testuak2)
        #tf_idfs2 = get_tf_idfs(testuak2)
        table_rows2 = [e + t for e, t in entitateak2.most_common()[:25]]#zip(entities2.most_common()[:25],
                       #tf_idfs2.most_common()[:25])]

    return JsonResponse({'taula_err1':taula_err1, 'taula_err2':taula_err2,
                        'titulua1':tituluak_bi[0], 'titulua2':tituluak_bi[1], 'warn':warn})


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