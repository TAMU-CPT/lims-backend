from django.contrib import admin

from web.models import ContainerType
from web.models import TubeType
from web.models import SampleType
from web.models import StorageLocation
from web.models import Box
from web.models import EnvironmentalSample
from web.models import Bacteria
from web.models import Lysate
from web.models import Experiment
from web.models import ExperimentalResult
from web.models import PhageDNAPrep
from web.models import SequencingRunPool
from web.models import SequencingRun
from web.models import Assembly

admin.site.register(ContainerType)
admin.site.register(TubeType)
admin.site.register(SampleType)
admin.site.register(StorageLocation)
admin.site.register(Box)
admin.site.register(EnvironmentalSample)
admin.site.register(Bacteria)
admin.site.register(Lysate)
admin.site.register(Experiment)
admin.site.register(ExperimentalResult)
admin.site.register(PhageDNAPrep)
admin.site.register(SequencingRunPool)
admin.site.register(SequencingRun)
admin.site.register(Assembly)
