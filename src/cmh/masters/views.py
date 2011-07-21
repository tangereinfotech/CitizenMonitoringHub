# encoding: utf-8
# Copyright 2011, Tangere Infotech Pvt Ltd [http://tangere.in]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import simplejson as json

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from cmh.usermgr.models import CmhUser, Official
from cmh.usermgr.utils import get_user_menus

from cmh.common.constants import UserRoles
from cmh.common.models import ComplaintDepartment, ComplaintType
from cmh.common.utils import debug
from cmh.common.utils import get_datatables_records
from cmh.common.constants import DeployDistrict
from cmh.common.models import  State, District, Block, GramPanchayat, Village

from cmh.masters.forms import AddCSOMember, RegisterDM, DmId, EditDM
from cmh.masters.forms import AddEditOfficial, DepartmentSelected
from cmh.masters.forms import AddBlock, AddComplaint, AddGramPanchayat, AddDep
from cmh.masters.forms import AddVillage, AddDistrict, AddState
from cmh.masters.forms import EditGp, EditVillage, EditDep, EditComp, EditBlk, EditOfficial, EditCso

from cmh.issuemgr.models import ReportData
@login_required
def masters (request):
    # Ensure CmhUser model instance exists for all User's
    for user in User.objects.filter (cmhuser = None):
        cmhuser = CmhUser.objects.create (user = user)

    cmhusers = CmhUser.objects.all ()

    paginator = Paginator (cmhusers, 10)

    try:
        page = int (request.GET.get ('page', '1'))
    except ValueError:
        page = 1

    try:
        cmhusers = paginator.page (page)
    except (EmptyPage, InvalidPage):
        cmhusers = paginator.page (paginator.num_pages)

    return render_to_response ("masters.html",
                               {'menus' : get_user_menus (request.user,masters),
                                'cmhusers' : cmhusers,
                                'user' : request.user})

