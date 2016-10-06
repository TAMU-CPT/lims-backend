BASE_TEMPLATE = """
{{% extends "base.html" %}}
{{% load cpt %}}
{{% load bootstrap3 %}}
{{% load staticfiles %}}

{{% block crumbs %}}
<ul class="breadcrumb">
    <li><a href="{{% url 'lims:index' %}}">LIMS</a></li>
    {CRUMBS}
</ul>
{{% endblock %}}

{{% block body %}}
    {SECTION}
{{% endblock %}}
"""

SECTIONS = {
'list': """
    <h1>All {TYPE_HUMAN} in all Storage Locations</h1>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Name</th>
                <th>Location</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
        {{% for object in object_list %}}
            <tr>
                <td>
                    <a href="{{% url 'lims:{URL_FORM2}-detail' object.id %}}">
                    {{{{ object }}}}
                    </a>
                </td>
                <td>
                    <ul class="breadcrumb">
                        <li>
                            <a href="{{% url 'lims:storage-location-detail' object.tube.box.location.id %}}">
                                {{{{ object.tube.box.location.name }}}}
                            </a>
                        </li>
                        <li>
                            <a href="{{% url 'lims:box-detail' object.tube.box.location.id object.tube.box.id %}}">
                                {{{{ object.tube.box.name }}}}
                            </a>
                        </li>
                        <li>
                            <a href="{{% url 'lims:box-detail' object.tube.box.location.id object.tube.box.id %}}#{{{{ object.tube.lysate.id | cptids_encode:'lysate' }}}}">
                                {{{{ object.tube.name }}}}
                            </a>
                        </li>
                    </ul>
                </td>
                <td>
                    <div class="btn-group">
                        <a href="#" class="btn btn-default dropdown-toggle noUnderline" data-toggle="dropdown">Actions <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li><a class="noUnderline" href="{{% url 'lims:{URL_FORM2}-edit'   object.id %}}">Edit {TYPE_HUMAN}</a></li>
                            <li><a class="noUnderline" href="{{% url 'lims:{URL_FORM2}-delete' object.id %}}">Delete {TYPE_HUMAN}</a></li>
                        </ul>
                    </div>
                </td>
            </tr>
        {{% endfor %}}
        </tbody>
    </table>
""",
'delete':"""
    <h1>{ACTION_HUMAN} {{{{ object }}}}</h1>
    <div class="row">
        <div class="col-md-8">
            <form method="post">
                {{% csrf_token %}}
                <p>Are you sure you want to delete "{{{{ object }}}}"?</p>
                <button type="submit" class="btn btn-default btn-danger" style="width:40%">Yes</button>
                <a class="btn btn-default btn-primary" style="width:40%" href="{{% url 'lims:{URL_FORM}-detail' object.id %}}">Cancel</a>
            </form>
        </div>
    </div>
""",
'detail': """
    <h1>
        {{{{ object }}}}
        <div class="btn-group">
            <a href="#" class="btn btn-default dropdown-toggle" data-toggle="dropdown">Actions <span class="caret"></span></a>
            <ul class="dropdown-menu">
                <li><a href="{{% url 'lims:{URL_FORM}-edit' object.id %}}">Edit {TYPE_HUMAN}</a></li>
                <li><a href="{{% url 'lims:{URL_FORM}-delete' object.id %}}">Delete {TYPE_HUMAN}</a></li>
            </ul>
        </div>
    </h1>

    <div class="row">
        {OBJ_META}
    </div>
""",
# FORM
'create': """
    <h1>{ACTION_HUMAN} {TYPE_HUMAN}</h1>
    <div class="row">
        <div class="col-md-8">
            <form method="post">
                {{% csrf_token %}}
                {{% bootstrap_form form %}}
                <button type="submit" class="btn btn-default btn-primary" style="width:100%">Submit</button>
            </form>
        </div>
    </div>
""",
'update': """
    <h1>{ACTION_HUMAN} {TYPE_HUMAN} {{{{ object.name }}}}</h1>
    <div class="row">
        <div class="col-md-8">
            <form method="post">
                {{% csrf_token %}}
                {{% bootstrap_form form %}}
                <button type="submit" class="btn btn-default btn-primary" style="width:100%">Submit</button>
            </form>
        </div>
    </div>
""",
}

section_file_mapping = {
    'list': '%s_list.html',
    'update': '%s_update.html',
    'create': '%s_create.html',
    'detail': '%s_detail.html',
    'delete': '%s_confirm_delete.html',
}

