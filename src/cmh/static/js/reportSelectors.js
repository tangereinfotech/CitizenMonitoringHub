
var RepSelector = {
    blkcheckarray : new Array(),
    gpcheckarray : new Array(),
    vcheckarray : new Array(),
    blkcount : 0,
    gpcount : 0, 
    vcount : 0,

    deptids : new Array (),
    blockids : new Array (),
    grampids : new Array (),
    villgids : new Array (),

    removeArrayElement : function (arr, elem) {
        for (var i=0; i < arr.length; i++) { 
            if(arr[i] == elem) {
                arr.splice (i, 1);
                break;
            }
        } 
    },

    fnAddSelectedDept : function (deptid) {
        this.deptids.push (deptid);  
    },

    fnRemSelectedDept : function (deptid) {
        removeArrayElement (this.deptids, deptid);
    },

    submitReport : function () {
        var form = document.createElement ("form");
        form.action = "/complaint/initial_report/";
        form.method = "post";

        document.body.appendChild (form);
        form.submit ();
    },

    fnMoveItems : function (box1, box2, identifier) {
        var varFromBox = document.getElementById(box1);
        var varToBox = document.getElementById(box2);
        if ((varFromBox != null) && (varToBox != null))
        {
            if(varFromBox.length < 1)
            {
                alert('No Value Selected','There are no items in the source ListBox');
                return false;
            }
            if(varFromBox.options.selectedIndex == -1) // when no Item is selected the index will be -1
            {
                alert('No Value Selected','Please select an Item to move');
                return false;
            }
            
            while (varFromBox.options.selectedIndex >= 0 )
            {
                var newOption = new Option(); // Create a new instance of ListItem
                newOption.text = varFromBox.options[varFromBox.options.selectedIndex].text;
                newOption.value = varFromBox.options[varFromBox.options.selectedIndex].value;
                varToBox.options[varToBox.length] = newOption; //Append the item in Target Listbox
                varFromBox.remove(varFromBox.options.selectedIndex); //Remove the item from Source Listbox
            }
        }
        return false;
    },

    appendRow : function (val, repdataid) {
        if (val == 'blk')
        {
            var tbl = document.getElementById('sel_loc'); // table reference
            var flag=0;
            var count=0;
            var textb = document.getElementById("id_block");
            var selectedval;
            if(textb.value != ''){
                if (blkcheckarray.length!=0)
                {
                    for (j=0;j<blkcheckarray.length;j++)
                    {
                        if(textb.value==blkcheckarray[j])
                        {
                            alert("Duplicate Selection","Block already added! Please choose a different block");
                            flag=1;
                            break;
                        }
                    }
                    if (!flag)
                    {
                        var row = tbl.insertRow(tbl.rows.length);      // append table row
                        $.post ("/complaint/storedata/" + repdataid + "/BLK/"  + textb.value + "/" + 0 + "/" + 0 +"/",
                                {},
                                function (data, textStatus, jqXHR) {
                                })
                        for (i=0; i<textb.options.length; i++)
                        {
                            if (textb.options[i].selected)
                            {
                                selectedval = textb.options[i].text;
                                createCell(row.insertCell(0), selectedval, 'row');
                                break;
                            }
                            count++;
                        }
                        for (i = 1; i < (tbl.rows[0].cells.length)-1; i++)
                        {
                            createCell(row.insertCell(i), '-----' , 'row');
                        }
                        var cell2 = row.insertCell((tbl.rows[0].cells.length)-1);
		                var btnEl = document.createElement('input');
		                btnEl.setAttribute('type', 'button');
		                btnEl.setAttribute('value', 'Remove');
		                btnEl.setAttribute('class', 'btn');
		                btnEl.setAttribute('style', 'width:80px');
		                btnEl.onclick =Redirector("BLK", repdataid, textb.value, 0, 0, row);
		                cell2.appendChild(btnEl);
                    }
                    blkcheckarray[blkcount] = textb.value;
                    blkcount++;
                }
                else
                {
                    var row = tbl.insertRow(tbl.rows.length);      // append table row
                    $.post ("/complaint/storedata/" + repdataid + "/BLK/"  + textb.value + "/" + 0 + "/" + 0 +"/",
                            {},
                            function (data, textStatus, jqXHR) {
                            })
                    for (i=0; i<textb.options.length; i++)
                    {
                        if (textb.options[i].selected)
                        {
                            selectedval = textb.options[i].text;
                            createCell(row.insertCell(0), selectedval, 'row');
                            break;
                        }
                        count++;
                    }
                    for (i = 1; i < (tbl.rows[0].cells.length)-1; i++)
                    {
                        createCell(row.insertCell(i), '-----' , 'row');
                    }
                    var cell2 = row.insertCell((tbl.rows[0].cells.length)-1);
		            var btnEl = document.createElement('input');
		            btnEl.setAttribute('type', 'button');
		            btnEl.setAttribute('value', 'Remove');
		            btnEl.setAttribute('class', 'btn');
		            btnEl.setAttribute('style', 'width:80px');
                    btnEl.onclick =Redirector("BLK",repdataid, textb.value, 0, 0, row);
		            cell2.appendChild(btnEl);
                    blkcheckarray[blkcount] = textb.value;
                    blkcount++;
                }
            }
            else{
                alert("Invalid Selection","Select a valid Block option");
            }
            document.getElementById("id_block").options.remove(count);
            document.getElementById("id_gp").options.length=1;
            
        }
        if (val == 'gp')
        {
            var tbl = document.getElementById('sel_loc'); // table reference
            var flag=0;
            var count=0;
            var textc = document.getElementById("id_gp");
            var textb = document.getElementById("id_block");
            var selectedval;
            if(textc.value != 0 && textc.value != '')
            {
                if (gpcheckarray.length!=0)
                {
                    for (j=0;j<gpcheckarray.length;j++)
                    {
                        if(textc.value==gpcheckarray[j])
                        {
                            alert("Duplicate Selection","GramPanchayat already added! Please choose a different GramPanchayat");
                            flag=1;
                            break;
                        }
                    }
                    if (!flag)
                    {
                        var row = tbl.insertRow(tbl.rows.length);      // append table row
                        $.post ("/complaint/storedata/" + repdataid + "/GP/"  + textb.value + "/" + textc.value + "/" + 0 +"/",
                                {},
                                function (data, textStatus, jqXHR) {
                                })
                        for (i=0; i<textb.options.length; i++)
                        {
                            if (textb.options[i].selected)
                            {
                                selectedval = textb.options[i].text;
                                createCell(row.insertCell(0), selectedval, 'row');
                            }
                        }
                        for (i=0; i<textc.options.length; i++)
                        {
                            if (textc.options[i].selected)
                            {
                                selectedval = textc.options[i].text;
                                createCell(row.insertCell(1), selectedval, 'row');
                                break;
                            }
                            count++;
                        }
                        for (i = 2; i < (tbl.rows[0].cells.length)-1; i++)
                        {
                            createCell(row.insertCell(i), '-----' , 'row');
                        }
                        var cell2 = row.insertCell((tbl.rows[0].cells.length)-1);
		                var btnEl = document.createElement('input');
		                btnEl.setAttribute('type', 'button');
		                btnEl.setAttribute('value', 'Remove');
		                btnEl.setAttribute('class', 'btn');
		                btnEl.setAttribute('style', 'width:80px');
		                btnEl.onclick =Redirector("GP",repdataid, textb.value, textc.value, 0, row);
		                cell2.appendChild(btnEl);
                        gpcheckarray[gpcount] = textc.value;
                        gpcount++;
                    }
                }
                else
                {
                    var row = tbl.insertRow(tbl.rows.length);      // append table row
                    $.post ("/complaint/storedata/" + repdataid + "/GP/"  + textb.value + "/" + textc.value + "/" + 0 +"/",
                            {},
                            function (data, textStatus, jqXHR) {
                            })
                    for (i=0; i<textb.options.length; i++)
                    {
                        if (textb.options[i].selected)
                        {
                            selectedval = textb.options[i].text;
                            createCell(row.insertCell(0), selectedval, 'row');
                        }
                    }
                    for (i=0; i<textc.options.length; i++)
                    {
                        if (textc.options[i].selected)
                        {
                            selectedval = textc.options[i].text;
                            createCell(row.insertCell(1), selectedval, 'row');
                            break;
                        }
                        count++;
                    }
                    for (i = 2; i < (tbl.rows[0].cells.length)-1; i++)
                    {
                        createCell(row.insertCell(i), '-----' , 'row');
                    }
                    var cell2 = row.insertCell((tbl.rows[0].cells.length)-1);
		            var btnEl = document.createElement('input');
		            btnEl.setAttribute('type', 'button');
		            btnEl.setAttribute('value', 'Remove');
		            btnEl.setAttribute('class', 'btn');
		            btnEl.setAttribute('style', 'width:80px');
		            btnEl.onclick = Redirector("GP", repdataid, textb.value, textc.value, 0, row);
		            cell2.appendChild(btnEl);
                    gpcheckarray[gpcount] = textc.value;
                    gpcount++;

                }
            }
            else
            {
                alert("Invalid Selection","Select a valid GramPanchayat");
            }
            document.getElementById("id_gp").options.remove(count);
            document.getElementById("id_village").options.length=1;
        }

        if (val == 'vill')
        {
            var tbl = document.getElementById('sel_loc'); // table reference
            var flag=0;
            var count=0;
            var texta = document.getElementById("id_village");
            var textb = document.getElementById("id_gp");
            var textc = document.getElementById("id_block");
            var selectedval;
            if(texta.value != 0 && texta.value != '')
            {
                if (vcheckarray.length!=0)
                {
                    for (j=0;j<vcheckarray.length;j++)
                    {
                        if(texta.value==vcheckarray[j])
                        {
                            alert("Duplicate Selection","Village already added! Please choose a different Village");
                            flag=1;
                            break;
                        }
                    }
                    if (!flag)
                    {
                        var row = tbl.insertRow(tbl.rows.length);      // append table row
                        $.post ("/complaint/storedata/" + repdataid + "/VILL/"  + textc.value + "/" + textb.value + "/" + texta.value +"/",
                                {},
                                function (data, textStatus, jqXHR) {
                                })
                        for (i=0; i<textc.options.length; i++)
                        {
                            if (textc.options[i].selected)
                            {
                                selectedval = textc.options[i].text;
                                createCell(row.insertCell(0), selectedval, 'row');
                            }
                        }
                        for (i=0; i<textb.options.length; i++)
                        {
                            if (textb.options[i].selected)
                            {
                                selectedval = textb.options[i].text;
                                createCell(row.insertCell(1), selectedval, 'row');
                            }
                        }
                        for (i=0; i<texta.options.length; i++)
                        {
                            if (texta.options[i].selected)
                            {
                                selectedval = texta.options[i].text;
                                createCell(row.insertCell(2), selectedval, 'row');
                                break;
                            }
                            count++;
                        }
                        var cell2 = row.insertCell((tbl.rows[0].cells.length)-1);
		                var btnEl = document.createElement('input');
		                btnEl.setAttribute('type', 'button');
		                btnEl.setAttribute('value', 'Remove');
		                btnEl.setAttribute('class', 'btn');
		                btnEl.setAttribute('style', 'width:80px');
		                btnEl.onclick =Redirector("VILL", repdataid, textc.value, textb.value, texta.value, row);
		                cell2.appendChild(btnEl);
                        vcheckarray[vcount] = texta.value;
                        vcount++;
                    }
                }
                else
                {
                    var row = tbl.insertRow(tbl.rows.length);      // append table row
                    $.post ("/complaint/storedata/" + repdataid + "/VILL/"  + textc.value + "/" + textb.value + "/" + texta.value +"/",
                            {},
                            function (data, textStatus, jqXHR) {
                            })
                    for (i=0; i<textc.options.length; i++)
                    {
                        if (textc.options[i].selected)
                        {
                            selectedval = textc.options[i].text;
                            createCell(row.insertCell(0), selectedval, 'row');
                        }
                    }
                    for (i=0; i<textb.options.length; i++)
                    {
                        if (textb.options[i].selected)
                        {
                            selectedval = textb.options[i].text;
                            createCell(row.insertCell(1), selectedval, 'row');
                        }
                    }
                    for (i=0; i<texta.options.length; i++)
                    {
                        if (texta.options[i].selected)
                        {
                            selectedval = texta.options[i].text;
                            createCell(row.insertCell(2), selectedval, 'row');
                            break;
                        }
                        count++;
                    }
                    var cell2 = row.insertCell((tbl.rows[0].cells.length)-1);
		            var btnEl = document.createElement('input');
		            btnEl.setAttribute('type', 'button');
		            btnEl.setAttribute('value', 'Remove');
		            btnEl.setAttribute('class', 'btn');
		            btnEl.setAttribute('style', 'width:80px');
		            btnEl.onclick = Redirector("VILL", repdataid, textc.value, textb.value, texta.value,row);
		            cell2.appendChild(btnEl);
                    vcheckarray[vcount] = texta.value;
                    vcount++;
                }
            }
            else
            {
                alert("Invalid Selection","Select a valid Village");
            }
            document.getElementById("id_village").options.remove(count);
        }
    }
}

