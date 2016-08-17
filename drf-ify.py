import os

DJANGO_MODULE = "web"

SERIALIZERS = os.path.join(DJANGO_MODULE, 'serializers.py')
VIEWS = os.path.join(DJANGO_MODULE, 'views.py')
MODELS = os.path.join(DJANGO_MODULE, 'models.py')

import importlib
m = importlib.import_module(DJANGO_MODULE + ".models")
BLACKLIST = ['Account', 'Organisation']

models = []

for x in dir(m):
    q = getattr(m, x)
    if x in BLACKLIST:
        continue
    b = q.__class__.__bases__
    if len(b) > 0 and b[0].__name__ == "type":
        models.append((
            x, [e.name for e in q._meta.fields]
        ))

# # Add Serializers
print 'Writing to %s' % SERIALIZERS
handle = open(SERIALIZERS, 'w')
header = (
    "from web.models import " + ", ".join([x[0] for x in models]),
    "from rest_framework import serializers",
    "",
    "",
)
handle.write('\n'.join(header))

def zzz():
    for data  in models:
        (key, fields) = data
        data = (
            "class %sSerializer(serializers.ModelSerializer):" % key,
            "    class Meta:",
            "        model = %s" % key,
            "        fields = (",
            "            %s" % ( ', '.join(["'%s'" % r for r in fields ]) ),
            "        )",
            "",
            ""
        )
        handle.write('\n'.join(data))

zzz()
handle.flush()
handle.close()


handle2 = open(VIEWS, 'a')
handle2.write("from rest_framework import viewsets\n")
header = "from directory.serializers import " + ', '.join(["%sSerializer" % x[0] for x in models]) + "\n\n"
handle2.write(header)


def www():
    for data  in models:
        (key, fields) = data
        data = (
            "class %sViewSet(viewsets.ModelViewSet):" % key,
            "    queryset = %s.objects.all()" % key,
            "    serializer_class = %sSerializer" % key,
            "",
            ""
        )
        print "router.register('web/%s', %s)" % (key.lower(), key)
        handle2.write('\n'.join(data))

www()
handle2.flush()
handle2.close()
