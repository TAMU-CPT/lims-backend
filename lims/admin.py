from django.contrib import admin

from lims.models import ContainerType
from lims.models import TubeType
from lims.models import SampleType
from lims.models import StorageLocation
from lims.models import Box
from lims.models import Tube
from lims.models import EnvironmentalSample
from lims.models import Bacteria
from lims.models import Lysate
from lims.models import Experiment
from lims.models import ExperimentalResult
from lims.models import PhageDNAPrep
from lims.models import SequencingRunPool
from lims.models import SequencingRun
from lims.models import Assembly

admin.site.register(ContainerType)
admin.site.register(TubeType)
admin.site.register(SampleType)
admin.site.register(StorageLocation)
admin.site.register(Box)
admin.site.register(Tube)
admin.site.register(EnvironmentalSample)
admin.site.register(Bacteria)
admin.site.register(Lysate)
admin.site.register(Experiment)
admin.site.register(ExperimentalResult)
admin.site.register(PhageDNAPrep)
admin.site.register(SequencingRunPool)
admin.site.register(SequencingRun)
admin.site.register(Assembly)