// create DIV element and append to the table cell
function createCell(cell, text, style) {
    var div = document.createElement('div'), // create DIV element
        txt = document.createTextNode(text); // create text node
    div.appendChild(txt);                    // append text node to the DIV
    div.setAttribute('class', style);        // set DIV class attribute
    div.setAttribute('className', style);    // set DIV class attribute for IE (?!)
    cell.appendChild(div);                   // append DIV to the table cell
}
function Redirector(cat, repdataid, code1, code2, code3, obj)
{
    return function()
    {
        deleteRow(cat, repdataid, code1, code2, code3, obj);
    };
}
function deleteRow(category, repdataid, bval,gpval,vval,obj)
{
    if (category == "BLK")
    {
        $.post ("/complaint/data/" + repdataid + "/blk/"  + bval +"/",
                {},
                function (data, textStatus, jqXHR) {
                })

        for (var i=0; i<blkcheckarray.length; i++)
        {

            if(blkcheckarray[i]==bval)
            {
                blkcheckarray.splice(i,1);
            }
        }
    }
    else if (category == "GP")
    {
        $.post ("/complaint/data/"+ repdataid + "/gp/"  + gpval +"/",
                {},
                function (data, textStatus, jqXHR) {
                })

        for (var i=0; i<gpcheckarray.length; i++)
        {

            if(gpcheckarray[i]==gpval)
            {
                gpcheckarray.splice(i,1);
            }
        }

    }
    else if (category == "VILL")
    {
        $.post ("/complaint/data/"+ repdataid + "/vill/"  + vval +"/",
                {},
                function (data, textStatus, jqXHR) {
                })

        for (var i=0; i<vcheckarray.length; i++)
        {

            if(vcheckarray[i]==vval)
            {
                vcheckarray.splice(i,1);
            }
        }
    }
    var delrow=obj.rowIndex;
    document.getElementById('sel_loc').deleteRow(delrow);
}
function doTableDelete (rowindex, id)
{
    var formid = "formloc-" + id;
    var form = document.getElementById (formid);
    form.submit ();
    htmldelete (rowindex);

}

function htmldelete(obj)
{
    document.getElementById('sel_loc').deleteRow(obj);
}

