from django.shortcuts import render
from django.http import HttpResponseRedirect
import re
import cgi
import cptids
from directory.models import Person

def guessAtMeaning(term):
    try:
        (id_type, id_val) = cptids.decode(term)
        if id_type == 'person':
            return Person.objects.get(id=id_val)
    except:
        return 'Unknown term: %s' % cgi.escape(term)


def Index(request):
    data = []
    if request.method == 'POST':
        query = request.POST['search']
        for term in re.split('\s+', query.strip()):
            data.append(guessAtMeaning(term))

    return render(request, 'search/index.html', {'results': data})
