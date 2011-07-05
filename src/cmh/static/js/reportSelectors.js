var blkcheckarray = new Array(), gpcheckarray = new Array(), vcheckarray = new Array();
var blkcount=0, gpcount=0, vcount=0;

function fnMoveItems(box1,box2) {
    var varFromBox = document.all(box1);
    var varToBox = document.all(box2);
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

        while ( varFromBox.options.selectedIndex >= 0 )
        {
            var newOption = new Option(); // Create a new instance of ListItem
            newOption.text = varFromBox.options[varFromBox.options.selectedIndex].text;
            newOption.value = varFromBox.options[varFromBox.options.selectedIndex].value;
            varToBox.options[varToBox.length] = newOption; //Append the item in Target Listbox

            $.post ("/complaint/storedata/DEP/"  + newOption.value + "/" + 0 + "/" + 0 +"/",
                    {},
                    function (data, textStatus, jqXHR) {
                    })


            varFromBox.remove(varFromBox.options.selectedIndex); //Remove the item from Source Listbox
        }
    }
    return false;
}

// append row to the HTML table
function appendRow(val) {
    if (val == 'blk')
    {
        var tbl = document.getElementById('sel_loc'); // table reference
        var flag=0;
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
                    $.post ("/complaint/storedata/" + "BLK" + "/"  + textb.value + "/" + 0 + "/" + 0 +"/",
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
                    for (i = 1; i < tbl.rows[0].cells.length; i++)
                    {
                        createCell(row.insertCell(i), '-----' , 'row');
                    }
                }
                blkcheckarray[blkcount] = textb.value;
                blkcount++;
            }
            else
            {
                var row = tbl.insertRow(tbl.rows.length);      // append table row
                $.post ("/complaint/storedata/" + "BLK" + "/"  + textb.value + "/" + 0 + "/" + 0 +"/",
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
                for (i = 1; i < tbl.rows[0].cells.length; i++)
                {
                    createCell(row.insertCell(i), '-----' , 'row');
                }
                blkcheckarray[blkcount] = textb.value;
                blkcount++;
            }
        }
        else{
            alert("Invalid Selection","Select a valid Block option");
        }


    }
    if (val == 'gp')
    {
        var tbl = document.getElementById('sel_loc'); // table reference
        var flag=0;
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
                    $.post ("/complaint/storedata/" + "GP" + "/"  + textb.value + "/" + textc.value + "/" + 0 +"/",
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
                        }
                    }
                    for (i = 2; i < tbl.rows[0].cells.length; i++)
                    {
                        createCell(row.insertCell(i), '-----' , 'row');
                    }
                    gpcheckarray[gpcount] = textc.value;
                    gpcount++;
                }
            }
            else
            {
                var row = tbl.insertRow(tbl.rows.length);      // append table row
                $.post ("/complaint/storedata/" + "GP" + "/"  + textb.value + "/" + textc.value + "/" + 0 +"/",
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
                    }
                }
                for (i = 2; i < tbl.rows[0].cells.length; i++)
                {
                    createCell(row.insertCell(i), '-----' , 'row');
                }
                gpcheckarray[gpcount] = textc.value;
                gpcount++;

            }
        }
        else
        {
            alert("Invalid Selection","Select a valid GramPanchayat");
        }

    }

    if (val == 'vill')
    {
        var tbl = document.getElementById('sel_loc'); // table reference
        var flag=0;
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
                    $.post ("/complaint/storedata/" + "VILL" + "/"  + textc.value + "/" + textb.value + "/" + texta.value +"/",
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
                        }
                    }
                    vcheckarray[vcount] = texta.value;
                    vcount++;
                }
            }
            else
            {
                var row = tbl.insertRow(tbl.rows.length);      // append table row
                $.post ("/complaint/storedata/" + "VILL" + "/"  + textc.value + "/" + textb.value + "/" + texta.value +"/",
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
                    }
                }
                vcheckarray[vcount] = texta.value;
                vcount++;
            }
        }
        else
        {
            alert("Invalid Selection","Select a valid Village");
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