@login_required
def process_dm (request):
    cmhuser_dm = CmhUser.objects.filter (user__approle__role = UserRoles.DM)
    if request.method == 'GET':
        if cmhuser_dm.count () == 0:
            return render_to_response ('create_dm.html',
                                       {'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user,
                                        'form' : RegisterDM ()})
        elif cmhuser_dm.count () == 1:
            return render_to_response ('view_dm.html',
                                       {'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user,
                                        'dm' : cmhuser_dm [0]})
        else:
            return render_to_response ('error_dm_count.html',
                                       {'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user})
    elif request.method == 'POST':
        if 'register' in request.POST: # Registering a new DM
            form = RegisterDM (request.POST)
            if form.is_valid ():
                dm = form.save ()
                return render_to_response ('view_dm.html',
                                           {'menus' : get_user_menus (request.user,process_dm),
                                            'user' : request.user,
                                            'dm' : dm})
            else:
                return render_to_response ('create_dm.html',
                                           {'menus' : get_user_menus (request.user,process_dm),
                                            'user' : request.user,
                                            'form' : form})
        elif 'cancel' in request.POST: # Cancel DM registration
            return HttpResponseRedirect (reverse (masters))
        elif 'edit_dm' in request.POST: # Edit DM record
            form = DmId (request.POST)
            if form.is_valid ():
                dmid = form.cleaned_data ['dmid']
                try:
                    dm = CmhUser.objects.get (user__approle__role = UserRoles.DM,
                                              id = dmid)
                    formdata = {'dmid' : dm.id,
                                'username' : dm.user.username,
                                'name' : dm.user.get_full_name (),
                                'phone' : dm.phone}
                    form = EditDM (formdata)
                    return render_to_response ('edit_dm.html',
                                               {'menus':get_user_menus(request.user,process_dm),
                                                'user' : request.user,
                                                'form' : form})
                except CmhUser.DoesNotExist, CmhUser.MultipleObjectsReturned:
                    return HttpResponse (reverse (masters))
        elif 'edit_save' in request.POST:
            debug ("Saving a DM object")
            form = EditDM (request.POST)
            if form.is_valid ():
                form.save ()
                return HttpResponseRedirect (reverse (process_dm))
            else:
                debug ("Invalid form:" , form.errors)
                return render_to_response ('edit_dm.html',
                                           {'menus': get_user_menus(request.user,process_dm),
                                            'user' : request.user,
                                            'form' : form})
        elif 'edit_cancel' in request.POST:
            return HttpResponseRedirect (reverse (process_dm))
        else:
            return HttpResponseRedirect (reverse (masters))
    else:
        return HttpResponseRedirect (reverse (masters))

@login_required
def officials (request):
    if request.method == 'GET':
        return render_to_response ('officials.html',
                                   {'menus' : get_user_menus (request.user,process_dm),
                                    'user' : request.user})
    else:
        return render_to_response ('error.html',
                                   {'error': 'No other method is supported',
                                    'menus' : get_user_menus (request.user,process_dm),
                                    'user' : request.user})



@login_required
def officialist(request):
    try:
        query = (Q (user__approle__role = UserRoles.OFFICIAL) |
                 Q (user__approle__role = UserRoles.DELEGATE))

        querySet = CmhUser.objects.filter (query)

        columnIndexNameMap = { 0: 'user__first_name',
                               1: 'get_role_name',
                               2: 'phone_number',
                               3: 'department__name',
                               4: 'supervisor_names',
                               5: 'id'}

        x = get_datatables_records (request, querySet, columnIndexNameMap, 'officials_datatable.html')
    except:
        import traceback
        traceback.print_exc ()
    return x

@login_required
def edit_off(request, offid):
    if request.method == "POST":
        form = EditOfficial(None, request.POST)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect (reverse (officials))
        else:
            return render_to_response ('edit_official.html',
                                       {'trial' : form,
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user})
    else:
        off = CmhUser.objects.get (id = offid)

        if (off.get_user_role () != UserRoles.ROLE_OFFICIAL and
            off.get_user_role () != UserRoles.ROLE_DELEGATE):
            raise Exception("Wrong data passed! The data passed doesnot belong to any official Please go back and click again")
        else:
            return render_to_response ('edit_official.html',
                                       {'trial' : EditOfficial (offobj = off ),
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user'  : request.user})


@login_required
def add_official (request):
    cmhuser_dm = CmhUser.objects.filter (user__approle__role = UserRoles.DM)
    if request.method == 'GET':
        if cmhuser_dm.count () == 0:
            return render_to_response ('error.html',
                                       {'error' : 'District Magistrate must be registered',
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user})
        elif cmhuser_dm.count () > 1:
            return render_to_response ('error.html',
                                       {'error' : 'Multiple DMs defined [%d]',
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user})
        else:
            departments = ComplaintDepartment.objects.all ()
            return render_to_response ('add_official.html',
                                          {'menus' : get_user_menus (request.user,process_dm),
                                           'user' : request.user,
                                           'form' : AddEditOfficial (departments = departments)})
    elif request.method == 'POST':
        if 'add_add_official' in request.POST:
            supervisors = None
            if 'pos_supervisors' in request.session:
                supervisors = json.loads (request.session ['pos_supervisors'])

            departments = ComplaintDepartment.objects.all ()
            form = AddEditOfficial (request.POST,
                                    departments = departments,
                                    supervisors = supervisors)

            if form.is_valid ():
                form.save ()
                return HttpResponseRedirect (reverse (officials))
            else:
                return render_to_response ('add_official.html',
                                           {'menus' : get_user_menus (request.user,process_dm),
                                            'user' : request.user,
                                            'form' : form})
        elif 'add_cancel_official' in request.POST:
            return HttpResponseRedirect (reverse (officials))
        else:
            return HttpResponseRedirect (reverse (officials))

    else:
        return HttpResponseRedirect (reverse (officials))


@login_required
def department_selected (request):
    form = DepartmentSelected (request.GET)
    if form.is_valid ():
        debug (form)
        try:
            dept_id = form.cleaned_data ['department']
            supervisors = Official.objects.filter (department__id = dept_id,
                                                   supervisor = None)
            sups = [(supervisor.id, supervisor.user.cmhuser.get_desc_name ())
                    for supervisor in supervisors]
            sups.insert (0, ('-1', '----'))
            serialized = json.dumps (sups)
            request.session ['pos_supervisors'] = serialized
            return HttpResponse (serialized)
        except:
            import traceback
            traceback.print_exc ()
            return HttpResponse ([])
    else:
        return HttpResponse ([])


@login_required
def csomembers (request):
    return render_to_response ("cso_master.html",
                               {'menus' : get_user_menus (request.user,csomembers),
                                'user' : request.user})


@login_required
def csolist(request):
    try:
        querySet = CmhUser.objects.filter (user__approle__role = UserRoles.CSO)

        columnIndexNameMap = { 0: 'id',
                               1: 'get_role_name',
                               2: 'phone_number',
                               3: 'id'}

        x = get_datatables_records (request, querySet, columnIndexNameMap, 'cso_datatable.html')
    except:
        import traceback
        traceback.print_exc ()
    return x

@login_required
def edit_cso(request, csoid):
    if request.method == "POST":
        form = EditCso(None, request.POST)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect (reverse (csomembers))
        else:
            return render_to_response ('edit_cso.html',
                                       {'trial' : form,
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user})
    else:
        cso = CmhUser.objects.get (id = csoid)

        if (cso.get_user_role () != UserRoles.ROLE_CSO):
            raise Exception("Wrong data passed! The data passed doesnot belong to any cso Please go back and click again")
        else:
            return render_to_response ('edit_cso.html',
                                       {'trial' : EditCso (csoobj = cso ),
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user'  : request.user})


@login_required
def add_cso_user (request):
    if request.method == 'GET':
        return render_to_response ('add_cso_member.html',
                                   {'menus' : get_user_menus (request.user,add_cso_user),
                                    'user' : request.user,
                                    'form' : AddCSOMember ()})
    elif request.method == 'POST':
        form = AddCSOMember (request.POST)
        if 'add' in request.POST:
            if form.is_valid ():
                form.save ()
                return HttpResponseRedirect (reverse (csomembers))
            else:
                return render_to_response ('add_cso_member.html',
                                           {'menus' : get_user_menus (request.user,add_cso_user),
                                            'user' : request.user,
                                            'form' : form})
        else:
            return HttpResponseRedirect (reverse (csomembers))
    else:
        return HttpResponseRedirect ("/")

@login_required
def state (request) :
    stateobj=State.objects.all()
    return render_to_response ('view_state.html',
                               {'states':stateobj,
                                'menus' : get_user_menus (request.user,process_dm),
                                'user' : request.user})

@login_required
def add_state(request):
    if request.method =="GET":
        form = AddState();
        return render_to_response ('edit_state.html',
                                   {'trial' : AddState (),
                                    'menus' : get_user_menus (request.user,process_dm),
                                    'flag'  : True,
                                    'user'  : request.user})
    elif request.method == "POST":
        form = AddState(request.POST)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect (reverse (state))
        else:
            return render_to_response ('edit_state.html',
                                       {'trial' : form,
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'flag'  : True,
                                        'user' : request.user})


@login_required
def district (request) :
    distobj=District.objects.all()
    return render_to_response ('view_district.html',
                               {'districts':distobj,
                                'menus' : get_user_menus (request.user,process_dm),
                                'user' : request.user})

@login_required
def add_district(request):
    if request.method =="GET":
        return render_to_response ('edit_district.html',
                                   {'trial' : AddDistrict (),
                                    'menus' : get_user_menus (request.user,process_dm),
                                    'flag'  : True,
                                    'user' : request.user})
    elif request.method == "POST":
        form = AddDistrict(request.POST)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect (reverse (district))
        else:
            return render_to_response ('edit_district.html',
                                   {'trial' : form,
                                    'menus' : get_user_menus (request.user,process_dm),
                                    'flag'  : True,
                                    'user' : request.user})

@login_required
def block (request) :
    dname=DeployDistrict.DISTRICT.name
    dcode=DeployDistrict.DISTRICT.get_code()
    scode = DeployDistrict.DISTRICT.state.get_code()
    sname = DeployDistrict.DISTRICT.state.name
    return render_to_response ('view_block.html',
                               {'disname':dname,
                                'discode':dcode,
                                'menus' : get_user_menus (request.user,process_dm),
                                'statecode': scode,
                                'statename': sname,
                                'user' : request.user})

@login_required
def blist (request):
    try:
        querySet = Block.objects.all ()

        columnIndexNameMap = { 0: 'code',
                               1: 'name',
                               2 : 'lattd',
                               3 : 'longd'}

        x = get_datatables_records (request, querySet, columnIndexNameMap, 'block_datatable.html')
    except:
        import traceback
        traceback.print_exc ()
    return x



@login_required
def addblock(request):
    if request.method =="GET":
        return render_to_response ('add_block.html',
                                   {'trial' : AddBlock (),
                                    'menus' : get_user_menus (request.user,process_dm),
                                    'user' : request.user})
    elif request.method == "POST":
        form = AddBlock(request.POST)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect (reverse (block))
        else:
            return render_to_response ('add_block.html',
                                       {'trial' : form,
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user})


@login_required
def gp (request) :
    dname=DeployDistrict.DISTRICT.name
    dcode=DeployDistrict.DISTRICT.get_code ()
    scode = DeployDistrict.DISTRICT.state.get_code ()
    sname = DeployDistrict.DISTRICT.state.name
    return render_to_response ('view_gp.html',
                               {'disname':dname,
                                'discode':dcode,
                                'statecode': scode,
                                'statename': sname,
                                'menus' : get_user_menus (request.user,process_dm),
                                'user' : request.user})

@login_required
def addgp(request):
    if request.method =="GET":
        return render_to_response ('add_gp.html',
                                   {'trial' : AddGramPanchayat (),
                                    'menus' : get_user_menus (request.user,process_dm),
                                    'user' : request.user})
    elif request.method == "POST":
        form = AddGramPanchayat(request.POST)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect (reverse (gp))
        else:
            return render_to_response ('add_gp.html',
                                       {'trial' : form,
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user})


@login_required
def village (request) :
    dname = DeployDistrict.DISTRICT.name
    dcode = DeployDistrict.DISTRICT.get_code ()
    scode = DeployDistrict.DISTRICT.state.get_code ()
    sname = DeployDistrict.DISTRICT.state.name
    return render_to_response ('view_village.html',
                               {'disname'  : dname,
                                'discode'  : dcode,
                                'statecode': scode,
                                'statename': sname,
                                'menus'    : get_user_menus (request.user,process_dm),
                                'user'     : request.user})


@login_required
def addvillage(request):
    if request.method =="GET":
        return render_to_response ('add_village.html',
                                   {'trial' : AddVillage (),
                                    'menus' : get_user_menus (request.user,process_dm),
                                    'user' : request.user})
    elif request.method == "POST":
        form = AddVillage(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( reverse(village) )
        else:
            return render_to_response ('add_village.html',
                                       {'trial' : form,
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user'  : request.user})



@login_required
def department (request) :
    return render_to_response ('view_dep.html',
                               {'menus'    : get_user_menus (request.user,process_dm),
                                'user'     : request.user})

@login_required
def complainttype(request) :
    return render_to_response ('view_comp_type.html',
                               {'menus'    : get_user_menus (request.user,process_dm),
                                'user'     : request.user})


@login_required
def adddep(request):
    if request.method=="GET":
        return render_to_response ('add_dep.html',
                                   {'trial' : AddDep (),
                                    'menus' : get_user_menus (request.user,process_dm),
                                    'user' : request.user})
    elif request.method == "POST":
        form = AddDep(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( reverse(department) )
        else:
            return render_to_response ('add_dep.html',
                                       {'trial' : form,
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user'  : request.user})


@login_required
def addcomp(request):
    if request.method=="GET":
        return render_to_response ('add_comp_type.html',
                                   {'trial' : AddComplaint (),
                                    'menus' : get_user_menus (request.user,process_dm),
                                    'user' : request.user})
    elif request.method == "POST":
        form = AddComplaint(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( reverse(complainttype) )
        else:
            return render_to_response ('add_comp_type.html',
                                       {'trial' : form,
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user'  : request.user})

def getgpinblocks (request):
    repdata = ReportData.objects.get (id = request.GET.get ('repdataid'))
    blockid = request.GET['blockid']
    try:
        gps = Block.objects.get (id = blockid).grampanchayat_set.all ().exclude(id__in = [gp.id for gp in repdata.gp.all()])
    except Block.DoesNotExist:
        gps = []
    retdata = [{'id' : gp.id, 'name' : str (gp)} for gp in gps]
    return HttpResponse (json.dumps ({'gps' : retdata}))


def getvillingps (request):
    repdata = ReportData.objects.get (id = request.GET.get ('repdataid'))
    gpid = request.GET['gpid']
    try:
        vills = GramPanchayat.objects.get (id = gpid).village_set.all ().exclude(id__in = [v.id for v in repdata.village.all()])
    except GramPanchayat.DoesNotExist:
        vills = []
    retdata = [{'id' : vill.id, 'name' : str (vill)} for vill in vills]
    return HttpResponse (json.dumps ({'vills' : retdata}))


@login_required
def getclassindep (request):
    depid = request.GET['depid']
    try:
        classes = ComplaintDepartments.objects.get (id = depid).ComplaintType_set.all ()
    except Block.DoesNotExist:
        classes = []
    retdata = [{'id' : dep.id, 'name' : str (dep)} for dep in classes]
    return HttpResponse (json.dumps ({'classes' : retdata}))


@login_required
def gplist (request):
    try:
        querySet = GramPanchayat.objects.all ()

        columnIndexNameMap = { 0: 'block__code',
                               1: 'block__name',
                               2: 'code',
                               3: 'name',
                               4: 'lattd',
                               5: 'longd'}

        x = get_datatables_records (request, querySet, columnIndexNameMap, 'gplist_datatable.html')
    except:
        import traceback
        traceback.print_exc ()
    return x




@login_required
def villist (request):
    try:
        querySet = Village.objects.all ()

        columnIndexNameMap = { 0: 'grampanchayat__block__code',
                               1: 'grampanchayat__block__name',
                               2: 'grampanchayat__code',
                               3: 'grampanchayat__name',
                               4: 'code',
                               5: 'name',
                               6: 'lattd',
                               7: 'longd'}

        x = get_datatables_records (request, querySet, columnIndexNameMap, 'villist_datatable.html')
    except:
        import traceback
        traceback.print_exc ()
    return x

@login_required
def deplist (request):
    try:
        querySet = ComplaintDepartment.objects.all()

        columnIndexNameMap = { 0: 'code',
                               1: 'name'}

        x = get_datatables_records (request, querySet, columnIndexNameMap, 'department_datatable.html')
    except:
        import traceback
        traceback.print_exc ()
    return x

@login_required
def clist (request):
    try:
        querySet = ComplaintType.objects.all()


        columnIndexNameMap = { 0: 'department__code',
                               1: 'code',
                               2: 'summary',
                               3: 'cclass'}

        x = get_datatables_records (request, querySet, columnIndexNameMap, 'comp_datatable.html')
    except:
        import traceback
        traceback.print_exc ()
    return x


@login_required
def editblk (request, blkcode):
    if request.method == "POST":
        form = EditBlk(None, request.POST)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect (reverse (block))
        else:
            return render_to_response ('edit_block.html',
                                       {'trial' : form,
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user})
    else:
        bcode = DeployDistrict.DISTRICT.code + "." + blkcode
        blk = Block.objects.get (code = bcode)
        return render_to_response ('edit_block.html',
                                   {'trial' : EditBlk (blkobj = blk),
                                    'menus' : get_user_menus (request.user,process_dm),
                                    'user'  : request.user})


@login_required
def editvill (request, block, gpcode, villcode):
    if request.method == "POST":
        form = EditVillage(None, request.POST)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect (reverse (village))

        else:
            return render_to_response ('edit_village.html',
                                       {'trial' : form,
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user})
    else:
        villcode = DeployDistrict.DISTRICT.code +"." + block + "." + gpcode + "." + villcode
        vilage = Village.objects.get(code = villcode)
        return render_to_response ('edit_village.html',
                                   {'trial' : EditVillage (villobj = vilage),
                                    'menus' : get_user_menus (request.user,process_dm),
                                    'user'  : request.user})



@login_required
def editgp (request, block, gpcode):
    if request.method == "POST":
        form = EditGp(None, request.POST)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect (reverse (gp))
        else:
            return render_to_response ('edit_gp.html',
                                       {'trial' : form,
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user})
    else:
        gpcode = DeployDistrict.DISTRICT.code + "." + block + "." + gpcode
        gramp = GramPanchayat.objects.get (code = gpcode)
        return render_to_response ('edit_gp.html',
                                   {'trial' : EditGp (gpobj = gramp),
                                    'menus' : get_user_menus (request.user,process_dm),
                                    'user'  : request.user})


@login_required
def editdep (request, depcode):
    if request.method == "POST":
        form = EditDep(None, request.POST)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect (reverse (department))
        else:
            return render_to_response ('edit_dep.html',
                                       {'trial' : form,
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user})
    else:
        dept = ComplaintDepartment.objects.get (code = depcode)
        return render_to_response ('edit_dep.html',
                                   {'trial' : EditDep (depobj = dept),
                                    'menus' : get_user_menus (request.user,process_dm),
                                    'user'  : request.user})

@login_required
def editc (request, compcode, depcode):
    if request.method == "POST":
        form = EditComp(None, request.POST)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect (reverse (complainttype))
        else:
            return render_to_response ('edit_comp_type.html',
                                       {'trial' : form,
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user})
    else:
        ccode = "%s.%03s" %(depcode,compcode)
        comp = ComplaintType.objects.get (code = ccode)
        return render_to_response ('edit_comp_type.html',
                                   {'trial' : EditComp (compobj = comp),
                                    'menus' : get_user_menus (request.user,process_dm),
                                    'user'  : request.user})