crumbs = {
    'list': """
    <li class="active">{TYPE_HUMAN}</li>
    """,
    'update': """
    <li><a href="{% url 'lims:storage-location-detail' object.tube.box.location.id %}">{{ object.tube.box.location.name }}</a></li>
    <li><a href="{% url 'lims:box-detail' object.tube.box.location.id object.tube.box.id %}">{{ object.tube.box.name }}</a></li>
    <li class="active">{{ object }}</li>
    """,
    'create': 'Add a new',
    'detail': """
    <li><a href="{% url 'lims:storage-location-detail' object.tube.box.location.id %}">{{ object.tube.box.location.name }}</a></li>
    <li><a href="{% url 'lims:box-detail' object.tube.box.location.id object.tube.box.id %}">{{ object.tube.box.name }}</a></li>
    <li class="active">{{ object }}</li>
    """,
    'delete': """
    <li><a href="{% url 'lims:storage-location-detail' object.tube.box.location.id %}">{{ object.tube.box.location.name }}</a></li>
    <li><a href="{% url 'lims:box-detail' object.tube.box.location.id object.tube.box.id %}">{{ object.tube.box.name }}</a></li>
    <li class="active">{{ object }}</li>
    """,
}
action_name_mapping = {
    'list': 'View',
    'update': 'Update',
    'create': 'Add a new',
    'detail': '',
    'delete': 'Delete',
}

OBJ_META_ROW = """            <tr>
                <td>
                    {key}
                </td>
                <td>
                    {value}
                </td>
            </tr>"""
OBJ_META = """<table class="table table-striped">
{{% load model_field %}}
{META_ROWS}
        </table>"""

URLS_TEMPLATE="""
from views import {fn}List, {fn}Detail, {fn}Create, {fn}Edit, {fn}Delete

url(r'^{URL_FORM}/$',                          {fn}List.as_view(),     name='{URL_FORM2}-list'),
url(r'^{URL_FORM}/create$',                    {fn}Create.as_view(),   name='{URL_FORM2}-create'),
url(r'^{URL_FORM}/(?P<pk>[0-9]+)$',            {fn}Detail.as_view(),   name='{URL_FORM2}-detail'),
url(r'^{URL_FORM}/(?P<pk>[0-9]+)/edit$',       {fn}Edit.as_view(),     name='{URL_FORM2}-edit'),
url(r'^{URL_FORM}/(?P<pk>[0-9]+)/delete$',     {fn}Delete.as_view(),   name='{URL_FORM2}-delete'),

## views.py

class {fn}List(ListView):
    model = {fn}

class {fn}Detail(DetailView):
    model = {fn}

class {fn}Create(CreateView):
    model = {fn}
    fields = ("{fields}")
    template_name_suffix = '_create'

class {fn}Edit(UpdateView):
    model = {fn}
    fields = ("{fields}")
    template_name_suffix = '_update'

class {fn}Delete(DeleteView):
    model = {fn}
    success_url = reverse_lazy('lims:{URL_FORM2}-list')
"""

def x(url_form, human_name, fields):
    print URLS_TEMPLATE.format(
        URL_FORM=url_form, # env_sample
        URL_FORM2=url_form.replace('_', '-'), #env-sample
        fn=human_name.replace(' ', ''), #EnvironmentalSample
        fields='", "'.join(fields), #...
    )

    for sec in section_file_mapping.keys():
        fn = section_file_mapping[sec] % human_name.replace(' ', '').lower()

        omr = []
        for field in fields:
            omr.append(OBJ_META_ROW.format(
                key="{% model_field_verbose_name from object." + field + " %}",
                value="{{ object." + field +" }}"
            ))

        data = {
            'TYPE_HUMAN': human_name, # Environmental Sample
            'ACTION_HUMAN': action_name_mapping[sec], # Delete/View
            'URL_FORM': url_form, # env_sample
            'URL_FORM2': url_form.replace('_', '-'),
            'CRUMBS': crumbs[sec].replace('{TYPE_HUMAN}', human_name),
            'OBJ_META': OBJ_META.format(META_ROWS='\n'.join(omr))
        }
        section = SECTIONS.get(sec)

        with open(fn.lower(), 'w') as handle:
            formatted_sec = section.format(**data)
            data['SECTION'] = formatted_sec
            out = BASE_TEMPLATE.format(**data)
            handle.write(out)


q = (
    # ('envsample', 'Environmental Sample', ('collection', 'location', 'sample_type', 'tube')),
    # ('lysate', 'Lysate', ('env_sample', 'host_lims', 'oldid', 'isolation', 'owner', 'source', 'tube')),
    # ('phagednaprep', 'Phage DNA Prep', ('lysate', 'morphology', 'tube')),
    ('bacteria', 'Bacteria', ('genus', 'species', 'strain')),
)

for w in q:
    x(*w)
