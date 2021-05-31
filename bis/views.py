from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic


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
        context["abizenak"] = sorted(list([h.abizenak for h in hizlariak]))
        context["urteak"] = sorted(list(set([p.data.year for p in parteHartzeak])))
        return context
